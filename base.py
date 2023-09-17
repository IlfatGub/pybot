import sqlite3 as sql3

class DataBase(object):
    def __init__(self, file):
        self.file = file
        # self.debetor = debetor
        # self.summ = summ
        
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
        
    def createTableDebtor(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS debtor_history (
        id INTEGER PRIMARY KEY,
        user_ct_id INTEGER NOT NULL,
        debtor_id INTEGER NOT NULL,
        summ INTEGER NOT NULL,
        datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_summ INTEGER NOT NULL
        )
        ''')
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_datetime
        AFTER INSERT ON debtor_history
        BEGIN
        UPDATE Debtor SET datetime = CURRENT_TIMESTAMP WHERE id = NEW.id;
        END;
        ''')
        self.commit_close(conn)
        
        
    def createTableDebtorHistoru(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS debtor (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        summ INTEGER NOT NULL
        )
        ''')
        self.commit_close(conn)

    def existsDebtor(self, debtor):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM debtor WHERE name = ?', (debtor,))
        return cursor.fetchone()[0]

    def addDebtor(self, debtor, summ):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO debtor (name, summ) VALUES (?, ?)', (debtor, summ))
        self.commit_close(conn)

    def addDebtDebtor(self, debtor, summ):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('UPDATE debtor SET summ = summ + ? WHERE name = ?' , (summ, debtor))
        self.commit_close(conn)

    def getDebtorSumm(self, debtor):
        if self.existsDebtor(debtor) == 0:
            return 0
        else: 
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM debtor WHERE name = ?', (debtor,))
            return cursor.fetchone()[2]
        
    def debtor(self, debtor, summ):
        if self.existsDebtor(debtor) == 0:
            self.addDebtor(debtor, summ)
        else:
            self.addDebtDebtor(debtor, summ)
            
       
    def deleteTable(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
        DROP TABLE IF EXISTS Users
        ''')
        self.commit_close(conn)
        
    def getUser(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users')
        users = cursor.fetchall()
        users_list = []
        for user in users:
            user_dict = {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'age': user[3],
                'created_at': user[4],
            }
            users_list.append(user_dict)
        return users_list
        # for user in users:
            # print(user)    

# db = DataBase("my_database.db")
# db.addTableUsers()
# db.deleteTable()
# db.createTableDebtor()
# db.createTableDebtorHistoru()
# db.debtor("Сергей", -1500)
# db.getDebtorSumm("Сергей")
# db.addUser('ilat', 'ilfat@mail.ru', '31')
# db.getUser()
# db.deleteTable()
