import ems.view.displayer as displayer
import ems.controller.input_getter as get_input
import ems.controller.event_cntrl as event_cntrl
import ems.controller.registration_cntrl as reg_cntrl
import ems.controller.attendance_cntrl as att_cntrl

def execute():
    displayer.display_header("Welcome to Event Management System!")

    while True:
        displayer.display_header("Start Page")
        event_cntrl.show_upcoming()

        displayer.display_subheader("Main Menu")
        main_menu_options = ("Events", "Registration", "Attendance", "Exit")
        displayer.display_menu("What do you want to do or work with today?", main_menu_options)
        option = get_input.getInt(len(main_menu_options))

        match option:
            case 1:
                event_cntrl.execute()
            case 2:
                reg_cntrl.execute()
            case 3:
                att_cntrl.execute()
            case 4:
                displayer.display_subheader("Thank you for using the system!")
                return
