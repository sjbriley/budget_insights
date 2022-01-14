"""dbhelper allows user to connect to Database and make
changes to budget.db
"""
import sqlite3
import json
import sys

# insert path two directories up (main project dir)
import os.path
sys.path.insert(0, os.path.join(__file__ ,"../.."))


class ProjectionsDatabase():
    """Allows user to connect to database using sqlite and
    make changes or get strored information"""
    def __init__(self, name='budget.db'):
        self.con = sqlite3.connect(name)
        self.cur = self.con.cursor()
        self.create_db()

    def create_db(self):
        """Executes command to create projections table if not exists"""
        try:
            # create projection table, linked to budgets
            # through Budget_id (one to many relation?)
            command = ('''CREATE TABLE IF NOT EXISTS projections (
                        Projections_id integer primary key autoincrement,
                        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        Name text,
                        Events text,
                        Budget_id int
                        );''')
            self.cur.execute(command)
            self.con.commit()
            return True
        except Exception as exception:
            print(exception)
            return False

    def create_projection(self, name, budget):
        """Inserts row into budget table with new budget
        Inputs:
            name (str): name of budget
            budget (str): a str which contains list of dictionaries
        """
        try:
            # check if name already exists
            command = "SELECT EXISTS(SELECT 1 FROM projections WHERE Name=?);"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()
            if results[0][0] == 1:
                return False
            budget_id = self.get_id_by_name(budget)
            # now that it does not exist, create it
            command = ('''INSERT INTO projections(Name, Budget_id)
                        VALUES (?, ?);''')
            values = (name, int(budget_id))
            self.cur.execute(command, values)
            self.con.commit()
        except Exception as exception:
            print(exception)
            return False
        return True

    def insert_event(self, name, events):
        """Inserts into events column in table projections
        Parameters:
            name (str): name of budget
            events (str): json dumps of events
        """
        try:
            # events = json.load(events)
            command = ('UPDATE projections SET Events = ? WHERE Name = ?;')
            self.cur.execute(command, (events, name))
            self.con.commit()
            return True
        except Exception as exception:
            print(exception)
            return False

    def get_events(self, name):
        """Returns events from projections for a name
        Parameters:
            name (str): name of budget
        Returns:
            results (str): events associated with the budget
        """
        try:
            command = "SELECT Events FROM projections WHERE Name = ?"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()[0][0]
            # results = json.dump(results)
            return results
        except Exception as exception:
            print(exception)
            return False

    def get_id_by_name(self, name):
        """Returns id of a projection by it's name
        Parameters:
            name (str): name of projection
        Returns:
            results (str): the ID associated with the budget
        """
        try:
            command = "SELECT Projection_id FROM projection WHERE Name = ?"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()[0][0]
            return results
        except Exception as exception:
            print(exception)
            return False

    def get_by_name(self, name):
        """Searches table projections by name
        parameters:
            name (str): name of budget
        returns:
            results (list): information associated with budget"""
        try:
            command = "SELECT * FROM projections WHERE Name = ?"
            self.cur.execute(command, (name,))
            results = self.cur.fetchall()[0]
            return results
        except Exception as exception:
            print(exception)
            return False

    def get_all_projections(self):
        """Returns results (list) containing all projections"""
        command = "SELECT * FROM projections"
        self.cur.execute(command)
        results = self.cur.fetchall()
        return results

    def delete_table(self):
        """Deletes entire tables from database"""
        command = "DROP TABLE projections"
        self.cur.execute(command)
        self.con.commit()

    def __del__(self):
        """Closes the database on deletion of instance"""
        self.con.close()
"""
from dbhelper import *  
d=Database()
d.create_db()
"""