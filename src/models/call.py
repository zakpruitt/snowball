import sqlite3
import threading


class Call:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(
            './resources/app/data/snowball.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.lock = threading.Lock()
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
        try:
            self.lock.acquire(True)
            self.cursor.execute('''
                                INSERT OR IGNORE INTO calls VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', call)
            self.conn.commit()
        finally:
            self.lock.release()

    def delete(self, date, sup_num):
        try:
            self.lock.acquire(True)
            self.cursor.execute(f'''
                                DELETE FROM calls 
                                WHERE date_created = '{date}'
                                AND support_number = '{sup_num}'  
                                ''')
            self.conn.commit()
        finally:
            self.lock.release()

    def read(self):
        try:
            self.lock.acquire(True)
            self.cursor.execute('''
                                SELECT * FROM calls
                                ''')
            return self.cursor.fetchall()
        finally:
            self.lock.release()

    def get_total_calls_and_email_count_by_employee(self, start=None, end=None, sub_dept = None):
        try:
            self.lock.acquire(True)
            if start == None and end == None and sub_dept==None:
                self.cursor.execute('''
                                    SELECT employees.name,
                                    count (*) as 'Calls and Emails', 
                                    SUM(CASE WHEN calls.email = 0 THEN 1 ELSE 0 END) "Calls Count",
                                    SUM(CASE WHEN calls.email = 1 THEN 1 ELSE 0 END) "Emails Count"
                                    FROM calls
                                    LEFT JOIN employees ON calls.employee_id = employees.id
                                    WHERE calls.sup_code != 'W' or 'N' 
                                    GROUP BY employees.name
                                    ''')
                return self.cursor.fetchall()
            elif start == None and end == None:
                self.cursor.execute(f'''
                                    SELECT employees.name,
                                    count (*) as 'Calls and Emails', 
                                    SUM(CASE WHEN calls.email = 0 THEN 1 ELSE 0 END) "Calls Count",
                                    SUM(CASE WHEN calls.email = 1 THEN 1 ELSE 0 END) "Emails Count"
                                    FROM calls
                                    LEFT JOIN employees ON calls.employee_id = employees.id
                                    WHERE employees.sub_dept = '{sub_dept}'
                                    AND calls.sup_code != 'W' or 'N' 
                                    GROUP BY employees.name
                                    ''')
                return self.cursor.fetchall()
            else:
                self.cursor.execute(f'''
                                    SELECT name,
                                    count (*) as 'Calls and Emails', 
                                    SUM(CASE WHEN calls.email = 0 THEN 1 ELSE 0 END) "Calls Count",
                                    SUM(CASE WHEN calls.email = 1 THEN 1 ELSE 0 END) "Emails Count"
                                    FROM calls
                                    LEFT JOIN employees ON calls.employee_id = employees.id
                                    WHERE date_created BETWEEN '{start}' and '{end}'
                                    AND employees.sub_dept = '{sub_dept}'
                                    AND calls.sup_code != 'W' or 'N' 
                                    GROUP BY employees.name
                                    ''')
                return self.cursor.fetchall()
        finally:
            self.lock.release()

    def get_calls_and_email_count_by_sub_dept(self, start=None, end=None):
        try:
            self.lock.acquire(True)
            if start == None and end == None:
                self.cursor.execute('''
                                    SELECT strftime('%m', date_created) AS month, sub_dept, count(sub_dept)
                                    FROM calls
                                    WHERE calls.sup_code != 'W' or 'N' 
                                    GROUP BY sub_dept, strftime('%m', date_created)
                                    ''')
                return self.cursor.fetchall()
        finally:
            self.lock.release()

    def get_total_calls_emails_counts(self, start=None, end=None):
        try:
            self.lock.acquire(True)
            if start == None and end == None:
                self.cursor.execute('''
                                    SELECT strftime('%m-%Y', date_created) AS month,
                                        COUNT(*) AS Total,
                                        SUM(CASE WHEN calls.email = 0 THEN 1 ELSE 0 END) "Calls Count",
                                        SUM(CASE WHEN calls.email = 1 THEN 1 ELSE 0 END) "Emails Total"
                                    FROM calls
                                    WHERE calls.sup_code != 'W' or 'N'
                                    GROUP BY strftime('%m%Y', date_created)
                                    Order BY strftime('%Y-%m', date_created);
                                    ''')
                return self.cursor.fetchall()
        finally:
            self.lock.release()

    def get_unregistered_employees(self):
        try:
            self.lock.acquire(True)
            self.cursor.execute('''
                                SELECT DISTINCT calls.original_user
                                FROM calls
                                LEFT JOIN employees on calls.original_user = employees.name
                                WHERE employees.name IS NULL
                                ''')
            return self.cursor.fetchall()
        finally:
            self.lock.release()

    # table

    def get_total_immediate_and_later_counts(self, start=None, end=None, sub_dept=None):
        try:
            self.lock.acquire(True)
            if start == None and end == None and sub_dept == None:
                self.cursor.execute('''
                                    SELECT 
                                        COUNT(*) AS Total,
                                        SUM(CASE WHEN employees.id = calls.employee_id THEN 1 ELSE 0 END) "Immediate Count",
                                        SUM(CASE WHEN employees.id != calls.employee_id THEN 1 ELSE 0 END) "Later Count"
                                    FROM calls
                                    LEFT JOIN employees ON calls.original_user = employees.name
                                    WHERE calls.email = 0
                                    AND calls.sup_code != 'W' or 'N' 
                                    ''')
                return self.cursor.fetchall()
            elif start == None and end == None and sub_dept != None:
                self.cursor.execute(f'''
                                    SELECT 
                                        COUNT(*) AS Total,
                                        SUM(CASE WHEN employees.id = calls.employee_id THEN 1 ELSE 0 END) "Immediate Count",
                                        SUM(CASE WHEN employees.id != calls.employee_id THEN 1 ELSE 0 END) "Later Count"
                                    FROM calls
                                    LEFT JOIN employees ON calls.original_user = employees.name
                                    WHERE calls.email = 0
                                    AND employees.sub_dept = "{sub_dept}"
                                    AND calls.sup_code != 'W' or 'N' 
                                    ''')
                return self.cursor.fetchall()
            else:
                self.cursor.execute(f'''
                                    SELECT 
                                        COUNT(*) AS Total,
                                        SUM(CASE WHEN employees.id = calls.employee_id THEN 1 ELSE 0 END) "Immediate Count",
                                        SUM(CASE WHEN employees.id != calls.employee_id THEN 1 ELSE 0 END) "Later Count"
                                    FROM calls
                                    LEFT JOIN employees ON calls.original_user = employees.name
                                    WHERE calls.email = 0
                                    AND employees.sub_dept = "{sub_dept}"
                                    AND calls.date_created BETWEEN '{start}' and '{end}'
                                    AND calls.sup_code != 'W' or 'N' 
                                    ''')
                return self.cursor.fetchall()
        finally:
            self.lock.release()

    def get_immediate_and_later_count_per_employee(self, start=None, end=None, sub_dept=None):
        try:
            self.lock.acquire(True)
            if start == None and end == None and sub_dept == None:
                self.cursor.execute('''
                                    SELECT 
                                        count_emp.name,
                                        COUNT(*) AS Total,
                                        SUM(CASE WHEN count_emp.id = org_emp.id THEN 1 ELSE 0 END) "Immediate Count",
                                        SUM(CASE WHEN count_emp.id != org_emp.id THEN 1 ELSE 0 END) "Later Count"
                                    FROM calls
                                    LEFT JOIN employees AS org_emp ON calls.original_user = org_emp.name
                                    LEFT JOIN employees AS count_emp ON calls.employee_id = count_emp.id
                                    WHERE calls.email = 0
                                    AND calls.sup_code != 'W' or 'N'
                                    GROUP BY count_emp.name
                                    ''')
                return self.cursor.fetchall()
            elif start == None and end == None and sub_dept != None:
                self.cursor.execute(f'''
                                    SELECT 
                                        count_emp.name,
                                        COUNT(*) AS Total,
                                        SUM(CASE WHEN count_emp.id = org_emp.id THEN 1 ELSE 0 END) "Immediate Count",
                                        SUM(CASE WHEN count_emp.id != org_emp.id THEN 1 ELSE 0 END) "Later Count"
                                    FROM calls
                                    LEFT JOIN employees AS org_emp ON calls.original_user = org_emp.name
                                    LEFT JOIN employees AS count_emp ON calls.employee_id = count_emp.id
                                    WHERE calls.email = 0
                                    AND count_emp.sub_dept = '{sub_dept}'
                                    AND calls.sup_code != 'W' or 'N'
                                    GROUP BY count_emp.name
                                    ''')
                return self.cursor.fetchall()
            else:
                self.cursor.execute(f'''
                                    SELECT 
                                        count_emp.name,
                                        COUNT(*) AS Total,
                                        SUM(CASE WHEN count_emp.id = org_emp.id THEN 1 ELSE 0 END) "Immediate Count",
                                        SUM(CASE WHEN count_emp.id != org_emp.id THEN 1 ELSE 0 END) "Later Count"
                                    FROM calls
                                    LEFT JOIN employees AS org_emp ON calls.original_user = org_emp.name
                                    LEFT JOIN employees AS count_emp ON calls.employee_id = count_emp.id
                                    WHERE calls.email = 0
                                    AND count_emp.sub_dept = '{sub_dept}'
                                    AND calls.date_created BETWEEN '{start}' and '{end}' 
                                    AND calls.sup_code != 'W' or 'N'
                                    GROUP BY count_emp.name
                                    ''')
                return self.cursor.fetchall()
        finally:
            self.lock.release()

    def get_total_email_counts(self, start=None, end=None, sub_dept=None):
        try:
            self.lock.acquire(True)
            if start == None and end == None and sub_dept == None:
                self.cursor.execute('''
                                    SELECT COUNT(*) as "Email Total"
                                    FROM calls
                                    LEFT JOIN employees ON calls.last_user = employees.name
                                    WHERE calls.email = 1
                                    AND calls.sup_code != 'W' or 'N'
                                    ''')
                return self.cursor.fetchall()
            elif start == None and end == None and sub_dept != None:
                self.cursor.execute(f'''
                                    SELECT COUNT(*) as "Email Total"
                                    FROM calls
                                    LEFT JOIN employees ON calls.last_user = employees.name
                                    WHERE calls.email = 1
                                    AND employees.sub_dept = "{sub_dept}"
                                    AND calls.sup_code != 'W' or 'N'
                                    ''')
                return self.cursor.fetchall()
            else:
                self.cursor.execute(f'''
                                    SELECT COUNT(*) as "Email Total"
                                    FROM calls
                                    LEFT JOIN employees ON calls.last_user = employees.name
                                    WHERE calls.email = 1
                                    AND employees.sub_dept = "{sub_dept}"
                                    AND calls.date_created BETWEEN '{start}' and '{end}'
                                    AND calls.sup_code != 'W' or 'N'
                                    ''')
                return self.cursor.fetchall()
        finally:
            self.lock.release()

    def get_email_counts_per_employee(self, start=None, end=None, sub_dept=None):
        try:
            self.lock.acquire(True)
            if start == None and end == None and sub_dept == None:
                self.cursor.execute('''
                                    SELECT count_emp.name, COUNT(*)
                                    FROM calls
                                    LEFT JOIN employees AS org_emp ON calls.original_user = org_emp.name
                                    LEFT JOIN employees AS count_emp ON calls.employee_id = count_emp.id
                                    WHERE calls.email = 1
                                    AND calls.sup_code != 'W' or 'N' 
                                    GROUP BY count_emp.name
                                    ''')
                return self.cursor.fetchall()
            elif start == None and end == None and sub_dept != None:
                self.cursor.execute(f'''
                                    SELECT count_emp.name, COUNT(*)
                                    FROM calls
                                    LEFT JOIN employees AS org_emp ON calls.original_user = org_emp.name
                                    LEFT JOIN employees AS count_emp ON calls.employee_id = count_emp.id
                                    WHERE calls.email = 1
                                    AND count_emp.sub_dept = '{sub_dept}'
                                    AND calls.sup_code != 'W' or 'N' 
                                    GROUP BY count_emp.name
                                    ''')
                return self.cursor.fetchall()
            else:
                self.cursor.execute(f'''
                                    SELECT count_emp.name, COUNT(*)
                                    FROM calls
                                    LEFT JOIN employees AS org_emp ON calls.original_user = org_emp.name
                                    LEFT JOIN employees AS count_emp ON calls.employee_id = count_emp.id
                                    WHERE calls.email = 1
                                    AND count_emp.sub_dept = '{sub_dept}'
                                    AND calls.date_created BETWEEN '{start}' and '{end}'
                                    AND calls.sup_code != 'W' or 'N' 
                                    GROUP BY count_emp.name
                                    ''')
                return self.cursor.fetchall()
        finally:
            self.lock.release()

    def close(self):
        self.cursor.close()
        self.conn.close()
