import ems.view.displayer as displayer
import ems.controller.input_getter as get_input
from ems.model.event_dao import event_dao
from ems.model.venue_dao import venue_dao
import ems.model.event as event_model

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
            case 6:
                return

def _add_event():
    displayer.display_header("Adding Event")

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
