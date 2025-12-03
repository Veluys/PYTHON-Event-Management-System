import psycopg2

from ems.model.event import Event

class EventDAO:
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()

    def insert_event(self, event : Event):
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

    @staticmethod
    def _get_base_view_query():
        return """
                SELECT
                    ed.event_name,
                    ed.event_date,
                    ed.start_time,
                    ed.end_time,
                    ed.venue_name
                FROM event_details AS ed
                INNER JOIN events AS e
                    ON ed.event_name = e.event_name
            """

    def view_events(self, event_status : str):
        view_query = EventDAO._get_base_view_query() + """
            WHERE event_status ILIKE %s
        """
        self.cur.execute(view_query, (event_status,))
        return self.cur.fetchall()

    def display_search(self, event_name : str):
        view_query = EventDAO._get_base_view_query() + """
            WHERE ed.event_name ILIKE %s
        """

        self.cur.execute(view_query, (event_name,))
        return self.cur.fetchone()

    def view_overlapped_events(self, event : Event):
        view_query = EventDAO._get_base_view_query() + """
            WHERE e.event_id != %s
                AND e.venue_id = %s
                AND e.event_date = %s
                AND %s::time BETWEEN e.start_time AND e.end_time
        """

        params = (event.event_id, event.venue_id, event.event_date, event.start_time)

        self.cur.execute(view_query, params)
        return self.cur.fetchall()

    def record_search(self, event_name : str):
        search_query = """
            SELECT
                event_name,
                event_date,
                start_time,
                end_time,
                venue_id,
                event_id
            FROM events
            WHERE event_name ILIKE %s
        """

        self.cur.execute(search_query, (event_name,))
        return self.cur.fetchone()

    def update_event(self, event : Event):
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

        update_value = [event.event_name, event.event_date, event.start_time,
                        event.end_time, event.venue_id, event.event_id]

        try:
            self.cur.execute(update_query, update_value)
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e

    def delete_event(self, event_name : str):
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

    def check_status(self, event_name : str):
        check_query = """
                    SELECT event_status
                    FROM event_details
                    WHERE event_name ILIKE %s
                """

        self.cur.execute(check_query, (event_name,))
        return self.cur.fetchone()[0]

    def emptyCheck(self):
        select_query = """
                    SELECT COUNT(*)
                    FROM events
                """

        self.cur.execute(select_query)
        return self.cur.fetchone()[0] == 0