import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.controller import Controller


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    controller = Controller(window)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()