from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

from ui.data.socket_data import *

EDGE_CP_ROUNDNESS = 100


class TA_GraphicsEdge(QGraphicsPathItem):
    def __init__(self, *args, **kwargs):
        """
        edge_data: (required) contains information on the edge
        color: (optional) Default color of line
        selected_color: (optional) Color of line if selected
        line_thickness: (optional) Width of line size
        """
        super().__init__(kwargs.pop("parent", None))

        if not ("edge_data" in kwargs.keys()):
            raise ValueError("TA_GraphicsEdge requires kwarg of 'edge_data' to be defined")

        self.edge = kwargs.pop("edge_data")
        self._color = QColor(kwargs.pop("color", "#001000"))
        self._color_selected = QColor(kwargs.pop("selected_color", "#00ff00"))
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)

        thickness = kwargs.pop("line_thickness", 2.0)
        self._pen.setWidthF(thickness)
        self._pen_selected.setWidthF(thickness)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

        self.posSource = [0, 0]
        self.posDestination = [200, 200]

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def boundingRect(self) -> QRectF:
        return self.shape().boundingRect()

    def shape(self):
        return self.calcPath()

    def calcPath(self):
        """
        Will handle drawing QPainterPath from two points
        """
        raise NotImplementedError("This method has to be overwritten in a child class")

    def intersectsWith(self, p1, p2) -> bool:
        """
        Determine if two paths cross
        """
        cutpath = QPainterPath(p1)
        cutpath.lineTo(p2)
        path = self.calcPath()
        return cutpath.intersects(path)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.setPath(self.calcPath())
        painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def updatePath(self):
        """
        Handles drawing QPainter Path from Point A to B
        """
        raise NotImplementedError("This method has to be overwritten in a child class")


class TA_GraphicsEdgeDirect(TA_GraphicsEdge):
    def calcPath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)


class TA_GraphicsEdgeBezier(TA_GraphicsEdge):
    def calcPath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5

        cpx_s = +dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0

        if self.edge.start_socket is not None:
            sspos = self.edge.start_socket.position

            if (s[0] > d[0] and sspos in (RIGHT_TOP, RIGHT_BOTTOM)) or (s[0] < d[0] and sspos in (LEFT_BOTTOM, LEFT_TOP)):
                cpx_d *= -1
                cpx_s *= -1

                cpy_d = (
                    (s[1] - d[1]) / math.fabs(
                        (s[1] - d[1]) if (s[1] - d[1]) != 0 else 0.00001
                    )
                ) * EDGE_CP_ROUNDNESS
                cpy_s = (
                    (d[1] - s[1]) / math.fabs(
                        (d[1] - s[1]) if (d[1] - s[1]) != 0 else 0.00001
                    )
                ) * EDGE_CP_ROUNDNESS

        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d, self.posDestination[0],
                     self.posDestination[1])

        return path
