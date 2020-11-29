from collections import OrderedDict
from enum import Enum


class ExporterException(Exception):
    pass


class IExporter:
    @staticmethod
    def from_iterable(
            mapped: OrderedDict,
            iterable,
            format='xlsx',
            *args,
            **kwargs,
    ):
        raise NotImplementedError


class StrEnum(Enum):
    @classmethod
    def choices(cls):
        return [
            (tag.name, tag.value)
            for tag in cls
        ]

    @classmethod
    def to_dict(cls):
        return {
            tag.name: tag.value
            for tag in cls
        }


# global
class MessageKind(StrEnum):
    info = 'info'

