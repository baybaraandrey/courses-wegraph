from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path

from .swagger import urlpatterns as swagger_urlpatterns

handler404 = 'courses.core.views.error404'

urlpatterns = [
    # Django Admin
    re_path(settings.ADMIN_URL, admin.site.urls),
    # Courses core
    re_path(r'^', include('courses.core.url')),
]

# API
urlpatterns += [
    re_path(r'^api/', include('config.api_router')),
    re_path(r'^jwt/', include('config.auth')),
    re_path(r'^', include(swagger_urlpatterns)),
]

# Templates
urlpatterns += [
    re_path('^', include('courses.hls.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
