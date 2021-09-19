"""Predictions displays budget tables and graphs"""
import json
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

import budget_dbhelper

matplotlib.use("TkAgg")
# tkinter colors in hex
SLATEGRAY3 = '#9FB6CD'
SLATEGRAY4 = '#6C7B8B'

class BudgePredictions():
    """Generates budget graphs & tables for viewing"""
    def __init__(self, name, master):
        self.budget_database = budget_dbhelper.BudgetDatabase()
        self.budget = self.budget_database.get_by_name(name)
        self.accounts = json.loads(self.budget[3])
        self.expenses = json.loads(self.budget[4])
        self.master = master

    def view_bar(self):
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

        canvas = FigureCanvasTkAgg(figure, self.master)
        canvas.get_tk_widget().place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.6)