from .SerializableObject import SerializableObject
from .TrafficItem import TrafficItem


class FlagRule(SerializableObject):
    """
    Data structure which helps determine 'interesting traffic'
    Anything deemed 'interesting' can be colored differently
    """
    def __init__(self, origin_ip: list, destination_ips: list, color: str = "black"):
        """
        :param origin_ip: If traffic originates from these IP addresses
        :param destination_ips: If traffic from origin goes to any of the IPs in this list
        :param color: Communication line will be colored this color (if criteria is met)
        """
        if not origin_ip or not destination_ips or not color:
            print("FlagRule: origin_ip, destination_ips, and color arguments are requried")
            exit(1)

        if not isinstance(origin_ip, list):
            print("FlagRule: origin_ip must be of type list")
            exit(1)

        if not isinstance(destination_ips, list):
            print("FlagRule: destination_ips must be of type list (array of strings)")
            exit(1)

        if not isinstance(color, str):
            print("FlagRule: color must be of type string")
            exit(1)

        self._origin = origin_ip
        self._destinations = destination_ips
        self._color = color

    @property
    def color(self) -> str:
        """
        Color to use when rendering this rule
        :return: str
        """
        return self._color

    @property
    def origin(self) -> list:
        """
        IP Address of origin device
        :return: str
        """
        return self._origin

    @property
    def destinations(self) -> list:
        """
        Destination IP addresses
        :return: list
        """
        return self._destinations

    def matches(self, traffic: TrafficItem) -> bool:
        """
        Determines if provided TrafficItem shall utilize this rule when rendered
        :param traffic: TrafficItem instance
        :return: true if item should use this rule, otherwise false
        """
        return traffic.source in self.origin and traffic.destination in self.destinations