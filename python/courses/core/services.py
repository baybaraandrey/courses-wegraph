from collections import OrderedDict

import tablib

from .interfaces import ExporterException, IExporter


class DocExporter(IExporter):
    @staticmethod
    def from_iterable(
            mapped: OrderedDict,
            iterable,
            format='xlsx',
            *args,
            **kwargs,
    ):
        data = tablib.Dataset(headers=mapped.values())
        for item in iterable:
            values = []
            for field in mapped.keys():
                try:
                    value = getattr(item, field)
                except AttributeError:
                    try:
                        value = item[field]
                    except (KeyError, TypeError):
                        raise ExporterException(
                            'Cannot retrieve field value %s' % field,
                        )

                values.append(value)
            data.append(values)

        return data.export(format=format)
