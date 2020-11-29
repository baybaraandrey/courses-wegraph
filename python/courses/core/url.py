from django.urls import re_path

from .views import (
    db_health,
    echo,
)

app_name = 'core'
urlpatterns = [
    re_path(r'^_echo/$', echo, name='echo'),
    re_path(r'^_health/$', db_health, name='db-health'),
]
