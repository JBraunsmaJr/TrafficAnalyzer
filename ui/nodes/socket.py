from collections import OrderedDict

from ui.serializable_ui import Serializable
from ui.nodes.graphics_socket import QGraphicsSocket


LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4


class Socket(Serializable):
    def __init__(self, node, index=0, position=LEFT_TOP, socket_type=1, multi_edges=True):
        self.node = node
        self.index = index
        self.position = LEFT_TOP
        self.is_multi_edges = multi_edges
        self.socket_type = socket_type
        self.graphicsSocket = QGraphicsSocket(self.node.graphicsNode, self.socket_type)
        self.graphicsSocket.setPos(*self.node.getSocketPosition(index, position))
        self.edges = []

    def __str__(self):
        return "<Socket %s %s..%s>" % ("ME" if self.is_multi_edges else "SE", hex(id(self))[2:5], hex(id(self))[-3:])

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeEdge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
        else:
            print("!W:", "Socket::removeEdge", edge, "is not in list to remove")

    def removeAllEdges(self):
        """
        Remove all edges from socket
        """
        while self.edges:
            edge = self.edges.pop(0)
            edge.remove()

    def serialize(self):
        return OrderedDict([
            ("id", self.id),
            ("index", self.index),
            ("multi_edges", self.is_multi_edges),
            ("position", self.position),
            ("socket_type", self.socket_type)
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        if restore_id:
            self.id = data["id"]
        self.is_multi_edges = data["multi_edges"]
        hashmap[data["id"]] = self
        return True

    def getSocketPosition(self):
        return self.node.getSocketPosition(self.index, self.position)

    def setConnectedEdge(self, edge=None):
        self.edge = edge

    def hasEdge(self):
        return self.edge is not None
