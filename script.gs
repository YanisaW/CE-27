#ดึงข้อมูลจาก google sheet ลง google calender
function appointmentCalendar() {

  //Set data from Spread Sheet
  var spreadSheetID = "1N73vry9JBDihujeGTJ4x_bCGYlvcqin-9puMqEO0jdA";
  var ss = SpreadsheetApp.openById(spreadSheetID);
  var sheet = ss.getActiveSheet();
  var lastRow = sheet.getLastRow();
  var lastColumn = sheet.getLastColumn();
  
  /*
  	Logger.log(lastRow);
 	Logger.log(lastColumn);
  */
  
  
    //Set data for Google Calendar
  var name = sheet.getRange(lastRow, 2).getValue();
  var tel = sheet.getRange(lastRow, 4).getValue();
  var timeStart = new Date(sheet.getRange(lastRow, 5).getValue());
  var timeEnd = new Date(timeStart);
  timeEnd.setMinutes(timeStart.getMinutes()+30);
  var dateAppointment = Utilities.formatDate(timeStart, timeStart.getTimezoneOffset(), "MMMM dd, yyyy");
  var formattedDateStart = Utilities.formatDate(timeStart, timeStart.getTimezoneOffset(), "HH:mm");
  var formattedDateEnd = Utilities.formatDate(timeEnd, timeEnd.getTimezoneOffset(), "HH:mm");
 
  var doctor = sheet.getRange(lastRow, 6).getValue();
 	Logger.log("ชื่อ: " + name);
 	Logger.log("เบอร์: " + tel);
  	Logger.log("แพทย์ผู้รักษา: " + doctor);
    Logger.log("วันที่นัด: " +  dateAppointment);
 	Logger.log("เวลาที่นัด: " + formattedDateStart + " - " + formattedDateEnd + " น.");
    
    
   //Creates a calendar event using the submitted data
  var calendar = CalendarApp.getCalendarById('c_7320crkcnsash49gbp5d6glgd8@group.calendar.google.com');
  var titles = ('ผู้จอง: '+ name);
  var descriptions = ' เบอร์: '+ tel +'\n แพทย์: '+ doctor;
  calendar.createEvent(titles, timeStart , timeEnd , {description: descriptions});

  }
