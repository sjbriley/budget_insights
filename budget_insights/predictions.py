"""Predictions displays budget tables and graphs"""
import json
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import random
import datetime
import sys
import tkinter as tk

import budget_dbhelper

matplotlib.use("TkAgg")
# tkinter colors in hex
SLATEGRAY3 = '#9FB6CD'
SLATEGRAY4 = '#6C7B8B'

class BudgetPredictions:
    """Generates budget graphs & tables for viewing
    """
    def __init__(self, name: str, master: tk.Tk) -> None:
        """
        Args:
            master (tk.Tk): root of GUI
            name (str): name of budget

        """
        self.budget_database = budget_dbhelper.BudgetDatabase()
        self.budget = self.budget_database.get_by_name(name)
        self.accounts = json.loads(self.budget[3])
        if self.budget[4] is not None:
            self.expenses = json.loads(self.budget[4])
        else:
            self.expenses = []
        self.master = master
        self.canvas = None

    def view_bar(self) -> None:
        """Displays a bar graph of budget.
        """
        # clear any previous displays
        if isinstance(self.canvas, FigureCanvasTkAgg):
            if self.canvas.get_tk_widget():
                self.canvas.get_tk_widget().destroy()
        x = []
        y = []
        for account in self.accounts:
            x.append(account['name'])
            y.append(int(account['balance']))
        y = np.array(y)

        figure = Figure()
        figure.patch.set_color(SLATEGRAY3)

        subplot = figure.add_subplot(111)
        subplot.bar(x, y, width = 0.72, label = 'Accounts', color=SLATEGRAY4)
        subplot.set_ylabel('Balance')
        subplot.yaxis.label.set_color(color='white')
        subplot.spines['top'].set_color('none')
        subplot.spines['bottom'].set_color('white')
        subplot.spines['left'].set_color('white')
        subplot.spines['right'].set_color('none')
        subplot.patch.set_color(SLATEGRAY3)
        subplot.tick_params(colors='white', top=False, bottom=False, left=True, right=False)

        figure.tight_layout()

        self.canvas = FigureCanvasTkAgg(figure, self.master)
        self.canvas.get_tk_widget().place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.6)

    def view_graph(self) -> None:
        """Displays a graph of budget.
        """
        # clear any previous displays
        if isinstance(self.canvas, FigureCanvasTkAgg):
            if self.canvas.get_tk_widget():
                self.canvas.get_tk_widget().destroy()
        # x = (datetime.datetime.now() + datetime.timedelta(hours=1))
        y = (1,2,3,4)
        y2 = (4,5,6,8.5)
        x = [datetime.datetime.now() + datetime.timedelta(minutes=i) for i in range(4)]
        # y = [i+random.gauss(0,1) for i,_ in enumerate(x)]

        figure = Figure()
        figure.patch.set_color(SLATEGRAY3)
        subplot = figure.add_subplot(111)
        subplot.plot(x, y, label='line 1')
        subplot.plot(x, y2, label='line 2')
        figure.tight_layout()
        # subplot.gcf().autofmt_xdate()
        # subplot.show()
        self.canvas = FigureCanvasTkAgg(figure, self.master)
        self.canvas.get_tk_widget().place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.6)