import ems.view.displayer as displayer
import ems.controller.input_getter as get_input
from ems.controller.input_getter import getLine
from ems.model.event_dao import event_dao
from ems.model.attendance_dao import att_dao

_VIEW_COLUMN_HEADERS = ("Sr-Code", "Program", "Year Level", "Full Name", "Attended")
_VIEW_COLUMN_SIZES = (0.15, 0.15, 0.10, 0.50, 0.10)

def execute():
    displayer.display_header("Attendance Page")
    event_name = getLine("Event Name: ")
    print()

    _selected_event_id = None
    try:
        matched_event = event_dao.record_search(event_name)
        if matched_event is None:
            print("There are no events with that given event name!")
            return
    except Exception as err:
        print("Searching event records failed!")
        displayer.show_error(err)
        return
    else:
        _selected_event_id = matched_event[0]

    while True:
        displayer.display_header("Attendance Page")

        displayer.display_subheader("Attendance Menu")
        att_operations = ("View Attendees", "View Absentees", "Search Participant",
                          "Set as Present", "Reset as Absent", "Exit")

        displayer.display_menu("Select an operation: ", att_operations)
        option = get_input.getInt(len(att_operations))

        match option:
            case 1:
                _view_attendance(_selected_event_id, attended=True)
            case 2:
                _view_attendance(_selected_event_id, attended=False)
            case 3:
                _search_registered(_selected_event_id)
            case 4:
                _update_attendance(_selected_event_id, setPresent=True)
            case 5:
                _update_attendance(_selected_event_id, setPresent=False)
            case 6:
                return

def _view_attendance(event_id, attended):
    participant_status = "Attendees" if attended else "Absentees"
    displayer.display_subheader(f"Viewing {participant_status}")

    try:
        participants = att_dao.view_attendance(event_id, attended)
    except Exception as err:
        print(f"Fetching records of {participant_status} failed!")
        displayer.show_error(err)
    else:
        if len(participants) == 0:
            print(f"There are currently no {participant_status}!\n")
            return
        else:
            displayer.displayTable(participant_status, _VIEW_COLUMN_HEADERS, participants, _VIEW_COLUMN_SIZES)

def _search_registered(event_id):
    displayer.display_subheader("Searching Participants")
    sr_code = getLine("Student Sr Code: ")
    print()

    try:
        participants = att_dao.search_attendance(event_id, sr_code)
    except Exception as err:
        print("Fetching student or/and registration records failed!")
        displayer.show_error(err)
    else:
        if participants[0] is None:
            print(f"There are no participants with an Sr-Code '{sr_code}'\n")
            return
        else:
            displayer.displayTable("Matched Participant", _VIEW_COLUMN_HEADERS, participants, _VIEW_COLUMN_SIZES)

def _update_attendance(event_id, setPresent):
    if setPresent:
        displayer.display_subheader("Marking Participant as Present")
    else:
        displayer.display_subheader("Marking Participant as Absent")

    sr_code = get_input.getLine("Sr-Code: ")

    if _can_update(event_id, sr_code, setPresent):
        try:
            att_dao.update_attendance(event_id, sr_code, setPresent)
        except Exception as err:
            print(f"Updating attendance status of {sr_code} failed!")
            displayer.show_error(err)
        else:
            str_new_att_status = "Attendee" if setPresent else "Absentee"
            print(f"The participant with an Sr Code of {sr_code} was successfully marked as an {str_new_att_status}.\n")

def _can_update(event_id, sr_code, setPresent):
    try:
        curr_att_status = att_dao.is_attendee(event_id, sr_code)
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