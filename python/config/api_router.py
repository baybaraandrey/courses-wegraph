from django.urls import include, re_path


from courses.core.api.router import api_urlpatterns as api_core
from courses.hls.api.v1.router import api_urlpatterns as api_v1_hls
from courses.users.api.v1.router import api_urlpatterns as api_v1_users

app_name = 'api'
api_urlpatterns_v1 = [
    re_path(r'^', include(api_core)),
    re_path(r'^', include(api_v1_users)),
    re_path(r'^', include(api_v1_hls)),
]
urlpatterns = [
    re_path(r'^v1/', include(api_urlpatterns_v1)),
]
