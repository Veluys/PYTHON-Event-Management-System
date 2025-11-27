import psycopg2

import ems.model.dbconnection as dbconn
import ems.model.venue as venue_model
import ems.view.displayer as displayer

class VenueDAO:
    def __init__(self):
        try:
            self.conn = dbconn.create_connection()
            self.cur = self.conn.cursor()
        except Exception as err:
            print("Database connection can't be established! Program would be terminated.")
            displayer.show_error(err)
            exit(1)

    @staticmethod
    def _is_a_venue(self, obj):
        if not isinstance(obj, venue_model.Venue):
            print("The passed parameter is not of venue type!")
            return False
        return True

    def getVenueNames(self):
        select_query = """
            SELECT venue_name
            FROM venues
            ORDER BY venue_name
        """

        self.cur.execute(select_query)
        return [row[0] for row in self.cur.fetchall()]

    def getVenueID(self, venue_name):
        select_query = """
            SELECT venue_id
            FROM venues
            WHERE venue_name ILIKE %s
            ORDER BY venue_name
        """

        self.cur.execute(select_query, (venue_name,))
        return self.cur.fetchone()[0]

venue_dao = VenueDAO()