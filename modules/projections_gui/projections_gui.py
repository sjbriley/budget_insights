import tkinter as tk
from tkinter import ttk
import sys

# insert path two directories up (main project dir)
import os.path
sys.path.insert(0, os.path.join(__file__ ,"../../.."))
print(sys.path)
from gui import Application

class ViewProjections(Application):
    def __init__(self):
        pass