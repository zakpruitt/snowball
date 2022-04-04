import sqlite3


class Call:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(
            'data/snowball.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS calls(
                                    support_number TEXT, 
                                    date_created TEXT, 
                                    sup_code TEXT,
                                    sub_dept TEXT,
                                    email TEXT,
                                    employee_id TEXT, 
                                    last_user TEXT, 
                                    original_user TEXT, 
                                    time_last_changed TEXT,
                                    FOREIGN KEY(employee_id) REFERENCES employees(id),
                                    PRIMARY KEY(support_number, date_created))
                            ''')

    def insert(self, call):
        self.cursor.execute('''
                            INSERT OR IGNORE INTO calls VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', call)
        self.conn.commit()

    def read(self):
        self.cursor.execute('''
                            SELECT * FROM calls
                            ''')
        return self.cursor.fetchall()

    def get_calls_and_email_count(self, start=None, end=None):
        if start == None and end == None:
            self.cursor.execute('''
                                SELECT strftime('%m', date_created), count (*) as 'Calls and Emails'
                                FROM calls
                                WHERE calls.sup_code != 'W' or 'N' 
                                GROUP BY strftime('%m', date_created)
                                ''')
            return self.cursor.fetchall()

        self.cursor.execute(f'''
                            SELECT strftime('%m', date_created), count (*) as 'Calls and Emails'
                            FROM calls
                            WHERE date_created BETWEEN '{start}' and '{end}'
                            AND calls.sup_code != 'W' or 'N' 
                            GROUP BY strftime('%m', date_created)
                            ''')
        return self.cursor.fetchall()
    
    def get_calls_and_email_count_by_sub_dept(self, start=None, end=None):
        if start == None and end == None:
            self.cursor.execute('''
                                SELECT strftime('%m', date_created) AS month, sub_dept, count(sub_dept)
                                FROM calls
                                WHERE calls.sup_code != 'W' or 'N' 
                                GROUP BY sub_dept, strftime('%m', date_created)
                                ''')
            return self.cursor.fetchall()

    def get_total_calls_emails_counts(self, start=None, end=None):
        if start == None and end == None:
            self.cursor.execute('''
                                SELECT strftime('%m', date_created) AS month,
                                COUNT(*) AS Total,
                                SUM(CASE WHEN calls.email = 0 THEN 1 ELSE 0 END) "Calls Count",
                                SUM(CASE WHEN calls.email = 1 THEN 1 ELSE 0 END) "Emails Total"
                                FROM calls
                                WHERE calls.sup_code != 'W' or 'N'
                                GROUP BY strftime('%m', date_created);
                                ''')
            return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
