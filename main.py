from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import json
import os

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setFixedSize(1200, 800)
        self.setCentralWidget(self.stacked_widget)
        self.pages = {}
        self.register(MainWindow(), "main")
        self.register(BudgetWindow(), "view budgets")
        self.register(HelpWindow(), "help")
        self.register(ProjectionWindow(), "view projection")
        
        self.goto("main")

    def register(self, widget, name):
        self.pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)
            
    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.pages:
            widget = self.pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())


class PageWindow(QtWidgets.QMainWindow):
    gotoSignal = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)

    def goto(self, name):
        self.gotoSignal.emit(name)
        

class MainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Insights")        
        self.setFixedSize(1200, 800)
        self.window_width = int(self.width())
        self.window_height = int(self.height())
        self.place_buttons()
        
        
    def place_buttons(self):
        
        width = int(self.window_width * 0.3)
        height = int(self.window_width * 0.1)
        
        view_budget_button = QtWidgets.QPushButton("View Budget", self)
        view_budget_button.resize(width, height)
        view_budget_button.move(self.center(self.window_width, width), height)
        view_budget_button.clicked.connect(lambda: self.goto('view budgets'))
        
        create_budget_button = QtWidgets.QPushButton("View Projections", self)
        create_budget_button.resize(width, height)
        create_budget_button.move(self.center(self.window_width, width), int(height*2 + height * 0.5))
        create_budget_button.clicked.connect(lambda: self.goto('view projection'))
        
        how_to_use_button = QtWidgets.QPushButton("How to use", self)
        how_to_use_button.resize(width, height)
        how_to_use_button.move(self.center(self.window_width, width), int(height*4))
        how_to_use_button.clicked.connect(lambda: self.goto('help'))
        

        
    def clear(self):
        pass
        # self.widget.clear()
        # self.inputBox.clear()
        
    def center(self, window_size, size):
        return int((window_size - size) / 2)

class BudgetWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Insights")
        self.setFixedSize(1200, 800)
        self.window_width = int(self.width())
        self.window_height = int(self.height())
        self.mint_csv = None
        self.load_json()
        self.place_buttons()
        
        
    def place_buttons(self):
        back_button = QtWidgets.QPushButton("Back", self)
        back_button.resize(100, 50)
        back_button.move(10, self.window_height-60)
        back_button.clicked.connect(lambda: self.goto('main'))
        self.step_label = False
        self.step_instructions = False
        if self.config['existing_budget'] == '':
            if self.config['mint_csv'] == '':
                self.step_label = QtWidgets.QLabel('Step 1', self)
                self.step_label.setFont(QtGui.QFont("Helvitca", 26))
                self.step_label.resize(150, 100)
                self.step_label.move(25, 25)
                self.step_instructions = QtWidgets.QLabel('Download Intuit Mint .csv by going to "All Transacations"\nand selecting "Export Transactions", then upload here ->', self)
                self.step_instructions.setFont(QtGui.QFont("Helvitca", 14))
                self.step_instructions.resize(600, 100)
                self.step_instructions.move(175, 25)
                
                self.button = QtWidgets.QPushButton("Select csv", self)
                self.button.clicked.connect(lambda: self.select_file())
                self.button.resize(200,100)
                self.button.move(800, 25)
            else:
                if not self.step_label:
                    self.step_label = QtWidgets.QLabel('Step 2', self)
                    self.step_label.setFont(QtGui.QFont("Helvitca", 26))
                    self.step_label.resize(150, 100)
                    self.step_label.move(25, 25)
                else:
                    self.step_label.setText('Step 2')
                if not self.step_instructions:
                    self.step_instructions = QtWidgets.QLabel('Provide a balance for each account recognized in your transactions,\nand add accounts that were not recognized.', self)
                    self.step_instructions.setFont(QtGui.QFont("Helvitca", 14))
                    self.step_instructions.resize(600, 100)
                    self.step_instructions.move(175, 25)
                else:
                    self.step_instructions.setText('Provide a balance for each account recognized in your transactions,\nand add accounts that were not recognized.')
    
    def select_file(self):
        # self.mint_csv = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())
        self.config['mint_csv'] = 'done'
        json.dump(self.config, open(os.getcwd() + '/config.json', 'w'))
        self.place_buttons()
    
    def load_json(self):
        path = os.getcwd() + '/config.json'
        try:
            self.config = json.load(open(path))
        except:
            self.config = {}
        if 'mint_csv' not in self.config:
            self.config['mint_csv'] = ''
        if 'existing_budget' not in self.config:
            self.config['existing_budget'] = ''
        
    
class ProjectionWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projections")        
        self.setFixedSize(1200, 800)
        self.window_width = int(self.width())
        self.window_height = int(self.height())
        self.place_buttons()
        
        
    def place_buttons(self):
        back_button = QtWidgets.QPushButton("Back", self)
        back_button.resize(100, 50)
        back_button.move(10, self.window_height-60)
        back_button.clicked.connect(lambda: self.goto('main'))
        
class HelpWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setFixedSize(1200, 800)
        self.window_width = int(self.width())
        self.window_height = int(self.height())
        self.place_buttons()
        
    def place_buttons(self):
        back_button = QtWidgets.QPushButton("Back", self)
        back_button.resize(100, 50)
        back_button.move(10, self.window_height-60)
        back_button.clicked.connect(lambda: self.goto('main'))
# class AddWindow(PageWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle("Add functions")
#         self.place_buttons()

#     def place_buttons(self):
#         # several text boxes for adding functions will be here
#         self.backButton = QtWidgets.QPushButton("Back", self)
#         self.backButton.resize(80, 30)
#         self.backButton.move(50, 10)
#         self.backButton.clicked.connect(lambda: self.goto("main"))
        
#         self.nameLabel = QtWidgets.QLabel('Name: ', self)
#         self.nameLabel.setFont(QtGui.QFont("Helvitca", 12))
#         self.nameLabel.move(70, 60)
        
#         self.nameBox = QtWidgets.QLineEdit(self)
#         self.nameBox.resize(400, 50)
#         self.nameBox.move(150, 50)
        
#         self.variableLabel = QtWidgets.QLabel('Variables: ', self)
#         self.variableLabel.setFont(QtGui.QFont("Helvitca", 12))
#         self.variableLabel.move(42, 120)
              
#         self.variablesBox = QtWidgets.QLineEdit(self)
#         self.variablesBox.resize(400, 50)
#         self.variablesBox.move(150, 110)
        
#         self.funcLabel = QtWidgets.QLabel('Function: ', self)
#         self.funcLabel.setFont(QtGui.QFont("Helvitca", 12))
#         self.funcLabel.move(45, 170)    
        
#         self.funcBox = QtWidgets.QTextEdit(self)
#         self.funcBox.resize(400, 200)
#         self.funcBox.move(150, 170)
        
#         self.addButton = QtWidgets.QPushButton('Add', self)
#         self.addButton.resize(80, 30)
#         self.addButton.move(470, 10)
#         self.addButton.clicked.connect(lambda: self.add())

#     def add(self):        
#         name = self.nameBox.text().replace(' ','').replace('\n','').lower()
#         variables = self.variablesBox.text().replace(' ','').replace('\n','').lower()
#         func = self.funcBox.toPlainText().replace(' ','').replace('\n','').lower()
        
        
#         for textBox in (self.nameBox, self.variablesBox, self.funcBox):
#             textBox.clear()
            
##################

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
   