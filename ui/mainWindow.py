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

#Main Window
class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        #Window Setup
        self.setWindowTitle("Engine Initial Variables")
        self.resize(500, 1000)
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        content = QWidget()
        contentLayout = QVBoxLayout(content)

        #Dict setup
        inputVars = {}
        derivedVars = {}

    
    def addGroup()
        







#Initialization Shtuff
def main():
    app = QApplication(sys.argv)

    window = mainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()