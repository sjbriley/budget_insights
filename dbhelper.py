import sqlite3

class Database():
    def __init__(self, name='budget.db'):
        self.con = sqlite3.connect(name)
        self.cur = self.con.cursor()
        # if the table has not been created yet, create it
        self.create_db()
        
    def create_db(self):
        # the name will be unique since there won't be much data, but still have an id
        command = ('''CREATE TABLE IF NOT EXISTS budget (
                    id integer primary key autoincrement,
                    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    Name text,
                    Balance int
                    );''')
        self.cur.execute(command)
        self.con.commit()
        
    def create_budget(self, name, balance):
        try:
            # check if name already exists
            command = "SELECT EXISTS(SELECT 1 FROM budget WHERE Name=?);"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()
            if results[0][0] == 1:
                return False
            
            # now that it does not exist, create it
            command = ('''INSERT INTO budget(Name, Balance)
                        VALUES (?, ?);''')
            values = (name, balance)
            self.cur.execute(command, values)
            self.con.commit()
        except Exception as e:
            print(e)
            return False
        return True
        
    def get_by_name(self, name):
        command = "SELECT * FROM budget WHERE Name = ?"
        self.cur.execute(command, (name,))
        results = self.cur.fetchall()
        print(results)
        
    def get_by_id(self, id):
        pass
        
    def get_all(self):
        command = "SELECT * FROM budget"
        self.cur.execute(command)
        results = self.cur.fetchall()
        return results
        
    def delete_table(self):
        command = "DROP TABLE budget"
        self.cur.execute(command)
        self.con.commit()
        
    def __del__(self):
        # on close of application, be sure the sqlite file is also closed
        self.con.close()
        
        
"""
from dbhelper import *  
d=Database()
d.create_db()
"""