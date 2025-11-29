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

    def view_upcoming(self):
        view_query = self._get_base_view_query() + """
            WHERE e.event_date BETWEEN (CURRENT_DATE + INTERVAL '1 day') AND (CURRENT_DATE + INTERVAL '3 days')
        """

        self.cur.execute(view_query)
        return self.cur.fetchall()

    def view_events(self):
        view_query = self._get_base_view_query() + "\nORDER BY e.event_date;"
        self.cur.execute(view_query)
        return self.cur.fetchall()

    def display_search(self, event_name):
        view_query = self._get_base_view_query() + "\nWHERE event_name ILIKE %s"
        self.cur.execute(view_query, (event_name,))
        return self.cur.fetchone()

    def view_overlapped_events(self, event_id, event):
        view_query = self._get_base_view_query() + """
            WHERE e.event_id != %s
                AND e.venue_id = %s
                AND e.event_date = %s
                AND %s::time BETWEEN e.start_time AND e.end_time
        """

        params = [event_id, event.venue_id, event.event_date, event.start_time]

        self.cur.execute(view_query, params)
        result = self.cur.fetchall()
        return result

    def _get_base_view_query(self):
        return """
            SELECT
                event_name,
                TO_CHAR(event_date, 'Mon DD, YYYY') AS event_date,
                LOWER(TO_CHAR(start_time, 'FMHH12:MI AM')) AS start_time,
                LOWER(TO_CHAR(end_time, 'FMHH12:MI AM')) AS end_time,
                venue_name
            FROM events e
            INNER JOIN venues v 
                ON e.venue_id = v.venue_id
        """

    def record_search(self, event_name):
        search_query = """
            SELECT
                event_id,
                event_name,
                event_date,
                start_time,
                end_time,
                venue_id
            FROM events
            WHERE event_name ILIKE %s
        """

        self.cur.execute(search_query, (event_name,))
        return self.cur.fetchone()

    def update_event(self, event_id, event):
        if not self._is_an_event(event):
            return

        update_query = """
            UPDATE events
            SET
                event_name = %s,
                event_date = %s,
                start_time = %s,
                end_time = %s,
                venue_id = %s
            WHERE event_id = %s
        """

        update_value = [event.event_name, event.event_date, event.start_time, event.end_time, event.venue_id, event_id]

        try:
            self.cur.execute(update_query, update_value)
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e

    def delete_event(self, event_name):
        delete_query = """
            DELETE FROM events
            WHERE event_name = %s
        """

        try:
            self.cur.execute(delete_query, (event_name,))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e

    def _is_an_event(self, obj):
        if not isinstance(obj, event_model.Event):
            print("The passed parameter is not of event type!")
            return False
        return True

    def emptyCheck(self):
        select_query = """
                    SELECT COUNT(*)
                    FROM events
                """

        self.cur.execute(select_query)
        return self.cur.fetchone()[0] == 0

event_dao = EventDAO()