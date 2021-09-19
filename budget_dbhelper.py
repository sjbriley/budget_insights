"""dbhelper allows user to connect to Database and make
changes to budget.db
"""
import sqlite3
import sys
import os
import json

class BudgetDatabase():
    """Allows user to connect to database using sqlite and
    make changes or get strored information"""
    def __init__(self, name='budget.db'):
        self.con = sqlite3.connect(name)
        self.cur = self.con.cursor()
        self.create_db()

    def create_db(self):
        """Executes command to create budgets if not exists"""
        try:
            # create budgets table
            command = ('''CREATE TABLE IF NOT EXISTS budgets (
                        Budget_id integer primary key autoincrement,
                        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        Name text,
                        Account text,
                        Expenses text
                        );''')
            self.cur.execute(command)
            self.con.commit()
            return True
        except Exception as exception:
            exception_handler()
            return False

    def create_budget(self, name, accounts):
        """Inserts row into budget table with new budget
        Parameters:
            name (str): name of budget
            accoutns (str): a str which contains list of dictionaries
        """
        try:
            # check if name already exists
            command = "SELECT EXISTS(SELECT 1 FROM budgets WHERE Name=?);"
            accounts = json.dumps(accounts)
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()
            if results[0][0] == 1:
                return False
            # now that it does not exist, create it
            command = ('''INSERT INTO budgets(Name, Account)
                        VALUES (?, ?);''')
            values = (name, accounts)
            self.cur.execute(command, values)
            self.con.commit()
        except Exception as exception:
            exception_handler()
            return False
        return True

    def get_id_by_name(self, name):
        """Returns id of a budget by it's name
        Parameters:
            name (str): name of budget
        Returns:
            results (str): the ID associated with the budget
        """
        try:
            command = "SELECT Budget_id FROM budgets WHERE Name = ?"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()[0][0]
            return results
        except Exception as exception:
            exception_handler()
            return False

    def update_expenses(self, name, expenses):
        """Inserts expenses into budget
        inputs:
            name (str): name of budget
            expenses (str): list of expenses
        """
        try:
            expenses = json.dumps(expenses)
            command = 'UPDATE budgets SET Expenses = ? WHERE Name = ?;'
            self.cur.execute(command, (expenses, name))
            self.con.commit()
            return True
        except Exception as exception:
            exception_handler()
            return False

    def get_by_name(self, name):
        """Searches table budgets by name
        parameters:
            name (str): name of budget
        returns:
            results (list): information associated with budget"""
        try:
            command = "SELECT * FROM budgets WHERE Name = ?"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()[0]
            return results
        except Exception as exception:
            exception_handler()
            return False

    def get_all_budgets(self):
        """Returns results (list) containing all budgets"""
        command = "SELECT * FROM budgets"
        self.cur.execute(command)
        results = self.cur.fetchall()
        return results

    def get_accounts_by_name(self, name):
        """Returns accounts for a budget
        parameters:
            name (str): name of budget
        returns
            results (list): accounts
        """
        try:
            command = "SELECT Account FROM budgets where Name = ?"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()
            return results[0][0]
        except Exception as exception:
            exception_handler()
            return False

    def get_expenses_by_name(self, name):
        """Returns expenses for a budget
        parameters:
            name (str): name of budget
        returns
            results (list): expenses
        """
        try:
            command = "SELECT Expenses FROM budgets where Name = ?"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()
            return results[0][0]
        except Exception as exception:
            exception_handler()
            return False

    def update_accounts(self, name, accounts):
        """Updates accounts for an existing budget
        parameters:
            name (str): name of budget
            accounts (str): new accounts
        """
        try:
            accounts = json.dumps(accounts)
            command = """UPDATE budgets SET Account = ?, Name = ?;"""
            self.cur.execute(command, (accounts, name))
            self.con.commit()
            return True
        except Exception as exception:
            exception_handler()
            return False

    def delete_table(self):
        """Deletes entire tables from database"""
        command = "DROP TABLE budgets"
        self.cur.execute(command)
        self.con.commit()

    def __del__(self):
        """Closes the database on deletion of instance"""
        self.con.close()

def exception_handler():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)