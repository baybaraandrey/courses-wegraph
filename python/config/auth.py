from django.conf import settings
from django.urls import re_path
from django.utils.decorators import method_decorator


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


class CustomObtainJSONWebToken(TokenObtainPairView):
    @method_decorator(decorator=swagger_auto_schema(
        tags=['jwt-auth'],
        operation_summary=(
            'Obtaining a token pair via a POST included '
            'the users username and password.'
        ),
        operation_description=(
            'Obtaining a token pair via a POST included '
            'the users username and password.'
            ' https://django-rest-framework-simplejwt.readthedocs.io/'
        ),
        responses={
            201: None,
            200: openapi.Schema(
                title='TokenObtainPairResponse',
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(
                        title='access',
                        type=openapi.TYPE_STRING,
                        description='ACCESS_TOKEN_LIFETIME: %s' % (
                            settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                        ),
                    ),
                    'refresh': openapi.Schema(
                        title='refresh',
                        type=openapi.TYPE_STRING,
                        description='REFRESH_TOKEN_LIFETIME: %s' % (
                            settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                        ),
                    ),
                },
            ),
        },
    ))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomRefreshJSONWebToken(TokenRefreshView):
    @method_decorator(decorator=swagger_auto_schema(
        tags=['jwt-auth'],
        operation_summary='Obtain a brand new access token'
                          ' with renewed expiration time',
        operation_description='Obtain a brand new access token'
                          ' with renewed expiration time',
        responses={
            201: None,
            200: openapi.Schema(
                title='TokenRefreshResponse',
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(
                        title='access',
                        type=openapi.TYPE_STRING,
                        description='ACCESS_TOKEN_LIFETIME: %s' % (
                            settings.SIMPLE_JWT[
                                'ACCESS_TOKEN_LIFETIME'],
                        ),
                    ),
                },
            ),
        },
    ))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomVerifyJSONWebToken(TokenVerifyView):
    @method_decorator(decorator=swagger_auto_schema(
        tags=['jwt-auth'],
        operation_summary='Confirmation that the JWT is valid',
        operation_description='Confirmation that the JWT is valid.'
                              ' If valid returns empty json.',
        responses={
            201: None,
            200: openapi.Schema(
                title='TokenVerifyResponse',
                type=openapi.TYPE_OBJECT,
                properties={},
            ),
        },
    ))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


obtain_jwt_token = CustomObtainJSONWebToken.as_view()
refresh_jwt_token = CustomRefreshJSONWebToken.as_view()
verify_jwt_token = CustomVerifyJSONWebToken.as_view()


app_name = 'jwt_auth'
urlpatterns = [
    re_path(r'^token/$', obtain_jwt_token,
            name='obtain-jwt-token-pairs'),
    re_path(r'^token/refresh/$', refresh_jwt_token,
            name='refresh-jwt-access-token'),
    re_path(r'^token/verify/$', verify_jwt_token,
            name='verify-jwt-token'),
]
