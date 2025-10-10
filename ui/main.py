from PyQt6.QtWidgets import (
                            QApplication,
                            QWidget,
                            QVBoxLayout,
                            QCheckBox,
                            QLabel,
                            QGridLayout,
                            QHBoxLayout,
                            QLineEdit,
                            QGroupBox,
                            QSizePolicy,
                            QSpacerItem,
                            QScrollArea,
                            QComboBox,
                            QMainWindow,
                            QPushButton,
)
from PyQt6.QtGui import(
                            QFontMetrics
)
from PyQt6.QtCore import(
                            Qt,
                            pyqtSignal
)
import sys

#Group vars information
chamberInputs = [
   #["Name",						"Symbol"],
    ["Pressure @ Chamber",			"P_c"	],
    ["Temperature @ Chamber",		"T_c"	],
]
throatInputs = [
   #["Name",						"Symbol"],
    ["Area @ Throat",				"A_t"	],
    ["Pressure @ Throat",			"P_t"	],
    ["Temperature @ Throat",		"T_t"	],
]
exitInputs = [
   #["Name",						"Symbol"],
    ["Area @ Exit",					"A_e"	],
    ["Mach Number @ Exit",			"Ma_e"	],
    ["Pressure @ Exit",				"P_e"	],
    ["Temperature @ Exit",			"T_e"	],
]
stagnationInputs = [
   #["Name",						"Symbol"],
    ["Pressure @ Stagnation",		"P_s"	],
    ["Temperature @ Stagnation",	"T_s"	],
]
generalInputs = [
   #["Name",						"Symbol"],
    ["Ratio Of Specific Heats",		"gamma"	],
    ["Specific Gas Constant",		"R"		],
    ["Molar Mass",					"M"		],
]
groupNames = ["Chamber", "Throat", "Exit", "Stagnation", "Misc"]
groupVars = [chamberInputs, throatInputs, exitInputs, stagnationInputs, generalInputs]


#---------------------------------------------
# Main window
#---------------------------------------------
class mainWindow(QMainWindow):
    toggled = pyqtSignal(str, bool)

    #---------------------------------------------
    # Main window setup
    #---------------------------------------------
    def __init__(self):
        super().__init__()
        # Window Setup
        self.setWindowTitle("Engine Initial Variables")
        self.resize(500, 1000)

        # Central widget
        centralWidget = QWidget()
        centralLayout = QVBoxLayout(centralWidget)

        # Scrollable widget
        self.scrollable_inputs = ScrollArea()
        centralLayout.addWidget(self.scrollable_inputs)

        # Global buttons
        self.run_button = QPushButton("Run Solver")
        centralLayout.addWidget(self.run_button, alignment=Qt.AlignmentFlag.AlignRight)
        

    #---------------------------------------------
    # Add group
    #---------------------------------------------
    #def addGroup(self, layout, row, title, data):


    #---------------------------------------------
    # Add variable row
    #---------------------------------------------
    #def addVariable(self, text=None, parent=None, units=None):        


#---------------------------------------------
# Initialization Shtuff
#---------------------------------------------
def main():
    app = QApplication(sys.argv)

    window = mainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()