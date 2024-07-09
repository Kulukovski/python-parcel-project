import sqlite3
import os
import glob


class db:
    def __init__(self):
        self.dbname = 'images.db'
        self.conn = sqlite3.connect('images.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS image_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_directory TEXT NOT NULL,
                variable1 TEXT,
                variable2 TEXT
            )
        ''')
        self.conn.commit()

    def close_table(self):
        self.conn.close()

    def insert_data(self, image_directory, var1, var2):
        self.cursor.execute('''
            INSERT INTO image_data (image_directory, variable1, variable2)
            VALUES (?, ?, ?)
        ''', (image_directory, var1, var2))

        self.conn.commit()

    def retrieve_data(self):
        self.cursor.execute('SELECT * FROM image_data')
        rows = self.cursor.fetchall()

        for row in rows:
            print(row)

    def clear_data(self):
        self.cursor.execute('DELETE FROM image_data')
        print('Cleared Database')
        self.conn.commit()

    def clear_dir(self):
        pattern = os.path.join('img', '*')
        files = glob.glob(pattern)

        for f in files:
            if os.path.isfile(f):
                try:
                    os.remove(f)
                except PermissionError as e:
                    print(f"PermissionError: {e} - Could not delete file: {f}")
                except Exception as e:
                    print(f"Error: {e} - Could not delete file: {f}")

        print('Cleared Dir')

    def get_last_id(self):
        self.cursor.execute('SELECT MAX(id) FROM image_data')
        result = self.cursor.fetchone()
        return result[0] if result[0] is not None else 0

    def get_image_directories(self):
        self.cursor.execute('SELECT image_directory FROM image_data')
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def get_all_ids(self):
        self.cursor.execute('SELECT id FROM image_data')
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def delete_row_by_id(self, row_id):
        self.cursor.execute('DELETE FROM image_data WHERE id = ?', (row_id,))
        self.conn.commit()

    def validate_list(self):
        for each, i in zip(self.get_image_directories(), self.get_all_ids()):
            x, y = each.split('/')
            z = 0
            for eych in os.listdir('img'):
                if eych == y:
                    z = 1
            if z == 0:
                self.delete_row_by_id(i)
