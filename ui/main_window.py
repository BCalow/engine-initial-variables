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
import numpy as np
import sys


#---------------------------------------------
# Group vars information
#---------------------------------------------
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
    checkboxToggled = pyqtSignal()
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

        self.row = 0
        self.fieldValues = {}

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
        # Section Header
        header = QLabel(f"<b>{title}</b>")
        self.layout.addWidget(header, self.row, 0, 1, 3)
        header.setContentsMargins(0, 6, 0, 2)
        self.row += 1

        # Add fields
        for name, symbol, units in fields:
            # Add checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(False)

            # Add name, symbol, input
            label_name = QLabel(name)
            label_symbol = QLabel(symbol)
            input_field = QLineEdit()

            # Set input size
            input_field.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            input_field.setFixedWidth(120)

            # Field disabled when not selected
            input_field.setEnabled(False)
            checkbox.toggled.connect(input_field.setEnabled)

            # Add to widget
            self.layout.addWidget(checkbox, self.row, 0)
            self.layout.addWidget(label_name, self.row, 1)
            self.layout.addWidget(label_symbol, self.row, 2)
            self.layout.addWidget(input_field, self.row, 3)

            unit_dropdown = None
            if units is not None:
                # Add unit dropdown select
                unit_dropdown = QComboBox()
                unit_dropdown.addItems(units)
                unit_dropdown.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                unit_dropdown.setFixedWidth(80)
                self.layout.addWidget(unit_dropdown, self.row, 4)

            # Store state and value to dict
            self.fieldValues[name] = {
                "symbol" : symbol,
                "checkbox" : checkbox,
                "input" : input_field,
                "unit" : unit_dropdown,
            }

            def handleToggle(state, input_field=input_field, unit_dropdown=unit_dropdown):
                input_field.setEnabled(state)
                if unit_dropdown:
                    unit_dropdown.setEnabled(state)

            # Checkbox signal
            checkbox.toggled.connect(lambda _: self.checkboxToggled.emit())
            checkbox.toggled.connect(handleToggle)

            # Initial state
            input_field.setEnabled(False)
            if unit_dropdown:
                unit_dropdown.setEnabled(False)

            self.row += 1

        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(separator, self.row, 0, 1, 5)
        self.row += 1

    #---------------------------------------------
    # Get checked variables data
    #---------------------------------------------
    def getCheckedData(self):
        """Return a dict of checked variables with their values and units."""
        checked_data = {}
        for name, widgets in self.fieldValues.items():
            checkbox = widgets["checkbox"]

            if checkbox.isChecked():
                input_field = widgets["input"]
                symbol = widgets["symbol"]
                raw_value = input_field.text().strip()

                value = None
                if raw_value:
                    try:
                        value = np.float64(raw_value)
                    except ValueError:
                        print(f"[Warning] Invalid numeric input for {name!r}: {raw_value}")
                        continue

                unit_dropdown = widgets["unit"]
                unit = unit_dropdown.currentText() if unit_dropdown else None

                checked_data[name] = {
                    "symbol": symbol, 
                    "value": value, 
                    "unit": unit
                    }
                
        return checked_data
    
    #---------------------------------------------
    # Disable fields
    #---------------------------------------------
    def disableField(self, derivedVars):
        """Disable any fields that have their results derived"""
        for name, widgets in self.fieldValues.items():
            if widgets["symbol"] in derivedVars:

                symbol = widgets["symbol"]

                value = derivedVars[symbol]

                checkbox = widgets["checkbox"]
                checkbox.setEnabled(False)

                unit_dropdown = widgets["unit"]
                if unit_dropdown:
                    unit_dropdown.setEnabled(False)

                input_field = widgets["input"]
                input_field.setEnabled(False)

                # Update input text
                if value is not None:
                    input_field.setText(f"{value:.6g}")
                else:
                    input_field.clear()

                # Add tooltip + styling
                input_field.setToolTip("Derived automatically from other inputs")
                input_field.setStyleSheet("color: gray; background-color: #f4f4f4;")

    #---------------------------------------------
    # Enable fields
    #---------------------------------------------
    def enableAllFields(self):
        """Enable all fields"""
        for name, widgets in self.fieldValues.items():
            checkbox = widgets["checkbox"]
            checkbox.setEnabled(True)

            unit_dropdown = widgets["unit"]
            
            input_field = widgets["input"]
            input_field.setToolTip("")
            input_field.setStyleSheet("")

            if checkbox.isChecked():
                input_field.setEnabled(True)
                if unit_dropdown:
                    unit_dropdown.setEnabled(True)
            else:
                input_field.setEnabled(False)
                if unit_dropdown:
                    unit_dropdown.setEnabled(False)
                

#---------------------------------------------
# Global buttons widget
#---------------------------------------------
class GlobalButtons(QWidget):
    runButtonClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Layout
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Buttons
        self.runButton = QPushButton("Run", self)
        self.runButton.setFixedWidth(120)
        self.layout.addWidget(self.runButton)

        # Run signal
        self.runButton.clicked.connect(lambda: self.runButtonClicked.emit())

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

        # Input sections
        self.inputSection = InputWidget()
        centralLayout.addWidget(self.inputSection)

        # Global buttons
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