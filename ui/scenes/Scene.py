from ui.scenes.AppGraphicsScene import QAppGraphicsScene
import uuid


class Scene:
    def __init__(self):
        self.nodes: dict = dict()
        self.edges: dict = dict()

        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()

    def initUI(self):
        self.graphicsScene = QAppGraphicsScene(self)
        self.graphicsScene.setGraphicsScene(self.scene_width, self.scene_height)

    def addNode(self, node, id=None):
        if not id:
            id = uuid.uuid4()
        self.nodes[id] = node
        self.graphicsScene.addItem(node.graphicsNode)

    def addEdge(self, edge, id=None):
        if not id:
            id = uuid.uuid4()
        self.edges[id] = edge

    def removeNode(self, id):
        node = self.nodes.get(id, None)

        if not node:
            return

        del self.nodes[id]
        self.graphicsScene.removeItem(node)

    def removeEdge(self, id):
        edge = self.edges.get(id, None)

        if not edge:
            return
        del self.edges[id]
