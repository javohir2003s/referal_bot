import sqlite3 

class DataBaseConf:
    def __init__(self, db_file="db.sqlite3"):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        
    def set_db_tables(self):
        with self.connection:
            self.cursor.execute(
                    "CREATE TABLE IF NOT EXISTS users("
                    "id INTEGER PRIMARY KEY,"
                    "user_id INTEGER NOT NULL,"
                    "full_name CHAR(255),"
                    "refer_id INTEGER,"
                    "flag CHAR(5))"
                )
            
create_table = DataBaseConf()

dbcreate = DataBaseConf()
dbcreate.set_db_tables()
         
class DataBase:
    def __init__(self, db_file) -> None:
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        
    def add_user(self, user_id, refer_id, full_name, flag):
        with self.connection:
            self.cursor.execute(f"INSERT INTO users (user_id, full_name, refer_id, flag) VALUES(?, ?, ?, ?)",
                (user_id, full_name, refer_id, flag)             
            )
    
    def update_user(self, user_id):
        with self.connection:
            self.cursor.execute(f"UPDATE users SET flag = 'True' WHERE user_id = (?)", (user_id,))
    
    def get_user(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM users WHERE user_id = (?)", (user_id,))
            result = result.fetchone()
            result = result if result is not None else 0
            return result

    def get_user_ball(self, user_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT COUNT(refer_id) FROM users WHERE refer_id = (?) GROUP BY flag HAVING flag= 'True'", (user_id,))
            result = result.fetchall()
            result = result if result is not None else 0
            return result[0][0]