import sqlite3

class Database():
    
    def __init__(self, db_file):
        self.connection= sqlite3.connect(db_file)
        self.cursor= self.connection.cursor()
        
    def add(self, user_id, dt, gmt, text=None):
        with self.connection:
            return self.cursor.execute("INSERT INTO info (user_id, date, text, gmt) VALUES (?, ?, ?, ?)", (user_id, dt, text, gmt, ))
    
    def delete(self, user_id, dt):
        with self.connection:
            return self.cursor.execute("DELETE FROM info WHERE user_id= ? and date= ?", (user_id, dt, ))
    
    def get_info(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM info").fetchall()
    
    def alarm(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE info SET attempts = attempts + 5 WHERE user_id= ?", (user_id, ))
    