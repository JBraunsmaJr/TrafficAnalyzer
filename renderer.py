from models.traffic_item import TrafficItem
from analyzers.argument_parser import AnalyzerConfig
from graphviz import Digraph


class Renderer:
    def __init__(self, config: AnalyzerConfig):
        self._edges: dict = dict()
        self._nodes: dict = dict()
        self._graph: Digraph = Digraph(config.session_name)
        self._config: AnalyzerConfig = config

    def get_rule(self, address: str):
        if not isinstance(address, str):
            raise TypeError(f"Renderer.get_rule: address must be of type string")

        for rule in self._config.render_rules.values():
            if rule.matches(address):
                return rule.shape, rule.color
        return "ellipse", "black"

    def _piece_label(self, address, hostname, label=None):
        """
        Stitches values together
        :param address: IP Address
        :param hostname: Hostname (if applicable) -- this gets displayed over ip
        :param label: Optional label to appear below address/hostname
        :return: Text to appear on node
        """
        text = hostname if hostname else address

        if label:
            text += "\n" + label

        return text

    def define_node(self, address, hostname, label=None):
        if not self._nodes.get(address):
            shape, color = self.get_rule(address)
            text = self._piece_label(address, hostname, label)
            self._graph.attr("node", shape=shape, color=color)
            self._graph.node(address,
                             label=text)
            self._nodes[address] = True

    def add_traffic(self, traffic: TrafficItem):
        """
        Adds visual representation of instance to graph
        :param traffic:
        :return:
        """
        if not traffic:
            return

        self.define_node(traffic.source, traffic.source_host_name)
        self.define_node(traffic.destination, traffic.destination_host_name)

        if not self._edges.get(traffic.id, False):
            self._graph.edge(traffic.source, traffic.destination)
            self._edges[traffic.id] = True

    def render(self):
        """
        Outputs current graph to PNG
        """
        self._graph.render(f"{self._config.session_name}.gv", view=True)
