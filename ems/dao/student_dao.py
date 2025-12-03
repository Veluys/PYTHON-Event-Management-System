class StudentDao:
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()

    def student_exists(self, sr_code):
        search_query = """
            SELECT
                CASE
                    WHEN COUNT(*) > 0 THEN true
                    ELSE false
                END as exists
            FROM students
            WHERE sr_code ILIKE %s
        """

        self.cur.execute(search_query, (sr_code,))
        return self.cur.fetchone()[0]