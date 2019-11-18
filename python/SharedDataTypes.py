from abc import abstractmethod, ABC


class Serializable(ABC):
    @abstractmethod
    def to_dict(self):
        pass