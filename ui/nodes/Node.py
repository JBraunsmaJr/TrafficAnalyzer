from ui.nodes.GraphicsNode import QGraphicsNode
from ui.nodes.Socket import *
from ui.widgets.NodeContentWidget import NodeContentWidget


class Node:
    def __init__(self, scene, title="Undefined Node", id=None,
                 inputs=[], outputs=[]):
        self.scene = scene
        self.title = title
        self._id = id

        self.content = NodeContentWidget()
        self.graphicsNode = QGraphicsNode(self)
        self.scene.addNode(self, id)

        self.inputs = []
        self.outputs = []

        self.socket_spacing = 22

        # create socket for inputs and outputs
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP)
            counter += 1
            self.outputs.append(socket)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

    def getSocketPosition(self, index, position):
        x = 0 if position in (LEFT_TOP, LEFT_BOTTOM) else self.graphicsNode.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from the bottom
            y = self.graphicsNode.height - self.graphicsNode.edge_size - \
                self.graphicsNode._padding - index * self.socket_spacing
        else:
            # start from the top
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
