import socket


class TrafficItem:
    """
    Data structure for capturing various metrics between a source and destination IP address
    """
    def __init__(self, source, destination, source_name, destination_name):

        # do some argument validation
        if not isinstance(source, str):
            print(f"Source: {source} -- must be of type string")
            exit(1)

        if not isinstance(destination, str):
            print(f"Destination: {destination} -- must be of type string")
            exit(1)

        if source_name and not isinstance(source_name, str):
            print(f"Source Name: {source_name} -- must be of type string")
            exit(1)

        if destination_name and not isinstance(destination_name, str):
            print(f"Destination Name: {destination_name} -- must be of type sring")
            exit(1)

        self._source = source
        self._destination = destination
        self._source_name = source_name
        self._destination_name = destination_name

        self._protocols = dict()
        self._counter = 1

    @property
    def counter(self):
        """
        Number of times a packet has been seen with the source and destination address (regardless of protocol)
        :return: integer
        """
        return self._counter

    @counter.setter
    def counter(self, value):
        self._counter = value

    def increment(self):
        """
        Increment the amount of times this source/destination pair have been seen in PCAP
        :return:
        """
        self.counter += 1

    def add_protocol(self, protocol):
        """
        This adds the protocol to the list of used protocols between source/destination
            If already tracked -- increments the counter by 1
            Otherwise: sets the counter to 1
        :param protocol:
        :return:
        """
        # validation check
        if not isinstance(protocol, str):
            print(f"add_protocol requires a string argument, '{protocol}'")
            return

        if self._protocols.get(protocol, None):
            self._protocols[protocol] += 1
        else:
            self._protocols[protocol] = 1

    @property
    def source(self):
        """
        Source IP address for this instance
        :return:
        """
        return self._source

    @property
    def destination(self):
        """
        Destination IP address for this instance
        :return:
        """
        return self._destination

    @property
    def source_name(self):
        """
        DNS Name (if applicable) of source
        :return: str if available. None if not available
        """
        return self._source_name

    @property
    def destination_name(self):
        """
        DNS Name (if applicable) of destination
        :return: str if available. None if not available
        """
        return self._destination_name

    def __protocols__(self):
        """
        Text representation of protocols utilized by this instance
        :return: str
        """
        text = ""
        for proto, count in self._protocols.items():
            text += f"\t\t{proto}: {count}\n"

        return text

    def __str__(self):
        sname = f" ({self.source_name})" if self.source_name else ""
        dname = f" ({self.destination_name})" if self.destination_name else ""

        return f"From {self.source}{sname} to {self.destination}{dname}\n" \
               f"\tCount: {self.counter}\n" \
               f"\tProtcols:\n" \
               f"{self.__protocols__()}"
