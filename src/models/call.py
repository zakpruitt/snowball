import sqlite3


class Call:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('data/snowball.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS calls(
                                    support_number TEXT PRIMARY KEY, 
                                    date_created TEXT, 
                                    sup_code TEXT,
                                    sub_dept TEXT,
                                    email TEXT,
                                    employee_id TEXT REFERENCES employees(id), 
                                    last_user TEXT REFERENCES employees(name), 
                                    original_user REFERENCES employees(name), 
                                    time_last_changed TEXT)
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

    def close(self):
        self.cursor.close()
        self.conn.close()