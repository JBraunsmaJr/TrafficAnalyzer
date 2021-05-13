from ui.nodes.graphics_node import QGraphicsNode
from ui.nodes.socket import *
from ui.widgets.node_content_widget import NodeContentWidget
from ui.serializable_ui import Serializable


class Node(Serializable):
    def __init__(self, scene, title="Undefined Node",
                 inputs=[], outputs=[]):
        super().__init__()

        self.scene = scene
        self.title = title

        self.content = NodeContentWidget(self)
        self.graphicsNode = QGraphicsNode(self)
        self.title = title

        self.scene.addNode(self, id)

        self.inputs = []
        self.outputs = []

        self.socket_spacing = 22

        # create socket for inputs and outputs
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, socket_type=item, position=LEFT_BOTTOM)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, socket_type=item, position=RIGHT_TOP)
            counter += 1
            self.outputs.append(socket)

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

    def getSocketPosition(self, index, position):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.graphicsNode.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = self.graphicsNode.height - self.graphicsNode.edge_size - \
                self.graphicsNode._padding - index * self.socket_spacing
        else:
            # start from top
            y = self.graphicsNode.title_height + self.graphicsNode._padding + \
                self.graphicsNode.edge_size + index * self.socket_spacing

        return [x, y]

    @property
    def position(self):
        """
        Returns position as QPointF
        """
        return self.graphicsNode.pos()

    def setPosition(self,x, y):
        """
        Sets position to desired coordinates
        :param x:
        :param y:
        """
        self.graphicsNode.setPos(x, y)

    def remove(self):
        for socket in (self.inputs + self.outputs):
            # if socket.hasEdge()
            for edge in socket.edges:
                edge.remove()

        self.scene.graphicsScene.removeItem(self.graphicsNode)
        self.graphicsNode = None
        self.scene.removeNode(self.id)

    def serialize(self):
        inputs, outputs = [], []
        for socket in self.inputs: inputs.append(socket.serialize())
        for socket in self.outputs: outputs.append(socket.serialize())

        return OrderedDict([
            ("id", self.id),
            ("title", self.title),
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

            data["inputs"].sort(key=lambda  socket: socket["index"] + socket["position"] * 10000)
            data["outputs"].sort(key=lambda  socket: socket["index"] + socket["position"] * 10000)

            self.inputs = []
            for socket_data in data["inputs"]:
                new_socket = Socket(node=self, index=socket_data["index"], position=socket_data["position"],
                                    socket_type=socket_data["socket_type"])
                new_socket.deserialize(socket_data, hashmap, restore_id)
                self.inputs.append(new_socket)

            self.outputs = []
            for socket_data in data["outputs"]:
                new_socket = Socket(node=self, index=socket_data["index"], position=socket_data["position"],
                                    socket_type=socket_data["socket_type"])
                new_socket.deserialize(socket_data, hashmap, restore_id)
                self.outputs.append(new_socket)

            return True
