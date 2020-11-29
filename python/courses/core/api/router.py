from django.conf.urls import re_path

from .views import (
    DebugTriggerError,
    DebugXlsxFileView,
)


api_urlpatterns = [
    re_path(
        r'^debug/test.xlsx$',
        DebugXlsxFileView.as_view(),
        name='debug-test-xlsx-file',
    ),
    re_path(
        r'^debug/trigger_error/$',
        DebugTriggerError.as_view(),
        name='debug-trigger-error',
    ),
]
