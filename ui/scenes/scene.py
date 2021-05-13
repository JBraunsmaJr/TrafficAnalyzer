from collections import OrderedDict

from ui.serializable_ui import Serializable
from ui.edges.edge import Edge
from ui.nodes.node import Node
from ui.scenes.app_graphics_scene import QAppGraphicsScene
import uuid


class Scene(Serializable):
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

    def clear(self):
        for item in self.nodes.values():
            item.remove()

        self.nodes.clear()

    def saveToFile(self, filename):
        with open(filename, "w") as file:
            file.write(json.dumps(self.serialize(), indent=4))
            print("Saving to", filename, "was successful")

    def loadFromFile(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data, encoding="utf-8")
            self.deserialize(data)

    def serialize(self):
        nodes, edges = [], []
        for node in self.nodes.values(): nodes.append(node.serialize())
        for edge in self.edges.values(): edges.append(edge.serialize())

        return OrderedDict([
            ("id", self.id),
            ("scene_width", self.scene_width),
            ("scene_height", self.scene_height),
            ("nodes", nodes),
            ("edges", edges)
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        self.clear()
        hashmap = {}
        if restore_id:
            self.id = data["id"]

        # create nodes
        for node_data in data["nodes"]:
            Node(self).deserialize(node_data, hashmap, restore_id)

        # create edges
        for edge_data in data["edges"]:
            Edge(self).deserialize(edge_data, hashmap, restore_id)

        return True
