class Event:
    def __init__(self):
        self.event_id = None
        self.event_name = None
        self.event_date = None
        self.start_time = None
        self.end_time = None
        self.venue_id = None

    def set_event_id(self, event_id):
        self.event_id = event_id

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

    def get_event_id(self):
        return self.event_id

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
