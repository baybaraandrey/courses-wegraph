from rest_framework import status as http_status
from rest_framework.response import Response

from .api.serializers import MessageSerializer
from .interfaces import MessageKind


class MessageResponseMixin:

    def message_response(
            self,
            msg_data={},
            msg_kind=MessageKind.info.value,
            status=http_status.HTTP_200_OK,
            **kwargs,
    ):
        return Response(
            data=MessageSerializer(
                {
                    'kind': msg_kind,
                    'data': msg_data,
                },
            ).data,
            status=status,
            **kwargs,
        )
