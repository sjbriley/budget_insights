"""Gui.py generates a GUI for user to build budgets and projectiosn
using Tkiner as the GUI. Conects with dbhelper which utilizes sqlite3
to handle database
"""

import tkinter as tk
from tkinter import ttk
from functools import partial
import json

import budget_dbhelper
import projections_dbhelper
import predictions

SMALL_FONT = ("Helvetica Neue", 12)
MEDIUM_FONT = ("Helvetica Neue", 20)
LARGE_FONT = ("Helvetica Neue", 28)
BACKGROUND_COLOR_1 = 'SlateGray4'
BACKGROUND_COLOR_2 = 'SlateGray3'

class Application(tk.Frame):
    """Class which is inherited from for all interface sub classes"""
    def __init__(self, master=None):
        super().__init__(master)
        geometry = "1000x700"
        self.master.configure(bg='SlateGray4')
        # resize the window
        master.geometry(geometry)
        master.title("Budget Insights")
        self.budget_database = budget_dbhelper.BudgetDatabase()
        self.projections_database = projections_dbhelper.ProjectionsDatabase()

        # get width and height for center() to use
        self.geometry = geometry
        self.width = int(geometry.split('x',maxsplit=1)[0])
        self.height = int(geometry.split('x',maxsplit=2)[1])

        # set quit button
        quit_button = ttk.Button(self.master, text="Quit", command=self.master.destroy)
        quit_button.place(relx=0.9, rely=0.9, relwidth=0.08, relheight=0.08)

    def center(self, size, width = True):
        """returns the center based on given size and current window"""
        if width is True:
            return int((self.width - size) / 2)
        return int((self.height - size) / 2)

    def change_view(self, destroy, create, budget=None, projection=None):
        """Helper function for changing pages and destroying instances
        inputs:
            destroy: a tk.Frame to be destroyed
            create: a tk.Frame class to be created
            budget (str): name of budget
            projeciton (str): name of projection
        """
        for child in destroy.winfo_children():
            child.destroy()
        if create in (ViewBudget, AddExpenses, AdjustAccounts, AdjustExpenses):
            create(self.master, budget)
        elif create == ViewProjection:
            create(self.master, projection)
        else:
            create(self.master)

class Home(Application):
    """Home page of application"""
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.place_buttons_and_text()

    def place_buttons_and_text(self):
        """Places buttons & labels on page"""
        budget_button = ttk.Button(self.master, text="Budgets",
                                   command = lambda: self.change_view(self.master, Budget))
        budget_button.place(x = self.center(500), rely=0.1, width=500, relheight=0.3)

        projection_button = ttk.Button(self.master, text="Projections",
                                       command = lambda: self.change_view(self.master, Projections))
        projection_button.place(x = self.center(500), rely=0.5, width=500, relheight=0.3)

class Projections(Application):
    """Interface which displays all existing projections or ability to go to new one"""
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.place_buttons_and_text()

    def place_buttons_and_text(self):
        """Places buttons & labels on page"""
        label = tk.Label(self.master, text="Projections", bg=BACKGROUND_COLOR_1)
        label.configure(font=LARGE_FONT)
        label.place(relx=0.4, rely=0.08, relheight=0.1, relwidth=0.2)

        back_button = ttk.Button(self.master, text="Back",
                                 command = lambda: self.change_view(self.master, Home))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)

        bg_label = tk.Label(self.master, bg=BACKGROUND_COLOR_2)
        bg_label.place(relx=0.08, rely=0.18, relwidth=0.84, relheight=0.54)

        # list all budgets
        projections = self.projections_database.get_all_projections()
        self.projections = projections
        for count, current_projection in enumerate(projections):
            # we need to use functools partial here instead of
            # lambda else the function calls will change
            current_projection_btn = (ttk.Button(self.master, text=current_projection[2],
                                                command = partial
                                                (self.change_view, self.master,
                                                 ViewProjection, projection=current_projection[2]))
                                     )
            current_projection_btn.place(relx = (0.1 + 0.2*int(count/5)),
                                        rely=(0.3 + 0.1*(count%5-1)),
                                        relwidth=0.19,
                                        relheight=0.08)

        new_projection_btn = ttk.Button(self.master, text="Create New Projection",
                                       command = lambda: self.change_view(
                                           self.master, NewProjection
                                           )
                                       )
        new_projection_btn.place(x = self.center(350), rely=0.8, width=350, relheight=0.08)
        # max 20 bugets can be displayed for now
        if len(projections) > 19:
            new_projection_btn.configure(state=tk.DISABLED)

class ViewProjection(Application):
    """Interface which displays a projection"""
    def __init__(self, master=None, projection=None):
        super().__init__(master)
        self.master = master
        self.projection = projection
        self.place_buttons_and_text()

    def place_buttons_and_text(self):
        """Places buttons & labels on page"""
        label = tk.Label(self.master, text=self.projection, bg=BACKGROUND_COLOR_1)
        label.configure(font=LARGE_FONT)
        label.place(x = self.center(300), rely=0.05, relheight=0.1, width=300)

class NewProjection(Application):
    """Interface which allows user to create projection"""
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.place_buttons_and_text()

        self.warning = tk.Label(self.master, text="", justify="center")
        self.warning.configure(font=MEDIUM_FONT, fg='red', bg=BACKGROUND_COLOR_1)
        self.warning.place(relx=0.3, rely=0.8, relwidth=0.4, relheight=0.05)

    def place_buttons_and_text(self):
        """Places buttons & labels on page"""
        back_button = ttk.Button(self.master, text="Back",
                                 command = lambda: self.change_view(self.master, Projections))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)

        bg_label = tk.Label(self.master, bg=BACKGROUND_COLOR_2)
        bg_label.place(relx=0.08, rely=0.19, relwidth=0.84, relheight=0.6)

        # name of the budget
        name = tk.Label(self.master, text="Projection Name: ", font=MEDIUM_FONT,
                        justify="right", bg=BACKGROUND_COLOR_1)
        name.place(relx=0.1, rely=0.08, relwidth=0.25, relheight=0.09)
        self.name_entry = tk.Entry(self.master, font=MEDIUM_FONT, bg='white',
                                   exportselection=0, relief='sunken')
        self.name_entry.place(relx=0.35, rely=0.08, relwidth=0.5, relheight=0.09)

        budget_label = tk.Label(self.master, text='Select a budet to work with',
                                font=MEDIUM_FONT, justify='center', bg=BACKGROUND_COLOR_2)
        budget_label.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.09)

        # list all budgets
        budgets = self.budget_database.get_all_budgets()
        self.budgets = budgets
        options = []
        for budget in budgets:
            options.append(budget[2])
        self.budget_var = tk.StringVar(self.master)
        budget_menu = ttk.OptionMenu(self.master, self.budget_var, "", *options)
        budget_menu.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.1)

        # submit budget
        submit_button = ttk.Button(self.master, text="Submit", command= lambda: self.submit())
        submit_button.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

    def submit(self):
        """submit the current projection"""
        budget = str(self.budget_var.get())
        name = self.name_entry.get()
        if len(name) < 1:
            self.warning.configure(text="Please enter a name")
            return
        if len(budget) < 1:
            self.warning.configure(text="Please select a budget")
            return
        if self.projections_database.create_projection(name, budget) is False:
            self.warning.configure(text="Projection name already exists")
            return
        self.change_view(self.master, ViewProjection, projection=name)

class Budget(Application):
    """Interface which displays all existing budgets or ability to go to new one"""
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.place_buttons_and_text()

    def place_buttons_and_text(self):
        """Places buttons & labels on page"""
        label = tk.Label(self.master, text="Budgets", bg=BACKGROUND_COLOR_1)
        label.configure(font=LARGE_FONT)
        label.place(relx=0.4, rely=0.08, relheight=0.1, relwidth=0.2)

        back_button = ttk.Button(self.master, text="Back",
                                 command = lambda: self.change_view(self.master, Home))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)

        bg_label = tk.Label(self.master, bg=BACKGROUND_COLOR_2)
        bg_label.place(relx=0.08, rely=0.18, relwidth=0.84, relheight=0.54)

        # list all budgets
        budgets = self.budget_database.get_all_budgets()
        self.budgets = budgets
        for count, current_budget in enumerate(budgets):
            # we need to use functools partial here instead of
            # lambda else the function calls will change
            current_budget_button = (ttk.Button(self.master, text=current_budget[2],
                                                command = partial
                                                (self.change_view, self.master,
                                                 ViewBudget, budget=current_budget[2]))
                                     )
            current_budget_button.place(relx = (0.1 + 0.2*int(count/5)),
                                        rely=(0.3 + 0.1*(count%5-1)),
                                        relwidth=0.19,
                                        relheight=0.08)

        new_budget_button = ttk.Button(self.master, text="Create New Budget",
                                       command = lambda: self.change_view(self.master, NewBudget))
        new_budget_button.place(x = self.center(350), rely=0.8, width=350, relheight=0.08)
        # max 20 bugets can be displayed for now
        if len(budgets) > 19:
            new_budget_button.configure(state=tk.DISABLED)

class NewBudget(Application):
    """Interface which allows new budget to be created & account to be added"""
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.accounts = []

        self.warning = tk.Label(self.master, text="", justify="center")
        self.warning.configure(font=MEDIUM_FONT, fg='red', bg=BACKGROUND_COLOR_1)
        self.warning.place(relx=0.3, rely=0.8, relwidth=0.4, relheight=0.05)

        self.place_buttons_and_text()
        self.place_account_details()

    def place_buttons_and_text(self):
        """Places buttons & labels on page"""
        back_button = ttk.Button(self.master, text="Back",
                                 command = lambda: self.change_view(self.master, Budget))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)

        # name of the budget
        name = tk.Label(self.master, text="Budget Name: ", font=MEDIUM_FONT,
                        justify="right", bg=BACKGROUND_COLOR_1)
        name.place(relx=0.1, rely=0.08, relwidth=0.2, relheight=0.09)
        self.name_entry = tk.Entry(self.master, font=MEDIUM_FONT, bg='white',
                                   exportselection=0, relief='sunken')
        self.name_entry.place(relx=0.35, rely=0.08, relwidth=0.5, relheight=0.09)

        bg_label = tk.Label(self.master, bg=BACKGROUND_COLOR_2)
        bg_label.place(relx=0.08, rely=0.2, relwidth=0.84, relheight=0.6)

        # submit budget
        submit_button = ttk.Button(self.master, text="Next", command= lambda: self.submit_budget())
        submit_button.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

    def place_account_details(self):
        """Places more buttons & labels which will be updated as user inputs accounts"""
        # account details
        name = tk.Label(self.master, text="Account Name: ",font=SMALL_FONT,
                        justify="right", bg=BACKGROUND_COLOR_2)
        name.place(relx=0.1, rely=0.21, relwidth=0.2, relheight=0.06)

        balance = tk.Label(self.master, text="Balance: ", font=SMALL_FONT,
                           justify="right", bg=BACKGROUND_COLOR_2)
        balance.place(relx=0.1, rely=0.31, relwidth=0.2, relheight=0.06)

        interest = tk.Label(self.master, text="Annual Interest\n(%, out of 100)",
                            font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        interest.place(relx=0.1, rely=0.41, relwidth=0.2, relheight=0.06)

        compound = tk.Label(self.master, text="Compounded: ", font=SMALL_FONT,
                            justify="right", bg=BACKGROUND_COLOR_2)
        compound.place(relx=0.1, rely=0.51, relwidth=0.2, relheight=0.06)

        type = tk.Label(self.master, text="Type: ", font=SMALL_FONT,
                        justify="right", bg=BACKGROUND_COLOR_2)
        type.place(relx=0.1, rely=0.61, relwidth=0.2, relheight=0.06)

        self.account_name_entry = tk.Entry(self.master, font=MEDIUM_FONT, bg='white',
                                           exportselection=0, relief='sunken')
        self.account_name_entry.place(relx=0.35, rely=0.21, relwidth=0.5, relheight=0.06)

        self.balance_entry = tk.Entry(self.master, font=MEDIUM_FONT,
                                      exportselection=0, relief='sunken')
        self.balance_entry.place(relx=0.35, rely=0.31, relwidth=0.5, relheight=0.06)

        self.interest_entry = tk.Entry(self.master, font=MEDIUM_FONT,
                                       exportselection=0, relief='sunken')
        self.interest_entry.place(relx=0.35, rely=0.41, relwidth=0.5, relheight=0.06)

        self.compounded_var = tk.StringVar(self.master)
        self.compounded = ttk.OptionMenu(self.master, self.compounded_var, "Daily",
                                         "Daily", "Weekly", "Monthly",
                                         "Quarterly", "Semi Annually", "Annually")
        self.compounded.place(relx=0.35, rely=0.51, relwidth=0.2, relheight=0.06)

        self.type_var = tk.StringVar(self.master)
        self.type = ttk.OptionMenu(self.master, self.type_var, "Checkings",
                                   "Cash", "Checkings", "Savings", "401k",
                                   "Brokerage", "Roth IRA", "Traditional IRA", "Asset")
        self.type.place(relx=0.35, rely=0.61, relwidth=0.2, relheight=0.06)

        submit_account_button = ttk.Button(self.master, text="Add Account",
                                           command= lambda: self.submit_account())
        submit_account_button.place(relx=0.35, rely=0.71, relwidth=0.1, relheight=0.06)

        type = tk.Label(self.master, text="Modify an Account- ", font=SMALL_FONT,
                        justify="right", bg=BACKGROUND_COLOR_2)
        type.place(relx=0.6, rely=0.71, relwidth=0.14, relheight=0.06)

        self.modify = tk.StringVar(self.master)
        self.modify.set('')
        options = ['']
        for option in self.accounts:
            options.append(option['name'])
        modify_option = ttk.OptionMenu(self.master, self.modify, *options,
                                       command= lambda x: self.change_account())
        modify_option.place(relx=0.75, rely=0.71, relwidth=0.15, relheight=0.06)

    def change_account(self):
        """Allows user to modify existing Account"""
        if self.modify.get() == '':
            return
        name = str(self.modify.get())
        for account in self.accounts:
            if account['name'] == name:
                # be sure old variables are deleted
                self.type_var.set("Checkings")
                self.compounded_var.set("Daily")
                self.interest_entry.delete(0, tk.END)
                self.balance_entry.delete(0, tk.END)
                self.account_name_entry.delete(0, tk.END)
                # set new variables
                self.type_var.set(account['type'])
                self.compounded_var.set(account['compound'])
                self.interest_entry.insert(0, account['interest'])
                self.balance_entry.insert(0, account['balance'])
                self.account_name_entry.insert(0, account['name'])
                return

    def submit_account(self):
        """Allows user to submit account"""
        account_name    = self.account_name_entry.get()
        account_balance = self.balance_entry.get().replace(',','').replace('$','')
        interest        = self.interest_entry.get().replace('%','')
        type            = self.type_var.get()
        compounded      = self.compounded_var.get()

        if len(account_name) < 1:
            self.warning.configure(text='Please enter an account name')
            return
        try:
            float(account_balance)
        except ValueError:
            self.warning.configure(text='Balance is not valid number')
            return
        try:
            float(interest)
        except ValueError:
            self.warning.configure(text='Interest rate is not valid number')
            return

        # clear warning
        self.warning.configure(text = '')

        account = {
                   'name': account_name,
                   'balance': account_balance,
                   'interest': interest,
                   'type': str(type),
                   'compound': str(compounded)
                   }

        # replace existing account with same name if one exists
        for count, existing_account in enumerate(self.accounts):
            if existing_account['name'] == account_name:
                self.accounts[count] = account
                self.place_account_details()
                return

        # if it does not exist, append it on
        self.accounts.append(account)
        self.place_account_details()

    def submit_budget(self):
        """Allows user to submit budget and go to expenses"""
        name = self.name_entry.get()
        if len(name) < 1:
            self.warning.configure(text='Please enter a name')
            return
        if len(self.accounts) < 1:
            self.warning.configure(text='Please add at least one account')
            return
        if self.budget_database.create_budget(name, self.accounts) is True:
            self.change_view(self.master, AddExpenses, budget=self.name_entry.get())
        else:
            self.warning.configure(text='Budget Name already exists')

class AddExpenses(Application):
    """Interface which allows expenses to be added to new budget"""
    def __init__(self, master, budget=None):
        super().__init__(master)
        self.name = budget
        self.master = master
        self.expenses = []

        self.warning = tk.Label(self.master, text="", justify="center")
        self.warning.configure(font=MEDIUM_FONT, fg='red', bg=BACKGROUND_COLOR_1)
        self.warning.place(relx=0.3, rely=0.8, relwidth=0.4, relheight=0.05)

        self.place_buttons_and_text()
        self.place_expense_details()

    def place_buttons_and_text(self):
        """Places buttons & labels on page"""
        back_button = ttk.Button(self.master, text="Back",
                                command = lambda: self.change_view(self.master, Budget))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)

        # name of the budget
        name = tk.Label(self.master, text='Add Expenses to Budget "{}"'.format(self.name),
                        font=MEDIUM_FONT, justify="center", bg=BACKGROUND_COLOR_1)
        name.place(relx=0.2, rely=0.08, relwidth=0.6, relheight=0.09)

        bg_label = tk.Label(self.master, bg=BACKGROUND_COLOR_2)
        bg_label.place(relx=0.08, rely=0.2, relwidth=0.84, relheight=0.6)

        # submit budget
        submit_button = ttk.Button(self.master, text="Submit", command= lambda: self.submit())
        submit_button.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

    def place_expense_details(self):
        """Places more buttons & labels which will be updated as user inputs expenses"""
        # account details
        name = tk.Label(self.master, text="Expense/Income Name: ",
                        font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        name.place(relx=0.1, rely=0.21, relwidth=0.2, relheight=0.06)

        description = tk.Label(self.master, text="Description: ", font=SMALL_FONT,
                                justify="right", bg=BACKGROUND_COLOR_2)
        description.place(relx=0.1, rely=0.31, relwidth=0.2, relheight=0.06)

        amount = tk.Label(self.master, text="Amount: ", font=SMALL_FONT,
                            justify="right", bg=BACKGROUND_COLOR_2)
        amount.place(relx=0.1, rely=0.41, relwidth=0.2, relheight=0.06)

        expense_income_label = tk.Label(self.master, text="Expense/Income: ", font=SMALL_FONT,
                                        justify="right", bg=BACKGROUND_COLOR_2)
        expense_income_label.place(relx=0.1, rely=0.51, relwidth=0.2, relheight=0.06)

        frequency_label = tk.Label(self.master, text="Frequency: ", font=SMALL_FONT,
                                    justify="right", bg=BACKGROUND_COLOR_2)
        frequency_label.place(relx=0.1, rely=0.61, relwidth=0.2, relheight=0.06)

        self.name_entry = tk.Entry(self.master, font=MEDIUM_FONT, bg='white',
                                    exportselection=0, relief='sunken')
        self.name_entry.place(relx=0.35, rely=0.21, relwidth=0.5, relheight=0.06)

        self.description_entry = tk.Entry(self.master, font=MEDIUM_FONT,
                                            exportselection=0, relief='sunken')
        self.description_entry.place(relx=0.35, rely=0.31, relwidth=0.5, relheight=0.06)

        self.amount_entry = tk.Entry(self.master, font=MEDIUM_FONT,
                                        exportselection=0, relief='sunken')
        self.amount_entry.place(relx=0.35, rely=0.41, relwidth=0.5, relheight=0.06)

        self.expense_income_var = tk.StringVar(self.master)
        self.expense_income = ttk.OptionMenu(self.master, self.expense_income_var, "Expense",
                                            "Income", "Expense")
        self.expense_income.place(relx=0.35, rely=0.51, relwidth=0.2, relheight=0.06)

        self.frequency_var = tk.StringVar(self.master)
        self.frequency = ttk.OptionMenu(self.master, self.frequency_var, "Bi Weekly",
                                        "Weekly", "Bi Weekly", "Monthly",
                                        "Quarterly", "Semi Annually", "Annually")
        self.frequency.place(relx=0.35, rely=0.61, relwidth=0.2, relheight=0.06)

        submit_account_button = ttk.Button(self.master, text="Add Expense/Income",
                                           command= lambda: self.submit_expenses())
        submit_account_button.place(relx=0.35, rely=0.71, relwidth=0.15, relheight=0.06)

        type = tk.Label(self.master, text="Modify an Expense/Income- ",
                        font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        type.place(relx=0.53, rely=0.71, relwidth=0.23, relheight=0.06)

        self.modify = tk.StringVar(self.master)
        self.modify.set('')
        options = [""]
        for option in self.expenses:
            options.append(option['name'])
        modify_option = ttk.OptionMenu(self.master, self.modify, *options,
                                        command= lambda x: self.change_expense())
        modify_option.place(relx=0.75, rely=0.71, relwidth=0.15, relheight=0.06)

    def change_expense(self):
        """Allows user to modify existing expense"""
        if self.modify.get() == '':
            return
        name = str(self.modify.get())
        for expense in self.expenses:
            if expense['name'] == name:
                # be sure old variables are deleted
                self.expense_income_var.set("Expense")
                self.frequency_var.set("Bi Weekly")
                self.name_entry.delete(0, tk.END)
                self.description_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
                # set new variables
                self.expense_income_var.set(expense['type'])
                self.frequency_var.set(expense['frequency'])
                self.name_entry.insert(0, expense['name'])
                self.description_entry.insert(0, expense['description'])
                self.amount_entry.insert(0, expense['amount'])
                return

    def submit_expenses(self):
        """Allows user to submit expenses and go to ViewBudget"""
        name            = self.name_entry.get()
        description     = self.description_entry.get()
        amount          = self.amount_entry.get().replace('$','').replace('-','').replace('$','')
        expense_income  = self.expense_income_var.get()
        frequency       = self.frequency_var.get()

        if len(name) < 1:
            self.warning.configure(text='Please enter a name')
            return
        if len(description) < 1:
            self.warning.configure(text='Please enter a description')
            return
        try:
            float(amount)
        except ValueError:
            self.warning.configure(text='Amount is not valid number')
            return
        if expense_income == 'expense':
            amount = -abs(float(amount))
            print('expense')
        else:
            amount = abs(float(amount))

        # clear warning
        self.warning.configure(text = '')

        expense = {
                   'name': name,
                   'description': description,
                   'amount': amount,
                   'type': str(expense_income),
                   'frequency': str(frequency)
                   }

        # replace existing account with same name if one exists
        for count, existing_expense in enumerate(self.expenses):
            if existing_expense['name'] == name:
                self.expenses[count] = expense
                self.place_expense_details()
                return

        # if it does not exist, append it on
        self.expenses.append(expense)
        self.place_expense_details()

    def submit(self):
        """Allows user to submit expenses and go to ViewBudget"""
        name = self.name
        if self.budget_database.update_expenses(name, self.expenses) is True:
            self.change_view(self.master, ViewBudget, budget=name)

class ViewBudget(Application):
    """Interface to view a budget"""
    def __init__(self, master, budget):
        super().__init__(master)
        self.budget = budget
        self.master = master
        self.place_buttons_and_text()
        prediciton = predictions.BudgePredictions(name=budget, master=self.master)
        prediciton.view_bar()

    def place_buttons_and_text(self):
        """Places buttons & labels on page"""

        label = tk.Label(self.master, text=self.budget, bg=BACKGROUND_COLOR_1)
        label.configure(font=LARGE_FONT)
        label.place(x = self.center(300), rely=0.05, relheight=0.1, width=300)

        back_button = ttk.Button(self.master, text="Back",
                                command = lambda: self.change_view(self.master, Budget))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)

        graph_button = ttk.Button(self.master, text="graph",
                                    command = lambda: self.change_view(self.master, Budget))
        graph_button.place(relx=0.38, rely=0.8, relwidth=0.11, relheight=0.08)

        table_button = ttk.Button(self.master, text="table",
                                    command = lambda: self.change_view(self.master, Budget))
        table_button.place(relx=0.51, rely=0.8, relwidth=0.11, relheight=0.08)

        graph_button = ttk.Button(self.master, text="Adjust accounts",
                                    command = lambda: self.change_view(self.master, 
                                                                       AdjustAccounts, budget=self.budget))
        graph_button.place(relx=0.68, rely=0.8, relwidth=0.11, relheight=0.08)

        graph_button = ttk.Button(self.master, text="Adjust Expenses",
                                    command = lambda: self.change_view(self.master, 
                                                                       AdjustExpenses, budget=self.budget))
        graph_button.place(relx=0.38, rely=0.8, relwidth=0.11, relheight=0.08)

        projections_button = ttk.Button(self.master, text="View associated projections",
                                         command = lambda: self.change_view(self.master, Budget))
        projections_button.place(relx=0.38, rely=0.9, relwidth=0.24, relheight=0.08)

        export_button = ttk.Button(self.master, text="Export as .csv",
                                    command = lambda: self.change_view(self.master, Budget))
        export_button.place(relx=0.5, rely=0.5, relwidth=0.24, relheight=0.08)

class AdjustAccounts(NewBudget):
    def __init__(self, master=None, budget=None):
        super().__init__(master=master)
        self.accounts = json.loads(self.budget_database.get_accounts_by_name(budget))
        self.name_entry.insert(0, budget)
        self.name_entry.configure(state=tk.DISABLED)
        self.place_account_details()

    def submit_budget(self):
        """Allows user to submit budget and go to expenses"""
        name = self.name_entry.get()
        if self.budget_database.update_accounts(name, self.accounts) is True:
            self.change_view(self.master, ViewBudget, budget=self.name_entry.get())
        else:
            self.warning.configure(text='Could not update accounts')
    
class AdjustExpenses(AddExpenses):
    def __init__(self, master=None, budget=None):
        super().__init__(master=master, budget=budget)
        self.expenses = json.loads(self.budget_database.get_expenses_by_name(budget))
        self.place_expense_details()

    # def submit_budget(self):
    #     """Allows user to submit budget and go to expenses"""
    #     name = self.name_entry.get()
    #     if self.budget_database.update_accounts(name, self.accounts) is True:
    #         self.change_view(self.master, ViewBudget, budget=self.name_entry.get())
    #     else:
    #         self.warning.configure(text='Could not update accounts')
# =================================================================
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = Home(master=root)
    app.mainloop()
    