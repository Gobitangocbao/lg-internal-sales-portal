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
 * v7.3 (chịu tải): đọc Config/Slots qua bộ nhớ đệm; trả busy:true để trang tự gửi lại.
 * v7.6 (200 người): khoá chỉ giữ vài chục mili-giây để "giữ chỗ slot + cấp số dòng" (lưu trong
 * Script Properties). Việc đọc/ghi sheet nằm ngoài khoá, mỗi đơn ghi vào đúng dòng đã cấp nên
 * 2 người không ghi đè nhau. (v7.5 dùng appendRow không khoá: thử 200 người thấy mất dòng, đã bỏ.)
 * Cột W lưu mã yêu cầu để đối chiếu.
 * v7.7 (30/09/2026): CHẶN VƯỢT HẠN MỨC. Mã NV đã có đơn còn hiệu lực (không phải Hủy/Từ chối) thì
 * đăng ký mới bị TỪ CHỐI: không ghi dòng, không giữ slot, trả limitReached:true. Kiểm tra cả khi
 * 1 người gửi 2 slot khác nhau cùng lúc (so trong khoá với các slot người đó vừa giữ chỗ).
 * v7.8 (30/09/2026): QUY TẮC ĐƠN HỢP LỆ dùng chung cho đăng ký / slot đã hết / tra cứu / nộp tiền:
 * mỗi Mã NV chỉ tính MAX_PER_EMPLOYEE đơn còn hiệu lực: ưu tiên đơn đã khai nộp/đã xử lý, rồi đến đơn đăng ký
 * SỚM NHẤT (theo thứ tự dòng). Đơn còn lại
 * (ví dụ đơn thừa tạo trước v7.7) = "Vượt hạn mức – không hợp lệ": không giữ slot, không được nộp tiền.
 * Script KHÔNG sửa/xoá các dòng đó; PM đổi trạng thái sang "Hủy" khi rà soát.
 * v7.9 (30/09/2026): MẬT KHẨU RIÊNG TỪNG NV. Đăng nhập kiểm tra ở máy chủ. Mật khẩu mặc định 123456 cho tới khi
 * NV tự đổi. Sheet "Accounts" (script tự tạo) chỉ THÊM dòng: mỗi lần đổi = 1 dòng CHANGE, lưu Salt + Mã băm
 * SHA-256, KHÔNG lưu mật khẩu gốc (PM cũng không xem được). Quên mật khẩu: PM thêm 1 dòng [thời gian, Mã NV, RESET]
 * -> mật khẩu trở về 123456. Sai 5 lần liên tiếp -> khoá 15 phút. Đăng nhập đúng -> cấp mã phiên (token) 12 giờ.
 * Config REQUIRE_LOGIN_TOKEN = TRUE: đăng ký / nộp tiền / tra cứu bắt buộc có token đúng Mã NV (bật khi mọi người
 * đã dùng trang mới). Chưa bật: token có gửi thì vẫn kiểm tra, không gửi thì cho qua như cũ.
 * v7.10 (30/09/2026): DANH SÁCH NV Ở MÁY CHỦ. Sheet "Employees" [Mã NV, Họ tên, Trạng thái, Ghi chú].
 * Đăng nhập / đổi mật khẩu / đăng ký / nộp tiền / tra cứu chỉ nhận Mã NV có trong sheet và Trạng thái khác "Ngừng".
 * Họ tên ghi vào đơn lấy theo sheet Employees (không lấy chữ trang gửi lên). Thêm người: thêm dòng; bỏ người: đổi
 * Trạng thái sang "Ngừng" (không xoá dòng). Sheet trống hoặc chưa có thì không chặn (như bản cũ).
 * v7.11 (30/09/2026) — GĐ 0 trước đợt 14/10:
 *  - Config OPEN_TIME / CLOSE_TIME (dd/mm/yyyy hh:mm, giờ VN): máy chủ từ chối đăng ký ngoài khung giờ. Để trống = không chặn.
 *  - Config PORTAL_PAUSED = TRUE: tạm dừng nhận đăng ký và khai nộp tiền (có hiệu lực sau tối đa 30 giây).
 *  - Máy chủ chặn khai nộp tiền trước PAY_OPEN_DELAY_HOURS giờ (mặc định 2) kể từ lúc đăng ký.
 *  - GET ?action=taken / ?action=status trả kèm giờ máy chủ, giờ mở/đóng, trạng thái tạm dừng cho trang.
 *  - Dọn các ô giữ chỗ slot đã hết hạn (Script Property 'claims' giới hạn 9 KB).
 *  - Config PAGE_FILE_ID = ID file HTML trên Drive: link web app mở thẳng trang đăng ký (1 link cho mọi NV).
 *  - Chế độ thử nhận testSheet = file "LoadTest ..." do công cụ thử tải (project Apps Script riêng) tạo.
 * v7.12 (30/09/2026): PM XÁC NHẬN ĐƠN TRƯỚC KHI NỘP TIỀN. Đơn mới = "Chờ PM xác nhận". PM đổi cột Trạng Thái
 * sang "Chờ nộp tiền" = đã xác nhận.
 * v7.13 (30/09/2026): nộp tiền mở NGAY khi PM xác nhận (PAY_OPEN_DELAY_HOURS mặc định 0; điền số giờ trong Config nếu muốn chờ thêm).
 * Chế độ thử tải: gửi test:true (POST) hoặc ?test=1 (GET) thì script dùng BẢN SAO sheet.
 *
 * Cách cài: xem docs/SETUP_APPS_SCRIPT.md
 */

// ID của Google Sheet "LG Internal Sales Database"
var SPREADSHEET_ID = '10aN5O3HL79asPGfug75IPv1w_ssGPo8edsASMuG3_aM';
// Bản sao dùng để thử tải (không phải dữ liệu thật)
var TEST_SPREADSHEET_ID = '1R4u0BEp2BjQBIEv3eCNm1WML4PedjgIsqjyhFWn4YY4';
var _useTest = false, _testRun = '', _testSheet = '';
// Khoá bộ nhớ đệm / Properties: bản sao dùng tiền tố riêng theo từng lượt thử, không lẫn với dữ liệu thật
function ck_(k) { return (_useTest ? 't' + _testRun + '_' : '') + k; }
var CLAIM_GRACE_MS = 120000; // slot vừa giữ chỗ nhưng chưa thấy trên sheet: coi là còn giữ trong 2 phút

var SHEET_REG = 'Registrations';
var SHEET_SLOTS = 'Slots';
var SHEET_CONFIG = 'Config';
var SHEET_LOG = 'ActivityLog';
var RECEIPT_FOLDER_NAME = 'Bien lai nop tien';
var MAX_FILE_BYTES = 5 * 1024 * 1024; // 5 MB
var LOCK_WAIT_MS = 30000;              // chờ tối đa 30 giây
var CACHE_CONFIG_SEC = 300;            // Config đổi thì sau tối đa 5 phút script mới thấy
var CACHE_SLOTS_SEC = 600;

var STATUS_NEW = 'Chờ nộp tiền';        // PM đã xác nhận đơn, chờ NV nộp tiền
var STATUS_WAIT_PM = 'Chờ PM xác nhận'; // đơn mới đăng ký, PM chưa xác nhận: chưa được nộp tiền
var STATUS_PAID = 'Đã khai nộp - chờ đối soát';
var STATUS_FREE = ['Hủy', 'Từ chối']; // đơn ở trạng thái này không giữ slot

// Cột trong Registrations (1-based)
var C = {
  TS: 1, CAMPAIGN: 2, DIVISION: 3, EMP_CODE: 4, EMP_NAME: 5, KHO: 6, MODEL: 7, SLOT: 8,
  PHONE: 9, ADDRESS: 10, AGREE: 11, STATUS: 12, PAYER_NAME: 13, PAYER_CODE: 14,
  AMOUNT: 15, BANK_TXN: 16, PAY_TIME: 17, RECEIPT: 18, PM_BY: 19, PM_DATE: 20, NOTE: 21, UA: 22,
  REQ: 23 // Mã yêu cầu (hệ thống)
};

/* ---------- Mở sheet (1 lần mỗi lượt chạy) ---------- */
var _book = null;
function book_() {
  if (_book) return _book;
  if (_useTest) {
    // File thử do công cụ thử tải tạo: tên phải bắt đầu "LoadTest " và không phải file dữ liệu thật
    if (_testSheet && _testSheet !== SPREADSHEET_ID) {
      try { var t = SpreadsheetApp.openById(_testSheet); if (/^LoadTest /.test(t.getName())) return (_book = t); } catch (e) {}
    }
    return (_book = SpreadsheetApp.openById(TEST_SPREADSHEET_ID));
  }
  try { var a = SpreadsheetApp.getActiveSpreadsheet(); if (a) return (_book = a); } catch (e) {}
  return (_book = SpreadsheetApp.openById(SPREADSHEET_ID));
}

function doGet(e) {
  _useTest = !!(e && e.parameter && e.parameter.test === '1');
  _testRun = _useTest ? str_(e.parameter.run).replace(/[^A-Za-z0-9]/g, '').slice(0, 12) : '';
  _testSheet = _useTest ? str_(e.parameter.sheet).replace(/[^A-Za-z0-9_-]/g, '') : '';
  var act = e && e.parameter ? str_(e.parameter.action) : '';
  if (act === 'taken') return json_(withSchedule_(taken_()));
  if (act === 'status') return json_(withSchedule_({ ok: true }));
  if (!act && !_useTest) { var pg = page_(); if (pg) return pg; }
  return json_({ ok: true, service: 'LG Internal Sales API', version: '7.13', test: _useTest, time: new Date().toISOString() });
}

/* ---------- Danh sách slot đã có người (chỉ mã slot, không kèm tên / Mã NV) ---------- */
var CACHE_TAKEN_SEC = 10;
function taken_() {
  var cache = CacheService.getScriptCache();
  var hit = cache.get(ck_('taken'));
  if (hit) return JSON.parse(hit);
  var reg = book_().getSheetByName(SHEET_REG);
  var n = reg.getLastRow() - 1;
  var v = n > 0 ? reg.getRange(2, C.EMP_CODE, n, C.STATUS - C.EMP_CODE + 1).getValues() : [];
  var eff = effective_(v.map(function (x) { return x[0]; }), v.map(function (x) { return x[C.STATUS - C.EMP_CODE]; }), maxPer_());
  var seen = {}, list = [];
  for (var r = 0; r < v.length; r++) {
    var slot = str_(v[r][C.SLOT - C.EMP_CODE]).replace(/^'+/, '');
    if (!slot || seen[slot]) continue;
    if (!eff[r]) continue; // đơn Hủy/Từ chối hoặc đơn thừa vượt hạn mức không giữ slot
    seen[slot] = true; list.push(slot);
  }
  // Cộng thêm slot vừa được giữ chỗ (chưa kịp hiện trên sheet)
  try {
    var claims = JSON.parse(PropertiesService.getScriptProperties().getProperty(ck_('claims')) || '{}');
    for (var k in claims) if (!seen[k] && Date.now() - claims[k].t < CLAIM_GRACE_MS) { seen[k] = true; list.push(k); }
  } catch (e) {}
  var out = { ok: true, taken: list, time: fmt_(new Date()) };
  cache.put(ck_('taken'), JSON.stringify(out), CACHE_TAKEN_SEC);
  return out;
}

function doPost(e) {
  try {
    var data = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    _useTest = data.test === true;
    _testRun = _useTest ? str_(data.testRun).replace(/[^A-Za-z0-9]/g, '').slice(0, 12) : '';
    _testSheet = _useTest ? str_(data.testSheet).replace(/[^A-Za-z0-9_-]/g, '') : '';
    if (/^(login|changePassword|register|payment|lookup)$/.test(String(data.action))) {
      var notEmp = empCheck_(data);
      if (notEmp) return json_(notEmp);
    }
    if (data.action === 'login') return json_(login_(data));
    if (data.action === 'changePassword') return json_(changePassword_(data));
    if (data.action === 'register' || data.action === 'payment' || data.action === 'lookup') {
      var denied = authCheck_(data);
      if (denied) return json_(denied);
    }
    if (data.action === 'register') return json_(register_(data));
    if (data.action === 'payment') return json_(payment_(data));
    if (data.action === 'lookup') return json_(lookup_(data));
    return json_({ ok: false, message: 'Yêu cầu không hợp lệ.' });
  } catch (err) {
    try { log_('ERROR', '', '', '', String(err)); } catch (e2) {}
    // Lỗi tạm của Google (quá tải, hết giờ): báo busy để trang tự gửi lại.
    // Gửi lại an toàn vì cùng Mã NV + cùng slot được coi là 1 đơn.
    return json_({ ok: false, busy: true, message: 'Hệ thống đang bận, vui lòng thử lại sau ít giây.' });
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
  var closed = windowCheck_(empCode, slotId, d.userAgent);
  if (closed) return closed;
  var cfg = config_();
  var warnings = [], notes = [];

  // Kiểm tra slot có trong danh sách và đúng kho (ngoài khoá, dùng bộ nhớ đệm)
  var slot = slots_()[slotId];
  if (!slot) warnings.push('Slot ' + slotId + ' không có trong danh sách.');
  else if (slot.kho !== str_(d.kho)) warnings.push('Slot ' + slotId + ' thuộc kho ' + slot.kho + ', không phải kho ' + d.kho + '.');

  var campaign = str_(cfg.CAMPAIGN_CODE);
  if (!campaign) notes.push('Config chưa có CAMPAIGN_CODE');
  var maxPer = Number(cfg.MAX_PER_EMPLOYEE) || 1;

  var reg = book_().getSheetByName(SHEET_REG);
  var iEmp = 0, iSlot = C.SLOT - C.EMP_CODE, iSt = C.STATUS - C.EMP_CODE;

  // ---- Bước 1: đọc sheet (không khoá). Quét HẾT các dòng còn hiệu lực ----
  var n = reg.getLastRow() - 1;
  var rows = n > 0 ? reg.getRange(2, C.EMP_CODE, n, C.STATUS - C.EMP_CODE + 1).getValues() : [];
  var empSlots = {}, slotOther = false;
  var eff = effective_(rows.map(function (x) { return x[iEmp]; }), rows.map(function (x) { return x[iSt]; }), maxPer);
  for (var r = 0; r < rows.length; r++) {
    if (!eff[r]) continue; // đơn đã Hủy/Từ chối hoặc đơn thừa vượt hạn mức: không tính, không giữ slot
    var em = String(rows[r][iEmp]).toUpperCase();
    var sl = String(rows[r][iSlot]).replace(/^'+/, '');
    if (sl === slotId && em === empCode) {
      // Chính người này đã giữ slot (gửi lại do mạng chập chờn): coi như thành công, không ghi thêm
      log_('REGISTER_REPEAT', empCode, slotId, d.userAgent, 'Gửi lại, đơn đã có ở dòng ' + (r + 2) + ', không ghi thêm');
      return { ok: true, row: r + 2, status: str_(rows[r][iSt]) || STATUS_WAIT_PM, repeat: true, warnings: [] };
    }
    if (sl === slotId) slotOther = true;
    else if (em === empCode) empSlots[sl] = r + 2;
  }
  // Đã đủ hạn mức: từ chối, không ghi dòng, không giữ slot
  if (Object.keys(empSlots).length >= maxPer) return limit_msg_(empCode, empSlots, maxPer, slotId, d.userAgent);
  if (slotOther) {
    log_('REGISTER_REJECTED_DUP_SLOT', empCode, slotId, d.userAgent, 'Slot đã có người đăng ký, không ghi đơn');
    return taken_msg_(slotId);
  }

  // ---- Bước 2: khoá rất ngắn, chỉ giữ chỗ slot + cấp số dòng (không đụng sheet trong khoá) ----
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(LOCK_WAIT_MS)) {
    return { ok: false, busy: true, message: 'Hệ thống đang bận, vui lòng thử lại sau ít giây.' };
  }
  var props = PropertiesService.getScriptProperties();
  var rowNo = 0, heldBy = null, overLimit = null;
  try {
    var claims = JSON.parse(props.getProperty(ck_('claims')) || '{}');
    // Cùng 1 Mã NV vừa giữ chỗ slot khác (chưa kịp hiện trên sheet): tính vào hạn mức
    var mine = {};
    for (var k0 in empSlots) mine[k0] = empSlots[k0];
    for (var k in claims) {
      if (k === slotId || claims[k].emp !== empCode || Date.now() - claims[k].t >= CLAIM_GRACE_MS) continue;
      var j = claims[k].row - 2;
      // Dòng đã hiện trên sheet thì đã được xét ở Bước 1 (kể cả khi PM đổi sang Hủy/Từ chối): bỏ qua
      if (j >= 0 && j < rows.length && String(rows[j][iSlot]).replace(/^'+/, '') === k) continue;
      mine[k] = claims[k].row;
    }
    if (Object.keys(mine).length >= maxPer) overLimit = mine;
    var c = overLimit ? null : claims[slotId];
    if (c) {
      var i2 = c.row - 2, inRead = i2 >= 0 && i2 < rows.length;
      // Dòng đã giữ bị PM đổi sang Hủy/Từ chối, hoặc giữ chỗ quá 2 phút mà không có dòng: slot được mở lại
      var freed = inRead && String(rows[i2][iSlot]).replace(/^'+/, '') === slotId && !eff[i2];
      var stale = Date.now() - c.t > CLAIM_GRACE_MS && (!inRead || String(rows[i2][iSlot]) !== slotId);
      if (!freed && !stale) heldBy = c;
    }
    if (!heldBy && !overLimit) {
      rowNo = Math.max(Number(props.getProperty(ck_('nextRow'))) || 0, n + 2);
      claims[slotId] = { emp: empCode, row: rowNo, t: Date.now() };
      pruneClaims_(claims);
      var upd = {};
      upd[ck_('claims')] = JSON.stringify(claims);
      upd[ck_('nextRow')] = String(rowNo + 1);
      props.setProperties(upd);
    }
  } finally {
    lock.releaseLock();
  }
  if (overLimit) return limit_msg_(empCode, overLimit, maxPer, slotId, d.userAgent);
  if (heldBy) {
    if (heldBy.emp === empCode) {
      log_('REGISTER_REPEAT', empCode, slotId, d.userAgent, 'Gửi lặp, đơn đang ghi ở dòng ' + heldBy.row + ', không ghi thêm');
      return { ok: true, row: heldBy.row, status: STATUS_WAIT_PM, repeat: true, warnings: [] };
    }
    log_('REGISTER_REJECTED_DUP_SLOT', empCode, slotId, d.userAgent, 'Slot vừa được người khác giữ chỗ (dòng ' + heldBy.row + '), không ghi đơn');
    return taken_msg_(slotId);
  }

  // ---- Bước 3: ghi vào đúng dòng đã cấp (ngoài khoá) ----
  if (warnings.length) notes = notes.concat(warnings);
  var ts = new Date();
  var row = new Array(C.REQ).fill('');
  row[C.TS - 1] = ts;
  row[C.CAMPAIGN - 1] = campaign;
  row[C.DIVISION - 1] = safe_(d.division);
  row[C.EMP_CODE - 1] = safe_(empCode);
  var master = employees_();
  var mName = master && master[str_(d.empCode).toUpperCase().replace(/\s+/g, '')];
  row[C.EMP_NAME - 1] = safe_(mName && mName.name ? mName.name : d.empName); // họ tên theo sheet Employees
  row[C.KHO - 1] = safe_(d.kho);
  row[C.MODEL - 1] = safe_(d.model);
  row[C.SLOT - 1] = "'" + slotId.replace(/^'+/, '');
  row[C.PHONE - 1] = "'" + str_(d.phone);
  row[C.ADDRESS - 1] = safe_(d.address);
  row[C.AGREE - 1] = 'Đồng ý';
  row[C.STATUS - 1] = STATUS_WAIT_PM;
  row[C.NOTE - 1] = safe_(notes.join(' | '));
  row[C.UA - 1] = safe_(str_(d.userAgent).slice(0, 300));
  row[C.REQ - 1] = Utilities.getUuid();
  try {
    if (reg.getMaxRows() < rowNo) reg.insertRowsAfter(reg.getMaxRows(), Math.max(50, rowNo - reg.getMaxRows()));
    reg.getRange(rowNo, 1, 1, C.REQ).setValues([row]);
  } catch (err) {
    releaseClaim_(slotId, rowNo); // ghi lỗi: trả slot lại để lần gửi lại (tự động) giữ chỗ lại
    throw err;
  }

  try { CacheService.getScriptCache().remove(ck_('taken')); } catch (e) {}
  log_('REGISTER', empCode, slotId, d.userAgent, 'Dòng ' + rowNo + (warnings.length ? ' | ' + warnings.join(' | ') : ''));
  return { ok: true, row: rowNo, status: STATUS_WAIT_PM, timestamp: fmt_(ts), warnings: warnings };
}

function releaseClaim_(slotId, rowNo) {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(LOCK_WAIT_MS)) return;
  try {
    var props = PropertiesService.getScriptProperties();
    var claims = JSON.parse(props.getProperty(ck_('claims')) || '{}');
    // Đánh dấu hết hạn (không xoá): dòng chưa ghi nên lần gửi sau được giữ chỗ lại
    if (claims[slotId] && claims[slotId].row === rowNo) { claims[slotId].t = 0; pruneClaims_(claims); props.setProperty(ck_('claims'), JSON.stringify(claims)); }
  } finally { lock.releaseLock(); }
}

// eff[i] = true nếu dòng i là đơn hợp lệ. Mỗi Mã NV chỉ có tối đa maxPer đơn hợp lệ:
// ưu tiên đơn đã khai nộp / đã xử lý (khác "Chờ PM xác nhận" / "Chờ nộp tiền"), sau đó đến đơn đăng ký sớm nhất.
// Đơn Hủy/Từ chối không bao giờ hợp lệ.
function effective_(emps, stats, maxPer) {
  var cnt = {}, eff = [], i, e, st;
  for (i = 0; i < emps.length; i++) eff.push(false);
  for (var pass = 0; pass < 2; pass++) {
    for (i = 0; i < emps.length; i++) {
      st = String(stats[i]);
      if (STATUS_FREE.indexOf(st) >= 0) continue;
      var progressed = !!st && st !== STATUS_NEW && st !== STATUS_WAIT_PM;
      if ((pass === 0) !== progressed) continue;
      e = String(emps[i]).toUpperCase();
      cnt[e] = (cnt[e] || 0) + 1;
      eff[i] = cnt[e] <= maxPer;
    }
  }
  return eff;
}
function maxPer_() { return Number(config_().MAX_PER_EMPLOYEE) || 1; }
var STATUS_OVER = 'Vượt hạn mức – không hợp lệ';

function limit_msg_(empCode, slots, maxPer, slotId, ua) {
  var list = Object.keys(slots);
  log_('REGISTER_REJECTED_LIMIT', empCode, slotId, ua, 'Đã có đơn: ' + list.join(', ') + ' | hạn mức ' + maxPer + ' SP/NV, không ghi đơn');
  return {
    ok: false, limitReached: true, existing: list,
    message: 'Mã NV ' + empCode + ' đã có đơn đăng ký hợp lệ (Slot ' + list.join(', ') + '). ' +
             'Theo quy định, mỗi nhân viên chỉ được mua tối đa ' + (maxPer < 10 ? '0' + maxPer : maxPer) + ' sản phẩm. ' +
             'Đăng ký này KHÔNG hợp lệ và KHÔNG được ghi nhận.'
  };
}

function taken_msg_(slotId) {
  try { CacheService.getScriptCache().remove(ck_('taken')); } catch (e) {}
  return { ok: false, slotTaken: true, message: 'Slot ' + slotId + ' đã có người đăng ký trước. Vui lòng chọn slot khác.' };
}

/* ---------- Khai nộp tiền (Tab 3) ---------- */
function payment_(d) {
  var req = ['slotId', 'empCode', 'payerName', 'payerCode', 'amount', 'bankTxn', 'payTime'];
  for (var i = 0; i < req.length; i++) {
    if (!str_(d[req[i]])) return { ok: false, message: 'Thiếu thông tin: ' + req[i] };
  }
  var slotId = str_(d.slotId), empCode = str_(d.empCode).toUpperCase();
  var reg = book_().getSheetByName(SHEET_REG);
  if (schedule_().paused) return pausedMsg_(empCode, slotId, d.userAgent, 'PAYMENT');

  // Kiểm tra trước (không khoá) để không lưu biên lai thừa
  var pre = findOrder_(reg, slotId, empCode);
  if (!pre) {
    log_('PAYMENT_NOT_FOUND', empCode, slotId, d.userAgent, 'Không tìm thấy đơn đăng ký');
    return { ok: false, message: 'Không tìm thấy đơn đăng ký với Slot ' + slotId + ' và Mã NV ' + empCode + '. Vui lòng đăng ký ở Tab 2 trước.' };
  }
  if (pre.paid && pre.txn === str_(d.bankTxn)) return { ok: true, row: pre.rowNo, status: STATUS_PAID, repeat: true };
  if (pre.paid) return paidAlready_(d, empCode, slotId, pre.rowNo);
  if (!pre.valid) return invalid_msg_(d, empCode, slotId, pre);
  if (pre.status === STATUS_WAIT_PM && !_useTest) return needPm_(empCode, slotId, d.userAgent, pre.rowNo);
  var early = payDelayCheck_(reg, pre.rowNo, empCode, slotId, d.userAgent);
  if (early) return early;

  // Lưu biên lai (việc chậm) trước khi khoá
  var link = '';
  if (d.fileBase64 && _useTest) {
    // Thử tải: kiểm tra và giải mã file như thật nhưng KHÔNG lưu vào Drive
    var tm = /^data:([^;]+);base64,(.+)$/.exec(d.fileBase64);
    if (!tm || Utilities.base64Decode(tm[2]).length > MAX_FILE_BYTES) return { ok: false, message: 'File thử không hợp lệ' };
  } else if (d.fileBase64) {
    try { link = saveReceipt_(d.fileBase64, d.fileName, slotId, empCode); }
    catch (err) { log_('RECEIPT_ERROR', empCode, slotId, d.userAgent, String(err)); return { ok: false, message: 'Không lưu được file biên lai: ' + err }; }
  }

  var lock = LockService.getScriptLock();
  if (!lock.tryLock(LOCK_WAIT_MS)) {
    return { ok: false, busy: true, message: 'Hệ thống đang bận, vui lòng thử lại sau ít giây.' };
  }
  var found, dup = false, bad = false, waitPm = false;
  try {
    found = findOrder_(reg, slotId, empCode); // kiểm tra lại trong khoá
    if (found && found.paid) dup = true;
    else if (found && !found.valid) bad = true;
    else if (found && found.status === STATUS_WAIT_PM && !_useTest) waitPm = true;
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
  if (bad) return invalid_msg_(d, empCode, slotId, found);
  if (waitPm) return needPm_(empCode, slotId, d.userAgent, found.rowNo);
  if (dup && found.txn === str_(d.bankTxn)) return { ok: true, row: found.rowNo, status: STATUS_PAID, repeat: true };
  if (dup) return paidAlready_(d, empCode, slotId, found.rowNo);

  log_('PAYMENT', empCode, slotId, d.userAgent, 'Dòng ' + found.rowNo + (link ? ' | có biên lai' : ' | chưa có file biên lai'));
  return { ok: true, row: found.rowNo, status: STATUS_PAID, receipt: !!link };
}

function paidAlready_(d, empCode, slotId, rowNo) {
  log_('PAYMENT_DUPLICATE', empCode, slotId, d.userAgent, 'Dòng ' + rowNo + ' đã khai nộp trước đó. Mã GD mới: ' + str_(d.bankTxn));
  return { ok: false, message: 'Đơn này đã khai nộp tiền trước đó. Nếu cần sửa, vui lòng liên hệ PM phụ trách.' };
}

// Đơn gần nhất khớp Slot + Mã NV (đọc cột D..P), kèm cờ hợp lệ theo quy tắc hạn mức
function findOrder_(reg, slotId, empCode) {
  var n = reg.getLastRow() - 1;
  if (n < 1) return null;
  var v = reg.getRange(2, C.EMP_CODE, n, C.BANK_TXN - C.EMP_CODE + 1).getValues();
  var iSt = C.STATUS - C.EMP_CODE, iSl = C.SLOT - C.EMP_CODE;
  var eff = effective_(v.map(function (x) { return x[0]; }), v.map(function (x) { return x[iSt]; }), maxPer_());
  var validSlots = [];
  for (var k = 0; k < v.length; k++) if (eff[k] && String(v[k][0]).toUpperCase() === empCode) validSlots.push(String(v[k][iSl]).replace(/^'+/, ''));
  for (var r = v.length - 1; r >= 0; r--) {
    if (String(v[r][iSl]).replace(/^'+/, '') === slotId && String(v[r][0]).toUpperCase() === empCode) {
      var paid = !!(str_(v[r][C.PAYER_NAME - C.EMP_CODE]) || str_(v[r][C.BANK_TXN - C.EMP_CODE]));
      return { rowNo: r + 2, paid: paid, txn: str_(v[r][C.BANK_TXN - C.EMP_CODE]), valid: eff[r], validSlots: validSlots, status: str_(v[r][iSt]) };
    }
  }
  return null;
}
function invalid_msg_(d, empCode, slotId, found) {
  log_('PAYMENT_REJECTED_INVALID', empCode, slotId, d.userAgent, 'Dòng ' + found.rowNo + ' không hợp lệ (vượt hạn mức hoặc đã hủy). Đơn hợp lệ: ' + (found.validSlots.join(', ') || 'không có'));
  return { ok: false, invalidOrder: true,
    message: 'Đơn Slot ' + slotId + ' KHÔNG hợp lệ (vượt hạn mức 01 sản phẩm/nhân viên hoặc đã bị hủy) nên không được nộp tiền.' +
             (found.validSlots.length ? ' Đơn hợp lệ của bạn là Slot ' + found.validSlots.join(', ') + '.' : '') };
}

/* ---------- Tra cứu đơn (Mã NV + 4 số cuối SĐT) ---------- */
function lookup_(d) {
  var empCode = str_(d.empCode).toUpperCase();
  var last4 = str_(d.phoneLast4).replace(/\D/g, '');
  if (!empCode || last4.length !== 4) return { ok: false, message: 'Vui lòng nhập Mã NV và đúng 4 số cuối điện thoại đã đăng ký.' };

  var reg = book_().getSheetByName(SHEET_REG);
  var n = reg.getLastRow() - 1;
  var v = n > 0 ? reg.getRange(2, 1, n, C.RECEIPT).getValues() : [];
  var eff = effective_(v.map(function (x) { return x[C.EMP_CODE - 1]; }), v.map(function (x) { return x[C.STATUS - 1]; }), maxPer_());
  var out = [];
  for (var r = 0; r < v.length; r++) {
    if (String(v[r][C.EMP_CODE - 1]).toUpperCase() !== empCode) continue;
    var phone = String(v[r][C.PHONE - 1]).replace(/\D/g, '');
    if (phone.slice(-4) !== last4) continue;
    out.push({
      time: v[r][0] instanceof Date ? fmt_(v[r][0]) : str_(v[r][0]),
      slot: str_(v[r][C.SLOT - 1]), kho: str_(v[r][C.KHO - 1]), model: str_(v[r][C.MODEL - 1]),
      status: (!eff[r] && STATUS_FREE.indexOf(String(v[r][C.STATUS - 1])) < 0) ? STATUS_OVER : (str_(v[r][C.STATUS - 1]) || 'Chưa có trạng thái'),
      valid: !!eff[r],
      paid: !!str_(v[r][C.BANK_TXN - 1]), receipt: !!str_(v[r][C.RECEIPT - 1])
    });
  }
  if (!out.length) {
    log_('LOOKUP_NOT_FOUND', empCode, '', d.userAgent, 'Tra cứu không khớp');
    return { ok: false, message: 'Không tìm thấy đơn khớp Mã NV và 4 số cuối điện thoại này.' };
  }
  return { ok: true, orders: out };
}

/* ---------- Khung giờ, tạm dừng, giờ máy chủ (v7.11) ---------- */
var CACHE_SCHED_SEC = 30; // đổi OPEN_TIME / CLOSE_TIME / PORTAL_PAUSED thì sau tối đa 30 giây có hiệu lực
// "14/10/2026 10:00" hoặc "14/10/2026 10:00:00" (giờ Việt Nam) -> mốc thời gian (ms); sai định dạng -> null
function vnTime_(v) {
  var m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})\s+(\d{1,2}):(\d{2})(?::(\d{2}))?$/.exec(str_(v));
  if (!m) return null;
  return Date.UTC(+m[3], +m[2] - 1, +m[1], +m[4] - 7, +m[5], +(m[6] || 0));
}
function schedule_() {
  var cache = CacheService.getScriptCache();
  var hit = cache.get(ck_('sched'));
  if (hit) return JSON.parse(hit);
  var sh = book_().getSheetByName(SHEET_CONFIG), o = { openAt: null, closeAt: null, paused: false };
  if (sh && sh.getLastRow() > 1) {
    var v = sh.getRange(2, 1, sh.getLastRow() - 1, 2).getValues();
    for (var i = 0; i < v.length; i++) {
      var k = str_(v[i][0]), val = v[i][1] instanceof Date ? fmt_(v[i][1]) : str_(v[i][1]);
      if (k === 'OPEN_TIME') { o.openAt = vnTime_(val); if (val && !o.openAt) o.badTime = true; }
      else if (k === 'CLOSE_TIME') { o.closeAt = vnTime_(val); if (val && !o.closeAt) o.badTime = true; }
      else if (k === 'PORTAL_PAUSED') o.paused = /^(true|1|yes|có|co)$/i.test(val);
    }
  }
  try { cache.put(ck_('sched'), JSON.stringify(o), CACHE_SCHED_SEC); } catch (e) {}
  return o;
}
function withSchedule_(out) {
  var s = schedule_();
  out.serverNow = Date.now(); out.openAt = s.openAt; out.closeAt = s.closeAt; out.paused = s.paused;
  if (s.badTime) out.badTime = true; // OPEN_TIME / CLOSE_TIME sai định dạng: không chặn, PM cần sửa
  return out;
}
function pausedMsg_(empCode, slotId, ua, what) {
  log_(what + '_REJECTED_PAUSED', empCode, slotId, ua, 'Cổng đang tạm dừng (PORTAL_PAUSED)');
  return { ok: false, paused: true, message: 'Cổng đăng ký đang tạm dừng để kiểm tra. Vui lòng thử lại sau ít phút.' };
}
// null = cho đăng ký; ngược lại trả lỗi (ngoài giờ mở/đóng hoặc đang tạm dừng)
function windowCheck_(empCode, slotId, ua) {
  var s = schedule_(), now = Date.now();
  if (s.paused) return pausedMsg_(empCode, slotId, ua, 'REGISTER');
  if (s.openAt && now < s.openAt) {
    log_('REGISTER_REJECTED_TIME', empCode, slotId, ua, 'Trước giờ mở cổng');
    return { ok: false, notOpen: true, openAt: s.openAt, message: 'Cổng đăng ký chưa mở. Giờ mở: ' + fmt_(new Date(s.openAt)) + '.' };
  }
  if (s.closeAt && now > s.closeAt) {
    log_('REGISTER_REJECTED_TIME', empCode, slotId, ua, 'Sau giờ đóng cổng');
    return { ok: false, closed: true, message: 'Cổng đăng ký đã đóng lúc ' + fmt_(new Date(s.closeAt)) + '.' };
  }
  return null;
}
// Chỉ cho khai nộp tiền sau PAY_OPEN_DELAY_HOURS giờ kể từ lúc đăng ký (cột A của dòng đơn)
function payDelayCheck_(reg, rowNo, empCode, slotId, ua) {
  if (_useTest) return null;
  var h = Number(config_().PAY_OPEN_DELAY_HOURS);
  if (!(h >= 0)) h = 0; // mặc định: không chờ, nộp tiền mở khi PM xác nhận
  if (!h) return null;
  var ts = reg.getRange(rowNo, C.TS).getValue();
  var t = ts instanceof Date ? ts.getTime() : vnTime_(ts);
  if (!t) return null; // không đọc được giờ đăng ký: không chặn, PM đối soát
  var openAt = t + h * 3600000;
  if (Date.now() >= openAt) return null;
  log_('PAYMENT_REJECTED_EARLY', empCode, slotId, ua, 'Dòng ' + rowNo + ' | mở nộp tiền lúc ' + fmt_(new Date(openAt)));
  return { ok: false, tooEarly: true, payOpenAt: openAt, message: 'Chưa đến giờ khai nộp tiền cho Slot ' + slotId + '. Mở lúc ' + fmt_(new Date(openAt)) + '.' };
}
function needPm_(empCode, slotId, ua, rowNo) {
  log_('PAYMENT_REJECTED_WAIT_PM', empCode, slotId, ua, 'Dòng ' + rowNo + ' chưa được PM xác nhận');
  return { ok: false, needPmConfirm: true, message: 'Đơn Slot ' + slotId + ' chưa được PM xác nhận nên chưa được nộp tiền. Nút Nộp tiền sẽ mở khi PM xác nhận. Vui lòng CHƯA chuyển khoản.' };
}
// Bỏ các ô giữ chỗ đã hết hạn (quá CLAIM_GRACE_MS): khi đó sheet đã là nguồn đúng
function pruneClaims_(claims) {
  var now = Date.now();
  for (var k in claims) if (!(now - claims[k].t < CLAIM_GRACE_MS)) delete claims[k];
}

/* ---------- Phục vụ trang đăng ký từ Drive (1 link cho mọi NV) ---------- */
var PAGE_CHUNK = 90000, CACHE_PAGE_SEC = 600;
function page_() {
  var id = str_(config_().PAGE_FILE_ID);
  if (!id) return null;
  var cache = CacheService.getScriptCache(), html = null;
  var meta = cache.get('pg_' + id);
  if (meta) {
    var keys = [];
    for (var i = 0; i < Number(meta); i++) keys.push('pg_' + id + '_' + i);
    var got = cache.getAll(keys), parts = [];
    for (var j = 0; j < keys.length; j++) { if (got[keys[j]] == null) { parts = null; break; } parts.push(got[keys[j]]); }
    if (parts) html = parts.join('');
  }
  if (html == null) {
    html = DriveApp.getFileById(id).getBlob().getDataAsString('UTF-8');
    try {
      var put = {}, n = Math.ceil(html.length / PAGE_CHUNK);
      for (var c = 0; c < n; c++) put['pg_' + id + '_' + c] = html.slice(c * PAGE_CHUNK, (c + 1) * PAGE_CHUNK);
      cache.putAll(put, CACHE_PAGE_SEC);
      cache.put('pg_' + id, String(n), CACHE_PAGE_SEC);
    } catch (e) {}
  }
  return HtmlService.createHtmlOutput(html)
    .setTitle('LG Internal Sales Portal')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/* ---------- Danh sách nhân viên được mua (v7.10) ---------- */
var SHEET_EMP = 'Employees';
var CACHE_EMP_SEC = 300; // sửa sheet Employees thì sau tối đa 5 phút script mới thấy (hoặc chạy clearCache)
// null = chưa có danh sách (không chặn); ngược lại { MÃ_NV: { name, active } }
function employees_() {
  var cache = CacheService.getScriptCache();
  var hit = cache.get(ck_('emps'));
  if (hit) return JSON.parse(hit);
  var sh = book_().getSheetByName(SHEET_EMP), o = null;
  if (sh && sh.getLastRow() > 1) {
    var v = sh.getRange(2, 1, sh.getLastRow() - 1, 3).getValues();
    for (var i = 0; i < v.length; i++) {
      var code = str_(v[i][0]).toUpperCase().replace(/\s+/g, '');
      if (!code) continue;
      o = o || {};
      o[code] = { name: str_(v[i][1]), active: !/ng[ừu]ng|stop|kh[oó]a|khoá/i.test(str_(v[i][2])) };
    }
  }
  try { cache.put(ck_('emps'), JSON.stringify(o), CACHE_EMP_SEC); } catch (e) {}
  return o;
}
function empCheck_(d) {
  if (_useTest) return null;
  var list = employees_();
  if (!list) return null;
  var emp = str_(d.empCode).toUpperCase().replace(/\s+/g, '');
  var e = list[emp];
  if (e && e.active) return null;
  log_('EMP_REJECTED', emp, str_(d.slotId), d.userAgent, (e ? 'Mã NV đang ở trạng thái Ngừng' : 'Mã NV không có trong sheet Employees') + ' | ' + str_(d.action));
  return { ok: false, notEmployee: true,
    message: e ? 'Mã NV ' + emp + ' hiện không được mua trong đợt này. Vui lòng liên hệ PM Support.'
               : 'Mã NV "' + emp + '" không có trong danh sách được mua đợt này. Kiểm tra lại hoặc liên hệ PM Support.' };
}

/* ---------- Tài khoản: đăng nhập, đổi mật khẩu (v7.9) ---------- */
var SHEET_ACC = 'Accounts';
var DEFAULT_PW = '123456';
var TOKEN_TTL_MS = 12 * 3600 * 1000;   // phiên đăng nhập 12 giờ
var LOGIN_MAX_FAIL = 5;                // sai 5 lần liên tiếp
var LOGIN_LOCK_SEC = 900;              // thì khoá 15 phút
var PW_ITER = 300;                     // số vòng băm
var PW_MIN = 6, PW_MAX = 32;

function accSheet_() {
  var b = book_(), sh = b.getSheetByName(SHEET_ACC);
  if (sh) return sh;
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(LOCK_WAIT_MS)) throw 'busy';
  try {
    sh = b.getSheetByName(SHEET_ACC);
    if (!sh) {
      sh = b.insertSheet(SHEET_ACC);
      sh.getRange(1, 1, 1, 6).setValues([['Thời gian', 'Mã NV', 'Thao tác (CHANGE / RESET)', 'Salt', 'Mã băm SHA-256 (không phải mật khẩu)', 'Ghi chú']]);
      sh.setFrozenRows(1);
    }
  } finally { lock.releaseLock(); }
  return sh;
}
// Dòng mới nhất của Mã NV quyết định: CHANGE = mật khẩu riêng; RESET hoặc chưa có dòng = mật khẩu mặc định
function account_(empCode) {
  var sh = accSheet_(), n = sh.getLastRow() - 1;
  var v = n > 0 ? sh.getRange(2, 2, n, 4).getValues() : [];
  for (var r = v.length - 1; r >= 0; r--) {
    if (str_(v[r][0]).toUpperCase() !== empCode) continue;
    var act = str_(v[r][1]).toUpperCase();
    if (act === 'CHANGE' && str_(v[r][2]) && str_(v[r][3])) return { custom: true, salt: str_(v[r][2]), hash: str_(v[r][3]) };
    if (act === 'RESET') return { custom: false };
  }
  return { custom: false };
}
function hex_(bytes) {
  var o = '';
  for (var i = 0; i < bytes.length; i++) { var b = (bytes[i] + 256) % 256; o += (b < 16 ? '0' : '') + b.toString(16); }
  return o;
}
function hashPw_(salt, pw) {
  var h = salt + '|' + pw;
  for (var i = 0; i < PW_ITER; i++) h = hex_(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, h + '|' + salt, Utilities.Charset.UTF_8));
  return h;
}
function pwOk_(acc, pw) { return acc.custom ? hashPw_(acc.salt, pw) === acc.hash : pw === DEFAULT_PW; }

function secret_() {
  var p = PropertiesService.getScriptProperties(), k = ck_('authSecret');
  var s = p.getProperty(k);
  if (!s) { s = Utilities.getUuid() + Utilities.getUuid(); p.setProperty(k, s); }
  return s;
}
function sign_(payload) {
  return Utilities.base64EncodeWebSafe(Utilities.computeHmacSha256Signature(payload, secret_())).replace(/=+$/, '');
}
function token_(empCode) { var pl = empCode + '.' + (Date.now() + TOKEN_TTL_MS); return pl + '.' + sign_(pl); }
function tokenEmp_(tok) {
  var m = /^(.+)\.(\d+)\.([A-Za-z0-9_-]+)$/.exec(str_(tok));
  if (!m || Number(m[2]) < Date.now() || sign_(m[1] + '.' + m[2]) !== m[3]) return '';
  return m[1];
}
// null = cho qua; ngược lại trả lỗi yêu cầu đăng nhập lại
function authCheck_(d) {
  if (_useTest) return null;
  var emp = str_(d.empCode).toUpperCase(), tok = str_(d.token);
  var need = /^(true|1|yes|có|co)$/i.test(str_(config_().REQUIRE_LOGIN_TOKEN));
  if (!tok && !need) return null;
  if (tok && tokenEmp_(tok) === emp && emp) return null;
  log_('AUTH_REJECTED', emp, str_(d.slotId), d.userAgent, tok ? 'Mã phiên sai / hết hạn / khác Mã NV' : 'Không có mã phiên');
  return { ok: false, authRequired: true, message: 'Phiên đăng nhập đã hết hạn hoặc không đúng Mã NV. Vui lòng đăng nhập lại.' };
}

function failKey_(emp) { return ck_('lf_' + emp); }
function lockedMsg_() { return { ok: false, locked: true, message: 'Nhập sai mật khẩu ' + LOGIN_MAX_FAIL + ' lần. Tài khoản tạm khoá ' + (LOGIN_LOCK_SEC / 60) + ' phút. Quên mật khẩu: liên hệ PM để đặt lại.' }; }
function isLocked_(emp) { return Number(CacheService.getScriptCache().get(failKey_(emp)) || 0) >= LOGIN_MAX_FAIL; }
function addFail_(emp) {
  var c = CacheService.getScriptCache(), k = failKey_(emp);
  var n = Number(c.get(k) || 0) + 1;
  c.put(k, String(n), LOGIN_LOCK_SEC);
  return n;
}
function empOk_(emp) { return /^[A-Z0-9.]{3,15}$/.test(emp); }

function login_(d) {
  var emp = str_(d.empCode).toUpperCase().replace(/\s+/g, ''), pw = String(d.password || '');
  if (!empOk_(emp) || !pw) return { ok: false, message: 'Vui lòng nhập Mã NV và mật khẩu.' };
  if (isLocked_(emp)) return lockedMsg_();
  var acc = account_(emp);
  if (!pwOk_(acc, pw)) {
    var n = addFail_(emp);
    log_('LOGIN_FAIL', emp, '', d.userAgent, 'Sai mật khẩu lần ' + n);
    if (n >= LOGIN_MAX_FAIL) return lockedMsg_();
    return { ok: false, message: 'Mật khẩu không đúng. Còn ' + (LOGIN_MAX_FAIL - n) + ' lần thử trước khi bị khoá ' + (LOGIN_LOCK_SEC / 60) + ' phút.' };
  }
  CacheService.getScriptCache().remove(failKey_(emp));
  log_('LOGIN', emp, '', d.userAgent, acc.custom ? 'Mật khẩu riêng' : 'Mật khẩu mặc định');
  var el = employees_(), nm = el && el[emp] ? el[emp].name : '';
  return { ok: true, token: token_(emp), defaultPassword: !acc.custom, empName: nm };
}

function changePassword_(d) {
  var emp = str_(d.empCode).toUpperCase().replace(/\s+/g, '');
  var oldPw = String(d.oldPassword || ''), newPw = String(d.newPassword || '');
  if (!empOk_(emp) || !oldPw || !newPw) return { ok: false, message: 'Vui lòng nhập đủ mật khẩu hiện tại và mật khẩu mới.' };
  if (isLocked_(emp)) return lockedMsg_();
  var bad = pwRule_(emp, oldPw, newPw);
  if (bad) return { ok: false, message: bad };
  var acc = account_(emp);
  if (!pwOk_(acc, oldPw)) {
    var n = addFail_(emp);
    log_('PASSWORD_CHANGE_FAIL', emp, '', d.userAgent, 'Sai mật khẩu hiện tại lần ' + n);
    if (n >= LOGIN_MAX_FAIL) return lockedMsg_();
    return { ok: false, message: 'Mật khẩu hiện tại không đúng. Còn ' + (LOGIN_MAX_FAIL - n) + ' lần thử.' };
  }
  var salt = Utilities.getUuid().replace(/-/g, '');
  accSheet_().appendRow([new Date(), emp, 'CHANGE', salt, hashPw_(salt, newPw), 'NV tự đổi trên cổng đăng ký']);
  CacheService.getScriptCache().remove(failKey_(emp));
  log_('PASSWORD_CHANGE', emp, '', d.userAgent, acc.custom ? 'Đổi mật khẩu riêng' : 'Đổi từ mật khẩu mặc định');
  return { ok: true, token: token_(emp), message: 'Đã đổi mật khẩu. Lần sau đăng nhập bằng mật khẩu mới.' };
}
// Quy tắc mật khẩu mới (trang cũng kiểm tra y hệt)
function pwRule_(emp, oldPw, newPw) {
  if (newPw.length < PW_MIN || newPw.length > PW_MAX) return 'Mật khẩu mới phải dài ' + PW_MIN + '–' + PW_MAX + ' ký tự.';
  if (/\s/.test(newPw)) return 'Mật khẩu mới không được có khoảng trắng.';
  if (newPw === DEFAULT_PW) return 'Không được dùng lại mật khẩu mặc định 123456.';
  if (newPw === oldPw) return 'Mật khẩu mới phải khác mật khẩu hiện tại.';
  if (newPw.toUpperCase().indexOf(emp) >= 0) return 'Mật khẩu mới không được chứa Mã NV.';
  if (/^(.)\1+$/.test(newPw) || '0123456789012345678909876543210'.indexOf(newPw) >= 0) return 'Mật khẩu quá dễ đoán (dãy số liên tiếp hoặc lặp một ký tự).';
  return '';
}

/* ---------- Bộ nhớ đệm Config / Slots ---------- */
function config_() {
  var cache = CacheService.getScriptCache();
  var hit = cache.get(ck_('cfg'));
  if (hit) return JSON.parse(hit);
  var sh = book_().getSheetByName(SHEET_CONFIG);
  var v = sh.getRange(2, 1, Math.max(sh.getLastRow() - 1, 1), 2).getValues();
  var o = {};
  for (var i = 0; i < v.length; i++) if (v[i][0]) o[String(v[i][0])] = v[i][1] instanceof Date ? fmt_(v[i][1]) : v[i][1];
  cache.put(ck_('cfg'), JSON.stringify(o), CACHE_CONFIG_SEC);
  return o;
}

function slots_() {
  var cache = CacheService.getScriptCache();
  var hit = cache.get(ck_('slots'));
  if (hit) return JSON.parse(hit);
  var sh = book_().getSheetByName(SHEET_SLOTS);
  var v = sh.getRange(2, 1, Math.max(sh.getLastRow() - 1, 1), 4).getValues();
  var o = {};
  for (var i = 0; i < v.length; i++) if (v[i][2]) o[String(v[i][2])] = { kho: String(v[i][0]), model: String(v[i][3]) };
  cache.put(ck_('slots'), JSON.stringify(o), CACHE_SLOTS_SEC);
  return o;
}

/** Chạy tay khi vừa sửa Config hoặc Slots để script thấy ngay. */
function clearCache() {
  CacheService.getScriptCache().removeAll(['cfg', 'slots', 'taken', 'emps', 'sched', 't_cfg', 't_slots', 't_taken', 't_sched']);
  var pid = str_(config_().PAGE_FILE_ID);
  if (pid) CacheService.getScriptCache().remove('pg_' + pid);
  Logger.log('Đã xoá bộ nhớ đệm Config, Slots, Employees, giờ mở/đóng, trang.');
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

// Nhật ký: cấp số dòng qua khoá riêng (UserLock) rồi ghi đúng dòng, để nhiều lượt cùng lúc không ghi đè nhau
function log_(action, empCode, slotId, ua, details) {
  var sh = book_().getSheetByName(SHEET_LOG);
  if (!sh) return;
  var line = [new Date(), action, safe_(empCode), slotId ? "'" + slotId : '', safe_(str_(ua).slice(0, 300)), safe_(details)];
  var last = sh.getLastRow(), r = 0;
  var lk = LockService.getUserLock();
  if (lk.tryLock(10000)) {
    try {
      var p = PropertiesService.getScriptProperties();
      r = Math.max(Number(p.getProperty(ck_('logNext'))) || 0, last + 1);
      p.setProperty(ck_('logNext'), String(r + 1));
    } finally { lk.releaseLock(); }
  }
  if (!r) { sh.appendRow(line); return; }
  if (sh.getMaxRows() < r) sh.insertRowsAfter(sh.getMaxRows(), Math.max(50, r - sh.getMaxRows()));
  sh.getRange(r, 1, 1, line.length).setValues([line]);
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

