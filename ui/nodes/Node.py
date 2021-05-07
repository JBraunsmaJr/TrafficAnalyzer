from ui.nodes.GraphicsNode import QGraphicsNode
from ui.widgets.NodeContentWidget import NodeContentWidget


class Node:
    def __init__(self, scene, title="Undefined Node", id=None):
        self.scene = scene
        self.title = title

        self.content = NodeContentWidget()
        self.graphicsNode = QGraphicsNode(self)
        self.scene.addNode(self, id)

        self.inputs = []
        self.outputs = []
