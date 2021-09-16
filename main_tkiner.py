import tkinter as tk
from tkinter import ttk

import dbhelper

SMALL_FONT = ("Helvetica Neue", 12)
MEDIUM_FONT = ("Helvetica Neue", 20)
LARGE_FONT = ("Helvetica Neue", 28)
    
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        geometry = "1000x700"
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
        if create == ViewBudget:
            create(self.master, budget)
        else:
            create(self.master)
    
class Home(Application):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.place_buttons_and_text()

    def place_buttons_and_text(self):
        budget_button = ttk.Button(self.master, text="Budget", command = lambda: self.change_view(self.master, Budget))
        budget_button.place(x = self.center(500), rely=0.1, width=500, relheight=0.3)
        
        projection_button = ttk.Button(self.master, text="Projections", command = lambda: self.change_view(self.master, Budget))
        projection_button.place(x = self.center(500), rely=0.5, width=500, relheight=0.3)
        
class Budget(Application):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.place_buttons_and_text()

    def place_buttons_and_text(self):
        label = tk.Label(self.master, text="Budgets")
        label.configure(font=LARGE_FONT)
        label.place(relx=0.4, rely=0.1, relheight=0.1, relwidth=0.2)

        back_button = ttk.Button(self.master, text="Back", command = lambda: self.change_view(self.master, Home))
        back_button.place(relx=0.02, rely=0.9, relwidth=0.08, relheight=0.08)

        # list all budgets
        budgets = self.db.get_all()
        for count, current_budget in enumerate(budgets):
            current_budget_button = (ttk.Button(self.master, text=current_budget[2], command = lambda: self.change_view(self.master, ViewBudget, budget=str(current_budget[2]))))
            current_budget_button.place(x = self.center(300), rely=(0.2 + 0.1*(count-1)), width=300, relheight=0.08)
            
        new_budget_button = ttk.Button(self.master, text="Create New Budget", command = lambda: self.change_view(self.master, NewBudget))
        new_budget_button.place(x = self.center(350), rely=0.8, width=350, relheight=0.08)
        
        # w = tk.Scrollbar(self.master, bg="white")
        # w.place(relx=0.2, rely=0.2, relheight=0.5, relwidth=0.6)
        
class NewBudget(Application):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.place_buttons_and_text()

    def place_buttons_and_text(self):
        name = tk.Label(self.master, text="Name: ")
        name.configure(font=MEDIUM_FONT, justify="right")
        name.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.09)
        
        amount = tk.Label(self.master, text="Amount: ")
        amount.configure(font=MEDIUM_FONT, justify="right")
        amount.place(relx=0.1, rely=0.2, relwidth=0.2, relheight=0.09)
        
        self.name_entry = tk.Entry(self.master, font=MEDIUM_FONT, bg='white', exportselection=0, relief='sunken')
        self.name_entry.place(relx=0.35, rely=0.1, relwidth=0.5, relheight=0.09)
        self.amount_entry = tk.Entry(self.master, font=MEDIUM_FONT, bg='white', exportselection=0, relief='sunken')
        self.amount_entry.place(relx=0.35, rely=0.2, relwidth=0.5, relheight=0.09)
        
        submit_button = ttk.Button(self.master, text="Submit", command= lambda: self.submit())
        submit_button.place(relx=0.1, rely=0.8, relwidth=0.2, relheight=0.1)
        
    def submit(self):
        if self.db.create_budget(self.name_entry.get(), self.amount_entry.get()) == True:
            print(self.db.get_all())
            self.change_view(self, ViewBudget, budget=self.name_entry.get())
        else:
            warning = tk.Label(self.master, text="Error- Name already exists")
            warning.configure(font=MEDIUM_FONT, fg='red')
            warning.place(relx=0.1, rely=0.7, relwidth=0.4, relheight=0.09)
        
class ViewBudget(Application):
    def __init__(self, master, budget):
        super().__init__(master)
        self.budget = budget
        self.master = master
        self.place_buttons_and_text()

    def place_buttons_and_text(self):
        
        label = tk.Label(self.master, text=self.budget)
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
# =================================================================
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = Home(master=root)
    app.mainloop()