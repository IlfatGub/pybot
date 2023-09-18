import sqlite3 as sql3
import time

class DataBase(object):
    # debetor = None
    # summ = None
    # user_ct_id = None
    
    def __init__(self, file, debtor = None, summ = None, user_ct_id = None):
        self.file = file
        self.debtor = debtor
        self.summ = summ
        self.user_ct_id = user_ct_id
        
    def setDebtor(self, value):
        self.debtor = value
    
    def setSumm(self, value):
        self.summ = value

    def setIserCtId(self, value):
        self.user_ct_id = value
        
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
        
    def query(self, sql, var):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, var)
        self.commit_close(conn)

    def query_select(self, sql, var = None):
        conn = self.connect()
        cursor = conn.cursor()
        if not var:
            cursor.execute(sql)
        else:
            cursor.execute(sql, var)
        return cursor.fetchall()
        
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
        UPDATE debtor_history SET date_ct = CURRENT_TIMESTAMP WHERE id = NEW.id;
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

    def existsDebtor(self):
        e = self.query_select('SELECT COUNT(*) FROM debtor WHERE name = ?', [self.debtor])
        return e[0]

    def addDebtor(self):
        self.query('INSERT INTO debtor (name, summ) VALUES (?, ?)', [self.debtor, self.summ])

    def addDebtDebtor(self):
        self.query('UPDATE debtor SET summ = summ + ? WHERE name = ?' , [self.summ, self.debtor])
        
    def addDebtDebtorHistory(self):
        res = self.query_select('SELECT id, summ FROM debtor WHERE name = ?', [self.debtor])
        print(type(res))
        if len(res) > 1:
            self.query(
                'INSERT INTO debtor_history (user_ct_id, debtor_id, summ, total_summ) VALUES (?, ?, ?, ?)', 
                [self.user_ct_id, res[0], self.summ,  res[1]])
        
    # def addDebtDebtorHistory(self, debtor, summ):
    #     conn = self.connect()
    #     cursor = conn.cursor()
    #     cursor.execute('INSERT INTO debtor (user_ct_id, summ) VALUES (?, ?)', (debtor, summ))
    #     self.commit_close(conn)
    #     cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS debtor_history (
    #     id INTEGER PRIMARY KEY,
    #     user_ct_id INTEGER NOT NULL,
    #     debtor_id INTEGER NOT NULL,
    #     summ INTEGER NOT NULL,
    #     datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    #     total_summ INTEGER NOT NULL
    #     )
    #     ''')

    def getDebtorSumm(self):
        if self.existsDebtor() == 0:
            return 0
        else: 
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM debtor WHERE name = ?', (self.debtor, ))
            return cursor.fetchone()[2]
    
    def getDebtorList(self):
       return self.query_select('SELECT id, name FROM debtor')
        
    def getDebetorId(self):
        return 0
    
    def debt(self):
        if self.existsDebtor() == 0:
            self.addDebtor()
        else:
            self.addDebtDebtor()
            self.addDebtDebtorHistory()
            
       
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
# db.createTableDebtor()
# db.debtor("Сергей", -1500)
# db.getDebtorSumm("Сергей")
# db.addUser('ilat', 'ilfat@mail.ru', '31')
# db.getUser()
# db.deleteTable()
