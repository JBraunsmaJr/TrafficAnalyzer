class Serializable:
    def __init__(self):
        self._id = id(self)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def serialize(self):
        raise NotImplemented()

    def deserialize(self):
        raise NotImplemented()