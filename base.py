import sqlite3 as sql3

class DataBase(object):
    def __init__(self, file):
        self.file = file
        
    def connect(self):
        return sql3.connect(self.file)
    
    def close(self, conn):
        return conn.close()
    
    def commit(self, conn):
        return conn.commit()
        
    def cursor(self):
        return self.connect().cursor()
        
    def commit_close(self, conn):
        conn.commit()
        conn.close()
        
    def addTableUsers(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_created_at
        AFTER INSERT ON Users
        BEGIN
        UPDATE Users SET created_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
        END;
        ''')
        self.commit_close(conn)

    def deleteTable(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
        DROP TABLE IF EXISTS Users
        ''')
        self.commit_close(conn)
        
    def addUser(self, username, mail, age):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', 
            (username, mail, age)
            )
        self.commit_close(conn)
    
    def getUser(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users')
        users = cursor.fetchall()
        for user in users:
            print(user)    

db = DataBase("my_database.db")
# db.addTableUsers()
# db.deleteTable()
db.addTableUsers()
db.addUser('ilat', 'ilfat@mail.ru', '31')
db.getUser()
# db.deleteTable()
