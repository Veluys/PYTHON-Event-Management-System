import ems.view.displayer as displayer
import ems.controller.input_getter as get_input

def execute():
    while True:
        displayer.display_header("Events Page")

        displayer.display_subheader("Event Menu")
        event_operations = ("Add Events", "View Events", "Search Events", "Update Events", "Delete Events", "Exit")

        displayer.display_menu("Select an operation: ", event_operations)
        option = get_input.getInt(len(event_operations))

        match option:
            case 6:
                return
