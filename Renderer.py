from models.TrafficItem import TrafficItem
from ArgumentParser import AnalyzerConfig
from graphviz import Digraph

class Renderer:
    def __init__(self, config: AnalyzerConfig):
        self._edges: dict = dict()
        self._nodes: dict = dict()
        self._graph: Digraph = Digraph(config.session_name)
        self._config: AnalyzerConfig = config

    def add_traffic(self, traffic: TrafficItem):
        """
        Adds visual representation of instance to graph
        :param traffic:
        :return:
        """
        if not traffic:
            return

        if not self._nodes.get(traffic.source, False):
            self._nodes[traffic.source] = True
            self._graph.node(traffic.source,
                             label=traffic.source_host_name if traffic.source_host_name
                             else traffic.source)

        if not self._nodes.get(traffic.destination, False):
            self._nodes[traffic.destination] = True
            self._graph.node(traffic.destination,
                             label=traffic.destination_host_name if
                             traffic.destination_host_name else traffic.destination)

        if not self._edges.get(traffic.id, False):
            self._graph.edge(traffic.source, traffic.destination)
            self._edges[traffic.id] = True

    def render(self):
        """
        Outputs current graph to PNG
        """
        self._graph.render(view=True)
