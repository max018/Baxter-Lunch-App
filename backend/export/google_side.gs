function newOrderSheet(name, orders, editor) {
  var ss = SpreadsheetApp.create(name),
      sheet = ss.getActiveSheet();
  orders.forEach(function(order) {
    sheet.appendRow(order);
  });
  ss.addEditor(editor);
  return ss.getUrl();
}

