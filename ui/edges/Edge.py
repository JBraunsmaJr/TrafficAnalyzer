from ui.edges.GraphicsEdge import *


EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2


class Edge:
    def __init__(self, scene, start_socket, end_socket, edge_type=EDGE_TYPE_DIRECT, id=None):
        self._id = id
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.edge = self

        if self.end_socket:
            self.end_socket.edge = self

        self.graphicsEdge = QGraphicsEdgeDirect(self) if edge_type == EDGE_TYPE_DIRECT else QGraphicsEdgeBezier(self)
        self.updatePositions()
        self.scene.graphicsScene.addItem(self.graphicsEdge)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def updatePositions(self):
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
        if self.start_socket:
            self.start_socket.edge = None
        if self.end_socket:
            self.end_socket.edge = None

        self.end_socket = None
        self.start_socket = None

    def remove(self):
        self.remove_from_sockets()
        self.scene.graphicsScene.removeItem(self.graphicsEdge)
        self.graphicsEdge = None
        self.scene.removeEdge(self.id)
