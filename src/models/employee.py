import sqlite3


class Employee:
    def __init__(self):
        self.conn = sqlite3.connect('data/snowball.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS employees(
                                    id TEXT PRIMARY KEY, 
                                    name TEXT, 
                                    sub_dept TEXT)
                            ''')

    def insert(self, employee):
        self.cursor.execute('''
                            INSERT OR IGNORE INTO employees VALUES(?, ?, ?)
                            ''', employee)
        self.conn.commit()

    def read(self):
        self.cursor.execute('''
                            SELECT * FROM employees
                            ''')
        # for row in self.cursor:
        #     print(row)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()