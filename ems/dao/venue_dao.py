class VenueDAO:
    def __init__(self, conn):
        self.cur = conn.cursor()

    def getVenueNames(self):
        select_query = """
            SELECT venue_name
            FROM venues
            ORDER BY venue_name
        """

        self.cur.execute(select_query)
        return [venue_tuple[0] for venue_tuple in self.cur.fetchall()]

    def getVenueID(self, venue_name):
        select_query = """
            SELECT venue_id
            FROM venues
            WHERE venue_name ILIKE %s
            ORDER BY venue_name
        """

        self.cur.execute(select_query, (venue_name,))
        return self.cur.fetchone()[0]

    def emptyCheck(self):
        select_query = """
                    SELECT COUNT(*)
                    FROM venues
                """

        self.cur.execute(select_query)
        return self.cur.fetchone()[0] == 0