import frappe
from frappe.utils import nowdate, now, getdate,date_diff

@frappe.whitelist()
def gym_attendance_handler(member_id):
    default_member_image = frappe.db.get_single_value("Login Dashboard Settings", "default_member_image") 
    member_name = frappe.db.get_value("Gym Member", {"membership_id": member_id}, "name")
    if not member_name:
        return {
            "status": "error",
            "text": "❌ Member ID not found. Please check and try again."
        }

    member = frappe.get_doc("Gym Member", {"membership_id": member_id})
    days_left = 0
    if member.package_end:
        days_left = date_diff(member.package_end, nowdate())

    # Check if package expired
    if member.package_end and member.package_end < getdate(nowdate()):

        return {
            "status": "success",
            "message": "❌ Package Expired",
            "full_name": member.full_name,
            "membership_id": member.membership_id,
            "image": member.attach_image or "",
            "start_date": str(member.package_start_date or ""),
            "end_date": str(member.package_end or ""),
            "package_name": member.current_plan or "",
            "pending_due": 0,
            "days_left": 0
        }

    # Mark attendance
    attendance_name = frappe.db.exists("Gym Attendance", {
        "member_id": member.name,
        "date": nowdate()
    })

    if attendance_name:
        attendance = frappe.get_doc("Gym Attendance", attendance_name)
        logs = attendance.check_in_logs or []
        if logs and logs[-1].check_in_time and not logs[-1].check_out_time:
            logs[-1].check_out_time = now()
            attendance.save()
            return {
                "status": "success",
                "message": "Logged Out Successfully!!",
                "full_name": member.full_name,
                "membership_id": member.membership_id,
                "image":member.attach_image or default_member_image,
                "start_date": str(member.package_start_date or ""),
                "end_date": str(member.package_end or ""),
                "package_name": member.current_plan or "",
                "pending_due":  0,
                "days_left": days_left
            }

    # New check-in
    if not attendance_name:
        attendance = frappe.new_doc("Gym Attendance")
        attendance.member_id = member.name
        attendance.date = nowdate()
        attendance.append("check_in_logs", {"check_in_time": now()})
        attendance.insert()
    else:
        attendance = frappe.get_doc("Gym Attendance", attendance_name)
        attendance.append("check_in_logs", {"check_in_time": now()})
        attendance.save()

    return {
        "status": "success",
        "message": "Logged In Successfully!!",
        "full_name": member.full_name,
        "membership_id": member.membership_id,
        "image": member.attach_image or default_member_image,
        "start_date": str(member.package_start_date or ""),
        "end_date": str(member.package_end or ""),
        "package_name": member.current_plan or "",
        "pending_due":  0,
        "days_left": days_left
    }

