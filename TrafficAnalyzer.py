from TrafficItem import TrafficItem
import dpkt
import socket
import os
import dns.resolver, dns.reversename


class TrafficAnalyzer:
    """
    Handles the parsing and metric gathering from PCAP files
    """

    def __init__(self):
        self._ipmap = dict()
        self._dnsmap = dict()
        self._failed_dns = []

        self._packet_counter = 0
        self._tcp_counter = 0
        self._udp_counter = 0
        self._ip_counter = 0

    @property
    def packet_counter(self):
        """
        Total packets analyzed by this instance (including non-ip)
        """
        return self._packet_counter

    @property
    def tcp_counter(self):
        """
        Number of TCP packets currently analyzed by this instance
        """
        return self._tcp_counter

    @property
    def udp_counter(self):
        """
        Number of UDP packets currently analyzed by this instance
        """
        return self._udp_counter

    @property
    def ip_counter(self):
        """
        Number of ip packets currently analyzed by this instance
        """
        return self._ip_counter

    @property
    def ip_map(self):
        """
        Dictionary of source-->destination
        Key: source+destination
        Value: TrafficItem Instance for this particular traffic pattern
        """
        return self._ipmap

    @property
    def dns_map(self):
        """
        Dictionary of resolved entries
        Key: IP
        Value: Resolved DNS (if applicable)
        """
        return self._dnsmap

    def resolve_domain(self, ip_address):
        """
        Attempts to resolve the specified ip address (in string format)
        :param ip_address: Address to resolve
        :return: resolve domain (if found) otherwise None
        """
        # argument validation
        if not isinstance(ip_address, str):
            print("TrafficAnalyzer.resolve_domain: ip_address must be of type str")
            exit(1)

        if ip_address in self._failed_dns:
            return None

        if self._dnsmap.get(ip_address, None):
            return self._dnsmap[ip_address]
        else:
            try:
                request = dns.reversename.from_address(ip_address)

                if not request:
                    self._failed_dns.append(ip_address)
                    return None

                name = str(dns.resolver.resolve(request, "PTR")[0])
                self._dnsmap[ip_address] = name
                return name
            except Exception as ex:
                self._failed_dns.append(ip_address)
                return None

    def display_as_text(self):
        """
        Display ipmap in text format
        """

        # Brief summary of findings
        print(f"Total Packets: {self.packet_counter}\n"
              f"Total IP Packets: {self.ip_counter}\n"
              f"Total TCP Packets: {self.tcp_counter}\n"
              f"Total UDP Packets: {self.udp_counter}\n"
              f"Source to Destination: {len(self.ip_map)}\n")

        for item in self._ipmap.values():
            print(item)

    def parse_pcap(self, file, display_text=False):
        """
        Parse through a PCAP file and collect metrics on it
        :param file: path to PCAP file
        :param display_text: when parsing is complete -- should it output the results? (default False)
        """

        # argument validation
        if not isinstance(file, str):
            print(f"TrafficAnalyzer.parse_pcap: {file} -- must be of type string")
            exit(1)

        if not os.path.exists(file):
            print(f"TrafficAnalyzer.parse_pcap: {file} -- does not exist")
            exit(1)

        # pcap files must be read as binary
        with open(file, "rb") as pcap:
            for tk, packet in dpkt.pcap.Reader(pcap):
                eth = dpkt.ethernet.Ethernet(packet)
                self._packet_counter += 1

                # we're only focusing on IP packets
                if not isinstance(eth.data, dpkt.ip.IP):
                    continue

                ip = eth.data

                # increment our local counters
                self._ip_counter += 1

                if ip.p == dpkt.ip.IP_PROTO_UDP:
                    self._udp_counter += 1
                elif ip.p == dpkt.ip.IP_PROTO_TCP:
                    self._tcp_counter += 1

                source_address = socket.inet_ntoa(ip.src)
                destination_address = socket.inet_ntoa(ip.dst)

                # attempt to get dns names for src/dst
                source_name = self.resolve_domain(source_address)
                destination_name = self.resolve_domain(destination_address)

                key = f"{source_address} {destination_address}"

                if not self._ipmap.get(key, None):
                    item = TrafficItem(source_address,
                                       destination_address,
                                       source_name=source_name,
                                       destination_name=destination_name)
                    self._ipmap[key] = item
                else:
                    item = self._ipmap[key]

                # Increment our counters and protocols utilized during communications
                # between source and destination
                item.increment()
                item.add_protocol(ip.get_proto(ip.p).__name__)

        if display_text:
            self.display_as_text()