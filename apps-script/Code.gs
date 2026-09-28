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
var SPREADSHEET_ID = '10aN5O3HL79asPGfug75IPv1w_ssGPo8edsASMuG3_aM';

var SHEET_REG = 'Registrations';
var SHEET_SLOTS = 'Slots';
var SHEET_CONFIG = 'Config';
var SHEET_LOG = 'ActivityLog';
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
    if (data.action === 'register') return json_(register_(data));
    if (data.action === 'payment') return json_(payment_(data));
    if (data.action === 'lookup') return json_(lookup_(data));
    return json_({ ok: false, message: 'Yêu cầu không hợp lệ.' });
  } catch (err) {
    try { log_('ERROR', '', '', '', String(err)); } catch (e2) {}
    return json_({ ok: false, message: 'Lỗi máy chủ: ' + err });
  }
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
