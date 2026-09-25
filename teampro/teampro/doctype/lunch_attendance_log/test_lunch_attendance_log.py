# Copyright (c) 2026, TeamPRO and Contributors
# See license.txt

import json
import random
from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import getdate, nowtime

from teampro.teampro.doctype.lunch_attendance_log.lunch_attendance_log import (
    LunchAttendanceLog,
)
from teampro import lunch_attendance as LA


def _ensure_test_employee(name="Lunch Test Employee", mobile="+919999900001"):
    """Create (or get) a minimal Employee for tests.

    The Employee DocType on this site has several mandatory custom fields
    (short_code, biometric_pin, custom_service, holiday_list, gender,
    date_of_birth, date_of_joining) that we must populate.
    """
    existing = frappe.db.get_value("Employee", {"employee_name": name})
    if existing:
        return existing

    holiday_list = frappe.db.get_value("Holiday List", {}, ["name"], order_by="name asc")
    service = frappe.db.get_value("Services", {}, ["name"], order_by="name asc")

    emp = frappe.get_doc(
        {
            "doctype": "Employee",
            "employee_name": name,
            "first_name": name,
            "cell_number": mobile,
            "status": "Active",
            "company": frappe.db.get_single_value("Global Defaults", "default_company")
            or frappe.db.get_value("Company", {}, "name", order_by="name asc"),
            "gender": "Male",
            "date_of_birth": "1990-01-01",
            "date_of_joining": "2020-01-01",
            "holiday_list": holiday_list,
            "custom_service": service,
            "short_code": frappe.generate_hash(length=8).upper(),
            "biometric_pin": str(random.randint(100000, 999999)),
        }
    )
    emp.insert(ignore_permissions=True)
    return emp.name


def _make_log(employee, date=None, response="Pending"):
    mobile = frappe.db.get_value("Employee", employee, "cell_number")
    log = frappe.get_doc(
        {
            "doctype": "Lunch Attendance Log",
            "employee": employee,
            "mobile_number": mobile,
            "date": date or getdate(),
            "response": response,
        }
    )
    log.insert(ignore_permissions=True)
    return log


class TestLunchAttendanceLog(FrappeTestCase):
    """Tests for Lunch Attendance Log creation, uniqueness and lifecycle."""

    def setUp(self):
        frappe.db.delete("Lunch Attendance Log")
        self.employee = _ensure_test_employee()

    def tearDown(self):
        frappe.db.delete("Lunch Attendance Log")

    # --- DocType behaviour -------------------------------------------------
    def test_log_creation_defaults_to_pending(self):
        log = _make_log(self.employee)
        self.assertEqual(log.response, "Pending")
        self.assertTrue(log.name.startswith("LAL-"))

    def test_duplicate_log_per_employee_per_date_rejected(self):
        _make_log(self.employee)
        with self.assertRaises(frappe.DuplicateEntryError):
            _make_log(self.employee)

    def test_response_sets_responded_at(self):
        log = _make_log(self.employee)
        log.response = "Yes"
        log.save(ignore_permissions=True)
        self.assertTrue(log.responded_at)

    # --- Eligibility helpers ----------------------------------------------
    def test_get_eligible_employees_filters_by_mobile(self):
        settings = LA.get_settings()
        # Employee created in setUp has a mobile number, so it should be
        # returned when the "All Active Employees" filter is used.
        employees = LA.get_eligible_employees(settings)
        names = [e["name"] for e in employees]
        self.assertIn(self.employee, names)

    # --- Webhook payload parsing ------------------------------------------
    def _make_incoming_wa_message(self, payload, sender="919999900001"):
        """Insert a WhatsApp Message row mimicking the frappe_whatsapp webhook."""
        return frappe.get_doc(
            {
                "doctype": "WhatsApp Message",
                "type": "Incoming",
                "from": sender,
                "message": payload,
                "content_type": "button",
                "message_id": f"wamid.test.{frappe.generate_hash(8)}",
            }
        ).insert(ignore_permissions=True)

    def test_handle_incoming_yes_updates_log(self):
        log = _make_log(self.employee)
        # Ensure the feature is enabled for the hook to run.
        settings = LA.get_settings()
        enabled_before = settings.enabled
        send_conf_before = settings.send_confirmation_reply
        create_entry_before = settings.create_lunch_entry_on_yes
        settings.db_set(
            {
                "enabled": 1,
                "send_confirmation_reply": 0,
                "create_lunch_entry_on_yes": 0,
                "cutoff_time": "23:59:59",
            },
            notify=False,
        )

        try:
            with patch.object(LA, "send_free_form_text") as mock_send:
                msg = self._make_incoming_wa_message("LUNCH_YES")
                LA.handle_incoming_whatsapp_message(msg, "after_insert")

            log.reload()
            self.assertEqual(log.response, "Yes")
            self.assertTrue(log.responded_at)
            mock_send.assert_not_called()  # confirmation disabled
        finally:
            settings.db_set(
                {
                    "enabled": enabled_before,
                    "send_confirmation_reply": send_conf_before,
                    "create_lunch_entry_on_yes": create_entry_before,
                },
                notify=False,
            )

    def test_handle_incoming_no_updates_log(self):
        log = _make_log(self.employee)
        settings = LA.get_settings()
        enabled_before = settings.enabled
        send_conf_before = settings.send_confirmation_reply
        create_entry_before = settings.create_lunch_entry_on_yes
        settings.db_set(
            {
                "enabled": 1,
                "send_confirmation_reply": 0,
                "create_lunch_entry_on_yes": 0,
                "cutoff_time": "23:59:59",
            },
            notify=False,
        )

        try:
            with patch.object(LA, "send_free_form_text"):
                msg = self._make_incoming_wa_message("LUNCH_NO")
                LA.handle_incoming_whatsapp_message(msg, "after_insert")

            log.reload()
            self.assertEqual(log.response, "No")
        finally:
            settings.db_set(
                {
                    "enabled": enabled_before,
                    "send_confirmation_reply": send_conf_before,
                    "create_lunch_entry_on_yes": create_entry_before,
                },
                notify=False,
            )

    def test_handle_incoming_ignores_non_lunch_payload(self):
        log = _make_log(self.employee)
        msg = self._make_incoming_wa_message("SOME_OTHER_BUTTON")
        LA.handle_incoming_whatsapp_message(msg, "after_insert")
        log.reload()
        self.assertEqual(log.response, "Pending")

    def _simulate_meta_webhook_payload(self, button_title, button_id="auto_gen_uuid", sender="919999900001"):
        """Set ``frappe.local.form_dict`` to mimic a real Meta webhook body.

        Meta auto-generates Quick-Reply button ids; the only controllable
        field is the button title (``Yes`` / ``No``). The frappe_whatsapp
        webhook stores ``button_reply.id`` in WhatsApp Message.message, so
        the handler must read the title from the raw form_dict.
        """
        frappe.local.form_dict = frappe._dict(
            {
                "entry": [
                    {
                        "changes": [
                            {
                                "value": {
                                    "messages": [
                                        {
                                            "from": sender,
                                            "id": f"wamid.test.{frappe.generate_hash(6)}",
                                            "type": "interactive",
                                            "interactive": {
                                                "type": "button_reply",
                                                "button_reply": {
                                                    "id": button_id,
                                                    "title": button_title,
                                                },
                                            },
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }
        )

    def test_handle_incoming_matches_by_button_title_yes(self):
        """Production path: Meta auto-generates payload, match on title 'Yes'."""
        log = _make_log(self.employee)
        settings = LA.get_settings()
        enabled_before = settings.enabled
        send_conf_before = settings.send_confirmation_reply
        create_entry_before = settings.create_lunch_entry_on_yes
        cutoff_before = settings.cutoff_time
        settings.db_set(
            {
                "enabled": 1,
                "send_confirmation_reply": 0,
                "create_lunch_entry_on_yes": 0,
                "cutoff_time": "23:59:59",
            },
            notify=False,
        )
        saved_form_dict = getattr(frappe.local, "form_dict", None)
        try:
            self._simulate_meta_webhook_payload("Yes", button_id="meta_auto_uuid_123")
            # WhatsApp Message.message stores the auto-generated id, NOT LUNCH_YES.
            msg = self._make_incoming_wa_message("meta_auto_uuid_123")
            LA.handle_incoming_whatsapp_message(msg, "after_insert")

            log.reload()
            self.assertEqual(log.response, "Yes")
        finally:
            frappe.local.form_dict = saved_form_dict
            settings.db_set(
                {
                    "enabled": enabled_before,
                    "send_confirmation_reply": send_conf_before,
                    "create_lunch_entry_on_yes": create_entry_before,
                    "cutoff_time": cutoff_before,
                },
                notify=False,
            )

    def test_handle_incoming_matches_by_button_title_no(self):
        """Production path: Meta auto-generates payload, match on title 'No'."""
        log = _make_log(self.employee)
        settings = LA.get_settings()
        enabled_before = settings.enabled
        send_conf_before = settings.send_confirmation_reply
        create_entry_before = settings.create_lunch_entry_on_yes
        cutoff_before = settings.cutoff_time
        settings.db_set(
            {
                "enabled": 1,
                "send_confirmation_reply": 0,
                "create_lunch_entry_on_yes": 0,
                "cutoff_time": "23:59:59",
            },
            notify=False,
        )
        saved_form_dict = getattr(frappe.local, "form_dict", None)
        try:
            self._simulate_meta_webhook_payload("No", button_id="meta_auto_uuid_456")
            msg = self._make_incoming_wa_message("meta_auto_uuid_456")
            LA.handle_incoming_whatsapp_message(msg, "after_insert")

            log.reload()
            self.assertEqual(log.response, "No")
        finally:
            frappe.local.form_dict = saved_form_dict
            settings.db_set(
                {
                    "enabled": enabled_before,
                    "send_confirmation_reply": send_conf_before,
                    "create_lunch_entry_on_yes": create_entry_before,
                    "cutoff_time": cutoff_before,
                },
                notify=False,
            )

    def test_handle_incoming_idempotent_on_double_tap(self):
        log = _make_log(self.employee)
        settings = LA.get_settings()
        enabled_before = settings.enabled
        send_conf_before = settings.send_confirmation_reply
        create_entry_before = settings.create_lunch_entry_on_yes
        settings.db_set(
            {
                "enabled": 1,
                "send_confirmation_reply": 0,
                "create_lunch_entry_on_yes": 0,
                "cutoff_time": "23:59:59",
            },
            notify=False,
        )

        try:
            with patch.object(LA, "send_free_form_text"):
                msg1 = self._make_incoming_wa_message("LUNCH_YES")
                LA.handle_incoming_whatsapp_message(msg1, "after_insert")
                first_responded_at = frappe.db.get_value(
                    "Lunch Attendance Log", log.name, "responded_at"
                )
                msg2 = self._make_incoming_wa_message("LUNCH_NO")
                LA.handle_incoming_whatsapp_message(msg2, "after_insert")

            log.reload()
            # Second tap must not flip the answer.
            self.assertEqual(log.response, "Yes")
            self.assertEqual(str(log.responded_at), str(first_responded_at))
        finally:
            settings.db_set(
                {
                    "enabled": enabled_before,
                    "send_confirmation_reply": send_conf_before,
                    "create_lunch_entry_on_yes": create_entry_before,
                },
                notify=False,
            )

    def test_handle_incoming_after_cutoff_expires_log(self):
        log = _make_log(self.employee)
        settings = LA.get_settings()
        enabled_before = settings.enabled
        send_conf_before = settings.send_confirmation_reply
        create_entry_before = settings.create_lunch_entry_on_yes
        cutoff_before = settings.cutoff_time
        settings.db_set(
            {
                "enabled": 1,
                "send_confirmation_reply": 0,
                "create_lunch_entry_on_yes": 0,
                "cutoff_time": "00:00:01",  # already in the past
            },
            notify=False,
        )

        try:
            with patch.object(LA, "send_free_form_text"):
                msg = self._make_incoming_wa_message("LUNCH_YES")
                LA.handle_incoming_whatsapp_message(msg, "after_insert")

            log.reload()
            self.assertEqual(log.response, "Expired")
        finally:
            settings.db_set(
                {
                    "enabled": enabled_before,
                    "send_confirmation_reply": send_conf_before,
                    "create_lunch_entry_on_yes": create_entry_before,
                    "cutoff_time": cutoff_before,
                },
                notify=False,
            )

    # --- Scheduled trigger -------------------------------------------------
    def test_send_daily_creates_pending_logs(self):
        settings = LA.get_settings()
        snapshot = {
            "enabled": settings.enabled,
            "whatsapp_template_name": settings.whatsapp_template_name,
            "language_code": settings.language_code,
            "eligibility_filter": settings.eligibility_filter,
            "send_confirmation_reply": settings.send_confirmation_reply,
            "create_lunch_entry_on_yes": settings.create_lunch_entry_on_yes,
        }
        # Point to the existing lunch_attendance template if present, else skip.
        template_name = frappe.db.get_value(
            "WhatsApp Templates", {"template_name": "lunch_attendance"}
        )
        if not template_name:
            self.skipTest("lunch_attendance WhatsApp Template not present on site")

        settings.db_set(
            {
                "enabled": 1,
                "whatsapp_template_name": template_name,
                "eligibility_filter": "All Active Employees",
                "send_confirmation_reply": 0,
                "create_lunch_entry_on_yes": 0,
            },
            notify=False,
        )

        try:
            fake_emp = frappe.db.get_value(
                "Employee", self.employee, ["name", "employee_name", "cell_number", "holiday_list"],
                as_dict=True,
            )
            with patch.object(LA, "send_lunch_template") as mock_send, patch.object(
                LA, "get_eligible_employees", return_value=[fake_emp]
            ):
                mock_send.return_value = ("wamid.test.scheduled", {})
                LA.send_daily_lunch_attendance()

            log = frappe.db.get_value(
                "Lunch Attendance Log",
                {"employee": self.employee, "date": getdate()},
                ["response", "template_sent"],
                as_dict=True,
            )
            self.assertIsNotNone(log)
            self.assertEqual(log.response, "Pending")
            self.assertEqual(log.template_sent, 1)
            mock_send.assert_called_once()
        finally:
            update = {k: v for k, v in snapshot.items()}
            settings.db_set(update, notify=False)

    def test_send_daily_is_idempotent(self):
        # Pre-create the log; the scheduler must not duplicate it.
        _make_log(self.employee)
        settings = LA.get_settings()
        enabled_before = settings.enabled
        settings.db_set({"enabled": 1}, notify=False)
        # Isolate from real site employees: only consider the test employee.
        fake_emp = frappe.db.get_value(
            "Employee", self.employee, ["name", "employee_name", "cell_number", "holiday_list"],
            as_dict=True,
        )
        try:
            with patch.object(LA, "send_lunch_template") as mock_send, patch.object(
                LA, "get_eligible_employees", return_value=[fake_emp]
            ):
                LA.send_daily_lunch_attendance()
            # No new send because a log already existed.
            mock_send.assert_not_called()
            count = frappe.db.count(
                "Lunch Attendance Log",
                {"employee": self.employee, "date": getdate()},
            )
            self.assertEqual(count, 1)
        finally:
            settings.db_set({"enabled": enabled_before}, notify=False)

    def test_send_daily_disabled_noop(self):
        settings = LA.get_settings()
        enabled_before = settings.enabled
        settings.db_set({"enabled": 0}, notify=False)
        try:
            with patch.object(LA, "send_lunch_template") as mock_send:
                LA.send_daily_lunch_attendance()
            mock_send.assert_not_called()
        finally:
            settings.db_set({"enabled": enabled_before}, notify=False)
