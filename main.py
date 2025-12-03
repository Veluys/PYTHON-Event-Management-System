import psycopg2

import ems.view.displayer as displayer
from ems.controller import *

def get_connection():
    try:
        connection = psycopg2.connect(
            dbname="plan_et",
            user="postgres",
            password="byte",
            host="localhost",
            port="5432"
        )
    except Exception as e:
        print("Database connection can't be established! Program would be forcefully terminated!")
        displayer.show_error(e)
        exit(1)
    else:
        return connection

conn = get_connection()
event_cntrl = EventCntrl(conn)
reg_cntrl = RegCntrl(conn)
att_cntrl = AttendCntrl(conn)

def main():
    displayer.display_header("Welcome to PLAN ET: The BSU-MALVAR Event Management System")

    while True:
        displayer.display_header("Start Page")
        displayer.display_subheader("Main Menu")
        main_menu_options = ("Events", "Registration", "Attendance", "Exit")
        displayer.display_menu("What do you want to do or work with today?", main_menu_options)
        option = getInt(len(main_menu_options))

        match option:
            case 1:
                event_cntrl.execute()
            case 2:
                reg_cntrl.execute()
            case 3:
                att_cntrl.execute()
            case 4:
                displayer.display_subheader("Thank you for using Plan_ET. Happy Planning!")
                conn.close()

if __name__ == '__main__':
    main()