import psycopg2

from ems.model.registration import Registration


class RegDao:
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()

    def insert_participant(self, new_reg_record : Registration):
        insert_query = """
                INSERT INTO registration (event_id, sr_code)
                VALUES (%s, %s)
        """

        try:
            self.cur.execute(insert_query, (new_reg_record.event_id, new_reg_record.sr_code))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e

    def view_registered(self, event_id, sr_code=None):
        view_query = """
                SELECT
                    sr_code,
                    dept_shortname,
                    year_level,
                    full_name
                FROM participant_details
                WHERE event_id = %s
            """

        if sr_code is not None:
            view_query += """
                AND sr_code ILIKE %s;
            """
            self.cur.execute(view_query, (event_id, sr_code))
            return self.cur.fetchone()
        else:
            view_query += """
                ORDER BY year_level, dept_shortname, full_name;
            """
            self.cur.execute(view_query, (event_id,))
            return self.cur.fetchall()

    def is_registered(self, regRecord : Registration):
        search_query = """
            SELECT 
                CASE
                    WHEN COUNT(*) > 0 THEN true
                    ELSE false
                END as is_registered
            FROM registration
            WHERE event_id = %s
                AND sr_code ILIKE %s
        """

        self.cur.execute(search_query, (regRecord.event_id, regRecord.sr_code))
        return self.cur.fetchone()[0]

    def remove_participant(self, reg_record : Registration):
        delete_query = """
            DELETE FROM registration
            WHERE event_id = %s
                AND sr_code = %s
        """

        try:
            self.cur.execute(delete_query, (reg_record.event_id, reg_record.sr_code))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e

    def emptyCheck(self, event_id):
        select_query = """
                    SELECT COUNT(*)
                    FROM registration
                    WHERE event_id = %s
                """

        self.cur.execute(select_query, (event_id,))
        return self.cur.fetchone()[0] == 0