from PyQt6.QtCore import QObject
from .solver import *


#---------------------------------------------
# Controller
#---------------------------------------------
class Controller(QObject):

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

        # Connect UI signals
        self.ui.inputSection.checkboxToggled.connect(self.checkboxToggled)
        self.ui.globalButtons.runButtonClicked.connect(self.runClicked)

    #---------------------------------------------
    # Handlers for UI signals
    #---------------------------------------------
    def checkboxToggled(self):
        """Called whenever a checkbox is toggled"""
        selectedData = self.ui.inputSection.getCheckedData()
        inputVars = {}

        # Extract symbol:value pairs
        for name, entry in selectedData.items():
            symbol = entry["symbol"]
            value = entry["value"]

            inputVars[symbol] = value

        derivedVars, overconstrainedVars = constraintChecker(inputVars)

        self.ui.inputSection.enableAllFields()

        if isinstance(derivedVars, dict) and derivedVars:
            self.ui.inputSection.disableField(derivedVars)
            self.ui.inputSection.disableField(overconstrainedVars)
        else:
            print("[Controller] No derived variables found.")


    def runClicked(self):
        """Called whenever a checkbox is toggled"""
        selectedData = self.ui.inputSection.getCheckedData()
        inputVars = {}

        # Extract symbol:value pairs
        for name, entry in selectedData.items():
            symbol = entry["symbol"]
            value = entry["value"]

            inputVars[symbol] = value

        derivedVars = equationSolver(inputVars)

        self.ui.inputSection.enableAllFields()

        if isinstance(derivedVars, dict) and derivedVars:
            self.ui.inputSection.disableField(derivedVars)
        else:
            print("[Controller] No derived variables found.")