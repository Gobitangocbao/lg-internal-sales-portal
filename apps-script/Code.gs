/**
 * LG Internal Sales Portal -> Google Sheet "LG Internal Sales Database"
 * Nhận đơn đăng ký (Tab 2), khai nộp tiền (Tab 3) và tra cứu đơn từ index.html.
 *
 * Nguyên tắc:
 *  - Chỉ THÊM dữ liệu. Không xoá dòng, không ghi đè ô đã có dữ liệu.
 *  - Không tự gửi email.
 *  - Mọi thao tác ghi đều ghi thêm 1 dòng vào sheet ActivityLog.
 *  - Trạng thái do máy chủ đặt, không tin trạng thái trình duyệt gửi lên.
 *
 * v7.3 (chịu tải): chỉ khoá (lock) đúng đoạn kiểm tra trùng + ghi dòng; đọc Config/Slots
 * qua bộ nhớ đệm; chờ khoá tối đa 30 giây; trả busy:true để trang tự gửi lại.
 *
 * Cách cài: xem docs/SETUP_APPS_SCRIPT.md
 */

// ID của Google Sheet "LG Internal Sales Database"
var SPREADSHEET_ID = '18dK1OgZe78DA5vsosES017_lazJ23OUXd5fJwm9zx3I';

var SHEET_REG = 'Registrations';
var SHEET_SLOTS = 'Slots';
var SHEET_CONFIG = 'Config';
var SHEET_LOG = 'ActivityLog';
var SHEET_USERS = 'Users';
var SHEET_PROGRAMS = 'Programs';
var SHEET_PRODUCTS = 'Products';
var RECEIPT_FOLDER_NAME = 'Bien lai nop tien';
var MAX_FILE_BYTES = 5 * 1024 * 1024; // 5 MB
var LOCK_WAIT_MS = 30000;              // chờ tối đa 30 giây
var CACHE_CONFIG_SEC = 300;            // Config đổi thì sau tối đa 5 phút script mới thấy
var CACHE_SLOTS_SEC = 600;

var STATUS_NEW = 'Chờ nộp tiền';
var STATUS_PAID = 'Đã khai nộp - chờ đối soát';
var STATUS_FREE = ['Hủy', 'Từ chối']; // đơn ở trạng thái này không giữ slot

// Cột trong Registrations (1-based)
var C = {
  TS: 1, CAMPAIGN: 2, DIVISION: 3, EMP_CODE: 4, EMP_NAME: 5, KHO: 6, MODEL: 7, SLOT: 8,
  PHONE: 9, ADDRESS: 10, AGREE: 11, STATUS: 12, PAYER_NAME: 13, PAYER_CODE: 14,
  AMOUNT: 15, BANK_TXN: 16, PAY_TIME: 17, RECEIPT: 18, PM_BY: 19, PM_DATE: 20, NOTE: 21, UA: 22
};

/* ---------- Mở sheet (1 lần mỗi lượt chạy) ---------- */
var _book = null;
function book_() {
  if (_book) return _book;
  try { var a = SpreadsheetApp.getActiveSpreadsheet(); if (a) return (_book = a); } catch (e) {}
  return (_book = SpreadsheetApp.openById(SPREADSHEET_ID));
}

function doGet() {
  return json_({ ok: true, service: 'LG Internal Sales API', version: '7.3.1', time: new Date().toISOString() });
}

function doPost(e) {
  try {
    var data = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    if (data.action === 'auth') return json_(auth_(data));
    if (data.action === 'programs') return json_(programs_(data));
    if (data.action === 'program_create') return json_(program_create_(data));
    if (data.action === 'program_update') return json_(program_update_(data));
    if (data.action === 'products') return json_(products_(data));
    if (data.action === 'product_upload') return json_(product_upload_(data));
    if (data.action === 'register_product') return json_(register_product_(data));
    if (data.action === 'register') return json_(register_(data));
    if (data.action === 'payment') return json_(payment_(data));
    if (data.action === 'lookup') return json_(lookup_(data));
    return json_({ ok: false, message: 'Yêu cầu không hợp lệ.' });
  } catch (err) {
    try { log_('ERROR', '', '', '', String(err)); } catch (e2) {}
    return json_({ ok: false, message: 'Lỗi máy chủ: ' + err });
  }
}

/* ---------- P1: Multi-Program ---------- */
var PROG_COL = { ID: 1, NAME: 2, PM_ID: 3, PM_NAME: 4, STATUS: 5, START: 6, END: 7, DESC: 8, MAX_PER: 9, CREATED: 10 };

// List programs — users see Open only, PM sees all their programs
function programs_(d) {
  var sheet = book_().getSheetByName(SHEET_PROGRAMS);
  if (!sheet) return { ok: true, programs: [] };
  var n = sheet.getLastRow() - 1;
  if (n <= 0) return { ok: true, programs: [] };
  var data = sheet.getRange(2, 1, n, 10).getValues();
  var role = str_(d.role) || 'USER';
  var userId = str_(d.userId).toUpperCase();
  var result = [];
  for (var r = 0; r < n; r++) {
    var status = String(data[r][PROG_COL.STATUS - 1]).trim();
    var pmId = String(data[r][PROG_COL.PM_ID - 1]).trim().toUpperCase();
    // Users only see Open programs; PM sees their own programs in any status
    if (role === 'PM' && pmId === userId) {
      // PM sees all their programs
    } else if (status !== 'Open') {
      continue;
    }
    result.push({
      id: String(data[r][0]).trim(),
      name: String(data[r][1]).trim(),
      pmId: pmId,
      pmName: String(data[r][3]).trim(),
      status: status,
      startDate: String(data[r][5]).trim(),
      endDate: String(data[r][6]).trim(),
      description: String(data[r][7]).trim(),
      maxPerEmployee: Number(data[r][8]) || 1
    });
  }
  return { ok: true, programs: result };
}

// PM creates a new program
function program_create_(d) {
  if (str_(d.role) !== 'PM') return { ok: false, message: 'Chỉ PM mới được tạo chương trình.' };
  var req = ['programId', 'programName', 'startDate', 'endDate'];
  for (var i = 0; i < req.length; i++) {
    if (!str_(d[req[i]])) return { ok: false, message: 'Thiếu: ' + req[i] };
  }
  var sheet = book_().getSheetByName(SHEET_PROGRAMS);
  if (!sheet) return { ok: false, message: 'Sheet Programs chưa tồn tại.' };

  // Check duplicate ProgramID
  var n = sheet.getLastRow() - 1;
  if (n > 0) {
    var ids = sheet.getRange(2, 1, n, 1).getValues();
    for (var r = 0; r < n; r++) {
      if (String(ids[r][0]).trim().toUpperCase() === str_(d.programId).toUpperCase()) {
        return { ok: false, message: 'Mã chương trình đã tồn tại: ' + d.programId };
      }
    }
  }

  var row = [
    str_(d.programId),
    str_(d.programName),
    str_(d.userId),
    str_(d.userName),
    'Draft',
    str_(d.startDate),
    str_(d.endDate),
    str_(d.description) || '',
    Number(d.maxPerEmployee) || 1,
    new Date().toISOString()
  ];
  sheet.appendRow(row);
  try { log_('PROGRAM_CREATE', str_(d.userId), str_(d.userName), '', 'program=' + d.programId); } catch (e2) {}
  return { ok: true, message: 'Đã tạo chương trình ' + d.programId + ' (Draft).' };
}

// PM updates program status (Draft→Open, Open→Closed)
function program_update_(d) {
  if (str_(d.role) !== 'PM') return { ok: false, message: 'Chỉ PM mới được cập nhật chương trình.' };
  var progId = str_(d.programId);
  var newStatus = str_(d.newStatus);
  if (!progId || !newStatus) return { ok: false, message: 'Thiếu programId hoặc newStatus.' };
  if (['Open', 'Closed'].indexOf(newStatus) < 0) return { ok: false, message: 'Trạng thái không hợp lệ. Chỉ chấp nhận: Open, Closed.' };

  var sheet = book_().getSheetByName(SHEET_PROGRAMS);
  if (!sheet) return { ok: false, message: 'Sheet Programs chưa tồn tại.' };
  var n = sheet.getLastRow() - 1;
  if (n <= 0) return { ok: false, message: 'Không tìm thấy chương trình.' };

  var data = sheet.getRange(2, 1, n, 5).getValues();
  for (var r = 0; r < n; r++) {
    if (String(data[r][0]).trim().toUpperCase() === progId.toUpperCase()) {
      var currentStatus = String(data[r][4]).trim();
      // Validate transition: Draft→Open, Open→Closed
      if (newStatus === 'Open' && currentStatus !== 'Draft') {
        return { ok: false, message: 'Chỉ có thể mở chương trình đang ở trạng thái Draft.' };
      }
      if (newStatus === 'Closed' && currentStatus !== 'Open') {
        return { ok: false, message: 'Chỉ có thể kết sổ chương trình đang Open.' };
      }
      // Check PM ownership
      if (String(data[r][2]).trim().toUpperCase() !== str_(d.userId).toUpperCase()) {
        return { ok: false, message: 'Bạn không phải PM của chương trình này.' };
      }
      sheet.getRange(r + 2, PROG_COL.STATUS).setValue(newStatus);
      try { log_('PROGRAM_' + newStatus.toUpperCase(), str_(d.userId), str_(d.userName), '', 'program=' + progId); } catch (e2) {}
      return { ok: true, message: 'Đã chuyển chương trình ' + progId + ' sang ' + newStatus + '.' };
    }
  }
  return { ok: false, message: 'Không tìm thấy chương trình ' + progId + '.' };
}

/* ---------- P2: Products ---------- */
var PROD_COL = { PROG: 1, CODE: 2, KHO: 3, CAT: 4, MODEL: 5, DESC: 6, RRP: 7, PRICE: 8, QTY: 9, STATUS: 10, EMP: 11, TS: 12 };

// List products for a program
function products_(d) {
  var programId = str_(d.programId);
  if (!programId) return { ok: false, message: 'Thiếu programId.' };

  var sheet = book_().getSheetByName(SHEET_PRODUCTS);
  if (!sheet) return { ok: true, products: [] };
  var n = sheet.getLastRow() - 1;
  if (n <= 0) return { ok: true, products: [] };

  var data = sheet.getRange(2, 1, n, 12).getValues();
  var result = [];
  for (var r = 0; r < n; r++) {
    var pId = String(data[r][0]).trim();
    if (pId.toUpperCase() !== programId.toUpperCase()) continue;
    result.push({
      programId: pId,
      uniqueCode: String(data[r][1]).trim(),
      kho: String(data[r][2]).trim(),
      category: String(data[r][3]).trim(),
      model: String(data[r][4]).trim(),
      description: String(data[r][5]).trim(),
      rrp: Number(data[r][6]) || 0,
      internalPrice: Number(data[r][7]) || 0,
      qty: Number(data[r][8]) || 1,
      status: String(data[r][9]).trim() || 'Available',
      empCode: String(data[r][10]).trim(),
      timestamp: String(data[r][11]).trim()
    });
  }
  return { ok: true, products: result };
}

// PM uploads products (batch)
function product_upload_(d) {
  if (str_(d.role) !== 'PM') return { ok: false, message: 'Chỉ PM mới được upload sản phẩm.' };
  var programId = str_(d.programId);
  if (!programId) return { ok: false, message: 'Thiếu programId.' };
  var items = d.items; // array of {kho, category, model, description, rrp, internalPrice, qty}
  if (!items || !items.length) return { ok: false, message: 'Danh sách sản phẩm trống.' };

  var sheet = book_().getSheetByName(SHEET_PRODUCTS);
  if (!sheet) return { ok: false, message: 'Sheet Products chưa tồn tại.' };

  // Count existing products per kho for this program (to generate seq)
  var n = sheet.getLastRow() - 1;
  var khoSeq = {};
  if (n > 0) {
    var existing = sheet.getRange(2, 1, n, 3).getValues();
    for (var r = 0; r < n; r++) {
      if (String(existing[r][0]).trim().toUpperCase() === programId.toUpperCase()) {
        var k = String(existing[r][2]).trim().toUpperCase();
        khoSeq[k] = (khoSeq[k] || 0) + 1;
      }
    }
  }

  var rows = [];
  var ts = new Date().toISOString();
  for (var i = 0; i < items.length; i++) {
    var it = items[i];
    var kho = str_(it.kho).toUpperCase();
    if (!kho) continue;
    khoSeq[kho] = (khoSeq[kho] || 0) + 1;
    var seq = ('000' + khoSeq[kho]).slice(-3);
    var uniqueCode = programId.toUpperCase() + '-' + kho + '-' + seq;
    rows.push([
      programId, uniqueCode, kho,
      str_(it.category), str_(it.model), str_(it.description),
      Number(it.rrp) || 0, Number(it.internalPrice) || 0,
      Number(it.qty) || 1, 'Available', '', ts
    ]);
  }

  if (rows.length > 0) {
    var startRow = sheet.getLastRow() + 1;
    sheet.getRange(startRow, 1, rows.length, 12).setValues(rows);
  }

  try { log_('PRODUCT_UPLOAD', str_(d.userId), str_(d.userName), '', 'program=' + programId + ' count=' + rows.length); } catch (e2) {}
  return { ok: true, message: 'Đã upload ' + rows.length + ' sản phẩm vào chương trình ' + programId + '.' };
}

/* ---------- P3: Product Registration (optimized for 200-300 concurrent users) ---------- */
function register_product_(d) {
  // Validate required fields
  var uniqueCode = str_(d.uniqueCode);
  var empCode = str_(d.empCode).toUpperCase();
  var empName = str_(d.empName);
  var programId = str_(d.programId);
  if (!uniqueCode || !empCode || !empName || !programId) {
    return { ok: false, message: 'Thiếu thông tin đăng ký.' };
  }

  // Get max per employee from Programs sheet
  var progSheet = book_().getSheetByName(SHEET_PROGRAMS);
  var maxPer = 1;
  if (progSheet) {
    var pn = progSheet.getLastRow() - 1;
    if (pn > 0) {
      var pData = progSheet.getRange(2, 1, pn, 7).getValues();
      for (var pi = 0; pi < pn; pi++) {
        if (String(pData[pi][0]).trim().toUpperCase() === programId.toUpperCase()) {
          maxPer = Number(pData[pi][6]) || 1;
          // Check program is Open
          if (String(pData[pi][3]).trim() !== 'Open') {
            return { ok: false, message: 'Chương trình ' + programId + ' đã kết sổ, không thể đăng ký.' };
          }
          break;
        }
      }
    }
  }

  // Lock for atomic read-modify-write
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(LOCK_WAIT_MS)) {
    return { ok: false, busy: true, message: 'Hệ thống đang bận, vui lòng thử lại sau ít giây.' };
  }

  try {
    var prodSheet = book_().getSheetByName(SHEET_PRODUCTS);
    if (!prodSheet) return { ok: false, message: 'Sheet Products không tồn tại.' };
    var n = prodSheet.getLastRow() - 1;
    if (n <= 0) return { ok: false, message: 'Không tìm thấy sản phẩm.' };

    var data = prodSheet.getRange(2, 1, n, 12).getValues();
    var targetRow = -1;
    var empCount = 0;

    for (var r = 0; r < n; r++) {
      var pId = String(data[r][0]).trim().toUpperCase();
      if (pId !== programId.toUpperCase()) continue;

      var code = String(data[r][1]).trim();
      var status = String(data[r][9]).trim();
      var emp = String(data[r][10]).trim().toUpperCase();

      // Found our target product
      if (code === uniqueCode) {
        if (status !== 'Available') {
          // Already taken — check if same employee (idempotent)
          if (emp === empCode) {
            return { ok: true, message: 'Bạn đã đăng ký sản phẩm này rồi.', repeat: true };
          }
          return { ok: false, message: 'Sản phẩm ' + uniqueCode + ' đã có người đăng ký trước. Vui lòng chọn sản phẩm khác.' };
        }
        targetRow = r;
      }

      // Count how many products this employee already registered in this program
      if (status === 'Registered' && emp === empCode) {
        empCount++;
      }
    }

    if (targetRow < 0) return { ok: false, message: 'Không tìm thấy sản phẩm ' + uniqueCode + '.' };

    // Check employee quota
    if (empCount >= maxPer) {
      return { ok: false, message: 'Bạn đã đăng ký ' + empCount + ' sản phẩm, vượt hạn mức ' + maxPer + ' SP/nhân viên.' };
    }

    // Mark product as Registered
    var ts = new Date().toISOString();
    var sheetRow = targetRow + 2; // 1-indexed + header
    prodSheet.getRange(sheetRow, PROD_COL.STATUS).setValue('Registered');
    prodSheet.getRange(sheetRow, PROD_COL.EMP).setValue(empCode);
    prodSheet.getRange(sheetRow, PROD_COL.TS).setValue(ts);

    // Also write to Registrations sheet for backward compatibility
    var regSheet = book_().getSheetByName(SHEET_REG);
    if (regSheet) {
      var prodData = data[targetRow];
      var regRow = new Array(22).fill('');
      regRow[0] = ts;                          // Timestamp
      regRow[1] = programId;                   // Campaign/Program
      regRow[2] = str_(d.division);            // Division
      regRow[3] = empCode;                     // Emp Code
      regRow[4] = empName;                     // Emp Name
      regRow[5] = String(prodData[2]).trim();   // Kho
      regRow[6] = String(prodData[4]).trim();   // Model
      regRow[7] = uniqueCode;                  // Slot/UniqueCode
      regRow[8] = str_(d.phone);               // Phone
      regRow[9] = str_(d.address);             // Address
      regRow[10] = 'Đồng ý';                    // Agree
      regRow[11] = 'Mới đăng ký';              // Status
      regSheet.getRange(regSheet.getLastRow() + 1, 1, 1, 22).setValues([regRow]);
    }

    SpreadsheetApp.flush();
  } finally {
    lock.releaseLock();
  }

  try { log_('REGISTER_PRODUCT', empCode, empName, '', 'program=' + programId + ' product=' + uniqueCode); } catch (e2) {}
  return { ok: true, message: 'Đăng ký thành công sản phẩm ' + uniqueCode + '!' };
}

/* ---------- P0: Xác thực (auth) ---------- */
function auth_(d) {
  var id = str_(d.id).toUpperCase();
  var pw = str_(d.password);
  if (!id || !pw) return { ok: false, message: 'Vui l\u00f2ng nh\u1eadp M\u00e3 NV v\u00e0 m\u1eadt kh\u1ea9u.' };

  var sheet = book_().getSheetByName(SHEET_USERS);
  if (!sheet) return { ok: false, message: 'H\u1ec7 th\u1ed1ng ch\u01b0a c\u1ea5u h\u00ecnh danh s\u00e1ch nh\u00e2n vi\u00ean.' };

  var n = sheet.getLastRow() - 1;
  if (n <= 0) return { ok: false, message: 'Danh s\u00e1ch nh\u00e2n vi\u00ean tr\u1ed1ng.' };

  // Users sheet: A=ID, B=Password, C=Name, D=Dept, E=Phone, F=Email, G=Role, H=Status
  var data = sheet.getRange(2, 1, n, 8).getValues();
  for (var r = 0; r < n; r++) {
    var rowId = String(data[r][0]).trim().toUpperCase();
    if (rowId !== id) continue;

    // Check status
    var status = String(data[r][7]).trim();
    if (status && status.toLowerCase() !== 'active') {
      return { ok: false, message: 'T\u00e0i kho\u1ea3n \u0111\u00e3 b\u1ecb v\u00f4 hi\u1ec7u h\u00f3a. Li\u00ean h\u1ec7 PM Support.' };
    }

    // Check password (plaintext comparison — upgrade to SHA256 in P6)
    var storedPw = String(data[r][1]);
    if (storedPw !== pw) {
      return { ok: false, message: 'M\u1eadt kh\u1ea9u kh\u00f4ng \u0111\u00fang.' };
    }

    // Success — return user profile
    var user = {
      id: rowId,
      name: String(data[r][2]).trim(),
      dept: String(data[r][3]).trim(),
      phone: String(data[r][4]).trim(),
      email: String(data[r][5]).trim(),
      role: String(data[r][6]).trim() || 'USER'
    };

    try { log_('AUTH_LOGIN', id, user.name, '', 'role=' + user.role); } catch (e2) {}
    return { ok: true, user: user };
  }

  return { ok: false, message: 'M\u00e3 nh\u00e2n vi\u00ean kh\u00f4ng t\u1ed3n t\u1ea1i.' };
}

/* ---------- Đăng ký (Tab 2) ---------- */
function register_(d) {
  var req = ['division', 'empCode', 'empName', 'kho', 'model', 'slotId', 'phone', 'address'];
  for (var i = 0; i < req.length; i++) {
    if (!str_(d[req[i]])) return { ok: false, message: 'Thiếu thông tin: ' + req[i] };
  }
  if (d.agree !== true) return { ok: false, message: 'Chưa xác nhận cam kết Jeong-Do.' };

  var slotId = str_(d.slotId), empCode = str_(d.empCode).toUpperCase();
  var cfg = config_();
  var warnings = [], notes = [];

  // Kiểm tra slot có trong danh sách và đúng kho (ngoài khoá, dùng bộ nhớ đệm)
  var slot = slots_()[slotId];
  if (!slot) warnings.push('Slot ' + slotId + ' không có trong danh sách.');
  else if (slot.kho !== str_(d.kho)) warnings.push('Slot ' + slotId + ' thuộc kho ' + slot.kho + ', không phải kho ' + d.kho + '.');

  var campaign = str_(cfg.CAMPAIGN_CODE);
  if (!campaign) notes.push('Config chưa có CAMPAIGN_CODE');
  var maxPer = Number(cfg.MAX_PER_EMPLOYEE) || 1;

  // ---- Đoạn cần khoá: kiểm tra trùng + ghi dòng ----
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(LOCK_WAIT_MS)) {
    return { ok: false, busy: true, message: 'Hệ thống đang bận, vui lòng thử lại sau ít giây.' };
  }
  var rowNo, ts, rejected = false, byEmp = 0, sameRow = 0;
  try {
    var reg = book_().getSheetByName(SHEET_REG);
    var n = reg.getLastRow() - 1;
    // Chỉ đọc 9 cột D..L (Mã NV .. Trạng thái)
    var rows = n > 0 ? reg.getRange(2, C.EMP_CODE, n, C.STATUS - C.EMP_CODE + 1).getValues() : [];
    var iEmp = 0, iSlot = C.SLOT - C.EMP_CODE, iSt = C.STATUS - C.EMP_CODE;
    for (var r = 0; r < rows.length; r++) {
      if (STATUS_FREE.indexOf(String(rows[r][iSt])) >= 0) continue;
      if (String(rows[r][iSlot]) === slotId) {
        // Chính người này đã giữ slot (trang gửi lại do mạng chập chờn): coi như thành công, không ghi thêm
        if (String(rows[r][iEmp]).toUpperCase() === empCode) sameRow = r + 2; else rejected = true;
        break;
      }
      if (String(rows[r][iEmp]).toUpperCase() === empCode) byEmp++;
    }
    if (!rejected && !sameRow) {
      if (byEmp >= maxPer) warnings.push('Mã NV ' + empCode + ' đã đăng ký ' + byEmp + ' lần, vượt hạn mức ' + maxPer + ' sản phẩm/NV.');
      if (warnings.length) notes = notes.concat(warnings);
      ts = new Date();
      var row = new Array(22).fill('');
      row[C.TS - 1] = ts;
      row[C.CAMPAIGN - 1] = campaign;
      row[C.DIVISION - 1] = safe_(d.division);
      row[C.EMP_CODE - 1] = safe_(empCode);
      row[C.EMP_NAME - 1] = safe_(d.empName);
      row[C.KHO - 1] = safe_(d.kho);
      row[C.MODEL - 1] = safe_(d.model);
      row[C.SLOT - 1] = "'" + slotId.replace(/^'+/, '');
      row[C.PHONE - 1] = "'" + str_(d.phone);
      row[C.ADDRESS - 1] = safe_(d.address);
      row[C.AGREE - 1] = 'Đồng ý';
      row[C.STATUS - 1] = STATUS_NEW;
      row[C.NOTE - 1] = safe_(notes.join(' | '));
      row[C.UA - 1] = safe_(str_(d.userAgent).slice(0, 300));
      rowNo = n + 2;
      reg.getRange(rowNo, 1, 1, 22).setValues([row]);
      SpreadsheetApp.flush();
    }
  } finally {
    lock.releaseLock();
  }
  // ---- Hết đoạn khoá ----

  if (sameRow) {
    log_('REGISTER_REPEAT', empCode, slotId, d.userAgent, 'Gửi lại, đơn đã có ở dòng ' + sameRow + ', không ghi thêm');
    return { ok: true, row: sameRow, status: STATUS_NEW, repeat: true, warnings: [] };
  }
  if (rejected) {
    log_('REGISTER_REJECTED_DUP_SLOT', empCode, slotId, d.userAgent, 'Slot đã có người đăng ký, không ghi đơn');
    return { ok: false, slotTaken: true, message: 'Slot ' + slotId + ' đã có người đăng ký trước. Vui lòng chọn slot khác.' };
  }
  log_('REGISTER', empCode, slotId, d.userAgent, 'Dòng ' + rowNo + (warnings.length ? ' | ' + warnings.join(' | ') : ''));
  return { ok: true, row: rowNo, status: STATUS_NEW, timestamp: fmt_(ts), warnings: warnings };
}

/* ---------- Khai nộp tiền (Tab 3) ---------- */
function payment_(d) {
  var req = ['slotId', 'empCode', 'payerName', 'payerCode', 'amount', 'bankTxn', 'payTime'];
  for (var i = 0; i < req.length; i++) {
    if (!str_(d[req[i]])) return { ok: false, message: 'Thiếu thông tin: ' + req[i] };
  }
  var slotId = str_(d.slotId), empCode = str_(d.empCode).toUpperCase();
  var reg = book_().getSheetByName(SHEET_REG);

  // Kiểm tra trước (không khoá) để không lưu biên lai thừa
  var pre = findOrder_(reg, slotId, empCode);
  if (!pre) {
    log_('PAYMENT_NOT_FOUND', empCode, slotId, d.userAgent, 'Không tìm thấy đơn đăng ký');
    return { ok: false, message: 'Không tìm thấy đơn đăng ký với Slot ' + slotId + ' và Mã NV ' + empCode + '. Vui lòng đăng ký ở Tab 2 trước.' };
  }
  if (pre.paid && pre.txn === str_(d.bankTxn)) return { ok: true, row: pre.rowNo, status: STATUS_PAID, repeat: true };
  if (pre.paid) return paidAlready_(d, empCode, slotId, pre.rowNo);

  // Lưu biên lai (việc chậm) trước khi khoá
  var link = '';
  if (d.fileBase64) {
    try { link = saveReceipt_(d.fileBase64, d.fileName, slotId, empCode); }
    catch (err) { log_('RECEIPT_ERROR', empCode, slotId, d.userAgent, String(err)); return { ok: false, message: 'Không lưu được file biên lai: ' + err }; }
  }

  var lock = LockService.getScriptLock();
  if (!lock.tryLock(LOCK_WAIT_MS)) {
    return { ok: false, busy: true, message: 'Hệ thống đang bận, vui lòng thử lại sau ít giây.' };
  }
  var found, dup = false;
  try {
    found = findOrder_(reg, slotId, empCode); // kiểm tra lại trong khoá
    if (found && found.paid) dup = true;
    else if (found) {
      reg.getRange(found.rowNo, C.PAYER_NAME, 1, 6).setValues([[
        safe_(d.payerName), safe_(str_(d.payerCode).toUpperCase()), "'" + str_(d.amount),
        safe_(d.bankTxn), safe_(d.payTime), link
      ]]);
      reg.getRange(found.rowNo, C.STATUS).setValue(STATUS_PAID);
      SpreadsheetApp.flush();
    }
  } finally {
    lock.releaseLock();
  }
  if (!found) return { ok: false, message: 'Không tìm thấy đơn đăng ký. Vui lòng thử lại.' };
  if (dup && found.txn === str_(d.bankTxn)) return { ok: true, row: found.rowNo, status: STATUS_PAID, repeat: true };
  if (dup) return paidAlready_(d, empCode, slotId, found.rowNo);

  log_('PAYMENT', empCode, slotId, d.userAgent, 'Dòng ' + found.rowNo + (link ? ' | có biên lai' : ' | chưa có file biên lai'));
  return { ok: true, row: found.rowNo, status: STATUS_PAID, receipt: !!link };
}

function paidAlready_(d, empCode, slotId, rowNo) {
  log_('PAYMENT_DUPLICATE', empCode, slotId, d.userAgent, 'Dòng ' + rowNo + ' đã khai nộp trước đó. Mã GD mới: ' + str_(d.bankTxn));
  return { ok: false, message: 'Đơn này đã khai nộp tiền trước đó. Nếu cần sửa, vui lòng liên hệ PM phụ trách.' };
}

// Đơn gần nhất khớp Slot + Mã NV (đọc cột D..P)
function findOrder_(reg, slotId, empCode) {
  var n = reg.getLastRow() - 1;
  if (n < 1) return null;
  var v = reg.getRange(2, C.EMP_CODE, n, C.BANK_TXN - C.EMP_CODE + 1).getValues();
  for (var r = v.length - 1; r >= 0; r--) {
    if (String(v[r][C.SLOT - C.EMP_CODE]) === slotId && String(v[r][0]).toUpperCase() === empCode) {
      var paid = !!(str_(v[r][C.PAYER_NAME - C.EMP_CODE]) || str_(v[r][C.BANK_TXN - C.EMP_CODE]));
      return { rowNo: r + 2, paid: paid, txn: str_(v[r][C.BANK_TXN - C.EMP_CODE]) };
    }
  }
  return null;
}

/* ---------- Tra cứu đơn (Mã NV + 4 số cuối SĐT) ---------- */
function lookup_(d) {
  var empCode = str_(d.empCode).toUpperCase();
  var last4 = str_(d.phoneLast4).replace(/\D/g, '');
  if (!empCode || last4.length !== 4) return { ok: false, message: 'Vui lòng nhập Mã NV và đúng 4 số cuối điện thoại đã đăng ký.' };

  var reg = book_().getSheetByName(SHEET_REG);
  var n = reg.getLastRow() - 1;
  var v = n > 0 ? reg.getRange(2, 1, n, C.RECEIPT).getValues() : [];
  var out = [];
  for (var r = 0; r < v.length; r++) {
    if (String(v[r][C.EMP_CODE - 1]).toUpperCase() !== empCode) continue;
    var phone = String(v[r][C.PHONE - 1]).replace(/\D/g, '');
    if (phone.slice(-4) !== last4) continue;
    out.push({
      time: v[r][0] instanceof Date ? fmt_(v[r][0]) : str_(v[r][0]),
      slot: str_(v[r][C.SLOT - 1]), kho: str_(v[r][C.KHO - 1]), model: str_(v[r][C.MODEL - 1]),
      status: str_(v[r][C.STATUS - 1]) || 'Chưa có trạng thái',
      paid: !!str_(v[r][C.BANK_TXN - 1]), receipt: !!str_(v[r][C.RECEIPT - 1])
    });
  }
  if (!out.length) {
    log_('LOOKUP_NOT_FOUND', empCode, '', d.userAgent, 'Tra cứu không khớp');
    return { ok: false, message: 'Không tìm thấy đơn khớp Mã NV và 4 số cuối điện thoại này.' };
  }
  return { ok: true, orders: out };
}

/* ---------- Bộ nhớ đệm Config / Slots ---------- */
function config_() {
  var cache = CacheService.getScriptCache();
  var hit = cache.get('cfg');
  if (hit) return JSON.parse(hit);
  var sh = book_().getSheetByName(SHEET_CONFIG);
  var v = sh.getRange(2, 1, Math.max(sh.getLastRow() - 1, 1), 2).getValues();
  var o = {};
  for (var i = 0; i < v.length; i++) if (v[i][0]) o[String(v[i][0])] = v[i][1] instanceof Date ? fmt_(v[i][1]) : v[i][1];
  cache.put('cfg', JSON.stringify(o), CACHE_CONFIG_SEC);
  return o;
}

function slots_() {
  var cache = CacheService.getScriptCache();
  var hit = cache.get('slots');
  if (hit) return JSON.parse(hit);
  var sh = book_().getSheetByName(SHEET_SLOTS);
  var v = sh.getRange(2, 1, Math.max(sh.getLastRow() - 1, 1), 4).getValues();
  var o = {};
  for (var i = 0; i < v.length; i++) if (v[i][2]) o[String(v[i][2])] = { kho: String(v[i][0]), model: String(v[i][3]) };
  cache.put('slots', JSON.stringify(o), CACHE_SLOTS_SEC);
  return o;
}

/** Chạy tay khi vừa sửa Config hoặc Slots để script thấy ngay. */
function clearCache() {
  CacheService.getScriptCache().removeAll(['cfg', 'slots']);
  Logger.log('Đã xoá bộ nhớ đệm Config và Slots.');
}

/* ---------- Tiện ích ---------- */
function saveReceipt_(dataUrl, fileName, slotId, empCode) {
  var m = /^data:([^;]+);base64,(.+)$/.exec(dataUrl);
  if (!m) throw 'File không đúng định dạng';
  var mime = m[1];
  if (!/^image\/|^application\/pdf$/.test(mime)) throw 'Chỉ nhận ảnh hoặc PDF';
  var bytes = Utilities.base64Decode(m[2]);
  if (bytes.length > MAX_FILE_BYTES) throw 'File lớn hơn 5 MB';
  var ext = (String(fileName || '').match(/\.[A-Za-z0-9]{1,5}$/) || [''])[0];
  var name = 'BL_' + slotId.replace('#', '') + '_' + empCode + '_' +
    Utilities.formatDate(new Date(), 'Asia/Ho_Chi_Minh', 'yyyyMMdd-HHmmss') + ext;
  var file = receiptFolder_().createFile(Utilities.newBlob(bytes, mime, name));
  return file.getUrl();
}

function receiptFolder_() {
  var ssFile = DriveApp.getFileById(book_().getId());
  var parents = ssFile.getParents();
  var parent = parents.hasNext() ? parents.next() : DriveApp.getRootFolder();
  var it = parent.getFoldersByName(RECEIPT_FOLDER_NAME);
  return it.hasNext() ? it.next() : parent.createFolder(RECEIPT_FOLDER_NAME);
}

function log_(action, empCode, slotId, ua, details) {
  var sh = book_().getSheetByName(SHEET_LOG);
  if (!sh) return;
  sh.appendRow([new Date(), action, safe_(empCode), slotId ? "'" + slotId : '', safe_(str_(ua).slice(0, 300)), safe_(details)]);
}

function str_(v) { return v === null || v === undefined ? '' : String(v).trim(); }

// Chặn chèn công thức: giá trị bắt đầu bằng = + - @ sẽ được lưu dạng chữ
function safe_(v) {
  var s = str_(v);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function fmt_(d) { return Utilities.formatDate(d, 'Asia/Ho_Chi_Minh', 'dd/MM/yyyy HH:mm:ss'); }

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

/** Chạy tay 1 lần trong trình soạn Apps Script để cấp quyền và kiểm tra. Không ghi gì vào sheet. */
function testSetup() {
  Logger.log('Slot #001: ' + JSON.stringify(slots_()['#001']));
  Logger.log('MAX_PER_EMPLOYEE: ' + config_().MAX_PER_EMPLOYEE);
  Logger.log('Thư mục biên lai: ' + receiptFolder_().getName());
}
