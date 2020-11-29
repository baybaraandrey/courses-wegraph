from rest_framework import serializers

from courses.core.interfaces import MessageKind


class JSONSerializableMultipleChoiceField(serializers.MultipleChoiceField):
    def to_internal_value(self, data):
        return list(super().to_internal_value(data))


class MessageSerializer(serializers.Serializer):
    kind = serializers.ChoiceField(
        choices=MessageKind.choices(),
        default=MessageKind.info.value,
    )
    data = serializers.JSONField(
        default={
            'status': 'ok',
        },
    )
