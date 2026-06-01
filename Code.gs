// Google Apps Script — paste this at script.google.com
// After deploying, copy the Web App URL into index.html (APPS_SCRIPT_URL)

var SHEET_NAME = "Orders";

function getSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow([
      "ID", "Chemical", "CAS #", "Supplier", "Catalog #",
      "Quantity", "URL", "Urgency", "Requested By", "Date", "Notes", "Status"
    ]);
    sheet.getRange(1, 1, 1, 11).setFontWeight("bold").setBackground("#1a3a5c").setFontColor("white");
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function makeId() {
  return Math.random().toString(36).substr(2, 8).toUpperCase();
}

function doPost(e) {
  return doGet(e);
}

function doGet(e) {
  var action = e.parameter.action;

  if (action === "list") {
    var sheet = getSheet();
    var rows = sheet.getDataRange().getValues();
    var orders = rows.slice(1).map(function(r) {
      return {
        id:           r[0], chemical:  r[1], cas:       r[2],
        supplier:     r[3], catalog:   r[4], quantity:  r[5],
        url:          r[6], urgency:   r[7], requested_by: r[8],
        date:         r[9], notes:     r[10], status:   r[11]
      };
    });
    return respond(orders);
  }

  if (action === "add") {
    var sheet = getSheet();
    var id = makeId();
    sheet.appendRow([
      id,
      e.parameter.chemical || "",
      e.parameter.cas || "",
      e.parameter.supplier || "",
      e.parameter.catalog || "",
      e.parameter.quantity || "",
      e.parameter.url || "",
      e.parameter.urgency || "Normal",
      e.parameter.requested_by || "",
      new Date().toLocaleString(),
      e.parameter.notes || "",
      "Pending"
    ]);
    return respond({ ok: true, id: id });
  }

  if (action === "status") {
    var sheet = getSheet();
    var rows = sheet.getDataRange().getValues();
    for (var i = 1; i < rows.length; i++) {
      if (rows[i][0] === e.parameter.id) {
        sheet.getRange(i + 1, 12).setValue(e.parameter.status);
        break;
      }
    }
    return respond({ ok: true });
  }

  return respond({ ok: true, message: "Lab Orders API" });
}

function respond(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
