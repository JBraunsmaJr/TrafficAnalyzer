from ui.nodes.GraphicsSocket import QGraphicsSocket


LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4


class Socket:
    def __init__(self, node, index=0, position=LEFT_TOP):
        self.node = node
        self.index = index
        self.position = LEFT_TOP
        self.graphicsSocket = QGraphicsSocket(self.node.graphicsNode)
        self.graphicsSocket.setPos(*self.node.getSocketPosition(index, position))