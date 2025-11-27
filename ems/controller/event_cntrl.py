import ems.view.displayer as displayer
import ems.controller.input_getter as get_input
from ems.model.event_dao import event_dao
from ems.model.venue_dao import venue_dao
import ems.model.event as event_model

_VIEW_COLUMN_HEADERS = ["Event Name", "Date", "Start Time", "End Time", "Venue"]
_VIEW_COLUMN_SIZES = [0.30, 0.20, 0.15, 0.15, 0.20]

def execute():
    while True:
        displayer.display_header("Events Page")

        displayer.display_subheader("Event Menu")
        event_operations = ("Add Events", "View Events", "Search Events", "Update Events", "Delete Events", "Exit")

        displayer.display_menu("Select an operation: ", event_operations)
        option = get_input.getInt(len(event_operations))

        match option:
            case 1:
                _add_event()
            case 2:
                _view_events()
            case 3:
                _search_event()
            case 4:
                _update_event()
            case 5:
                _delete_event()
            case 6:
                return

def _add_event():
    displayer.display_subheader("Adding Event")

    venues = None
    try:
        venues = venue_dao.getVenueNames()
    except Exception as err:
        print("Fetching venue names failed!")
        displayer.show_error(err)
        return

    event = event_model.Event()
    event.set_event_name(get_input.getLine("Event name: "))
    event.set_event_date(get_input.getDate("Event Date"))
    event.set_start_time(get_input.getTime("Start Time"))
    event.set_end_time(get_input.getTime("End Time"))
    displayer.display_menu("Venues: ", venues)
    venue_option = get_input.getInt(len(venues)) - 1
    try:
        venue_name = venues[venue_option]
        event.set_venue_id(venue_dao.getVenueID(venue_name))
    except Exception as err:
        print("Matching venue id for the selected venue name failed")
        displayer.show_error(err)

    try:
        event_dao.insert_event(event)
    except Exception as err:
        print("Adding new event failed!")
        displayer.show_error(err)
    else:
        print("New event was added successfully")

def _view_events():
    displayer.display_subheader("Viewing Events")

    try:
        events = event_dao.view_events()
    except Exception as err:
        print("Fetching event records failed!")
        displayer.show_error(err)
    else:
        if len(events) == 0:
            print("There are currently no participants!\n")
            return
        displayer.displayTable("Events", _VIEW_COLUMN_HEADERS, events, _VIEW_COLUMN_SIZES)

def _search_event():
    displayer.display_subheader("Search Event")
    event_name = get_input.getLine("Event name: ")
    print()

    event = None
    try:
        event = event_dao.view_events(event_name)
    except Exception as err:
        print("Searching event records failed!")
        displayer.show_error(err)
    else:
        if event[0] is None:
            print(f"There are no records that matched the event name '{event_name}'\n")
            return
        displayer.displayTable("Matched Event", _VIEW_COLUMN_HEADERS, event, _VIEW_COLUMN_SIZES)

def _update_event():
    displayer.display_subheader("Updating Event")
    old_event_name = get_input.getLine("Event name: ")

    matched_event = None
    try:
        matched_event = event_dao.record_search(old_event_name)
    except Exception as err:
        print("Searching event records failed!")
        displayer.show_error(err)
    else:
        if matched_event is None:
            print(f"There are no records that matched the event name '{old_event_name}' \n")
            return

    print()

    venues = None
    try:
        venues = venue_dao.getVenueNames()
    except Exception as err:
        print("Fetching venue names failed!")
        displayer.show_error(err)
        return

    event = event_model.Event()
    print("Note: Only provide values to the field(s) you want to update. Otherwise simply press enter.")

    event_name = get_input.getLine("Event name: ", True)
    event.set_event_name(event_name if event_name is not None else matched_event[1])

    event_date = get_input.getDate("Event Date", True)
    event.set_event_date(event_date if event_date is not None else matched_event[2])

    start_time = get_input.getTime("Start Time", True)
    event.set_start_time(start_time if start_time is not None else matched_event[3])

    end_time = get_input.getTime("End Time", True)
    event.set_end_time(end_time if end_time is not None else matched_event[4])

    displayer.display_menu("Venues: ", venues)
    venue_option = get_input.getInt(len(venues), True)

    if venue_option != -1:
        venue_option -= 1
        try:
            venue_name = venues[venue_option]
            event.set_venue_id(venue_dao.getVenueID(venue_name))
        except Exception as err:
            print("Matching venue id for the selected venue name failed")
            displayer.show_error(err)
    else:
        event.set_venue_id(matched_event[5])

    try:
        event_dao.update_event(matched_event[0], event)
    except Exception as err:
        print(f"Updating the event record of {old_event_name} failed!")
        displayer.show_error(err)
    else:
        print("Event was updated successfully")

def _delete_event():
    displayer.display_subheader("Search Event")
    event_name = get_input.getLine("Event name: ")
    print()

    try:
        matched_event = event_dao.record_search(event_name)
    except Exception as err:
        print("Searching event records failed!")
        displayer.show_error(err)
    else:
        if matched_event is None:
            print(f"There are no records that matched the event name '{event_name}' \n")
            return

    try:
        event_dao.delete_event(event_name)
    except Exception as err:
        print("Deleting the event record failed!")
        displayer.show_error(err)
    else:
        print("Event was deleted successfully")
