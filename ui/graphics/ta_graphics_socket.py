from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ui.ta_config import SOCKET_COLORS


class TA_GraphicsSocket(QGraphicsItem):
    def __init__(self, socket_data, socket_type: int =1):
        self.socket_data = socket_data
        super().__init__(socket_data.node_data.graphicsNode)

        self.radius = 6.0
        self.outline_width = 1.0

        self._color_background = SOCKET_COLORS[socket_type]
        self._color_outline = QColor("#FF000000")
        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # paint circle
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def boundingRect(self) -> QRectF:
        w = -self.radius - self.outline_width
        h = 2 * (self.radius + self.outline_width)
        return QRectF(w, w, h, h)
