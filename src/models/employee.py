import sqlite3


class Employee:
    def __init__(self):
        self.conn = sqlite3.connect('data/snowball.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS employees(
                                    id TEXT PRIMARY KEY, 
                                    name TEXT, 
                                    sub_dept TEXT,
                                    color TEXT)
                            ''')

    def insert(self, employee):
        self.cursor.execute('''
                            INSERT OR IGNORE INTO employees VALUES(?, ?, ?, ?)
                            ''', employee)
        self.conn.commit()

    def read(self):
        self.cursor.execute('''
                            SELECT * FROM employees
                            ''')
        # for row in self.cursor:
        #     print(row)
        return self.cursor.fetchall()

    def find_employee(self, name):
        name = name.upper()
        self.cursor.execute(f'''
                            SELECT * 
                            FROM employees
                            WHERE employees.name = "{name}"
                            ''')
        # for row in self.cursor:
        #     print(row)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def build_employee(self, employee_id, name, sub_dept):
        return tuple(employee_id, name, sub_dept)