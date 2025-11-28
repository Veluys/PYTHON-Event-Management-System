import ems.view.displayer as displayer
import ems.controller.input_getter as get_input
from ems.controller.input_getter import getLine
from ems.model.registration_dao import reg_dao
from ems.model.event_dao import event_dao
from ems.model.student_dao import stud_dao
from ems.model.attendance_dao import att_dao

_VIEW_COLUMN_HEADERS = ("Sr-Code", "Program", "Year Level", "Full Name", "Attended")
_VIEW_COLUMN_SIZES = (0.10, 0.20, 0.10, 0.50, 0.10)

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
