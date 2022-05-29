import sqlite3
import threading


class Employee:
    def __init__(self):
        self.conn = sqlite3.connect('./data/snowball.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.lock = threading.Lock()
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
        try:
            self.lock.acquire(True)
            self.cursor.execute('''
                                INSERT OR IGNORE INTO employees VALUES(?, ?, ?, ?)
                                ''', employee)
            self.conn.commit()
        finally:
            self.lock.release()

    def delete(self, id):
        try:
            self.lock.acquire(True)
            self.cursor.execute(f'''
                                DELETE FROM employees
                                WHERE employees.id = "{id}"
                                ''')
            self.conn.commit()
        finally:
            self.lock.release()

    def read(self):
        try:
            self.lock.acquire(True)
            self.cursor.execute('''
                                SELECT * FROM employees
                                ''')
            return self.cursor.fetchall()
        finally:
            self.lock.release()

    def find_employee(self, name):
        try:
            self.lock.acquire(True)
            name = name.upper()
            self.cursor.execute(f'''
                                SELECT * 
                                FROM employees
                                WHERE employees.name = "{name}"
                                ''')
            return self.cursor.fetchall()
        finally:
            self.lock.release()

    def get_color_by_name(self, name):
        try:
            self.lock.acquire(True)
            name = name.upper()
            self.cursor.execute(f'''
                                SELECT * 
                                FROM employees
                                WHERE employees.name = "{name}"
                                ''')
            return self.cursor.fetchone()[3]
        finally:
            self.lock.release()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def build_employee(self, employee_id, name, sub_dept):
        return tuple(employee_id, name, sub_dept)