from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class NodeContentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.widget_label = QLabel("Some Label Title")
        self.text_area = QTextEdit("Sample Text")

        self.layout.addWidget(self.widget_label)
        self.layout.addWidget(self.text_area)