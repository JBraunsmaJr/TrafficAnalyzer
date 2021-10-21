from collections import OrderedDict

from ui.graphics.ta_graphics_edge import TA_GraphicsEdgeBezier, TA_GraphicsEdgeDirect
from ui.serializable_ui import Serializable

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2
EDGE_TYPE_HIGHWAY = 3


class EdgeData(Serializable):
    def __init__(self, *args, **kwargs):
        """

        """
        if not "scene" in kwargs:
            raise ValueError("EdgeData requires kwargs of 'scene' of type 'Scene'")

        self.scene = kwargs.pop("scene")
        self._start_socket = kwargs.pop("start_socket", None)
        self._end_socket = kwargs.pop("end_socket", None)
        self.edge_type = kwargs.pop("edge_type", EDGE_TYPE_DIRECT)

    @property
    def start_socket(self):
        return self._start_socket

    @start_socket.setter
    def start_socket(self, value):
        # type check (cannot be None to do this)
        self._start_socket = value

        if self.start_socket:
            self.start_socket.addEdge(self)

    @property
    def end_socket(self):
        return self._end_socket

    @end_socket.setter
    def end_socket(self, value):
        self._end_socket = value

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
            self.graphicsEdge = TA_GraphicsEdgeDirect(edge_data=self)
        elif self.edge_type == EDGE_TYPE_BEZIER:
            self.graphicsEdge = TA_GraphicsEdgeBezier(edge_data=self)
        else:
            self.graphicsEdge = TA_GraphicsEdgeBezier(edge_data=self)

        self.scene.graphicsScene.addItem(self.graphicsEdge)

        if self.start_socket:
            self.updatePositions()

    def updatePositions(self):
        """
        Ensure endpoints of the node match the socket position
        """
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node_data.graphicsNode.pos().x()
        source_pos[1] += self.start_socket.node_data.graphicsNode.pos().y()

        self.graphicsEdge.setSource(*source_pos)

        if self.end_socket:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node_data.graphicsNode.pos().x()
            end_pos[1] += self.end_socket.node_data.graphicsNode.pos().y()

            self.graphicsEdge.setDestination(*end_pos)

        self.graphicsEdge.update()

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
            ("end", self.end_socket_id)
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        if restore_id:
            self.id = data["id"]

        self.start_socket = hashmap[data["start"]]
        self.end_socket = hashmap[data["end"]]
        self.edge_type = data["edge_type"]
