from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import ListAPIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from courses.core.api.paginations import StandardResultsSetPagination
from courses.hls.models import Category, Course


from .serializers import CategorySerializer, CourseSerializer


class CategoryListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.queryset

    @swagger_auto_schema(
        tags=['hls'],
        operation_summary='Get hls courses categories.',
        operation_description='Get hls courses categories.',
        responses={
            200: openapi.Response('', CategorySerializer(many=True)),
        },
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CourseListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.queryset.filter(category_id=self.kwargs.get('pk', 0))

    @swagger_auto_schema(
        tags=['hls'],
        operation_summary='Get hls courses.',
        operation_description='Get hls courses.',
        responses={
            200: openapi.Response('', CourseSerializer(many=True)),
        },
    )
    def get(self, request, pk, *args, **kwargs):
        return super().list(request, *args, **kwargs)
