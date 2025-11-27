import ems.view.displayer as displayer
import ems.controller.input_getter as get_input

def execute():
    displayer.display_header("Welcome to Event Management System!")

    while True:
        displayer.display_header("Start Page")

        displayer.display_subheader("Main Menu")
        main_menu_options = ("Events", "Registration", "Attendance", "Exit")
        displayer.display_menu("What do you want to do or work with today?", main_menu_options)
        option = get_input.getInt(len(main_menu_options))

        match option:
            case 4:
                displayer.display_subheader("Thank you for using the system!")
                return
