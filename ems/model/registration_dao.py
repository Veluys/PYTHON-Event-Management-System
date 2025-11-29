import psycopg2

import ems.model.dbconnection as dbconn
import ems.model.student as student_model
import ems.view.displayer as displayer

class RegDao:
    def __init__(self):
        try:
            self.conn = dbconn.create_connection()
            self.cur = self.conn.cursor()
        except Exception as err:
            print("Database connection can't be established! Program would be terminated.")
            displayer.show_error(err)
            exit(1)

    def insert_participant(self, event_id, sr_code):
        insert_query = """
                INSERT INTO registration (event_id, sr_code)
                VALUES (%s, %s)
        """
        insert_value = [event_id, sr_code]

        try:
            self.cur.execute(insert_query, insert_value)
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e

    def view_registered(self, event_id, sr_code=None):
        view_query = """
                SELECT
                	s.sr_code,
                	pshortname,
                	year_level,
                	CONCAT(last_name, ', ', first_name, ' ', middle_name) AS full_name
                FROM students AS s
                INNER JOIN registration AS r
                    ON event_id = %s
                    AND s.sr_code = r.sr_code
                INNER JOIN programs AS p
                	ON s.program_id = p.program_id
            """

        if sr_code is not None:
            view_query += """
                WHERE s.sr_code ILIKE %s;
            """
            self.cur.execute(view_query, (event_id, sr_code))
            return (self.cur.fetchone(),)
        else:
            view_query += """
                ORDER BY year_level, pshortname, full_name;
            """
            self.cur.execute(view_query, (event_id,))
            return self.cur.fetchall()

    def is_registered(self, sr_code):
        search_query = """
            SELECT *
            FROM registration
            WHERE sr_code ILIKE %s
        """

        self.cur.execute(search_query, (sr_code,))
        return self.cur.fetchone()

    def remove_participant(self, event_id, sr_code):
        delete_query = """
            DELETE FROM registration
            WHERE event_id = %s
                AND sr_code = %s
        """

        try:
            self.cur.execute(delete_query, (event_id, sr_code))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e

reg_dao = RegDao()