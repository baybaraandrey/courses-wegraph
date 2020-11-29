from django.db import connection
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status


def error404(request, exception, *args, **kwargs):
    """
    Generic 404 error handler.
    """
    data = {
        'detail': 'Not found.',
    }
    return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)


def index(request):
    return redirect('core:db-health')


@csrf_exempt
def echo(request):
    return JsonResponse(
        {
            'path': request.path,
            'method': request.method,
            'agent': request.headers.get('User-Agent'),
        },
    )


def db_health(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
        res = cursor.fetchone()
    return JsonResponse(
        {
            'status': res[0],
        },
    )
