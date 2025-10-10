from PyQt6.QtCore import QObject
from .solver import *


#---------------------------------------------
# Controller
#---------------------------------------------
class Controller(QObject):

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        #self.solver = equationSolver()

        self.ui.inputSection.checkboxToggled.connect(self.checkboxToggled)
        self.ui.globalButtons.runButtonClicked.connect(self.runClicked)

    #---------------------------------------------
    # Handlers for UI signals
    #---------------------------------------------
    def checkboxToggled(self):
        checked = self.ui.inputSection.getCheckedVariables()
        print(self.ui.inputSection.getCheckedVariables())

    def runClicked(self):
        checked = self.ui.inputSection.getCheckedVariables()
        print(self.ui.inputSection.getCheckedVariables())