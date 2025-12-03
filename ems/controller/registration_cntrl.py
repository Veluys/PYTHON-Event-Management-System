import ems.view.displayer as displayer
from ems.controller.input_getter import getLine, getInt
from ems.dao import RegDao, EventDAO, StudentDao
from ems.model import Event, Registration

class RegCntrl:
    def __init__(self, conn):
        self.event_dao = EventDAO(conn)
        self.reg_dao = RegDao(conn)
        self.stud_dao = StudentDao(conn)

        self._VIEW_PARTICIPANT_HEADERS = ("Sr-Code", "Department", "Year Level", "Full Name")
        self._VIEW_PARTICIPANT_COLUMN_SIZES = (0.15, 0.20, 0.15, 0.50)

        self._VIEW_EVENT_COLUMN_HEADERS = ["Event Name", "Date", "Start Time", "End Time", "Venue"]
        self._VIEW_EVENT_COLUMN_SIZES = [0.30, 0.20, 0.15, 0.15, 0.20]

    def execute(self):
        displayer.display_header("Registration Page")

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

        try:
            self._selected_event_status = self.event_dao.check_status(event_name)
        except Exception as err:
            print("Checking event status failed!")
            displayer.show_error(err)
            return

        self.registration_menu(self._selected_event_status)
        print()

    def registration_menu(self, status:str):
        is_completed = status == "completed"
        operations = ("View Participants", "Search Participant", "Exit") if is_completed else \
                     ("Add Participants", "View Participants", "Search Participant", "Remove Participants", "Exit")

        while True:
            displayer.display_header("Registration Page")
            displayer.displayTable("Selected Event", self._VIEW_EVENT_COLUMN_HEADERS,
                                   (self.selected_event_details,), self._VIEW_EVENT_COLUMN_SIZES)
            displayer.display_subheader("Registration Menu")
            displayer.display_menu("Select an operation: ", operations)

            option = getInt(len(operations))

            if is_completed or (option >= 2 and option != len(operations)):
                if self.reg_dao.emptyCheck(self._selected_event_id):
                    print("There are no participants!")
                    continue

            handlers = [self._view_registered, self._search_registered]
            if not is_completed:
                handlers = [self._add_participant] + handlers + [self._remove_participant]
            handlers = handlers + [None]

            if option < len(handlers):
                handlers[option - 1]()
            else:
                return

            print()

    def _add_participant(self):
        displayer.display_subheader("Adding Participant")

        sr_code = getLine("Student Sr Code: ")

        try:
            if not self.stud_dao.student_exists(sr_code):
                print(f"There are no students that matched the given Sr-Code {sr_code}")
                return
        except Exception as err:
            print("Searching student records failed!")
            displayer.show_error(err)

        new_reg_record = Registration(self._selected_event_id, sr_code)
        try:
            if self.reg_dao.is_registered(new_reg_record):
                print(f"Student with Sr-Code {sr_code} is already registered!")
                return
        except Exception as err:
            print("Searching registration records failed!")
            displayer.show_error(err)
            return

        try:
            self.reg_dao.insert_participant(new_reg_record)
        except Exception as err:
            print("Inserting new registration failed!")
            displayer.show_error(err)
        else:
            print("New participant was added successfully!")

    def _view_registered(self):
        displayer.display_subheader("Viewing Participants")

        try:
            participants = self.reg_dao.view_registered(self._selected_event_id)
        except Exception as err:
            print("Fetching student records failed!")
            displayer.show_error(err)
            return

        if not participants:
            print("There are currently no participants!")
            return
        else:
            displayer.displayTable("Registered Participants", self._VIEW_PARTICIPANT_HEADERS,
                                   participants, self._VIEW_PARTICIPANT_COLUMN_SIZES)

    def _search_registered(self):
        displayer.display_subheader("Searching Participants")
        sr_code = getLine("Student Sr Code: ")
        print()

        try:
            participants = self.reg_dao.view_registered(self._selected_event_id, sr_code)
        except Exception as err:
            print("Fetching student records failed!")
            displayer.show_error(err)
            return

        if not participants:
            print(f"There are no participants with an Sr-Code '{sr_code}'")
            return
        else:
            displayer.displayTable("Matched Participant", self._VIEW_PARTICIPANT_HEADERS,
                                   (participants,), self._VIEW_PARTICIPANT_COLUMN_SIZES)

    def _remove_participant(self):
        displayer.display_subheader("Remove Participant")
        sr_code = getLine("Student Sr Code: ")
        print()

        reg_record = Registration(self._selected_event_id, sr_code)
        try:
            if not self.reg_dao.is_registered(reg_record):
                print(f"There are no participants with an Sr-Code '{sr_code}'")
                return
        except Exception as err:
            print("Searching student records failed!")
            displayer.show_error(err)

        try:
            self.reg_dao.remove_participant(reg_record)
        except Exception as err:
            print("Removing the participant failed!")
            displayer.show_error(err)
        else:
            print("Participant was removed successfully")