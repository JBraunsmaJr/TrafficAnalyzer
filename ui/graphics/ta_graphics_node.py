from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class TA_GraphicsNode(QGraphicsItem):
    def __init__(self, *args, **kwargs):
        if not ("node_data" in kwargs.keys()):
            raise ValueError("TA_GraphicsNode requires kwarg 'node_data' to be set")

        super().__init__(kwargs.pop("parent", None))

        self.node_data = kwargs.pop("node_data")
        self.content = self.node_data.content

        self._title_color = Qt.white
        self._title_font = QFont("Arial", 10)

        self.width = 180
        self.height = 240
        self.edge_size = 10.0
        self.title_height = 24.0
        self.padding = 4.0

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

        self.initTitle()
        self.title = self.node_data.title

        self.initSockets()
        self.initContent()
        self.initUI()

        self.wasMoved = False

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        # optimize me
        for node in self.scene().scene.nodes:
            if node.graphicsNode.isSelected():
                node.updateConnectedEdges()
        self.wasMoved = True

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseMoveEvent(event)
        if self.wasMoved:
            self.wasMoved = False

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def initContent(self):
        self.graphicsContent = QGraphicsProxyWidget(self)
        self.content.setGeometry