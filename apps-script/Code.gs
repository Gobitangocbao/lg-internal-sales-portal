/**
 * LG Internal Sales Portal -> Google Sheet "LG Internal Sales Database"
 * Nhận đơn đăng ký (Tab 2) và khai nộp tiền (Tab 3) từ index.html, ghi vào sheet.
 *
 * Nguyên tắc:
 *  - Chỉ THÊM dữ liệu. Không xoá dòng, không ghi đè ô đã có dữ liệu.
 *  - Không tự gửi email.
 *  - Mọi thao tác đều ghi thêm 1 dòng vào sheet ActivityLog.
 *  - Trạng thái do máy chủ đặt, không tin trạng thái trình duyệt gửi lên.
 *
 * Cách cài: xem docs/SETUP_APPS_SCRIPT.md
 */

var SHEET_REG = 'Registrations';
var SHEET_SLOTS = 'Slots';
var SHEET_CONFIG = 'Config';
var SHEET_LOG = 'ActivityLog';
var RECEIPT_FOLDER_NAME = 'Bien lai nop tien';
var MAX_FILE_BYTES = 5 * 1024 * 1024; // 5 MB

var STATUS_NEW = 'Chờ nộp tiền';
var STATUS_PAID = 'Đã khai nộp - chờ đối soát';

// Cột trong Registrations (1-based)
var C = {
  TS: 1, CAMPAIGN: 2, DIVISION: 3, EMP_CODE: 4, EMP_NAME: 5, KHO: 6, MODEL: 7, SLOT: 8,
  PHONE: 9, ADDRESS: 10, AGREE: 11, STATUS: 12, PAYER_NAME: 13, PAYER_CODE: 14,
  AMOUNT: 15, BANK_TXN: 16, PAY_TIME: 17, RECEIPT: 18, PM_BY: 19, PM_DATE: 20, NOTE: 21, UA: 22
};

function doGet() {
  return json_({ ok: true, service: 'LG Internal Sales API', time: new Date().toISOString() });
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
  } catch (err) {
    return json_({ ok: false, message: 'Hệ thống đang bận, vui lòng thử lại sau ít giây.' });
  }
  try {
    var data = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    if (data.action === 'register') return json_(register_(data));
    if (data.action === 'payment') return json_(payment_(data));
    return json_({ ok: false, message: 'Yêu cầu không hợp lệ.' });
  } catch (err) {
    log_('ERROR', '', '', '', String(err));
    return json_({ ok: false, message: 'Lỗi máy chủ: ' + err });
  } finally {
    lock.releaseLock();
  }
}

/* ---------- Đăng ký (Tab 2) ---------- */
function register_(d) {
  var req = ['division', 'empCode', 'empName', 'kho', 'model', 'slotId', 'phone', 'address'];
  for (var i = 0; i < req.length; i++) {
    if (!str_(d[req[i]])) return { ok: false, message: 'Thiếu thông tin: ' + req[i] };
  }
  if (d.agree !== true) return { ok: false, message: 'Chưa xác nhận cam kết Jeong-Do.' };

  var ss = SpreadsheetApp.getActive();
  var reg = ss.getSheetByName(SHEET_REG);
  var slotId = str_(d.slotId), empCode = str_(d.empCode).toUpperCase();
  var warnings = [], notes = [];

  // Kiểm tra slot có trong danh sách và đúng kho
  var slot = findSlot_(slotId);
  if (!slot) {
    warnings.push('Slot ' + slotId + ' không có trong danh sách.');
  } else if (slot.kho !== str_(d.kho)) {
    warnings.push('Slot ' + slotId + ' thuộc kho ' + slot.kho + ', không phải kho ' + d.kho + '.');
  }

  // CHẶN trùng slot: slot đã có đơn còn hiệu lực (không phải Hủy / Từ chối) thì không nhận
  var rows = regRows_(reg);
  var maxPer = Number(config_('MAX_PER_EMPLOYEE')) || 1;
  var slotTaken = 0, byEmp = 0;
  rows.forEach(function (r) {
    var st = String(r[C.STATUS - 1]);
    if (st === 'Hủy' || st === 'Từ chối') return;
    if (String(r[C.SLOT - 1]) === slotId) slotTaken++;
    if (String(r[C.EMP_CODE - 1]).toUpperCase() === empCode) byEmp++;
  });
  if (slotTaken > 0) {
    log_('REGISTER_REJECTED_DUP_SLOT', empCode, slotId, d.userAgent, 'Slot đã có người đăng ký, không ghi đơn');
    return { ok: false, slotTaken: true,
      message: 'Slot ' + slotId + ' đã có người đăng ký trước. Vui lòng chọn slot khác.' };
  }
  // Vượt hạn mức 1 SP/NV: vẫn ghi nhận kèm cảnh báo (sheet tô đỏ để PM xử lý)
  if (byEmp >= maxPer) warnings.push('Mã NV ' + empCode + ' đã đăng ký ' + byEmp + ' lần, vượt hạn mức ' + maxPer + ' sản phẩm/NV.');

  var campaign = str_(config_('CAMPAIGN_CODE'));
  if (!campaign) notes.push('Config chưa có CAMPAIGN_CODE');
  if (warnings.length) notes = notes.concat(warnings);

  var row = new Array(22).fill('');
  row[C.TS - 1] = new Date();
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
  reg.appendRow(row);
  var rowNo = reg.getLastRow();

  log_('REGISTER', empCode, slotId, d.userAgent, 'Dòng ' + rowNo + (warnings.length ? ' | ' + warnings.join(' | ') : ''));
  return { ok: true, row: rowNo, status: STATUS_NEW, timestamp: fmt_(row[0]), warnings: warnings };
}

/* ---------- Khai nộp tiền (Tab 3) ---------- */
function payment_(d) {
  var req = ['slotId', 'empCode', 'payerName', 'payerCode', 'amount', 'bankTxn', 'payTime'];
  for (var i = 0; i < req.length; i++) {
    if (!str_(d[req[i]])) return { ok: false, message: 'Thiếu thông tin: ' + req[i] };
  }
  var ss = SpreadsheetApp.getActive();
  var reg = ss.getSheetByName(SHEET_REG);
  var slotId = str_(d.slotId), empCode = str_(d.empCode).toUpperCase();

  // Tìm đơn đăng ký gần nhất khớp Slot + Mã NV
  var rows = regRows_(reg), found = -1;
  for (var r = rows.length - 1; r >= 0; r--) {
    if (String(rows[r][C.SLOT - 1]) === slotId && String(rows[r][C.EMP_CODE - 1]).toUpperCase() === empCode) { found = r; break; }
  }
  if (found < 0) {
    log_('PAYMENT_NOT_FOUND', empCode, slotId, d.userAgent, 'Không tìm thấy đơn đăng ký');
    return { ok: false, message: 'Không tìm thấy đơn đăng ký với Slot ' + slotId + ' và Mã NV ' + empCode + '. Vui lòng đăng ký ở Tab 2 trước.' };
  }
  var rowNo = found + 2;
  var cur = rows[found];

  // Không ghi đè khai nộp cũ
  if (str_(cur[C.PAYER_NAME - 1]) || str_(cur[C.BANK_TXN - 1])) {
    log_('PAYMENT_DUPLICATE', empCode, slotId, d.userAgent, 'Dòng ' + rowNo + ' đã khai nộp trước đó. Mã GD mới: ' + str_(d.bankTxn));
    return { ok: false, message: 'Đơn này đã khai nộp tiền trước đó. Nếu cần sửa, vui lòng liên hệ PM phụ trách.' };
  }

  // Lưu biên lai (nếu có) vào Drive, thư mục riêng tư của chủ sheet
  var link = '';
  if (d.fileBase64) {
    try { link = saveReceipt_(d.fileBase64, d.fileName, slotId, empCode); }
    catch (err) { log_('RECEIPT_ERROR', empCode, slotId, d.userAgent, String(err)); return { ok: false, message: 'Không lưu được file biên lai: ' + err }; }
  }

  reg.getRange(rowNo, C.PAYER_NAME, 1, 6).setValues([[
    safe_(d.payerName), safe_(str_(d.payerCode).toUpperCase()), "'" + str_(d.amount),
    safe_(d.bankTxn), safe_(d.payTime), link
  ]]);
  reg.getRange(rowNo, C.STATUS).setValue(STATUS_PAID);

  log_('PAYMENT', empCode, slotId, d.userAgent, 'Dòng ' + rowNo + (link ? ' | có biên lai' : ' | chưa có file biên lai'));
  return { ok: true, row: rowNo, status: STATUS_PAID, receipt: !!link };
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
  var ssFile = DriveApp.getFileById(SpreadsheetApp.getActive().getId());
  var parents = ssFile.getParents();
  var parent = parents.hasNext() ? parents.next() : DriveApp.getRootFolder();
  var it = parent.getFoldersByName(RECEIPT_FOLDER_NAME);
  return it.hasNext() ? it.next() : parent.createFolder(RECEIPT_FOLDER_NAME);
}

function findSlot_(slotId) {
  var sh = SpreadsheetApp.getActive().getSheetByName(SHEET_SLOTS);
  var v = sh.getRange(2, 1, Math.max(sh.getLastRow() - 1, 1), 4).getValues();
  for (var i = 0; i < v.length; i++) {
    if (String(v[i][2]) === slotId) return { kho: String(v[i][0]), model: String(v[i][3]) };
  }
  return null;
}

function regRows_(reg) {
  var n = reg.getLastRow() - 1;
  return n > 0 ? reg.getRange(2, 1, n, 22).getValues() : [];
}

function config_(key) {
  var sh = SpreadsheetApp.getActive().getSheetByName(SHEET_CONFIG);
  var v = sh.getRange(2, 1, Math.max(sh.getLastRow() - 1, 1), 2).getValues();
  for (var i = 0; i < v.length; i++) if (String(v[i][0]) === key) return v[i][1];
  return '';
}

function log_(action, empCode, slotId, ua, details) {
  var sh = SpreadsheetApp.getActive().getSheetByName(SHEET_LOG);
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
  Logger.log('Slot #001: ' + JSON.stringify(findSlot_('#001')));
  Logger.log('MAX_PER_EMPLOYEE: ' + config_('MAX_PER_EMPLOYEE'));
  Logger.log('Thư mục biên lai: ' + receiptFolder_().getName());
}
