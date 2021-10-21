import abc
import socket


class BaseAnalyzer(metaclass=abc.ABCMeta):
    """
    Basic implementation for any analyzer
    """

    def __init__(self):
        self._counter: int = 0
        self._ipmap: dict = dict()
        self._dnsmap: dict = dict()
        self._failed_dns: list = []

    @abc.abstractmethod
    def parse_file(self, file: str):
        """
        Parse PCAP file
        :param file: File to process
        """
        pass

    @abc.abstractmethod
    def display_as_text(self):
        """
        Display all metrics via text
        """
        pass

    @abc.abstractmethod
    def display_as_static_graph(self):
        """
        Display all metrics via static graph
        """
        pass

    @property
    def dns_map(self) -> dict:
        """
        Dictionary of resolved DNS records
        Key: IP Address
        Value: DNS Name
        :return: Dictionary
        """
        return self._dnsmap

    @property
    def ip_map(self) -> dict:
        """
        Dictionary of source to destination
        Key: Source IP + Destination IP (format is 'x.x.x.x y.y.y.y')
        Value: TrafficItem instance for this particular traffic pattern
        :return: Dictionary
        """
        return self._ipmap

    def resolve_domain(self, ip_address: str) -> str:
        """
        Attempts to resolve the specified ip address (in string format)
        :param ip_address: Address to resolve
        :return: Resolved domain (if found) otherwise none
        """
        if not isinstance(ip_address, str):
            raise TypeError(f"BasicAnalyzer.resolve_domain: ip_address must be of type string")

        if ip_address in self._failed_dns:
            return None

        if self.ip_map.get(ip_address, None):
            return self.ip_map[ip_address]

        try:
            name = socket.gethostbyaddr(ip_address)[0]
            self.ip_map[ip_address] = name
            return name
        except socket.error:
            self._failed_dns.append(ip_address)
            return None

    @property
    def counter(self) -> int:
        """
        Number of items that have been processed
        :return:
        """
        return self._counter

    def _increment(self):
        """
        Increment processed items by 1
        """
        self._counter += 1