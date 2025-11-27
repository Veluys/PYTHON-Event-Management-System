class Event:
    def __init__(self, event_name, event_date, start_time, end_time, venue_id):
        self.event_name = event_name
        self.event_date = event_date
        self.start_time = start_time
        self.end_time = end_time
        self.venue_id = venue_id

    def set_event_name(self, event_name):
        self.event_name = event_name

    def set_event_date(self, event_date):
        self.event_date = event_date

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_end_time(self, end_time):
        self.end_time = end_time

    def set_venue_id(self, venue_id):
        self.venue_id = venue_id

    def get_event_name(self):
        return self.event_name

    def get_event_date(self):
        return self.event_date

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_venue_id(self):
        return self.venue_id
