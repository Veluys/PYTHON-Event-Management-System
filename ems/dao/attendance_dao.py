import psycopg2

from ems.model.registration import Registration


class AttendDao:
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()

    @staticmethod
    def _get_base_view_query():
        return """
            
        """

    def view_attendance(self, event_id, attended):
        view_query = """
            SELECT
                sr_code,
                dept_shortname,
                year_level,
                full_name
            FROM participant_details
            WHERE event_id = %s
        """

        if attended is not None:
            if attended:
                view_query += "\nAND attended ILIKE 'Yes'"
            else:
                view_query += "\nAND attended ILIKE 'No'"

        view_query += " ORDER BY year_level, dept_shortname, full_name; "

        self.cur.execute(view_query, (event_id,))
        return self.cur.fetchall()

    def is_attendee(self, reg_record : Registration):
        check_query = """
            SELECT attended
            FROM registration
            WHERE event_id = %s
                AND sr_code = %s
        """

        self.cur.execute(check_query, (reg_record.event_id, reg_record.sr_code))
        return self.cur.fetchone()[0]

    def update_attendance(self, reg_record : Registration, setPresent):
        update_query = """
            UPDATE registration
            SET attended = %s
            WHERE event_id = %s
                AND sr_code = %s
        """

        try:
            self.cur.execute(update_query, (setPresent, reg_record.event_id, reg_record.sr_code))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e