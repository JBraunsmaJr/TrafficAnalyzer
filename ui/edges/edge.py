from collections import OrderedDict

from ui.serializable_ui import Serializable
from ui.edges.graphics_edge import *


EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2


class Edge(Serializable):
    def __init__(self, scene, start_socket=None, end_socket=None, edge_type=EDGE_TYPE_DIRECT):
        self.scene = scene
        self._start_socket = start_socket
        self._end_socket = end_socket
        self.start_socket = start_socket
        self.end_socket = end_socket
        self.edge_type = edge_type
        self.scene.addEdge(self)

    @property
    def start_socket(self):
        """
        Starting socket for this edge
        """
        return self._start_socket

    @start_socket.setter
    def start_socket(self, value):
        if self._start_socket:
            self._start_socket.removeEdge(self)

        self._start_socket = value

        if self.start_socket:
            self.start_socket.addEdge(self)

    @property
    def end_socket(self):
        """
        Destination socket for this edge
        """
        return self._end_socket

    @end_socket.setter
    def end_socket(self, value):
        # if we were assigned to same socket before, delete us from the socket
        if self._end_socket:
            self._end_socket.removeEdge(self)

        # assign new end socket
        self._end_socket = value

        # add edge to socket class
        if self.end_socket:
            self.end_socket.addEdge(self)

    @property
    def edge_type(self):
        """
        Methodology in how the edge is rendered
        """
        return self._edge_type

    @edge_type.setter
    def edge_type(self, value):
        if hasattr(self, "graphicsEdge") and self.graphicsEdge is not None:
            self.scene.graphicsScene.removeItem(self.graphicsEdge)

        self._edge_type = value

        if self.edge_type == EDGE_TYPE_DIRECT:
            self.graphicsEdge = QGraphicsEdgeDirect(self)
        elif self.edge_type == EDGE_TYPE_BEZIER:
            self.graphicsEdge = QGraphicsEdgeBezier(self)
        else:
            self.graphicsEdge = QGraphicsEdgeBezier(self)

        self.scene.graphicsScene.addItem(self.graphicsEdge)

        if self.start_socket:
            self.updatePositions()

    def updatePositions(self):
        """
        Ensure the endpoints of the node match the socket positions
        for both the start and ending sockets
        """
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.graphicsNode.pos().x()
        source_pos[1] += self.start_socket.node.graphicsNode.pos().y()

        self.graphicsEdge.setSource(*source_pos)

        if self.end_socket:
           end_pos = self.end_socket.getSocketPosition()
           end_pos[0] += self.end_socket.node.graphicsNode.pos().x()
           end_pos[1] += self.end_socket.node.graphicsNode.pos().y()
           self.graphicsEdge.setDestination(*end_pos)

        self.graphicsEdge.update()

    def remove_from_sockets(self):
        """
        Remove associated sockets
        """
        if self.start_socket:
            self.start_socket.edge = None
        if self.end_socket:
            self.end_socket.edge = None

        self.end_socket = None
        self.start_socket = None

    def remove(self):
        """
        Remove this edge from existence
        """
        self.remove_from_sockets()
        self.scene.graphicsScene.removeItem(self.graphicsEdge)
        self.graphicsEdge = None
        self.scene.removeEdge(self.id)

    def serialize(self):
        return OrderedDict([
            ("id", self.id),
            ("edge_type", self.edge_type),
            ("start", self.start_socket.id),
            ("end", self.end_socket.id)
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        if restore_id:
            self.id = data["id"]
        self.start_socket = hashmap[data["start"]]
        self.end_socket = hashmap[data["end"]]
        self.edge_type = data["edge_type"]

