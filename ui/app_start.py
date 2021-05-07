import sys
from PyQt5.QtWidgets import *
from ui.AppWindow import AppWindow


if __name__ == "__main__":
    app = QApplication([])
    window = AppWindow()
    sys.exit(app.exec_())