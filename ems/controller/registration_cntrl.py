import ems.view.displayer as displayer
import ems.controller.input_getter as get_input
from ems.controller.input_getter import getLine
from ems.model.registration_dao import reg_dao
from ems.model.event_dao import event_dao
from ems.model.student_dao import stud_dao

_VIEW_COLUMN_HEADERS = ("Sr-Code", "Program", "Year Level", "Full Name")
_VIEW_COLUMN_SIZES = (0.15, 0.20, 0.15, 0.50)

def execute():
    displayer.display_header("Registration Page")
    event_name = getLine("Event Name: ")
    print()

    matched_event = None
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
        displayer.display_header("Registration Page")

        displayer.display_subheader("Registration Menu")
        reg_operations = ("Add Participant", "View Participants", "Search Participant", "Remove Participants", "Exit")

        displayer.display_menu("Select an operation: ", reg_operations)
        option = get_input.getInt(len(reg_operations))

        match option:
            case 1:
                _add_participant(_selected_event_id)
            case 5:
                return

def _add_participant(event_id):
    displayer.display_subheader("Adding Participant")

    sr_code = getLine("Student Sr Code: ")

    try:
        if not stud_dao.student_exists(sr_code):
            print(f"There are no students that matched the given Sr-Code {sr_code}\n")
            return
    except Exception as err:
        print("Searching student records failed!")
        displayer.show_error(err)

    try:
        reg_dao.insert_participant(event_id, sr_code)
    except Exception as err:
        print("Searching student records failed!")
        displayer.show_error(err)
    else:
        print("New participant was added successfully!\n")
