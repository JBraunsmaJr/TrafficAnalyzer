from collections import OrderedDict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from ui.serializable_ui import Serializable


class NodeContentWidget(QWidget, Serializable):
    def __init__(self, node, parent=None):
        self.node_data = node
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

    def setEditingflag(self, value):
        self.node_data.scene.graphicsScene.views()[0].editingFlag = value

    def serialize(self):
        return OrderedDict([])

    def deserialize(self, data, hashmap={}):
        return False


class TextEdit(QTextEdit):
    def focusInEvent(self, event):
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)