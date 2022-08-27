"""Gui.py generates a GUI for user to build budgets and projectiosn
using Tkiner as the GUI. Conects with dbhelper which utilizes sqlite3
to handle database
"""

import tkinter as tk
from tkinter import ttk
from functools import partial
import json
from typing import Optional

import budget_dbhelper
import projections_dbhelper
import predictions

SMALL_FONT = ("Helvetica Neue", 12)
MEDIUM_FONT = ("Helvetica Neue", 20)
LARGE_FONT = ("Helvetica Neue", 28)
BACKGROUND_COLOR_1 = 'SlateGray4'
BACKGROUND_COLOR_2 = 'SlateGray3'
GEOMETRY = "1000x700"

def center(size: int, width: bool = True) -> int:
    """Returns the center based on given size and current window

    Args:
        size (int): the width or height of widget
        width (bool): If True, return calculation based on width.
                        If False, then based on height.

    Returns:
        int: Distance from either top or bottom of application to be centered

    """
    screen_width = int(GEOMETRY.split('x',maxsplit=1)[0])
    screen_height = int(GEOMETRY.split('x')[1])
    if width is True:
        return int((screen_width - size) / 2)
    return int((screen_height - size) / 2)

class Application(tk.Frame):
    """Class which is inherited from for all interface sub classes
    Allows for ease of changing views from one page to another,
    simplifying navigation.
    """
    def __init__(self, master: tk.Tk, budget_database=None, projections_database=None) -> None:
        """
        Args:
            master (tk.Tk): root of GUI
            budget_database (BudgetDatabase): helper for budget database
            projections_database (ProjectionsDatabase): helper for projections database

        """
        super().__init__(master)
        self.master.configure(bg='SlateGray4')
        # resize the window
        master.geometry(GEOMETRY)
        master.title("Budget Insights")
        if budget_database is None:
            self.budget_database = budget_dbhelper.BudgetDatabase()
        else:
            self.budget_database = budget_database
        if projections_database is None:
            self.projections_database = projections_dbhelper.ProjectionsDatabase()
        else:
            self.projections_database = projections_database
        # set quit button
        quit_button = ttk.Button(self.master, text="Quit", command=self.master.destroy)
        quit_button.place(relx=0.9, rely=0.9, relwidth=0.08, relheight=0.08)

    def change_view(
        self, destroy: tk.Frame, create: tk.Frame,
        budget: Optional[str] = None, projection=None
        ) -> None:
        """Helper function for changing pages and destroying instances.

        Args:
            destroy (tk.Frame): frame to be destroyed
            create (tk.Frame): frame to be created
            budget (str): name of budget
            projeciton (str): name of projection

        """
        for child in destroy.winfo_children():
            child.destroy()
        if create in (ViewBudget, AddExpenses, AdjustAccounts, AdjustExpenses):
            create(
                master=self.master,
                budget=budget,
                budget_database=self.budget_database,
                projections_database=self.projections_database
                )
        elif create == ViewProjection:
            create(
                master=self.master,
                projection=projection,
                budget_database=self.budget_database,
                projections_database=self.projections_database
                )
        elif create == NewBudget and budget is not None:
            create(
                master=self.master,
                budget=budget,
                budget_database=self.budget_database,
                projections_database=self.projections_database
                )
        else:
            create(master=self.master)

class Home(Application):
    """Home page of application.
    Inherits from Application to allow changing of views.
    """
    def __init__(self, master: tk.Tk, projections_database=None, budget_database=None) -> None:
        """
        Args:
            master (tk.Tk): root of GUI

        """
        super().__init__(
                master=master,
                projections_database=projections_database,
                budget_database=budget_database
                )
        self.master = master
        self.place_buttons_and_text()

    def place_buttons_and_text(self) -> None:
        """Places buttons & labels on page"""
        budget_button = ttk.Button(self.master, text="Budgets",
                                   command = lambda: self.change_view(self.master, Budget))
        budget_button.place(x = center(500), rely=0.1, width=500, relheight=0.2)

        projection_button = ttk.Button(self.master, text="Projections",
                                       command = lambda: self.change_view(self.master, Projections))
        projection_button.place(x = center(500), rely=0.4, width=500, relheight=0.2)

        info_button = ttk.Button(self.master, text="Information & How to Use",
                                       command = lambda: self.change_view(self.master, info))
        info_button.place(x = center(500), rely=0.7, width=500, relheight=0.2)

class info(Application):

    def __init__(self, master: tk.Tk):
        super().__init__(master=master)
        self.master = master
        label = tk.Label(self.master, text="Information & How to Use", bg=BACKGROUND_COLOR_1)
        label.configure(font=LARGE_FONT)
        label.place(rely=0.08, relheight=0.1, relwidth=1)

        back_button = ttk.Button(self.master, text="Back",
                                 command = lambda: self.change_view(self.master, Home))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)

        bg_label = tk.Label(self.master, bg=BACKGROUND_COLOR_2)
        bg_label.place(relx=0.08, rely=0.18, relwidth=0.84, relheight=0.54)

        instructions = tk.Label(self.master, bg=BACKGROUND_COLOR_2, justify = tk.LEFT, text =
                                '1. Create a budget on the "Budgets" screen'
                                '\n\n2. Add expenses, income, investments to the budget'
                                '\n\n3. View your current budget using provided tables and graphs'
                                '\n\n4. Using a budget that you have created, create a Projection under the "Projections" screen'
                                '\n\n5. Add events to your projections, such as a change in housing expenses or a tax return'
                                '\n\n6. View how these forecasted events affect your budget in the future'
                                '\n\n7. Continue adding events years outward to have an idea of your estimated financial situation'
                                '\n\n8. Export data to either a .csv or an Excel Workbook'
                                '\n\n9. Create several budgets and projections'
                                )
        instructions.configure(font=SMALL_FONT)
        instructions.place(relx = 0.08, rely = 0.21)

class Projections(Application):
    """Interface which displays all existing projections or ability to go to new one
    Inherits from Application to allow changing of views.
    """
    def __init__(self, master: tk.Tk, projections_database=None, budget_database=None) -> None:
        """
        Args:
            master (tk.Tk): root of GUI

        """
        super().__init__(
                        master=master,
                        projections_database=projections_database,
                        budget_database=budget_database
                        )
        self.master = master
        self.place_buttons_and_text()

    def place_buttons_and_text(self) -> None:
        """Places buttons & labels on page
        """
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
        new_projection_btn.place(x = center(350), rely=0.8, width=350, relheight=0.08)
        # max 20 bugets can be displayed for now
        if len(projections) > 19:
            new_projection_btn.configure(state=tk.DISABLED)

class ViewProjection(Application):
    """Interface which displays a projection.
    Inherits from Application to allow changing of views.
    """
    def __init__(
            self,
            master=None,
            projection=None,
            projections_database=None,
            budget_database=None
            ) -> None:
        """
        Args:
            master (tk.Tk): root of GUI
            projection (str): name of projection

        """
        super().__init__(
                master=master,
                projections_database=projections_database,
                budget_database=budget_database
                )
        self.master = master
        self.projection = projection
        self.place_buttons_and_text()

    def place_buttons_and_text(self) -> None:
        """Places buttons & labels on page"""
        label = tk.Label(self.master, text=f'Projection: {self.projection}', bg=BACKGROUND_COLOR_1)
        label.configure(font=LARGE_FONT)
        label.place(x = center(300), rely=0.05, relheight=0.1, width=300)

        back_button = ttk.Button(self.master, text="Back",
                                 command = lambda: self.change_view(self.master, Projections))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)

        bg_label = tk.Label(self.master, bg=BACKGROUND_COLOR_2)
        bg_label.place(relx=0.08, rely=0.18, relwidth=0.84, relheight=0.54)

class NewProjection(Application):
    """Interface which allows user to create projection
    Inherits from Application to allow changing of views.
    """
    def __init__(self, master: tk.Tk, projections_database=None, budget_database=None) -> None:
        """
        Args:
            master (tk.Tk): root of GUI

        """
        super().__init__(
                master=master,
                projections_database=projections_database,
                budget_database=budget_database
                )
        self.master = master
        self.place_buttons_and_text()

        self.warning = tk.Label(self.master, text="", justify="center")
        self.warning.configure(font=MEDIUM_FONT, fg='red', bg=BACKGROUND_COLOR_1)
        self.warning.place(relx=0.3, rely=0.8, relwidth=0.4, relheight=0.05)

    def place_buttons_and_text(self) -> None:
        """Places buttons & labels on page
        """
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
        submit_button = ttk.Button(self.master, text="Submit", command= self.submit)
        submit_button.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

    def submit(self) -> None:
        """submit the current projection
        """
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
    """Interface which displays all existing budgets or ability to go to new one.
    Inherits from Application to allow changing of views.
    """
    def __init__(self, master: tk.Tk, projections_database=None, budget_database=None) -> None:
        """
        Args:
            master (tk.Tk): root of GUI

        """
        super().__init__(
                master=master,
                projections_database=projections_database,
                budget_database=budget_database
                )
        self.master = master
        self.place_buttons_and_text()

    def place_buttons_and_text(self) -> None:
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
            current_budget_button = (
                ttk.Button(self.master, text=current_budget[2],
                command = partial(
                                self.change_view,
                                self.master,
                                ViewBudget,
                                budget=current_budget[2]
                                )))
            current_budget_button.place(
                relx = (0.1 + 0.2*int(count/5)),
                rely=(0.3 + 0.1*(count%5-1)),
                relwidth=0.19,
                relheight=0.08
                )

        new_budget_button = ttk.Button(self.master, text="Create New Budget",
                                       command = lambda: self.change_view(self.master, NewBudget))
        new_budget_button.place(x = center(350), rely=0.8, width=350, relheight=0.08)
        # max 20 bugets can be displayed for now
        if len(budgets) > 19:
            new_budget_button.configure(state=tk.DISABLED)

class NewBudget(Application):
    """Interface which allows new budget to be created & account to be added.
    Inherits from Application to allow changing of views.
    """
    def __init__(self, master: tk.Tk, budget: Optional[str] = None, projections_database=None, budget_database=None) -> None:
        """
        Args:
            master (tk.Tk): root of GUI
            budget (str): name of budget

        """
        super().__init__(
                master=master,
                projections_database=projections_database,
                budget_database=budget_database
                )
        self.master = master
        if budget is not None:
            self.accounts = json.loads(self.budget_database.get_accounts_by_name(budget))
        else:
            self.accounts = []
        self.warning = tk.Label(self.master, text="", justify="center")
        self.warning.configure(font=MEDIUM_FONT, fg='red', bg=BACKGROUND_COLOR_1)
        self.warning.place(relx=0.3, rely=0.8, relwidth=0.4, relheight=0.05)

        self.place_buttons_and_text()
        self.place_account_details()

        if budget is not None:
            self.name_entry.insert(0, budget)
            self.name_entry.configure(state=tk.DISABLED)

    def place_buttons_and_text(self) -> None:
        """Places buttons & labels on page
        """
        # if instance of AdjustAccounts, back button should go back to ViewBudget
        if isinstance(self, AdjustAccounts):
            back_button = ttk.Button(
                self.master,
                text="Back",
                command = lambda: self.change_view(
                self.master,
                ViewBudget,
                budget=self.name_entry.get()
                ))
        else:
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
        submit_button = ttk.Button(self.master, text="Next", command= self.submit_budget)
        submit_button.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

    def place_account_details(self) -> None:
        """Places more buttons & labels which will be updated as user inputs accounts
        """
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

        type_act_label = tk.Label(self.master, text="Type: ", font=SMALL_FONT,
                        justify="right", bg=BACKGROUND_COLOR_2)
        type_act_label.place(relx=0.1, rely=0.61, relwidth=0.2, relheight=0.06)

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
        self.type_act = ttk.OptionMenu(self.master, self.type_var, "Checkings",
                                   "Cash", "Checkings", "Savings", "401k",
                                   "Brokerage", "Roth IRA", "Traditional IRA", "Asset")
        self.type_act.place(relx=0.35, rely=0.61, relwidth=0.2, relheight=0.06)

        submit_account_button = ttk.Button(self.master, text="Add Account",
                                           command= self.submit_account)
        submit_account_button.place(relx=0.35, rely=0.71, relwidth=0.1, relheight=0.06)

        type_act_label = tk.Label(self.master, text="Modify an Account- ", font=SMALL_FONT,
                        justify="right", bg=BACKGROUND_COLOR_2)
        type_act_label.place(relx=0.6, rely=0.71, relwidth=0.14, relheight=0.06)

        self.modify = tk.StringVar(self.master)
        self.modify.set('')
        options = ['']
        for option in self.accounts:
            options.append(option['name'])
        modify_option = ttk.OptionMenu(self.master, self.modify, *options,
                                       command= lambda x: self.change_account())
        modify_option.place(relx=0.75, rely=0.71, relwidth=0.15, relheight=0.06)

    def change_account(self) -> None:
        """Allows user to modify existing Account
        """
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

    def submit_account(self) -> None:
        """Allows user to submit account
        """
        account_name    = self.account_name_entry.get()
        account_balance = self.balance_entry.get().replace(',','').replace('$','')
        interest        = self.interest_entry.get().replace('%','')
        type_act        = self.type_var.get()
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
            'type': str(type_act),
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

    def submit_budget(self) -> None:
        """Allows user to submit budget and go to expenses
        """
        self.submit_account()
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
    """Interface which allows expenses to be added to new budget.
    Inherits from Application to allow changing of views.
    """
    def __init__(
        self, master: tk.Tk, budget: Optional[str] = None,
        projections_database=None, budget_database=None
        ) -> None:
        """
        Args:
            master (tk.Tk): root of GUI
            budget (str): name of budget

        """
        super().__init__(
                master=master,
                projections_database=projections_database,
                budget_database=budget_database
                )
        self.name = budget
        self.master = master
        self.expenses = []

        self.warning = tk.Label(self.master, text="", justify="center")
        self.warning.configure(font=MEDIUM_FONT, fg='red', bg=BACKGROUND_COLOR_1)
        self.warning.place(relx=0.3, rely=0.8, relwidth=0.4, relheight=0.05)

        self.place_buttons_and_text()
        self.place_expense_details()

    def place_buttons_and_text(self) -> None:
        """Places buttons & labels on page
        """
        # if instance of AdjustExpenses, back button should go back to ViewBudget
        if isinstance(self, AdjustExpenses):
            back_button = ttk.Button(
                self.master,
                text="Back",
                command = lambda: self.change_view(
                self.master,
                ViewBudget,
                budget=self.name
                ))
        else:
            back_button = ttk.Button(
                self.master,
                text="Back",
                command = lambda: self.change_view(
                self.master,
                NewBudget,
                budget=self.name
                ))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)

        # name of the budget
        name = tk.Label(self.master, text='Add Expenses to Budget "{}"'.format(self.name),
                        font=MEDIUM_FONT, justify="center", bg=BACKGROUND_COLOR_1)
        name.place(relx=0.2, rely=0.08, relwidth=0.6, relheight=0.09)

        bg_label = tk.Label(self.master, bg=BACKGROUND_COLOR_2)
        bg_label.place(relx=0.08, rely=0.2, relwidth=0.84, relheight=0.6)

        # submit budget
        submit_button = ttk.Button(self.master, text="Submit", command= self.submit)
        submit_button.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

    def place_expense_details(self) -> None:
        """Places more buttons & labels which will be updated as user inputs expenses
        """
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
                                           command= self.submit_expenses)
        submit_account_button.place(relx=0.35, rely=0.71, relwidth=0.15, relheight=0.06)

        type_exp = tk.Label(self.master, text="Modify an Expense/Income- ",
                        font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        type_exp.place(relx=0.53, rely=0.71, relwidth=0.23, relheight=0.06)

        self.modify = tk.StringVar(self.master)
        self.modify.set('')
        options = [""]
        for option in self.expenses:
            options.append(option['name'])
        modify_option = ttk.OptionMenu(self.master, self.modify, *options,
                                        command= lambda x: self.change_expense())
        modify_option.place(relx=0.75, rely=0.71, relwidth=0.15, relheight=0.06)

    def change_expense(self) -> None:
        """Allows user to modify existing expense
        """
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

    def submit_expenses(self) -> None:
        """Allows user to submit expenses and go to ViewBudget
        """
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

    def submit(self) -> None:
        """Allows user to submit expenses and go to ViewBudget
        """
        self.submit_expenses()
        name = self.name
        print(name)
        if self.budget_database.update_expenses(name, self.expenses) is True:
            self.change_view(self.master, ViewBudget, budget=name)

class ViewBudget(Application):
    """Interface to view a budget and connection with predictions.py.
    Inherits from Application to allow changing of views.
    """
    def __init__(
        self, master: tk.Tk, budget: Optional[str] = None,
        projections_database=None, budget_database=None
        ) -> None:
        """
        Args:
            master (tk.Tk): root of GUI
            budget (str): name of budget

        """
        super().__init__(
                master=master,
                projections_database=projections_database,
                budget_database=budget_database
                )
        self.budget = budget
        self.master = master
        self.prediction = predictions.BudgetPredictions(name=budget, master=self.master)
        self.prediction.view_graph()
        self.place_buttons_and_text()

    def place_buttons_and_text(self) -> None:
        """Places buttons & labels on page
        """
        label = tk.Label(self.master, text=f'Budget: {self.budget}', bg=BACKGROUND_COLOR_1)
        label.configure(font=LARGE_FONT)
        label.place(x = center(300), rely=0.05, relheight=0.1, width=300)

        back_button = ttk.Button(self.master, text="Back",
                                command = lambda: self.change_view(self.master, Budget))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)

        graph_button = ttk.Button(self.master, text="graph",
                                    command = self.prediction.view_graph)
        graph_button.place(relx=0.38, rely=0.8, relwidth=0.11, relheight=0.08)

        table_button = ttk.Button(self.master, text="bar",
                                    command = self.prediction.view_bar)
        table_button.place(relx=0.51, rely=0.8, relwidth=0.11, relheight=0.08)

        graph_button = ttk.Button(self.master, text="Adjust Accounts",
                                    command = lambda: self.change_view(self.master,
                                                                       AdjustAccounts,
                                                                       budget=self.budget))
        graph_button.place(relx=0.68, rely=0.8, relwidth=0.11, relheight=0.08)

        graph_button = ttk.Button(self.master, text="Adjust Expenses",
                                    command = lambda: self.change_view(self.master,
                                                                       AdjustExpenses,
                                                                       budget=self.budget))
        graph_button.place(relx=0.68, rely=0.9, relwidth=0.11, relheight=0.08)

        projections_button = ttk.Button(self.master, text="View associated projections",
                                         command = lambda: self.change_view(self.master, Budget))
        projections_button.place(relx=0.38, rely=0.9, relwidth=0.24, relheight=0.08)

        export_button = ttk.Button(self.master, text="Export as .csv",
                                    command = lambda: self.change_view(self.master, Budget))
        export_button.place(relx=0.2, rely=0.9, relwidth=0.1, relheight=0.08)

class AdjustAccounts(NewBudget):
    """Allows adjusting of accounts given a budget.
    Inherits from NewBudget to utilize the same screen
    with existing accounts already loaded in
    """
    def __init__(
        self, master: tk.Tk, budget: Optional[str] = None,
        projections_database=None, budget_database=None
        ) -> None:
        """
        Args:
            master (tk.Tk): root of GUI
            budget (str): name of budget

        """
        super().__init__(
                master=master,
                projections_database=projections_database,
                budget_database=budget_database
                )
        self.accounts = json.loads(self.budget_database.get_accounts_by_name(budget))
        self.name_entry.insert(0, budget)
        self.name_entry.configure(state=tk.DISABLED)
        self.place_account_details()

    def submit_budget(self) -> None:
        """Allows user to submit budget and go to expenses
        """
        self.submit_account()
        name = self.name_entry.get()
        if self.budget_database.update_accounts(name, self.accounts) is True:
            self.change_view(self.master, ViewBudget, budget=self.name_entry.get())
        else:
            self.warning.configure(text='Could not update accounts')

class AdjustExpenses(AddExpenses):
    """Allows of adjusting of expenses given a budget.
    Inherits from AddExpenses to utilize the same screen
    with existing accounts already loaded in.
    """
    def __init__(
        self, master: tk.Tk, budget: Optional[str] = None,
        projections_database=None, budget_database=None
        ) -> None:
        """
        Args:
            master (tk.Tk): root of GUI
            budget (str): name of budget
            projections_database
            budget_database

        """
        super().__init__(
                master=master,
                budget=budget,
                projections_database=projections_database,
                budget_database=budget_database
                )
        self.expenses = json.loads(self.budget_database.get_expenses_by_name(budget))
        self.place_expense_details()

    # def submit(self):f
    #     """Allows user to submit budget and go to expenses
    #     """
    #     self.submit_expenses()
    #     name = self.name_entry.get()
    #     if self.budget_database.update_accounts(name, self.accounts) is True:
    #         self.change_view(self.master, ViewBudget, budget=self.name_entry.get())
    #     else:
    #         self.warning.configure(text='Could not update accounts')

# =================================================================

def main():
    root = tk.Tk()
    root.resizable(False, False)
    app = Home(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()