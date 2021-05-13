class TrafficItem:
    """
    Data structure for storing various metrics between a source and destination device
    Represents One Way Communication
    """

    def __init__(self,
                 source: str,
                 destination: str,
                 source_name: str = None,
                 destination_name: str = None):

        if not isinstance(source, str):
            raise TypeError(f"Source: {source} -- must be of type string")

        if not isinstance(destination, str):
            raise TypeError(f"Destination: {destination} -- must be of type string")

        if source_name and not isinstance(source_name, str):
            raise TypeError(f"Source Name: {source_name} must be of type string")

        if destination_name and not isinstance(destination_name, str):
            raise TypeError(f"Destination Name: {destination_name} must be of type string")

        self._source = source
        self._destination = destination
        self._source_host_name = source_name
        self._destination_host_name = destination_name

        self._protocols: dict = dict()
        self._counter: int = 0

    def increment(self):
        """
        Increments counter by 1
        """
        self.counter += 1

    @property
    def counter(self) -> int:
        """
        Number of times a packet has been seen with the source and destination IP address
        (regardless of protocol
        :return: int
        """
        return self._counter

    @counter.setter
    def counter(self, value):
        self._counter = value


    @property
    def source(self) -> str:
        """
        Source IP Address
        :return: IP Address as str
        """
        return self._source

    @property
    def destination(self) -> str:
        """
        Destination IP Address
        :return: IP address as str
        """
        return self._destination

    @property
    def destination_host_name(self) -> str:
        """
        Hostname for destination device
        :return: hostname (if available for destination device), otherwise None
        """
        return self._destination_host_name

    @property
    def source_host_name(self) -> str:
        """
        Hostname for source device
        :return: hostname (if available for source device), otherwise None
        """
        return self._source_host_name

    @property
    def source_label(self, include_ip_address: bool = True) -> str:
        """
        Label that will be used when rendering
        :param include_ip_address: Default True: If Hostname is available -- should IP address still be displayed?
        :return: str
        """
        if self.source_host_name:
            text = [self.source_host_name]

            if include_ip_address:
                text.insert(0, self.source)
        else:
            text = [self.source]

        return "\n".join(text)

    @property
    def id(self) -> str:
        """
        This method of identification is not only unique, but allows us to know the flow of traffic!
        :return: string id. Format is "x.x.x.x y.y.y.y" -- where X = Source, Y = destination
        """
        return f"{self.source} {self.destination}"

    @property
    def destination_label(self, include_ip_address: bool = True) -> str:
        """
        Label that will be used when rendering
        :param include_ip_address: Default True: If hostname is available -- should IP address still be displayed?
        :return: str
        """
        if self.destination_host_name:
            text = [self.destination_host_name]

            if include_ip_address:
                text.insert(0, self.destination)
        else:
            text = [self.destination]

        return "\n".join(text)

    def add_protocol(self, protocol: str):
        """
        This adds the protocol to the list of used protocols between source/destination
            If already tracked -- increments counter by 1
            Otherwise: sets the counter for said protocol to 1
        :param protocol: string representation of protocol
        """
        # validation check
        if not isinstance(protocol, str):
            raise TypeError(f"TrafficItem.add_protocol: protocol must be of type string")

        if self._protocols.get(protocol, None):
            self._protocols[protocol] += 1
        else:
            self._protocols[protocol] = 1

        self.increment()

    def __protocols__(self) -> str:
        """
        Text Represenation of protocols utilized by this instance
        :return:
        """
        text = ""
        for proto, count in self._protocols.items():
            text += f"\t\t{proto}: {count}\n"

        return text

    def __str__(self):
        sname = f" ({self.source_host_name})" if self.source_host_name else ""
        dname = f" ({self.destination_host_name})" if self.destination_host_name else ""

        return f"From {self.source}{sname} to {self.destination}{dname}\n" \
               f"\tCount: {self.counter}\n" \
               f"\tProtocols:\n" \
               f"{self.__protocols__()}"
