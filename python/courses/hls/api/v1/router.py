from django.conf.urls import re_path

from .views import (
    CategoryListView,
    CourseListView,
)

api_urlpatterns = [
    re_path(
        r'^course/hls/category/$',
        CategoryListView.as_view(),
        name='courses-hls-category-list',
    ),
    re_path(
        r'^course/hls/category/(?P<pk>\d+)/course/$',
        CourseListView.as_view(),
        name='courses-hls-course-list',
    ),
]
