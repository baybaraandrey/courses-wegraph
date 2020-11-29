from django.db.models import Model

from rest_framework import serializers


class ObjectExistsValidator:
    def __init__(self, ObjectModel: Model):
        self.ObjectModel = ObjectModel

    def __call__(self, value):
        id_ = value
        if not self.ObjectModel.objects.filter(id=id_).exists():
            msg = '%s with id="%d" does not exists' % (
                getattr(self.ObjectModel, '__name__', 'Object'),
                id_,
            )
            raise serializers.ValidationError(msg)


def unique_list_validator(value):
    if len(set(value)) != len(value):
        raise serializers.ValidationError(
            'List of identifiers must be unique',
        )
