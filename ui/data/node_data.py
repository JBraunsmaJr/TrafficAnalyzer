from typing import Tuple

from PyQt5.QtCore import QPointF

from ui.graphics.ta_graphics_node import TA_GraphicsNode
from ui.data.socket_data import *
from ui.widgets.node_content_widget import NodeContentWidget
from ui.serializable_ui import Serializable


class NodeData(Serializable):
    def __init__(self, **kwargs):
        if not ("scene" in kwargs.keys()):
            raise ValueError("NodeData requires kwarg of 'scene'")

        super().__init__()

        self.scene = kwargs.pop("scene")
        self.title = kwargs.pop("title", "Undefined Node")

        self.content = NodeContentWidget(self)
        self.graphicsNode = TA_GraphicsNode(self)

        self.scene.addNode(self, id)

        self.inputs = []
        self.outputs = []

        self.socket_spacing = kwargs("socket_spacing", 22)

        counter = 0
        for item in kwargs.pop("inputs", []):
            socket = SocketData(node=self, index=counter, socket_type=item, position=LEFT_BOTTOM)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in kwargs.pop("outputs", []):
            socket = SocketData(node=self, index=counter, socket_type=item, position=RIGHT_TOP)
            counter += 1
            self.outputs.append(socket)

    def updateConnectedEdges(self) -> None:
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

    def getSocketPosition(self, index: int, position: int) -> Tuple:
        """
        Gets position of socket
        """
        if position in (LEFT_TOP, LEFT_BOTTOM, BOTTOM_LEFT, TOP_LEFT):
            x = 0
        elif position in (TOP_MIDDLE, BOTTOM_MIDDLE):
            x = self.graphicsNode.width // 2
        else:
            x = self.graphicsNode.width

        if position in (TOP_LEFT, TOP_RIGHT, TOP_MIDDLE):
            y = self.graphicsNode.title_height + self.graphicsNode.padding + \
                self.graphicsNode.edge_size + index * self.socket_spacing
        elif position in (LEFT_MIDDLE, RIGHT_MIDDLE):
            y = self.graphicsNode.height // 2
        else:
            y = self.graphicsNode.height - self.graphicsNode.edge_size - \
                self.graphicsNode.padding - index * self.socket_spacing

        return [x, y]

    def remove(self):
        for socket in (self.inputs + self.outputs):
            for edge in socket.edges:
                edge.remove()

        self.scene.graphicsScene.removeItem(self.graphicsNode)
        self.graphicsNode = None
        self.scene.removeNode(self.id)

    @property
    def position(self) -> QPointF:
        """
        Returns position
        """
        return self.graphicsNode.pos()

    def setPosition(self, x: int, y: int):
        """
        Sets position to desired coordinates
        """
        self.graphicsNode.setPos(x,y)

    def serialize(self):
        inputs, outputs = [], []

        for socket in self.inputs: inputs.append(socket.serialize())
        for socket in self.outputs: outputs.append(socket.serialize())

        return OrderedDict([
            ("id", self.id),
            ("title", self.self.title),
            ("pos_x", self.graphicsNode.scenePos().x()),
            ("pos_y", self.graphicsNode.scenePos().y()),
            ("inputs", inputs),
            ("outputs", outputs),
            ("content", self.content.serialize())
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        if restore_id:
            self.id = data["id"]

        hashmap[data["id"]] = self

        self.setPosition(data["pos_x"], data["pos_y"])
        self.title = data["title"]

        data["inputs"].sort(key=lambda socket: socket["index"] + socket["position"] * 10000)
        data["outputs"].sort(key=lambda socket: socket["index"] + socket["position"] * 10000)

        self.inputs = []
        for socket_data in data["inputs"]:
            new_socket = SocketData(node_data=self, index=socket_data["index"], position=socket_data["position"],
                                    socket_type=socket_data["socket_type"])
            new_socket.deserialize(socket_data, hashmap, restore_id)
            self.inputs.append(new_socket)

        self.outputs = []
        for socket_data in data["outputs"]:
            new_socket = SocketData(node_data=self, index=socket_data["index"], position=socket_data["position"],
                                    socket_type=socket_data["socket_type"])
            new_socket.deserialize(socket_data, hashmap, restore_id)
            self.outputs.append(new_socket)

        return True