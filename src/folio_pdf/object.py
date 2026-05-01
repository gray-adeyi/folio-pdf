from abc import abstractmethod


class AbstractFolioObject:
    @property
    @abstractmethod
    def handle(self) -> int:
        """Returns the object handle"""
        ...
