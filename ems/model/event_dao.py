import psycopg2

import ems.model.dbconnection as dbconn
import ems.model.event as event_model
import ems.view.displayer as displayer

class EventDAO:
    def __init__(self):
        try:
            self.conn = dbconn.create_connection()
            self.cur = self.conn.cursor()
        except Exception as err:
            print("Database connection can't be established! Program would be terminated.")
            displayer.show_error(err)
            exit(1)

    def _is_an_event(self, obj):
        if not isinstance(obj, event_model.Event):
            print("The passed parameter is not of event type!")
            return False
        return True

    def insert_event(self, event):
        if not self._is_an_event(event):
            return

        insert_query = """
                INSERT INTO events (event_name, event_date, start_time, end_time, venue_id)
                        VALUES (%s, %s, %s, %s, %s);
        """
        insert_value = [event.event_name, event.event_date, event.start_time, event.end_time, event.venue_id]

        try:
            self.cur.execute(insert_query, insert_value)
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e

    def view_events(self):
        view_query = EventDAO._get_base_view_query() + """
            SELECT
                event_name,
                TO_CHAR(event_date, 'Mon DD, YYYY') AS event_date,
                LOWER(TO_CHAR(start_time, 'FMHH12:MI AM')) AS start_time,
                LOWER(TO_CHAR(end_time, 'FMHH12:MI AM')) AS end_time,
                venue_name
            FROM events_cte
        """

        self.cur.execute(view_query)
        return self.cur.fetchall()

    def search_event(self, event_name):
        search_query = EventDAO._get_base_view_query() + """
            SELECT
                event_name,
                TO_CHAR(event_date, 'Mon DD, YYYY') AS event_date,
                LOWER(TO_CHAR(start_time, 'FMHH12:MI AM')) AS start_time,
                LOWER(TO_CHAR(end_time, 'FMHH12:MI AM')) AS end_time,
                venue_name
            FROM events_cte
            WHERE event_name ILIKE ?
        """

        self.cur.execute(search_query)
        return self.cur.fetchall()

    @staticmethod
    def _get_base_view_query():
        return """
            WITH events_cte AS (
                SELECT
                    e.event_name,
                    event_date,
                    start_time,
                    end_time,
                    v.venue_name
                FROM events AS e
                INNER JOIN venues AS v
                    ON e.venue_id = v.venue_id
                ORDER BY event_date
            )
        """

event_dao = EventDAO()