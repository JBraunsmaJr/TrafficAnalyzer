import abc
import uuid


class Tool(metaclass=abc.ABCMeta):
    def __init__(self, data_type=str.__class__, name=None):
        self._data_type = data_type

        # default name will be something completely random
        # for identification purposes (don't want None)
        if not name:
            self._name = uuid.uuid4()
        else:
            self._name = name

    @abc.abstractmethod
    def run(self):
        pass

    @property
    def data_type(self):
        """
        Retrieves the type of data (singular)
        That this tool returns
        """
        return self._data_type

    @property
    def name(self):
        """
        Retrieves the name/ID of this tool
        """
        return self._name
