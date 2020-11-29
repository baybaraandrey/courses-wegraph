from collections import OrderedDict

from django.http import FileResponse
from django.utils.decorators import method_decorator

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from courses.core.services import DocExporter
from courses.core.utils import file_from_bytes

from .renderers import XlsxRenderer


class DebugXlsxFileView(APIView):
    renderer_classes = (XlsxRenderer, )

    @method_decorator(decorator=swagger_auto_schema(
        tags=['debug'],
        operation_summary='Returns test xlsx file.',
        operation_description='Returns test xlsx file.',
        responses={
            200: openapi.TYPE_FILE,
        },
    ))
    def get(self, request):
        bytes_ = DocExporter.from_iterable(
            OrderedDict({
                'field1': 'TitleField1',
                'field2': 'TitleField2',
            }),
            [
                {
                    'field1': 'x**2',
                    'field2': 'y**3',
                },
                {
                    'field1': 'z**2',
                    'field2': 'w**3',
                },
            ],
        )

        doc = file_from_bytes(bytes_)

        response = FileResponse(doc)
        response['Content-Disposition'] = 'attachment; filename=test.xlsx'

        return response


class DebugTriggerError(APIView):
    permission_classes = (IsAdminUser, )

    @method_decorator(decorator=swagger_auto_schema(
        tags=['debug'],
        operation_summary='Trigger an error.',
        operation_description='Trigger an error.',
        responses={
            500: openapi.TYPE_STRING,
        },
    ))
    def get(self, request):
        impossible = 1 / 0 # noqa
