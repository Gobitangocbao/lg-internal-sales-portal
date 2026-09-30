/* ======================================================================
 * LG Internal Sales — CÔNG CỤ THỬ TẢI (project Apps Script RIÊNG, không nằm trong web app thật)
 * Cách chạy: chọn hàm loadTest300 > Chạy. Lần đầu Google hỏi cấp quyền: chị tự bấm Cho phép.
 * - Tạo 1 file Google Sheet THỬ MỚI (chép Slots + Config, sheet đơn trống). Không đọc/ghi đơn thật.
 * - Gửi yêu cầu thật tới web app (chế độ test) theo 3 đợt: đăng nhập, đăng ký, khai nộp tiền (ảnh ~1 MB, không lưu Drive).
 * - Tự gửi lại khi máy chủ báo bận (tối đa 6 vòng), giống trang thật.
 * - Ghi kết quả vào sheet "LoadTestReport" trong file thử và in ra Nhật ký thực thi.
 * ====================================================================== */
// ID file dữ liệu thật: CHỈ ĐỌC để chép sheet Slots, Config và dòng tiêu đề sang file thử
var SPREADSHEET_ID = '10aN5O3HL79asPGfug75IPv1w_ssGPo8edsASMuG3_aM';
var SHEET_REG = 'Registrations', SHEET_SLOTS = 'Slots', SHEET_CONFIG = 'Config', SHEET_LOG = 'ActivityLog';
var C = { TS: 1, EMP_CODE: 4, SLOT: 8, STATUS: 12, REQ: 23 };
var STATUS_NEW = 'Chờ nộp tiền', STATUS_WAIT_PM = 'Chờ PM xác nhận', STATUS_FREE = ['Hủy', 'Từ chối'];
function str_(v) { return v === null || v === undefined ? '' : String(v).trim(); }
// Giống hệt quy tắc đơn hợp lệ trong web app (Code.gs v7.12)
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
var LOADTEST_URL = 'https://script.google.com/macros/s/AKfycbwb-pp3WQoWjqk54MYqndew-Sny3Yeha80INufk6aSxCuF7zMIAt2cWsJI3urZVHbEC4w/exec';
function loadTest300() { return loadTest_(300, 50); }
function loadTest_(N, NPAY) {
  var t0 = Date.now(), run = 'L' + Utilities.formatDate(new Date(), 'Asia/Ho_Chi_Minh', 'MMddHHmmss');
  // 1) File thử mới
  var real = SpreadsheetApp.openById(SPREADSHEET_ID);
  var ss = SpreadsheetApp.create('LoadTest ' + run + ' (xoá được sau khi xem kết quả)');
  real.getSheetByName(SHEET_SLOTS).copyTo(ss).setName(SHEET_SLOTS);
  var cfgSh = real.getSheetByName(SHEET_CONFIG).copyTo(ss).setName(SHEET_CONFIG);
  var cv = cfgSh.getRange(2, 1, Math.max(cfgSh.getLastRow() - 1, 1), 2).getValues();
  var cfgMap = {};
  for (var i = 0; i < cv.length; i++) { cfgMap[str_(cv[i][0])] = cv[i][1]; if (/^(OPEN_TIME|CLOSE_TIME|PORTAL_PAUSED)$/.test(str_(cv[i][0]))) cfgSh.getRange(i + 2, 2).setValue(''); }
  var regSh = ss.getSheets()[0].setName(SHEET_REG);
  regSh.getRange(1, 1, 1, C.REQ).setValues(real.getSheetByName(SHEET_REG).getRange(1, 1, 1, C.REQ).getValues());
  ss.insertSheet(SHEET_LOG).getRange(1, 1, 1, 6).setValues([['Thời gian', 'Thao tác', 'Mã NV', 'Slot', 'Trình duyệt', 'Chi tiết']]);
  SpreadsheetApp.flush();

  var slotRows = ss.getSheetByName(SHEET_SLOTS).getRange(2, 1, ss.getSheetByName(SHEET_SLOTS).getLastRow() - 1, 4).getValues()
    .filter(function (r) { return str_(r[2]); });
  var users = [];
  for (var u = 0; u < N; u++) {
    // 60% tranh 10 slot đầu, 40% chọn ngẫu nhiên
    var sr = slotRows[Math.random() < 0.6 ? Math.floor(Math.random() * Math.min(10, slotRows.length)) : Math.floor(Math.random() * slotRows.length)];
    users.push({ emp: 'LT' + ('00' + u).slice(-3), slot: str_(sr[2]), kho: str_(sr[0]), model: str_(sr[3]) });
  }
  var post = function (o) { o.test = true; o.testRun = run; o.testSheet = ss.getId(); o.userAgent = 'LOADTEST ' + run;
    return { url: LOADTEST_URL, method: 'post', contentType: 'text/plain;charset=utf-8', payload: JSON.stringify(o), muteHttpExceptions: true, followRedirects: true }; };
  // Gửi song song, gửi lại khi bận (tối đa 6 vòng); trả kết quả cuối + thời điểm nhận (giây kể từ đầu đợt)
  var wave = function (reqs) {
    var start = Date.now(), res = new Array(reqs.length), at = new Array(reqs.length), pending = reqs.map(function (_, k) { return k; });
    var waits = [0, 3000, 6000, 12000, 20000, 30000];
    for (var round = 0; round < waits.length && pending.length; round++) {
      if (waits[round]) Utilities.sleep(waits[round]);
      var out = UrlFetchApp.fetchAll(pending.map(function (k) { return reqs[k]; }));
      var now = (Date.now() - start) / 1000, next = [];
      for (var q = 0; q < out.length; q++) {
        var k = pending[q], j = null;
        try { j = JSON.parse(out[q].getContentText()); } catch (e) { j = { ok: false, busy: true, http: out[q].getResponseCode() }; }
        res[k] = j; at[k] = now;
        if (j.busy) next.push(k);
      }
      pending = next;
    }
    return { res: res, at: at, secs: (Date.now() - start) / 1000 };
  };
  var stats = function (w) {
    var a = w.at.slice().sort(function (x, y) { return x - y; });
    return { p95: a[Math.max(0, Math.ceil(a.length * 0.95) - 1)], max: a[a.length - 1],
             err: w.res.filter(function (r) { return !r || r.busy || (r.ok === false && !r.slotTaken && !r.limitReached); }).length };
  };
  // 2) Đăng nhập
  var wl = wave(users.map(function (x) { return post({ action: 'login', empCode: x.emp, password: '123456' }); }));
  // 3) Đăng ký
  var wr = wave(users.map(function (x) { return post({ action: 'register', division: 'LOAD TEST', empCode: x.emp, empName: 'NGUOI THU ' + x.emp,
    kho: x.kho, model: x.model, slotId: x.slot, phone: '09' + ('0000000' + Math.floor(Math.random() * 1e8)).slice(-8), address: 'Load test', agree: true }); }));
  // 4) Khai nộp tiền kèm ảnh ~1 MB (không lưu Drive trong chế độ thử)
  var winners = [];
  for (var w = 0; w < N; w++) if (wr.res[w] && wr.res[w].ok) winners.push(w);
  var img = 'data:image/jpeg;base64,' + Utilities.base64Encode(Utilities.newBlob(new Array(750000).fill(65)).getBytes());
  var payers = winners.slice(0, NPAY);
  var wp = wave(payers.map(function (k) { var x = users[k]; return post({ action: 'payment', slotId: x.slot, empCode: x.emp, payerName: 'NGUOI THU',
    payerCode: x.emp, amount: '1', bankTxn: 'LT' + k, payTime: 'loadtest', fileName: 'bl.jpg', fileBase64: img }); }));

  // 5) Đối chiếu dữ liệu trên sheet thử
  SpreadsheetApp.flush();
  var n = regSh.getLastRow() - 1;
  var v = n > 0 ? regSh.getRange(2, 1, n, C.STATUS).getValues() : [];
  var eff = effective_(v.map(function (x) { return x[C.EMP_CODE - 1]; }), v.map(function (x) { return x[C.STATUS - 1]; }), (Number(cfgMap.MAX_PER_EMPLOYEE) || 1));
  var bySlot = {}, byEmp = {}, dupSlot = 0, dupEmp = 0, blank = 0;
  for (var r = 0; r < v.length; r++) {
    if (!str_(v[r][C.EMP_CODE - 1])) { blank++; continue; }
    if (!eff[r]) continue;
    var sl = str_(v[r][C.SLOT - 1]).replace(/^'+/, ''), em = str_(v[r][C.EMP_CODE - 1]);
    bySlot[sl] = (bySlot[sl] || 0) + 1; if (bySlot[sl] === 2) dupSlot++;
    byEmp[em] = (byEmp[em] || 0) + 1; if (byEmp[em] === 2) dupEmp++;
  }
  var lost = 0;
  winners.forEach(function (k) { var row = wr.res[k].row, x = users[k];
    var got = row >= 2 && row - 2 < v.length ? v[row - 2] : null;
    if (!got || str_(got[C.EMP_CODE - 1]) !== x.emp || str_(got[C.SLOT - 1]).replace(/^'+/, '') !== x.slot) lost++; });
  var effRows = eff.filter(function (x) { return x; }).length;
  var sl_ = stats(wl), sr_ = stats(wr), sp_ = stats(wp);
  var paidOk = wp.res.filter(function (r) { return r && r.ok; }).length;
  var rows = [
    ['Tiêu chí', 'Kết quả', 'Ngưỡng', 'Đạt?'],
    ['Sản phẩm bị 2 người cùng đặt thành công', dupSlot, 0, dupSlot === 0],
    ['Dòng mất / ghi đè (đơn báo thành công nhưng sheet không khớp)', lost, 0, lost === 0],
    ['Dòng trống xen giữa trên sheet (tham khảo)', blank, 'tham khảo', ''],
    ['NV có hơn 1 đơn hợp lệ', dupEmp, 0, dupEmp === 0],
    ['Số báo "thành công" / số đơn hợp lệ trên sheet', winners.length + ' / ' + effRows, 'khớp', winners.length === effRows],
    ['Đăng ký: 95% người có kết quả cuối sau (giây, tính theo đợt gửi nên là mức trên)', sr_.p95, '≤ 60', sr_.p95 <= 60],
    ['Đăng ký: người chờ lâu nhất (giây)', sr_.max, '≤ 120', sr_.max <= 120],
    ['Đăng ký: lỗi cuối cùng sau tự gửi lại', sr_.err + ' / ' + N, '≤ 1%', sr_.err <= N * 0.01],
    ['Đăng nhập: 95% (giây) · tối đa · lỗi', sl_.p95 + ' · ' + sl_.max + ' · ' + sl_.err, 'tham khảo', ''],
    ['Khai nộp tiền ~1 MB: thành công · 95% (giây) · lỗi', paidOk + '/' + payers.length + ' · ' + sp_.p95 + ' · ' + sp_.err, 'tham khảo', ''],
    ['Tổng thời gian chạy (giây)', Math.round((Date.now() - t0) / 1000), '', ''],
    ['Mã lượt thử', run, '', '']
  ];
  ss.insertSheet('LoadTestReport').getRange(1, 1, rows.length, 4).setValues(rows);
  Logger.log(rows.map(function (x) { return x.join(' | '); }).join('\n'));
  Logger.log('File kết quả: ' + ss.getUrl());
  return ss.getUrl();
}
