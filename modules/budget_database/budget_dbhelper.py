"""dbhelper allows user to connect to Database and make
changes to budget.db
"""
import sqlite3
import sys
import os
import json
from typing import Union

# insert path two directories up (main project dir)
import os.path
sys.path.insert(0, os.path.join(__file__ ,"../.."))

class BudgetDatabase():
    """Allows user to connect to database using sqlite and
    make changes or get strored information"""
    def __init__(self, name: str = 'budget.db'):
        self.con = sqlite3.connect(name)
        self.cur = self.con.cursor()
        self.create_db()

    def create_db(self) -> bool:
        """Executes command to create budgets table if not exists
        
        Returns:
            bool: pass or fail
            
        """
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

    def create_budget(self, name: str, accounts: str) -> bool:
        """Inserts row into budget table with new budget
        
        Args:
            name (str): name of budget
            accounts (str): a str which contains list of dictionaries
            
        Returns:
            bool: pass or fail
            
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

    def get_id_by_name(self, name:str) -> Union[str, bool]:
        """Returns id of a budget by it's name
        
        Args:
            name (str): name of budget
            
        Returns:
            str | bool: the ID associated with the budget
            
        """
        try:
            command = "SELECT Budget_id FROM budgets WHERE Name = ?"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()[0][0]
            return results
        except Exception as exception:
            exception_handler()
            return False

    def update_expenses(self, name:str, expenses:str) -> bool:
        """Inserts expenses into the budget database
        
        Args:
            name (str): name of budget
            expenses (str): list of expenses
            
        Returns:
            bool: pass or fail
            
        """
        try:
            expenses = json.dumps(expenses)
            command = """UPDATE budgets SET Expenses = ? WHERE Name = ?;"""
            self.cur.execute(command, (expenses, name))
            self.con.commit()
            return True
        except Exception as exception:
            exception_handler()
            return False

    def get_by_name(self, name: str) -> Union[list, bool]:
        """Searches table budgets by name
        
        Args:
            name (str): name of budget
            
        Returns:
            list | bool: information associated with budget
            
        """
        try:
            command = "SELECT * FROM budgets WHERE Name = ?"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()[0]
            return results
        except Exception as exception:
            exception_handler()
            return False

    def get_all_budgets(self) -> list:
        """Returns every row contained in budgets table
        
        Returns:
            list: contains every row in budgets table
            
        """
        command = "SELECT * FROM budgets"
        self.cur.execute(command)
        results = self.cur.fetchall()
        return results

    def get_accounts_by_name(self, name:str) -> Union[list, bool]:
        """Returns accounts for a budget
        
        Args:
            name (str): name of budget
            
        Returns:
            list: account information associated with name
            
        """
        try:
            command = "SELECT Account FROM budgets where Name = ?"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()
            return results[0][0]
        except Exception as exception:
            exception_handler()
            return False

    def get_expenses_by_name(self, name:str) -> Union[list, bool]:
        """Returns expenses for a budget
        
        Args:
            name (str): name of budget
            
        Returns:
            list: expenses associated with name
            
        """
        try:
            command = "SELECT Expenses FROM budgets where Name = ?"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()
            return results[0][0]
        except Exception as exception:
            exception_handler()
            return False

    def update_accounts(self, name:str, accounts:str) -> bool:
        """Updates accounts for an existing budget
        
        Args:
            name (str): name of budget
            accounts (str): new accounts
            
        Returns:
            bool: pass or fail
            
        """
        try:
            accounts = json.dumps(accounts)
            command = """UPDATE budgets SET Account = ? WHERE Name = ?;"""
            self.cur.execute(command, (accounts, name))
            self.con.commit()
            return True
        except Exception as exception:
            exception_handler()
            return False

    def delete_table(self) -> bool:
        """Deletes entire tables from database
        
        Returns:
            bool: pass or fail
            
        """
        try:
            command = "DROP TABLE budgets"
            self.cur.execute(command)
            self.con.commit()
            return True
        except:
            return False

    def __del__(self) -> None:
        """Closes the database on deletion of instance"""
        self.con.close()

def exception_handler() -> None:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)