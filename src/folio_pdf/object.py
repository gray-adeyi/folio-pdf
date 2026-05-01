from abc import abstractmethod
import ctypes as ct


class AbstractFolioObject:
    @property
    @abstractmethod
    def handle(self) -> ct.c_uint64:
        """Returns the object handle"""
        ...
