from abc import abstractmethod
import ctypes as ct


class AbstractFolioObject:
    _requires_close: bool

    @property
    @abstractmethod
    def handle(self) -> ct.c_uint64:
        """Returns the object handle"""
        ...

    def close(self):
        err_msg = (
            "close method has not been implemented for folio object"
            if self._requires_close
            else "folio object does not require close"
        )
        raise NotImplementedError(err_msg)

    def __enter__(self):
        return self

    def __exit__(self):
        if self._requires_close:
            self.close()
