from logging import getLogger
from pickle import HIGHEST_PROTOCOL, dump as pickle_dump, load as pickle_load
from typing import Any, Dict, Optional


class CacheBase:
    """Base class for key-value cache"""
    conn_string: str
    logger: Any  # avoid getLoggerClass()

    def __init__(self, conn_string: str) -> None:
        self.conn_string = conn_string
        self.logger = getLogger()

    def __getitem__(self, key: str) -> Any:
        raise NotImplementedError

    def __setitem__(self, key: str, value: Any) -> None:
        raise NotImplementedError

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def save(self) -> None:
        raise NotImplementedError


class PickledDictCache(CacheBase):
    """A simple storage implementation. Too memory-greedy for large-scale usage."""
    values: Dict[str, Any]

    def __init__(self, conn_string: str) -> None:
        super().__init__(conn_string)
        try:
            with open(self.conn_string, 'rb') as f:
                self.values = pickle_load(f)
        except OSError as e:
            self.logger.warning('Can\'t open file "%s": "%s". Cache unavailable.', self.conn_string, e)
            self.values = {}

    def __getitem__(self, key: str) -> Any:
        return self.values[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.values[key] = value

    def save(self) -> None:
        try:
            with open(self.conn_string, 'wb') as f:
                pickle_dump(self.values, f, protocol=HIGHEST_PROTOCOL)
        except OSError as e:
            self.logger.error('Can\'t open file "%s": "%s" for writing. Cache not saved.', self.conn_string, e)
