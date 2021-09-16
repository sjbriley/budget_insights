import tkinter as tk
from tkinter import ttk
from functools import partial

import dbhelper

SMALL_FONT = ("Helvetica Neue", 12)
MEDIUM_FONT = ("Helvetica Neue", 20)
LARGE_FONT = ("Helvetica Neue", 28)
BACKGROUND_COLOR_1 = 'SlateGray4'
BACKGROUND_COLOR_2 = 'SlateGray3'
    
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        geometry = "1000x700"
        self.master.configure(bg='SlateGray4')
        # resize the window
        master.geometry(geometry)
        master.title("Budget Projector")
        self.db = dbhelper.Database()

        # get width and height for center() to use
        self.geometry = geometry
        self.width = int(geometry.split('x')[0])
        self.height = int(geometry.split('x')[1])
        
        # set quit button
        quit_button = ttk.Button(self.master, text="Quit", command=self.master.destroy)
        quit_button.place(relx=0.9, rely=0.9, relwidth=0.08, relheight=0.08)
        
    def center(self, size, width = True):
        # returns the center based on given size and current window
        if width == True: return int((self.width - size) / 2)
        else: return int((self.width - size) / 2)
        
    def change_view(self, destroy, create, budget=None):
        """Helper function for changing pages and destroying instances
        inputs:
            destroy: a tk.Frame to be destroyed
            create: a tk.Frame class to be created
            master: root, tk.tk
        """
        for w in destroy.winfo_children():
            w.destroy()
        if create == ViewBudget or create == AddExpenses:
            create(self.master, budget)
        else:
            create(self.master)
    
class Home(Application):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.place_buttons_and_text()

    def place_buttons_and_text(self):
        budget_button = ttk.Button(self.master, text="Budgets", command = lambda: self.change_view(self.master, Budget))
        budget_button.place(x = self.center(500), rely=0.1, width=500, relheight=0.3)
        
        projection_button = ttk.Button(self.master, text="Projections", command = lambda: self.change_view(self.master, Budget))
        projection_button.place(x = self.center(500), rely=0.5, width=500, relheight=0.3)
        
class Budget(Application):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.place_buttons_and_text()

    def place_buttons_and_text(self):
        label = tk.Label(self.master, text="Budgets", bg=BACKGROUND_COLOR_1)
        label.configure(font=LARGE_FONT)
        label.place(relx=0.4, rely=0.08, relheight=0.1, relwidth=0.2)

        back_button = ttk.Button(self.master, text="Back", command = lambda: self.change_view(self.master, Home))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)

        bg_label = tk.Label(self.master, bg=BACKGROUND_COLOR_2)
        bg_label.place(relx=0.08, rely=0.18, relwidth=0.84, relheight=0.54)
        
        # list all budgets
        budgets = self.db.get_all()
        self.budgets = budgets
        for count, current_budget in enumerate(budgets):
            # we need to use functools partial here instead of lambda
            current_budget_button = (ttk.Button(self.master, text=current_budget[2], command = partial(self.change_view, self.master, ViewBudget, budget=current_budget[2])))
            current_budget_button.place(relx = (0.1 + 0.2*int(count/5)), rely=(0.3 + 0.1*(count%5-1)), relwidth=0.19, relheight=0.08)
            
        new_budget_button = ttk.Button(self.master, text="Create New Budget", command = lambda: self.change_view(self.master, NewBudget))
        new_budget_button.place(x = self.center(350), rely=0.8, width=350, relheight=0.08)
        # max 20 bugets can be displayed for now
        if len(budgets) > 19: new_budget_button.configure(state=tk.DISABLED)
        
class NewBudget(Application):
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
        back_button = ttk.Button(self.master, text="Back", command = lambda: self.change_view(self.master, Budget))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)
        
        # name of the budget
        name = tk.Label(self.master, text="Budget Name: ", font=MEDIUM_FONT, justify="right", bg=BACKGROUND_COLOR_1)
        name.place(relx=0.1, rely=0.08, relwidth=0.2, relheight=0.09)
        self.name_entry = tk.Entry(self.master, font=MEDIUM_FONT, bg='white', exportselection=0, relief='sunken')
        self.name_entry.place(relx=0.35, rely=0.08, relwidth=0.5, relheight=0.09)
        
        bg_label = tk.Label(self.master, bg=BACKGROUND_COLOR_2)
        bg_label.place(relx=0.08, rely=0.2, relwidth=0.84, relheight=0.6)
        
        # submit budget
        submit_button = ttk.Button(self.master, text="Next", command= lambda: self.submit())
        submit_button.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)
    
    def place_account_details(self):        
        # account details
        name = tk.Label(self.master, text="Account Name: ",font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        name.place(relx=0.1, rely=0.21, relwidth=0.2, relheight=0.06)
        
        balance = tk.Label(self.master, text="Balance: ", font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        balance.place(relx=0.1, rely=0.31, relwidth=0.2, relheight=0.06)
        
        interest = tk.Label(self.master, text="Annual Interest\n(%, out of 100)", font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        interest.place(relx=0.1, rely=0.41, relwidth=0.2, relheight=0.06)
        
        compound = tk.Label(self.master, text="Compounded: ", font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        compound.place(relx=0.1, rely=0.51, relwidth=0.2, relheight=0.06)
        
        type = tk.Label(self.master, text="Type: ", font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        type.place(relx=0.1, rely=0.61, relwidth=0.2, relheight=0.06)
        
        self.account_name_entry = tk.Entry(self.master, font=MEDIUM_FONT, bg='white', exportselection=0, relief='sunken')
        self.account_name_entry.place(relx=0.35, rely=0.21, relwidth=0.5, relheight=0.06)
        
        self.balance_entry = tk.Entry(self.master, font=MEDIUM_FONT, exportselection=0, relief='sunken')
        self.balance_entry.place(relx=0.35, rely=0.31, relwidth=0.5, relheight=0.06)
        
        self.interest_entry = tk.Entry(self.master, font=MEDIUM_FONT, exportselection=0, relief='sunken')
        self.interest_entry.place(relx=0.35, rely=0.41, relwidth=0.5, relheight=0.06)
        
        self.compounded_var = tk.StringVar(self.master)
        self.compounded = ttk.OptionMenu(self.master, self.compounded_var, "Daily", "Daily", "Weekly", "Monthly", "Quarterly", "Semi Annually", "Annually")
        self.compounded.place(relx=0.35, rely=0.51, relwidth=0.2, relheight=0.06)
        
        self.type_var = tk.StringVar(self.master)
        self.type = ttk.OptionMenu(self.master, self.type_var, "Checkings", "Cash", "Checkings", "Savings", "401k", "Brokerage", "Roth IRA", "Traditional IRA", "Asset")
        self.type.place(relx=0.35, rely=0.61, relwidth=0.2, relheight=0.06)
        
        submit_account_button = ttk.Button(self.master, text="Add Account", command= lambda: self.submit_account())
        submit_account_button.place(relx=0.35, rely=0.71, relwidth=0.1, relheight=0.06)
        
        type = tk.Label(self.master, text="Modify an Account- ", font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        type.place(relx=0.6, rely=0.71, relwidth=0.14, relheight=0.06)
        
        self.modify = tk.StringVar(self.master)
        self.modify.set('N/A')
        options = ["N/A"]
        for option in self.accounts:
            options.append(option['name'])
        modify_option = ttk.OptionMenu(self.master, self.modify, *options, command= lambda x: self.change_account())
        modify_option.place(relx=0.75, rely=0.71, relwidth=0.15, relheight=0.06)
        
        # text = 'Accounts: '
        # for i in self.accounts:
        #     if i != self.accounts[-1]:
        #         text += i['name'] + ', '
        #     else:
        #         text += i['name']
        # accounts_list = tk.Label(self.master, text=text, justify='left', bg=BACKGROUND_COLOR_1, font=MEDIUM_FONT, fg='white')
        # accounts_list.place(relx=0.1, rely=0.85, relwidth=0.8, relheight=0.08)
        
    def change_account(self):
        if self.modify.get() == 'N/A': return
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
        account_name    = self.account_name_entry.get()
        account_balance = self.balance_entry.get().replace(',','').replace('$','')
        interest        = self.interest_entry.get().replace('%','')
        type            = self.type_var.get()
        compounded      = self.compounded_var.get()
        
        if len(account_name) < 1:
            self.warning.configure(text='Please enter an account name')
            return
        try: float(account_balance)
        except ValueError:
            self.warning.configure(text='Balance is not valid number')
            return
        try: float(interest)
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
        
    def submit(self):
        name = self.name_entry.get()
        if len(name) < 1: 
            self.warning.configure(text='Please enter a name')
            return
        if len(self.accounts) < 1:
            self.warning.configure(text='Please add at least one account')
            return
        if self.db.create_budget(name, str(self.accounts)) == True:
            self.db.active_budget = name
            self.change_view(self.master, AddExpenses, budget=self.name_entry.get())
        else:
            self.warning.configure(text='Budget Name already exists')
            
class AddExpenses(Application):
    def __init__(self, master, budget=None):
        super().__init__(master)
        self.name = budget
        self.master = master
        self.budget = self.db.get_by_name(self.name)
        self.expenses = []

        self.warning = tk.Label(self.master, text="", justify="center")
        self.warning.configure(font=MEDIUM_FONT, fg='red', bg=BACKGROUND_COLOR_1)
        self.warning.place(relx=0.3, rely=0.8, relwidth=0.4, relheight=0.05)
        
        self.place_buttons_and_text()
        self.place_account_details()
        
    def place_buttons_and_text(self):
        back_button = ttk.Button(self.master, text="Back", command = lambda: self.change_view(self.master, Budget))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)
        
        # name of the budget
        name = tk.Label(self.master, text='Add Expenses to Budget "{}"'.format(self.name), font=MEDIUM_FONT, justify="center", bg=BACKGROUND_COLOR_1)
        name.place(relx=0.2, rely=0.08, relwidth=0.6, relheight=0.09)
        
        bg_label = tk.Label(self.master, bg=BACKGROUND_COLOR_2)
        bg_label.place(relx=0.08, rely=0.2, relwidth=0.84, relheight=0.6)
        
        # submit budget
        submit_button = ttk.Button(self.master, text="Submit", command= lambda: self.submit())
        submit_button.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)
    
    def place_account_details(self):        
        # account details
        name = tk.Label(self.master, text="Expense/Income Name: ",font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        name.place(relx=0.1, rely=0.21, relwidth=0.2, relheight=0.06)
        
        description = tk.Label(self.master, text="Description: ", font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        description.place(relx=0.1, rely=0.31, relwidth=0.2, relheight=0.06)
        
        amount = tk.Label(self.master, text="Amount: ", font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        amount.place(relx=0.1, rely=0.41, relwidth=0.2, relheight=0.06)
        
        expense_income_label = tk.Label(self.master, text="Expense/Income: ", font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        expense_income_label.place(relx=0.1, rely=0.51, relwidth=0.2, relheight=0.06)
        
        frequency_label = tk.Label(self.master, text="Frequency: ", font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        frequency_label.place(relx=0.1, rely=0.61, relwidth=0.2, relheight=0.06)
        
        self.name_entry = tk.Entry(self.master, font=MEDIUM_FONT, bg='white', exportselection=0, relief='sunken')
        self.name_entry.place(relx=0.35, rely=0.21, relwidth=0.5, relheight=0.06)
        
        self.description_entry = tk.Entry(self.master, font=MEDIUM_FONT, exportselection=0, relief='sunken')
        self.description_entry.place(relx=0.35, rely=0.31, relwidth=0.5, relheight=0.06)
        
        self.amount_entry = tk.Entry(self.master, font=MEDIUM_FONT, exportselection=0, relief='sunken')
        self.amount_entry.place(relx=0.35, rely=0.41, relwidth=0.5, relheight=0.06)
        
        self.expense_income_var = tk.StringVar(self.master)
        self.expense_income = ttk.OptionMenu(self.master, self.expense_income_var, "Expense", "Income", "Expense")
        self.expense_income.place(relx=0.35, rely=0.51, relwidth=0.2, relheight=0.06)
        
        self.frequency_var = tk.StringVar(self.master)
        self.frequency = ttk.OptionMenu(self.master, self.frequency_var, "Bi Weekly", "Weekly", "Bi Weekly", "Monthly", "Quarterly", "Semi Annually", "Annually")
        self.frequency.place(relx=0.35, rely=0.61, relwidth=0.2, relheight=0.06)
        
        submit_account_button = ttk.Button(self.master, text="Add Expense/Income", command= lambda: self.submit_account())
        submit_account_button.place(relx=0.35, rely=0.71, relwidth=0.15, relheight=0.06)
        
        type = tk.Label(self.master, text="Modify an Expense/Income- ", font=SMALL_FONT, justify="right", bg=BACKGROUND_COLOR_2)
        type.place(relx=0.53, rely=0.71, relwidth=0.23, relheight=0.06)
        
        self.modify = tk.StringVar(self.master)
        self.modify.set('N/A')
        options = ["N/A"]
        for option in self.expenses:
            options.append(option['name'])
        modify_option = ttk.OptionMenu(self.master, self.modify, *options, command= lambda x: self.change_account())
        modify_option.place(relx=0.75, rely=0.71, relwidth=0.15, relheight=0.06)
        
    def change_account(self):
        if self.modify.get() == 'N/A': return
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
            
    def submit_account(self):
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
        try: float(amount)
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
                self.place_account_details()
                return
        
        # if it does not exist, append it on
        self.expenses.append(expense)
        self.place_account_details()
        
    def submit(self):
        name = self.name_entry.get()
        if len(name) < 1: 
            self.warning.configure(text='Please enter a name')
            return
        if self.db.update_expenses(name, str(self.expenses)) == True:
            self.db.active_budget = name
            self.change_view(self.master, ViewBudget)
class ViewBudget(Application):
    def __init__(self, master, budget):
        super().__init__(master)
        self.budget = budget
        self.master = master
        self.place_buttons_and_text()

    def place_buttons_and_text(self):
        
        label = tk.Label(self.master, text=self.budget, bg=BACKGROUND_COLOR_1)
        label.configure(font=LARGE_FONT)
        label.place(x = self.center(300), rely=0.05, relheight=0.1, width=300)
        
        back_button = ttk.Button(self.master, text="Back", command = lambda: self.change_view(self.master, Budget))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)
        
        graph_button = ttk.Button(self.master, text="graph", command = lambda: self.change_view(self.master, Budget))
        graph_button.place(relx=0.38, rely=0.8, relwidth=0.11, relheight=0.08)
        
        table_button = ttk.Button(self.master, text="table", command = lambda: self.change_view(self.master, Budget))
        table_button.place(relx=0.51, rely=0.8, relwidth=0.11, relheight=0.08)
        
        projections_button = ttk.Button(self.master, text="View associated projections", command = lambda: self.change_view(self.master, Budget))
        projections_button.place(relx=0.38, rely=0.9, relwidth=0.24, relheight=0.08)
        
        export_button = ttk.Button(self.master, text="Export as .csv", command = lambda: self.change_view(self.master, Budget))
        export_button.place(relx=0.5, rely=0.5, relwidth=0.24, relheight=0.08)
# =================================================================
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = Home(master=root)
    app.mainloop()