import ems.view.displayer as displayer
from ems.controller.input_getter import getInt, getLine, getTime, getDate
from ems.dao import EventDAO, VenueDAO
from ems.model.event import Event

class EventCntrl:
    def __init__(self, conn):
        self.event_dao = EventDAO(conn)
        self.venue_dao = VenueDAO(conn)

        self._VIEW_COLUMN_HEADERS = ["Event Name", "Date", "Start Time", "End Time", "Venue"]
        self._VIEW_COLUMN_SIZES = [0.30, 0.20, 0.15, 0.15, 0.20]

    def execute(self):
        while True:
            displayer.display_header("Events Page")

            if self.venue_dao.emptyCheck():
                print("There are currently no venues!\n")
                return

            displayer.display_subheader("Event Menu")
            event_operations = ("Add Events", "View Completed Events", "View Scheduled Events",
                                "View Upcoming Events", "View Ongoing Events", "Search Events",
                                "Update Events", "Delete Events", "Exit")

            displayer.display_menu("Select an operation: ", event_operations)
            option = getInt(len(event_operations))

            if option >= 2 and option != 6 and self.event_dao.emptyCheck():
                print("There are currently no events!\n")
                return

            match option:
                case 1:
                    self._add_event()
                case 2:
                    self._view_events("completed")
                case 3:
                    self._view_events("scheduled")
                case 4:
                    self._view_events("upcoming")
                case 5:
                    self._view_events("ongoing")
                case 6:
                    self._search_event()
                case 7:
                    self._update_event()
                case 8:
                    self._delete_event()
                case 9:
                    self.event_dao.cur.close()
                    self.venue_dao.cur.close()
                    return

    def _add_event(self):
        displayer.display_subheader("Adding Event")

        try:
            venues = self.venue_dao.getVenueNames()
        except Exception as err:
            print("Fetching venue names failed!")
            displayer.show_error(err)
            return

        event_name = getLine("Event name: ")

        try:
            matched_event = self.event_dao.record_search(event_name)
        except Exception as err:
            print("Checking if event_name already exists failed!")
            displayer.show_error(err)
            return

        if matched_event:
            print(f"An event with an event name of '{event_name}' already exists in the database!\n")
            return

        event_date = getDate("Event Date")
        start_time = getTime("Start Time")

        while True:
            end_time = getTime("End Time")
            try:
                if end_time < start_time:
                    raise ValueError("Error! End Time is before Start Time!")
            except ValueError as err:
                displayer.show_error(err)
            else:
                break

        displayer.display_menu("Venues: ", venues)
        venue_option = getInt(len(venues)) - 1
        try:
            venue_id = self.venue_dao.getVenueID(venues[venue_option])
        except Exception as err:
            print("Matching venue id for the selected venue name failed")
            displayer.show_error(err)
            return

        event = Event(event_name, event_date, start_time, end_time, venue_id)

        try:
            overlapped_events = self.event_dao.view_overlapped_events(event)
        except Exception as err:
            print("Checking for overlapped events failed!")
            displayer.show_error(err)
            return

        if overlapped_events:
            print("The event can't be added to the database!")
            displayer.displayTable("Overlapped Events",
                                   self._VIEW_COLUMN_HEADERS, overlapped_events, self._VIEW_COLUMN_SIZES)
            return

        try:
            self.event_dao.insert_event(event)
        except Exception as err:
            print("Adding new event failed!")
            displayer.show_error(err)
        else:
            print("New event was added successfully")

    def _view_events(self, status : str):
        try:
            events = self.event_dao.view_events(status)
        except Exception as err:
            print("Fetching event records failed!")
            displayer.show_error(err)
            return

        if not events:
            print("There are currently no events!\n")
            return

        displayer.displayTable(f"Viewing {status.title()} Events", self._VIEW_COLUMN_HEADERS,
                               events, self._VIEW_COLUMN_SIZES)

    def _search_event(self):
        displayer.display_subheader("Search Event")
        event_name = getLine("Event name: ")
        print()

        try:
            matched_event = self.event_dao.display_search(event_name)
        except Exception as err:
            print("Searching event records failed!")
            displayer.show_error(err)
            return

        if not matched_event:
            print(f"There are no records that matched the event name '{event_name}'\n")
            return

        displayer.displayTable("Matched Event", self._VIEW_COLUMN_HEADERS, matched_event, self._VIEW_COLUMN_SIZES)

    def is_manipulable(self, event_name : str):
        try:
            event_status = self.event_dao.check_status(event_name)
        except Exception as err:
            print("Checking event status failed!")
            displayer.show_error(err)
            return False

        if event_status in ("completed", "ongoing"):
            print("Completed or ongoing events can't be manipulated!")
            return False
        else:
            return True

    def _update_event(self):
        displayer.display_subheader("Updating Event")
        old_event_name = getLine("Event name: ")

        try:
            matched_event = self.event_dao.record_search(old_event_name)
        except Exception as err:
            print("Searching event records failed!")
            displayer.show_error(err)
            return

        if not matched_event:
            print(f"There are no records that matched the event name '{old_event_name}' \n")
            return

        if not self.is_manipulable(old_event_name):
            return

        upd_event = Event(*matched_event)

        try:
            venues = self.venue_dao.getVenueNames()
        except Exception as err:
            print("Fetching venue names failed!")
            displayer.show_error(err)
            return

        print("Note: Only provide values to the field(s) you want to update. Otherwise simply press enter.")

        new_event_name = getLine("Event name: ", True)

        if new_event_name:
            try:
                matched_event = self.event_dao.record_search(new_event_name)
            except Exception as err:
                print("Checking if event_name already exists failed!")
                displayer.show_error(err)
                return

            if matched_event:
                print(f"An event with an event name of '{new_event_name}' already exists in the database!\n")
                return
            else:
                upd_event.event_name = new_event_name

        event_date = getDate("Event Date", True)
        if event_date: upd_event.event_date = event_date

        start_time = getTime("Start Time", True)
        if start_time: upd_event.start_time = start_time

        while True:
            end_time = getTime("End Time", True)

            if end_time:
                try:
                    if end_time < start_time():
                        raise ValueError("Error! End Time is before Start Time!")
                except ValueError as err:
                    displayer.show_error(err)
                else:
                    upd_event.end_time = end_time
            else:
                break

        displayer.display_menu("Venues: ", venues)
        venue_option = getInt(len(venues), True)

        if venue_option != -1:
            try:
                upd_event.venue_id = self.venue_dao.getVenueID(venues[venue_option - 1])
            except Exception as err:
                print("Matching venue id for the selected venue name failed")
                displayer.show_error(err)
                return

        try:
            overlapped_events = self.event_dao.view_overlapped_events(upd_event)
        except Exception as err:
            print("Checking for overlapped events failed!")
            displayer.show_error(err)
            return

        if overlapped_events:
            print("The event can't be updated!")
            displayer.displayTable("Overlapped Events",
                                   self._VIEW_COLUMN_HEADERS, overlapped_events, self._VIEW_COLUMN_SIZES)
            return

        try:
            self.event_dao.update_event(upd_event)
        except Exception as err:
            print(f"Updating the event record of {old_event_name} failed!")
            displayer.show_error(err)
        else:
            print("Event was updated successfully")


    def _delete_event(self):
        displayer.display_subheader("Search Event")
        event_name = getLine("Event name: ")
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

        if not self.is_manipulable(event_name):
            return

        try:
            self.event_dao.delete_event(event_name)
        except Exception as err:
            print("Deleting the event record failed!")
            displayer.show_error(err)
        else:
            print("Event was deleted successfully")