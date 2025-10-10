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
                            QFrame,
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
chamberInputs = ["Chamber Data", [
   #["Name",						"Symbol",           ["Units"],                          ],
    ["Pressure @ Chamber",			"P_c",	            ["Pa", "kPa", "bar", "psi", "atm"]  ],
    ["Temperature @ Chamber",		"T_c",	            ["°C", "°K", "°F"]                  ],
]]
throatInputs = ["Throat Data", [
   #["Name",						"Symbol",           ["Units"],                          ],
    ["Area @ Throat",				"A_t",	            ["m²", "cm²", "ft²", "in²"]         ],
    ["Pressure @ Throat",			"P_t",	            ["Pa", "kPa", "bar", "psi", "atm"]  ],
    ["Temperature @ Throat",		"T_t",	            ["°C", "°K", "°F"]                  ],
]]
exitInputs = ["Exit Data", [
   #["Name",						"Symbol",           ["Units"],                          ],
    ["Area @ Exit",					"A_e",	            ["m²", "cm²", "ft²", "in²"]         ],
    ["Mach Number @ Exit",			"Ma_e",	            None                                ],
    ["Pressure @ Exit",				"P_e",	            ["Pa", "kPa", "bar", "psi", "atm"]  ],
    ["Temperature @ Exit",			"T_e",	            ["°C", "°K", "°F"]                  ],
]]
stagnationInputs = ["Stagnation Data", [
   #["Name",						"Symbol",           ["Units"],                          ],
    ["Pressure @ Stagnation",		"P_s",	            ["Pa", "kPa", "bar", "psi", "atm"]  ],
    ["Temperature @ Stagnation",	"T_s",	            ["°C", "°K", "°F"]                  ],
]]
generalInputs = ["Misc. Data", [
   #["Name",						"Symbol",           ["Units"],                          ],
    ["Ratio Of Specific Heats",		"gamma",	        None                                ],
    ["Specific Gas Constant",		"R",		        None                                ],
    ["Molar Mass",					"M",		        ["kg/mol", "g/mol"]                 ],
]]


#---------------------------------------------
# Inputs widget
#---------------------------------------------
class InputWidget(QWidget):
    #---------------------------------------------
    # Inputs widget setup
    #---------------------------------------------
    def __init__(self):
        super().__init__()

        # Layout
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setHorizontalSpacing(12)
        self.layout.setVerticalSpacing(6)

        # Row counter
        self.row = 0

        self.addSection(chamberInputs[0], chamberInputs[1])
        self.addSection(throatInputs[0], throatInputs[1])
        self.addSection(exitInputs[0], exitInputs[1])
        self.addSection(stagnationInputs[0], stagnationInputs[1])
        self.addSection(generalInputs[0], generalInputs[1])

        self.layout.setRowStretch(self.row, 1)
        self.setLayout(self.layout)

    #---------------------------------------------
    # Add section
    #---------------------------------------------
    def addSection(self, title, fields):
        """Add a titled input section"""
        # Section Header
        header = QLabel(f"<b>{title}</b>")
        self.layout.addWidget(header, self.row, 0, 1, 3)
        header.setContentsMargins(0, 6, 0, 2)
        self.row += 1

        # Add fields
        for name, symbol, units in fields:
            label_name = QLabel(name)
            label_symbol = QLabel(symbol)
            input_field = QLineEdit()

            input_field.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            input_field.setFixedWidth(120)

            # Add to widget
            self.layout.addWidget(label_name, self.row, 0)
            self.layout.addWidget(label_symbol, self.row, 1)
            self.layout.addWidget(input_field, self.row, 2)

            if units is not None:
                unit_dropdown = QComboBox()
                unit_dropdown.addItems(units)
                unit_dropdown.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                unit_dropdown.setFixedWidth(80)
                self.layout.addWidget(unit_dropdown, self.row, 3)


            self.row += 1

        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(separator, self.row, 0, 1, 4)
        self.row += 1


#---------------------------------------------
# Inputs widget
#---------------------------------------------
class GlobalButtons(QWidget):
    def __init__(self):
        super().__init__()

        # Layout
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Buttons
        self.runButton = QPushButton("run", self)
        self.runButton.setFixedWidth(120)
        self.layout.addWidget(self.runButton)

        self.setLayout(self.layout)


#---------------------------------------------
# Main window
#---------------------------------------------
class MainWindow(QMainWindow):
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
        #self.scrollable_inputs = ScrollArea()
        #centralLayout.addWidget(self.scrollable_inputs)

        self.inputSection = InputWidget()
        centralLayout.addWidget(self.inputSection)

        self.globalButtons = GlobalButtons()
        centralLayout.addWidget(self.globalButtons)

        self.setCentralWidget(centralWidget)
 


#---------------------------------------------
# Initialization Shtuff
#---------------------------------------------
def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()