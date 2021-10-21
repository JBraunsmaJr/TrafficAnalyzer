from analyzers.base_analyzer import BaseAnalyzer
from models.traffic_item import TrafficItem
from renderer import Renderer
from analyzers.argument_parser import AnalyzerConfig
import dpkt
import socket
import os


class BasicAnalyzer(BaseAnalyzer):

    def __init__(self, config: AnalyzerConfig):
        # invoke our parent constructor
        super(BasicAnalyzer, self).__init__()

        self._protocol_counter: dict = dict()
        self._ip_counter: int = 0
        self._renderer: Renderer = Renderer(config)

    def protocol_count(self, name: str) -> int:
        """
        Number of times a protocol has been seen during analysis
        :param name: protocol name (string)
        :return: number of times (int) that protocol has been seen
        """
        return self._protocol_counter.get(name, 0)

    @property
    def ip_counter(self) -> int:
        """
        Number of IP packets analyzed by this instance
        :return: int
        """
        return self._ip_counter

    def parse_file(self, file: str):
        # argument validation
        if not isinstance(file, str):
            raise TypeError(f"BasicAnalyzer.parse_false: {file}  - file must be of type string")

        if not os.path.exists(file):
            raise FileNotFoundError(f"BasicAnalyzer.parse_file: {file} does not exist")

        # pcap files must be read as binary when using dpkt
        with open(file, "rb") as pcap:
            for _, buffer in dpkt.pcap.Reader(pcap):
                eth = dpkt.ethernet.Ethernet(buffer)
                self._increment()

                # we're only focusing on IP packets
                if not isinstance(eth.data, dpkt.ip.IP):
                    continue

                ip = eth.data

                # increment our local counters
                protocol_name = ip.get_proto(ip.p).__name__
                if self._protocol_counter.get(protocol_name, None):
                    self._protocol_counter[protocol_name] += 1
                else:
                    self._protocol_counter[protocol_name] = 1

                source_ip_address = socket.inet_ntoa(ip.src)
                destination_ip_address = socket.inet_ntoa(ip.dst)

                # attempt to resolve dns
                source_hostname = self.resolve_domain(source_ip_address)
                destination_hostname = self.resolve_domain(destination_ip_address)

                key = f"{source_ip_address} {destination_ip_address}"
                if not self._ipmap.get(key, None):
                    item = TrafficItem(source_ip_address,
                                       destination_ip_address,
                                       source_hostname,
                                       destination_hostname)
                    self._ipmap[key] = item
                else:
                    item = self._ipmap[key]

                item.add_protocol(protocol_name)

                # add item to our renderer
                self._renderer.add_traffic(item)

    def display_as_text(self):
        for ip, item in self.ip_map.items():
            print(item)

    def display_as_static_graph(self):
        self._renderer.render()
