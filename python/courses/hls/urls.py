from django.urls import re_path, path

from .views import IndexView, SubCategoryListView, CourseDetailView

app_name = 'hls'
urlpatterns = [
    re_path('^$', IndexView.as_view(), name='index'),
    path('courses/<str:subcategory>/', SubCategoryListView.as_view(),
         name='subcategory_detail'),
    path('course/<str:course>/', CourseDetailView.as_view(),
         name='course_detail'),
]
