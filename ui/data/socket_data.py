from collections import OrderedDict
from ui.serializable_ui import Serializable
from ui.graphics.ta_graphics_socket import TA_GraphicsSocket


LEFT_TOP = 1
LEFT_MIDDLE = 2
LEFT_BOTTOM = 3
BOTTOM_LEFT = 4
BOTTOM_MIDDLE = 5
BOTTOM_RIGHT = 6
RIGHT_BOTTOM = 7
RIGHT_MIDDLE = 8
RIGHT_TOP = 9
TOP_RIGHT = 10,
TOP_MIDDLE = 11,
TOP_LEFT = 12


class SocketData(Serializable):
    def __init__(self, *args, **kwargs):
        if not ("node_data" in kwargs.keys()):
            raise ValueError("SocketData requires node information: 'node_data' -- must be set")

        self.node_data = kwargs.pop("node_data")
        self.position = kwargs.pop("position", LEFT_TOP)
        self.socket_type = kwargs.pop("socket_type", 1)
        self.is_multi_edges = kwargs.pop("multi_edges", True)
        self.index = kwargs.pop("index", 0)

        self.edges = []

        self.graphicsSocket = TA_GraphicsSocket(self.node_data.graphicsNode, self.socket_type)
        self.graphicsSocket.setPos(*self.node_data.getSocketPosition(self.index, self.position))

        # store other data that we don't necessarily need at this time
        self._data = kwargs

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

