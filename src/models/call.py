import sqlite3


class Call:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('data/snowball.db', check_same_thread=False)
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

    def close(self):
        self.cursor.close()
        self.conn.close()
