from abc import abstractmethod


class AbstractPDFElement:
    @property
    @abstractmethod
    def handle(self): ...
