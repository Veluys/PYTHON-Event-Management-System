import psycopg2

import ems.model.dbconnection as dbconn
import ems.model.student as student_model
import ems.view.displayer as displayer

class StudentDao:
    def __init__(self):
        try:
            self.conn = dbconn.create_connection()
            self.cur = self.conn.cursor()
        except Exception as err:
            print("Database connection can't be established! Program would be terminated.")
            displayer.show_error(err)
            exit(1)

    def student_exists(self, sr_code):
        search_query = """
            SELECT *
            FROM students
            WHERE sr_code ILIKE %s
        """

        self.cur.execute(search_query, (sr_code,))
        return bool(self.cur.fetchone())


stud_dao = StudentDao()