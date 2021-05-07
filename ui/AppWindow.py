from PyQt5.QtCore import QFile
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from analyzers.BasicAnalyzer import BasicAnalyzer
from models.TrafficItem import TrafficItem
from ui.edges.Edge import Edge
from ui.views.GraphicsView import QAppGraphicsView
from ui.scenes.Scene import Scene
from ui.nodes.Node import Node
import os


class AppWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.stylesheet_filename = os.path.join(script_dir, "qss", "nodestyles.qss")

        self.loadStylesheet(self.stylesheet_filename)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 1200, 800)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.scene = Scene()
        node = Node(self.scene, "Something Crazy",
                    inputs=[1,2,3],
                    outputs=[1])

        node2 = Node(self.scene, "Meow Meow",
                     inputs=[1])

        node2.setPosition(300, 100)

        edge1 = Edge(self.scene, node.outputs[0], node2.inputs[0])

        self.view = QAppGraphicsView(self.scene.graphicsScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Traffic Analyzer")
        self.show()

    def loadStylesheet(self, filename):
        print("STYLE loading:", filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding="utf-8"))

    def consumePCAPResults(self, analyzer: BasicAnalyzer):
        for traffic in analyzer.ip_map.values():
            if not isinstance(traffic, TrafficItem):
                continue

            if not self.scene.nodes.get(traffic.source, None):
                node = Node(self.scene, traffic.source, id=traffic.source)

            if not self.scene.nodes.get(traffic.destination, None):
                node = Node(self.scene, traffic.destination, id=traffic.destination)
