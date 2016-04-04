// this needs to be put on Google's end as an Apps Script
// then its Apps Script ID should be put in config.py

function newOrderSheet(name, orders, editor) {
  var ss = SpreadsheetApp.create(name),
      sheet = ss.getActiveSheet();
  orders.forEach(function(order) {
    sheet.appendRow(order);
  });
  ss.addEditor(editor);
  return ss.getUrl();
}

