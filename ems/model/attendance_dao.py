import psycopg2

import ems.model.dbconnection as dbconn
import ems.view.displayer as displayer

class AttendDao:
    def __init__(self):
        try:
            self.conn = dbconn.create_connection()
            self.cur = self.conn.cursor()
        except Exception as err:
            print("Database connection can't be established! Program would be terminated.")
            displayer.show_error(err)
            exit(1)

    def _get_base_view_query(self):
        return """
            SELECT
                s.sr_code,
                pshortname,
                year_level,
                CONCAT(last_name, ', ', first_name, ' ', middle_name) AS full_name,
                CASE
                    WHEN attended = true
                        THEN 'Yes'
                    ELSE
                        'No'
                END AS attended
            FROM students AS s
            INNER JOIN registration AS r
                ON s.sr_code = r.sr_code
            INNER JOIN programs AS p
                ON s.program_id = p.program_id
            WHERE event_id = %s    
        """

    def view_attendance(self, event_id, attended):
        view_query = self._get_base_view_query()
        if attended is not None:
            if attended:
                view_query += " AND attended = true "
            else:
                view_query += " AND attended = false "

            view_query += " ORDER BY year_level, pshortname, full_name; "

        self.cur.execute(view_query, (event_id,))
        participants = self.cur.fetchall()
        return participants

    def search_attendance(self, event_id, sr_code):
        view_query = self._get_base_view_query() + " AND s.sr_code ILIKE %s;"

        self.cur.execute(view_query, (event_id, sr_code))
        return (self.cur.fetchone(),)

    def is_attendee(self, event_id, sr_code):
        check_query = """
            SELECT attended
            FROM registration
            WHERE event_id = %s
                AND sr_code = %s
        """

        self.cur.execute(check_query, (event_id, sr_code))
        result = self.cur.fetchone()
        return None if result is None else result[0]

    def update_attendance(self, event_id, sr_code, setPresent):
        update_query = """
            UPDATE registration
            SET
                attended = %s
            WHERE event_id = %s
                AND sr_code = %s
        """

        try:
            self.cur.execute(update_query, (setPresent, event_id, sr_code))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e

att_dao = AttendDao()