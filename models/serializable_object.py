import json
import abc


class SerializableObject(metaclass=abc.ABCMeta):
    """
    Base class for ensuring entities are serializable (to JSON)
    """

    def to_json(self):
        """
        Convert this instance into JSON
        :return: JSON string
        """
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)

    def __repr__(self):
        return self.to_json()