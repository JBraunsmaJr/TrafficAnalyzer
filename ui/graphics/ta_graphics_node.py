from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class TA_GraphicsNode(QGraphicsItem):
    def __init__(self, *args, **kwargs):
        """
        node_data: (required) Contains node information pertianing to this rendered instance
        title_color: (optional) QtColor, default White
        width: (optional) width of node (default 180)
        height: (optional) height of node (default 240)
        edge_size: (optional) thickness of connections (default 10)
        title_height: (optional) height of title bar (default 24)
        padding: (optional) padding for borders (default 4)
        """

        if not ("node_data" in kwargs.keys()):
            raise ValueError("TA_GraphicsNode requires kwarg 'node_data' to be set")

        super().__init__(kwargs.pop("parent", None))

        self.node_data = kwargs.pop("node_data")
        self.content = self.node_data.content

        self._title_color = kwargs.pop("title_color", Qt.white)
        self._title_font = QFont("Arial", 10)

        self.width = kwargs.pop("width", 180)
        self.height = kwargs.pop("height", 240)
        self.edge_size = kwargs.pop("edge_size", 10.0)
        self.title_height = kwargs.pop("title_height", 24.0)
        self.padding = kwargs.pop("padding", 4.0)

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
        self.node_data.updateConnectedEdges()
        self.wasMoved = True
        """
        for node in self.scene().scene.nodes:
            if node.graphicsNode.isSelected():
                node.updateConnectedEdges()
        """

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseMoveEvent(event)
        if self.wasMoved:
            self.wasMoved = False

    def boundingRect(self):
        return QRectF(
            0, 0,
            self.width,
            self.height
        ).normalized()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def initContent(self):
        self.graphicsContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(self.edge_size, self.title_height + self.edge_size,
                                 self.width - 2 * self.edge_size, self.height - 2 * self.edge_size - self.title_height)
        self.graphicsContent.setWidget(self.content)

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def initSockets(self):
        pass

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self.padding, 0)
        self.title_item.setTextWidth(self.width - 2 * self.padding)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size,
                           self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size,
                                    self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
