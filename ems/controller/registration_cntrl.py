import ems.view.displayer as displayer
import ems.controller.input_getter as get_input
from ems.model.registration_dao import reg_dao
from ems.model.event_dao import event_dao

_VIEW_COLUMN_HEADERS = ("Sr-Code", "Program", "Year Level", "Full Name")
_VIEW_COLUMN_SIZES = (0.15, 0.20, 0.15, 0.50)

def execute():
    while True:
        displayer.display_header("Registration Page")

        displayer.display_subheader("Registration Menu")
        reg_operations = ("Add Participant", "View Participants", "Search Participant", "Remove Participants", "Exit")

        displayer.display_menu("Select an operation: ", reg_operations)
        option = get_input.getInt(len(reg_operations))

        match option:
            case 5:
                return
