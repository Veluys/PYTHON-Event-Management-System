import ems.view.displayer as displayer
import ems.controller.input_getter as get_input
from ems.controller.input_getter import getLine
from ems.dao.event_dao import EventDAO
from ems.dao.attendance_dao import AttendDao
from ems.dao.registration_dao import RegDao
from ems.model.event import Event
from ems.model.registration import Registration

class AttendCntrl:
    def __init__(self, conn):
        self.event_dao = EventDAO(conn)
        self.reg_dao = RegDao(conn)
        self.att_dao = AttendDao(conn)

        self._VIEW_PARTICIPANTS_COL = ("Sr-Code", "Department", "Year Level", "Full Name")
        self._VIEW_PARTICIPANTS_SIZE = (0.15, 0.20, 0.15, 0.50)

        self._VIEW_EVENT_COLUMN_HEADERS = ("Event Name", "Date", "Start Time", "End Time", "Venue")
        self._VIEW_EVENT_COLUMN_SIZES = (0.30, 0.20, 0.15, 0.15, 0.20)

    def execute(self):
        displayer.display_header("Attendance Page")

        if self.event_dao.emptyCheck():
            print("There are currently no events!\n")
            return

        event_name = getLine("Event Name: ")
        print()

        try:
            matched_event = self.event_dao.record_search(event_name)
        except Exception as err:
            print("Searching event records failed!")
            displayer.show_error(err)
            return

        if not matched_event:
            print(f"There are no records that matched the event name '{event_name}' \n")
            return

        self.selected_event_details = self.event_dao.display_search(event_name)
        self._selected_event_id = Event(*matched_event).event_id

        if self.reg_dao.emptyCheck(self._selected_event_id):
            print("There are no participants!")
            return

        try:
            self._selected_event_status = self.event_dao.check_status(event_name)
        except Exception as err:
            print("Checking event status failed!")
            displayer.show_error(err)
            return

        if not self._selected_event_status == "ongoing":
            print("Attendance unavailable for non-ongoing events!")
            return

        displayer.display_header("Attendance Page")
        displayer.displayTable("Selected Event", self._VIEW_EVENT_COLUMN_HEADERS,
                               (self.selected_event_details,), self._VIEW_EVENT_COLUMN_SIZES)

        displayer.display_subheader("Attendance Menu")
        att_operations = ("View Attendees", "View Absentees", "Search Participant",
                          "Set as Present", "Reset as Absent", "Exit")

        displayer.display_menu("Select an operation: ", att_operations)
        option = get_input.getInt(len(att_operations))

        match option:
            case 1:
                self._view_attendance(attended=True)
            case 2:
                self._view_attendance(attended=False)
            case 3:
                self._get_attendance()
            case 4:
                self._update_attendance(setPresent=True)
            case 5:
                self._update_attendance(setPresent=False)
            case 6:
                return

        print()

    def _view_attendance(self, attended):
        participant_status = "Attendees" if attended else "Absentees"
        displayer.display_subheader(f"Viewing {participant_status}")

        try:
            participants = self.att_dao.view_attendance(self._selected_event_id, attended)
        except Exception as err:
            print(f"Fetching records of {participant_status} failed!")
            displayer.show_error(err)
            return

        if not participants:
            print(f"There are currently no {participant_status}!\n")
            return
        else:
            displayer.displayTable(participant_status, self._VIEW_PARTICIPANTS_COL,
                                   participants, self._VIEW_PARTICIPANTS_SIZE)

    def _get_attendance(self):
        displayer.display_subheader("Finding Participant's Attendance")
        sr_code = getLine("Student Sr Code: ")
        print()

        reg_record = Registration(self._selected_event_id, sr_code)
        try:
            if not self.reg_dao.is_registered(reg_record):
                print(f"There are no participants with an Sr Code of '{sr_code}'")
        except Exception as err:
            print("Fetching student or/and registration records failed!")
            displayer.show_error(err)
            return

        if self.att_dao.is_attendee(reg_record):
            print(f"The participant with an Sr Code of {sr_code} is an attendee")
        else:
            print(f"The participant with an Sr Code of {sr_code} is an absentee")

    def _update_attendance(self, setPresent):
        if setPresent:
            displayer.display_subheader("Marking Participant as Present")
        else:
            displayer.display_subheader("Marking Participant as Absent")

        sr_code = get_input.getLine("Sr-Code: ")

        if self._can_update(sr_code, setPresent):
            regRecord = Registration(self._selected_event_id, sr_code)
            try:
                self.att_dao.update_attendance(regRecord, setPresent)
            except Exception as err:
                print(f"Updating attendance status of {sr_code} failed!")
                displayer.show_error(err)
            else:
                str_new_att_status = "Attendee" if setPresent else "Absentee"
                print(f"The participant with an Sr Code of {sr_code} was successfully marked as an {str_new_att_status}.\n")

    def _can_update(self, sr_code, setPresent):
        regRecord = Registration(self._selected_event_id, sr_code)
        try:
            curr_att_status = self.att_dao.is_attendee(regRecord)
        except Exception as err:
            print(f"Fetching records of {sr_code} failed!\n")
            displayer.show_error(err)
            return False

        if curr_att_status is None:
            print(f"There are no participants with an Sr-Code '{sr_code}'\n")
            return False

        if curr_att_status and setPresent:
            str_curr_att_status = "Attendee" if curr_att_status else "Absentee"
            print(f"The participant with an Sr-Code of {sr_code} is already marked as an {str_curr_att_status}\n")
            return False

        return True