from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http.response import Http404

from django_filters import rest_framework as filters

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from courses.core.api.paginations import StandardResultsSetPagination
from courses.core.api.serializers import MessageSerializer
from courses.core.mixins import MessageResponseMixin
from courses.core.pyjwt import InvalidJWTTokenError
from courses.users.utils import (
    create_password_recovery_link,
    get_tokens_for_user,
    payload_from_token,
)

from .filters import UserFilter
from .permissions import IsAdminOrOwner
from .serializers import (
    AdminUserSerializer,
    CheckPasswordStrengthSerializer,
    CheckUsernameAvailabilitySerializer,
    RecoveryPasswordSerializer,
    RequestPasswordRecoveryEmailSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)

User = get_user_model()


class CheckUsernameAvailabilityView(MessageResponseMixin, APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        tags=['jwt-auth', 'users', 'debug'],
        operation_summary='Check username availability',
        request_body=CheckUsernameAvailabilitySerializer,
        responses={
            200: openapi.Response('', MessageSerializer),
        },
    )
    def post(self, request):
        p = CheckUsernameAvailabilitySerializer(data=request.data)
        p.is_valid(raise_exception=True)
        return self.message_response(
            msg_data={
                'username': 'Username is available for registration',
            },
        )


class CheckPasswordStrengthView(MessageResponseMixin, APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        tags=['jwt-auth', 'users', 'debug'],
        operation_summary='Check password strength',
        request_body=CheckPasswordStrengthSerializer,
        responses={
            200: openapi.Response('', MessageSerializer),
        },
    )
    def post(self, request):
        p = CheckPasswordStrengthSerializer(data=request.data)
        p.is_valid(raise_exception=True)
        return self.message_response(
            msg_data={
                'password': 'Password is acceptable',
            },
        )


class UserRegistrationView(
    CreateModelMixin,
    GenericAPIView,
):
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(
        tags=['jwt-auth', 'users'],
        operation_summary='Register user via password',
        operation_description='Register user via password',
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RequestPasswordRecoveryEmailView(MessageResponseMixin, APIView):
    """Test feature"""

    permission_classes = (AllowAny,)

    def get_object(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        tags=['jwt-auth', 'users'],
        operation_summary='Request password recovery via link sended to email.',
        operation_description='Request password recovery'
                              ' via link sended to email.',
        request_body=RequestPasswordRecoveryEmailSerializer,
        responses={
            200: openapi.Response('', MessageSerializer),
        },
    )
    def post(self, request, *args, **kwargs):
        data = RequestPasswordRecoveryEmailSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        user = self.get_object(data.validated_data['email'])
        send_mail(
            subject='Password recovery',
            message='To confirm password recovery'
                    ' click on the link below \n%s' % (
                        create_password_recovery_link(uid=user.id,
                                                      sub=user.email),
                    ),
            from_email='admin@gmail.com',
            recipient_list=[data.validated_data['email']],
        )

        return self.message_response(msg_data={
            'detail': 'Confirmation mail is sended',
        })


class RecoveryPasswordView(MessageResponseMixin, APIView):
    """Test feature"""

    permission_classes = (AllowAny,)

    def get_object(self, id_):
        try:
            return User.objects.get(id=id_)
        except User.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        tags=['jwt-auth', 'users'],
        operation_summary='Verify token and set new password.',
        operation_description='Verify token and set new password.',
        request_body=RecoveryPasswordSerializer,
        responses={
            200: openapi.Response('', MessageSerializer),
        },
    )
    def post(self, request, *args, **kwargs):
        data = RecoveryPasswordSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        try:
            data.update(
                instance=self.get_object(
                    payload_from_token(
                        token=data.validated_data['token'])['uid'],
                ),
                validated_data=data.validated_data,
            )
        except InvalidJWTTokenError:
            return self.message_response(
                msg_data={
                    'detail': 'Token is invalid or expired',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return self.message_response(msg_data={
            'detail': 'Password successfully updated',
        })


class UserViewSet(
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    permission_classes = (
        IsAdminOrOwner,
        IsAuthenticated,
    )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        tags=['users'],
        operation_summary='Get my user profile.',
        operation_description='Get my user profile.',
        responses={
            200: openapi.Response('', UserSerializer),
        },
    )
    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(
        tags=['users'],
        operation_summary='Update user profile.',
        operation_description='Update user profile.',
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['users'],
        operation_summary='Patch update user profile.',
        operation_description='Patch update user profile.',
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['users'],
        operation_summary='Get user.',
        operation_description='Get user.',
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class AdminUserViewSet(
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        tags=['admin-users'],
        operation_summary='Create user profile.',
        operation_description='Create user profile.',
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['admin-users'],
        operation_summary='Get my user profile.',
        operation_description='Get my user profile.',
        responses={
            200: openapi.Response('', AdminUserSerializer),
        },
    )
    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = AdminUserSerializer(
            request.user, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(
        tags=['admin-users'],
        operation_summary='Patch update user profile.',
        operation_description='Patch update user profile.',
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['admin-users'],
        operation_summary='Update user profile.',
        operation_description='Update user profile.',
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['admin-users'],
        operation_summary='Get user.',
        operation_description='Get user.',
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['admin-users'],
        operation_summary='Delete user.',
        operation_description='Delete user.',
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AdminUserListView(ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.order_by('id').all()
    serializer_class = AdminUserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(
        tags=['admin-users'],
        operation_id='api_v1_users_filtered_users_list',
        operation_summary='Get users.',
        operation_description='Get users.',
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AdminObtainUserTokenView(APIView):
    permission_classes = (IsAdminUser,)

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        tags=['admin-users', 'jwt-auth'],
        operation_summary='Obtain JWT token pairs',
        operation_description='Obtain JWT token pairs'
                              ' for user with provided id',
        responses={
            201: None,
            200: openapi.Schema(
                title='TokenObtainPairResponse',
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(
                        title='access',
                        type=openapi.TYPE_STRING,
                    ),
                    'refresh': openapi.Schema(
                        title='refresh',
                        type=openapi.TYPE_STRING,
                    ),
                },
            ),
        },
    )
    def get(self, request, id, *args, **kwargs):
        return Response(get_tokens_for_user(self.get_object(id)))
