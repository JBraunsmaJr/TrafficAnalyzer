from .SerializableObject import SerializableObject


class RenderRule(SerializableObject):
    """
    Data structure which stores basic rule information for rendering
    Shape, Color, IP/IP Prefix
    """

    def __init__(self, prefix: str, shape: str = "ellipsis", color="lightgrey"):
        """
        :param prefix:
        :param shape:
        :param color:
        """

        if not isinstance(prefix, str):
            print("RenderRule: prefix must be of type string")
            exit(1)

        if not isinstance(shape, str):
            print("RenderRule: shape must be of type string")
            exit(1)

        if not isinstance(color, str):
            print("RenderRule: color must be of type string")
            exit(1)

        self._prefix = prefix
        self._shape = shape
        self._color = color

    @property
    def prefix(self) -> str:
        """
        Prefix which specifies whether or not to apply rule settings
        :return: str
        """
        return self._prefix

    @property
    def shape(self) -> str:
        """
        Shape to use when rendering item
        :return: str
        """
        return self._shape

    @property
    def color(self) -> str:
        """
        Color to use when rendering item
        :return: str
        """
        return self._color

    def matches(self, ip: str) -> bool:
        """
        Returns true if IP Address meets the prefix criteria
        :param ip: IP Address (string format)
        :return: true if match, otherwise false
        """
        return ip.startswith(self.prefix) or ip == self.prefix
