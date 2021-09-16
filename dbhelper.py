import sqlite3
from tkinter.constants import E

class Database():
    def __init__(self, name='budget.db'):
        self.con = sqlite3.connect(name)
        self.cur = self.con.cursor()
        # if the table has not been created yet, create it
        self.create_db()
        self.active_budget = ''
        
    def create_db(self):
        # the name will be unique since there won't be much data, but still have an id
        try:
            # create budget table
            command = ('''CREATE TABLE IF NOT EXISTS budget (
                        budget_id integer primary key autoincrement,
                        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        Name text,
                        Account text,
                        Expenses text
                        );''')
            self.cur.execute(command)
            self.con.commit()
            
            # create projection table
            command = ('''CREATE TABLE IF NOT EXISTS projections (
                        projections_id integer primary key autoincrement,
                        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        Name text,
                        Events text
                        );''')
            self.cur.execute(command)
            self.con.commit()
            
            # create table to link the two tables
            command = ('''CREATE TABLE IF NOT EXISTS link (
                        projections_id int,
                        budget_id int
                        );''')
            self.cur.execute(command)
            self.con.commit()
        except Exception as e:
            print(e)
            return False
        
    def create_budget(self, name, accounts):
        """Inserts row into budget table with new budget
        Inputs:
            name (str): name of budget
            accoutns (str): a str which contains list of dictionaries
        """
        try:
            # check if name already exists
            command = "SELECT EXISTS(SELECT 1 FROM budget WHERE Name=?);"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()
            if results[0][0] == 1:
                return False
            
            # now that it does not exist, create it
            command = ('''INSERT INTO budget(Name, Account)
                        VALUES (?, ?);''')
            values = (name, accounts)
            self.cur.execute(command, values)
            self.con.commit()
        except Exception as e:
            print(e)
            return False
        return True
        
    def update_expenses(self, name, expenses):
        """Inserts expenses into budget
        inputs:
            name (str): name of budget
            expenses (str): list of expenses
        """
        try:
            command = ('UPDATE budget SET Expenses = ? WHERE Name = ?;')
            self.cur.execute(command, (expenses, name))
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_by_name(self, name):
        try:
            command = "SELECT * FROM budget WHERE Name = ?"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()[0]
            return results
        except Exception as e:
            print(e)
            return False
            
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