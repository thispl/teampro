# Copyright (c) 2024, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr, add_days, date_diff, format_datetime
from datetime import datetime


class AttendanceSummary(Document):
	pass

@frappe.whitelist()
def get_data_summary(emp, from_date, to_date):
	no_of_days = date_diff(add_days(to_date, 1), from_date)
	dates = [add_days(from_date, i) for i in range(no_of_days)]
	emp_details = frappe.db.get_value('Employee', emp, ['employee_name', 'department'])
	present=0
	absent=0
	on_duty=0
	late =0
	on_leave=0
	data = "<table class='table table-bordered=1'>"
	data += "<tr><td style='border: 1px solid black;' colspan=9><b><center>Summary Table</b></center></td><tr>"
	data += "<tr style='color:white;'><td style='border: 1px solid black;background-color:#0f1568';><b><center>No of Days</b></center></b><td style='border: 1px solid black;background-color:#0f1568;'><b><center>Present Count</b></center></b><td style='border: 1px solid black;background-color:#0f1568;'><b><center>Absent Count</b></center></b><td style='border: 1px solid black;background-color:#0f1568;'><b><center>Leave Count</b></center></b><td style='border: 1px solid black;background-color:#0f1568;'><b><center>OD Count</b></center></b><td style='border: 1px solid black;background-color:#0f1568;'><b><center>Late Count</b></center></b></td></tr>"
	
	for date in dates:
		dt = datetime.strptime(date, '%Y-%m-%d')
		d = dt.strftime('%d-%b')
		day = datetime.date(dt).strftime('%a')
		attendance = frappe.db.exists('Attendance', {'employee': emp, 'attendance_date': date, 'docstatus': ('!=', 2)})
		hh=check_holiday(date,emp)
		if attendance and not hh:
			att = frappe.get_doc('Attendance', {'attendance_date': date, 'employee': emp, 'docstatus': ('!=', 2)})
			in_time = att.in_time or ''
			out_time = att.out_time or ''
			time_in = in_time
			time_out = out_time
			shift = 'G'  
			status = att.status 
			working_hours = round(att.bt_difference, 2) if att.bt_difference else ''
			leave_type = att.leave_type or ''
			late_entry_time = 0 
			
			if isinstance(in_time, datetime):
				in_time = in_time.strftime('%H:%M:%S')
			if isinstance(out_time, datetime):
				out_time = out_time.strftime('%H:%M:%S')
			if in_time:
				start_time = datetime.strptime('09:30:00', '%H:%M:%S') 
				employee_in_time = datetime.strptime(in_time, '%H:%M:%S') 
				if employee_in_time > start_time:
					late_duration = employee_in_time - start_time
					if late_duration:
						late += 1

	
			if status == 'Present':
				present += 1
			if status == 'Half Day':
				present += 0.5
			if status == 'Absent':
				absent +=1
			if status == 'On Duty':
				on_duty += 1
			if status == 'On Leave':
				on_leave += 1
			
	row_data = """
		<tr>
			<td style='border: 1px solid black;'><center>{days}</center></td>
			<td style='border: 1px solid black;'><center>{present}</center></td>
			<td style='border: 1px solid black;'><center>{absent}</center></td>
			<td style='border: 1px solid black;'><center>{on_leave}</center></td>
			<td style='border: 1px solid black;'><center>{od}</center></td>
			<td style='border: 1px solid black;'><center>{late}</center></td>

			
		</tr>
	""".format(
		days=no_of_days, present=present, absent=absent,on_leave = on_leave,
		od=on_duty, late = late
	)
	data += row_data

	data += "</table>"
	return data

@frappe.whitelist()
def get_data_system(emp, from_date, to_date):
	no_of_days = date_diff(add_days(to_date, 1), from_date)
	dates = [add_days(from_date, i) for i in range(no_of_days)]
	emp_details = frappe.db.get_value('Employee', emp, ['employee_name', 'department'])
	
	data = "<table class='table table-bordered=1'>"
	data += "<tr style='color:white;'><td style='border: 1px solid black;background-color:#0f1568';><b><center>ID</b></center></b><td style='border: 1px solid black;background-color:#0f1568;' colspan=2><b><center>%s</b></center></b><td style='border: 1px solid black;background-color:#0f1568;'><b><center>Name</b></center></b><td style='border: 1px solid black;background-color:#0f1568;' colspan=2><b><center>%s</b></center></b><td style='border: 1px solid black;background-color:#0f1568;'><b><center>Dept</b></center></b><td style='border: 1px solid black;background-color:#0f1568;' colspan=3><b><center>%s</b></center></b></tr>" % (emp, emp_details[0], emp_details[1])
	data += "<tr><td style='border: 1px solid black;' colspan=9><b><center>Attendance</b></center></td><tr>"
	data += "<tr style='color:white;'><td style='border: 1px solid black;background-color:#0f1568';><b><center>Date</b></center></b><td style='border: 1px solid black;background-color:#0f1568;'><b><center>Day</b></center></b><td style='border: 1px solid black;background-color:#0f1568;'><b><center>Working</b></center></b><td style='border: 1px solid black;background-color:#0f1568;'><b><center>In Time</b></center></b><td style='border: 1px solid black;background-color:#0f1568;'><b><center>Out Time</b></center></b><td style='border: 1px solid black;background-color:#0f1568;'><b><center>Shift</b></center></b><td style='border: 1px solid black;background-color:#0f1568;'><b><center>Status</b></center></b><td style='border: 1px solid black;background-color:#0f1568;'><b><center>Late Entry Time</b></center></b></td></tr>"
	
	for date in dates:
		dt = datetime.strptime(date, '%Y-%m-%d')
		d = dt.strftime('%d-%b')
		day = datetime.date(dt).strftime('%a')
		attendance = frappe.db.exists('Attendance', {'employee': emp, 'attendance_date': date, 'docstatus': ('!=', 2)})
		hh=check_holiday(date,emp)
		if attendance and not hh:
			att = frappe.get_doc('Attendance', {'attendance_date': date, 'employee': emp, 'docstatus': ('!=', 2)})
			in_time = att.in_time or ''
			out_time = att.out_time or ''
			time_in = in_time
			time_out = out_time
			shift = 'G'  
			status = att.status 
			working_hours = round(att.bt_difference, 2) if att.bt_difference else ''
			leave_type = att.leave_type or ''
			late_entry_time = 0 
			
			if isinstance(in_time, datetime):
				in_time = in_time.strftime('%H:%M:%S')
			if isinstance(out_time, datetime):
				out_time = out_time.strftime('%H:%M:%S')
			if in_time:
				start_time = datetime.strptime('09:30:00', '%H:%M:%S') 
				employee_in_time = datetime.strptime(in_time, '%H:%M:%S') 
				if employee_in_time > start_time:
					late_duration = employee_in_time - start_time
					late_entry_time = str(late_duration)  
				else:
					late_entry_time = '00:00:00'
			else:
				late_entry_time = '-'

			# holiday = check_holiday(date, emp)
			# if holiday:
			# 	row_data = """
			# 		<tr>
			# 			<td style='border: 1px solid black;'><center>{date}</center></td>
			# 			<td style='border: 1px solid black;'><center>{day}</center></td>
			# 			<td style='border: 1px solid black;'><center>WO</center></td>
			# 			<td style='border: 1px solid black;'><center></center></td>
			# 			<td style='border: 1px solid black;'><center></center></td>
			# 			<td style='border: 1px solid black;'><center></center></td>
			# 			<td style='border: 1px solid black; color: #BD2A0F;'><center>{holiday}</center></td>
			# 			<td style='border: 1px solid black;'><center></center></td>
			# 			<td style='border: 1px solid black;'><center></center></td>
			# 		</tr>
			# 	""".format(date=dt.strftime('%d-%b'), day=day,holiday=holiday)
			if status == 'On Leave':
				row_data = """
					<tr>
						<td style='border: 1px solid black;'><center>{date}</center></td>
						<td style='border: 1px solid black;'><center>{day}</center></td>
						<td style='border: 1px solid black;'><center>On Leave</center></td>
						<td style='border: 1px solid black;'><center></center></td>
						<td style='border: 1px solid black;'><center></center></td>
						<td style='border: 1px solid black;'><center></center></td>
						<td style='border: 1px solid black; color: #BD2A0F;'><center>{leave_type}</center></td>
						<td style='border: 1px solid black;'><center></center></td>
					</tr>
				""".format(date=dt.strftime('%d-%b'), day=day, leave_type=leave_type)
			elif status == 'Present' and att.attendance_request :
				row_data = """
					<tr>
						<td style='border: 1px solid black;'><center>{date}</center></td>
						<td style='border: 1px solid black;'><center>{day}</center></td>
						<td style='border: 1px solid black;'><center>W</center></td>
						<td style='border: 1px solid black;'><center></center></td>
						<td style='border: 1px solid black;'><center></center></td>
						<td style='border: 1px solid black;'><center></center></td>
						<td style='border: 1px solid black; color: #BD2A0F;'><center>OD</center></td>
						<td style='border: 1px solid black;'><center></center></td>
					</tr>
				""".format(date=dt.strftime('%d-%b'), day=day)
			elif status == 'Absent' and att.attendance_request :
				row_data = """
					<tr>
						<td style='border: 1px solid black;'><center>{date}</center></td>
						<td style='border: 1px solid black;'><center>{day}</center></td>
						<td style='border: 1px solid black;'><center>W</center></td>
						<td style='border: 1px solid black;'><center></center></td>
						<td style='border: 1px solid black;'><center></center></td>
						<td style='border: 1px solid black;'><center></center></td>
						<td style='border: 1px solid black; color: #BD2A0F;'><center>OD</center></td>
						<td style='border: 1px solid black;'><center></center></td>
					</tr>
				""".format(date=dt.strftime('%d-%b'), day=day)
			
			else:
				if status=='Present' and frappe.db.exists('Attendance Permission',{'employee':att.employee,'permission_date':att.attendance_date,'docstatus':1}):
					status='P/PR'
				elif status=='Present' and not frappe.db.exists('Attendance Permission',{'employee':att.employee,'permission_date':att.attendance_date,'docstatus':1}):
					status='P'
				elif status=='Half Day' and frappe.db.exists('Attendance Permission',{'employee':att.employee,'permission_date':att.attendance_date,'docstatus':1}):
					status='HD/PR'
				elif status=='Half Day' and att.leave_type and att.leave_application:
					status='HD/'+att.leave_type
				elif status=='Absent':
					status='AB'
				else:
					status=status
				row_data = """
					<tr>
						<td style='border: 1px solid black;'><center>{date}</center></td>
						<td style='border: 1px solid black;'><center>{day}</center></td>
						<td style='border: 1px solid black;'><center>W</center></td>
						<td style='border: 1px solid black;'><center>{time_in}</center></td>
						<td style='border: 1px solid black;'><center>{time_out}</center></td>
						<td style='border: 1px solid black;'><center>{shift}</center></td>
						<td style='border: 1px solid black;'><center>{status}</center></td>
						<td style='border: 1px solid black;'><center>{late_entry_time}</center></td>
					</tr>
				""".format(
					date=dt.strftime('%d-%b'), day=day, time_in=format_datetime(time_in) or '-',
					time_out=format_datetime(time_out) or '-', shift=shift, status=status,late_entry_time=late_entry_time
				)
			data += row_data
		else:
			shift = 'G' 
			holiday = check_holiday(date, emp)
			if holiday:
				attendance = frappe.db.exists('Attendance', {'employee': emp, 'attendance_date': date, 'docstatus': ('!=', 2)})
				if attendance:
					frappe.errprint(date)
					att = frappe.get_doc('Attendance', {'attendance_date': date, 'employee': emp, 'docstatus': ('!=', 2)})
					if att and att.status!="Absent":
						status = att.status 
						if status=='Present':
							status='P/'+hh
						elif status=='Half Day':
							status='HD/'+hh
						else:
							status=status
						time_in=''
						time_out=''
						row_data = """
							<tr>
								<td style='border: 1px solid black;'><center>{date}</center></td>
								<td style='border: 1px solid black;'><center>{day}</center></td>
								<td style='border: 1px solid black;'><center>WO</center></td>
								<td style='border: 1px solid black;'><center>{time_in}</center></td>
								<td style='border: 1px solid black;'><center>{time_out}</center></td>
								<td style='border: 1px solid black;'><center>{shift}</center></td>
								<td style='border: 1px solid black; color: #BD2A0F;'><center>{status}</center></td>
								<td style='border: 1px solid black;'><center></center></td>
							</tr>
						""".format(date=dt.strftime('%d-%b'), day=day,time_in=format_datetime(att.in_time) or '-',
						time_out=format_datetime(att.out_time) or '-', shift=shift, status=status)
						data += row_data
					else:
						row_data = """
						<tr>
							<td style='border: 1px solid black;'><center>{date}</center></td>
							<td style='border: 1px solid black;'><center>{day}</center></td>
							<td style='border: 1px solid black;'><center>WO</center></td>
							<td style='border: 1px solid black;'><center></center></td>
							<td style='border: 1px solid black;'><center></center></td>
							<td style='border: 1px solid black;'><center></center></td>
							<td style='border: 1px solid black; color: #BD2A0F;'><center>{holiday}</center></td>
							<td style='border: 1px solid black;'><center></center></td>
						</tr>
					""".format(date=dt.strftime('%d-%b'), day=day,holiday=holiday)
					data += row_data

				else:
					row_data = """
						<tr>
							<td style='border: 1px solid black;'><center>{date}</center></td>
							<td style='border: 1px solid black;'><center>{day}</center></td>
							<td style='border: 1px solid black;'><center>WO</center></td>
							<td style='border: 1px solid black;'><center></center></td>
							<td style='border: 1px solid black;'><center></center></td>
							<td style='border: 1px solid black;'><center></center></td>
							<td style='border: 1px solid black; color: #BD2A0F;'><center>{holiday}</center></td>
							<td style='border: 1px solid black;'><center></center></td>
						</tr>
					""".format(date=dt.strftime('%d-%b'), day=day,holiday=holiday)
					data += row_data
	data += "</table>"
	return data



def check_holiday(date,emp):
	holiday_list = frappe.db.get_value('Employee',{'name':emp},'holiday_list')
	holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off, `tabHoliday`.description from `tabHoliday List` 
	left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
	doj= frappe.db.get_value("Employee",{'name':emp},"date_of_joining")
	status = ''
	desc = ''
	if holiday :
		if doj <= holiday[0].holiday_date:
			if holiday[0].weekly_off == 1:
				status = "Week off"
			else:
				status = holiday[0].description
		else:
			status = 'Not Joined'
	
	return status


from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days,date_diff
@frappe.whitelist()
def get_from_to_dates(month,year):
	if month == 'January':
		month1 = "01"
	if month == 'February':
		month1 = "02"
	if month == 'March':
		month1 = "03"
	if month == 'April':
		month1 = "04"
	if month == 'May':
		month1 = "05"
	if month == 'June':
		month1 = "06"
	if month == 'July':
		month1 = "07"
	if month == 'August':
		month1 = "08"
	if month == 'September':
		month1 = "09"
	if month == 'October':
		month1 = "10"
	if month == 'November':
		month1 = "11"
	if month == 'December':
		month1 = "12"
	formatted_start_date = year + '-' + month1 + '-01'
	formatted_end_date = get_last_day(formatted_start_date)
	return formatted_start_date,formatted_end_date

def format_timedelta(td):
    total_seconds = td.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    
    return formatted_time

