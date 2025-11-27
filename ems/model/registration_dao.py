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


reg_dao = RegDao()