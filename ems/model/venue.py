class Venue:
    def __init__(self):
        self.venue_id = None
        self.venue_name = None

    def set_venue_id(self, venue_id):
        self.venue_id = venue_id

    def set_venue_name(self, venue_name):
        self.venue_name = venue_name


    def get_venue_id(self):
        return self.venue_id

    def get_venue_name(self):
        return self.venue_name