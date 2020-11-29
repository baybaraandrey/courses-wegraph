from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

User = get_user_model()


class CheckUsernameAvailabilitySerializer(serializers.Serializer):
    username = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Check strength',
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Already registered')

        return value


class CheckPasswordStrengthSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        validators=[validate_password],
        help_text='Check strength',
    )


class RequestPasswordRecoveryEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'The user with the specified email address does not exist',
            )
        return value


class RecoveryPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, min_length=8)
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        validators=[validate_password],
        help_text='Passwords must matches',
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        validators=[validate_password],
        help_text='Passwords must matches',
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError('Doesn\'t match passwords')

        attrs.pop('password_confirmation')

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        validators=[validate_password],
        help_text='Passwords must matches',
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        validators=[validate_password],
        help_text='Passwords must matches',
    )

    def validate(self, data):
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise serializers.ValidationError('Doesn\'t match passwords')

        data.pop('password_confirmation', None)

        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phone',
            'password',
            'password_confirmation',
        )
        write_only_fields = (
            'password',
            'password_confirmation',
        )
        extra_kwargs = {
            'email': {'required': True},
            'phone': {'required': True},
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
        validators=[validate_password],
        help_text='Just ignore it if you don\'t want to change it',
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
        validators=[validate_password],
        help_text='Just ignore it if you don\'t want to change it',
    )
    current_password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Just ignore it you don\'t want to change it',
    )

    def validate(self, data):
        password = data.get('password', '')
        password_confirmation = data.get('password_confirmation', '')
        current_password = data.get('current_password', '')

        if password or password_confirmation:
            if password != password_confirmation:
                raise serializers.ValidationError('Doesn\'t match passwords')
            if not current_password:
                raise serializers.ValidationError('Current password required')
            if not self.instance.check_password(current_password):
                raise serializers.ValidationError('Wrong current password')

        data.pop('current_password', None)
        data.pop('password_confirmation', None)

        return data

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)

        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phone',
            'password',
            'password_confirmation',
            'current_password',
        )
        write_only_fields = (
            'password',
            'password_confirmation',
            'current_password',
        )


class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
        validators=[validate_password],
        help_text='Just ignore it if you don\'t want to change it',
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'url',
            'email',
            'phone',
            'is_staff',
            'is_superuser',
            'is_active',
        ]
        extra_kwargs = {
            'url': {
                'view_name': 'api:admin-users-detail', 'lookup_field': 'id'},
            'email': {'required': True},
            'phone': {'required': True},
        }

    def create(self, validated_data):
        password = validated_data.get('password')
        if not password:
            raise serializers.ValidationError(
                'Password required',
                code='invalid',
            )

        validated_data['password'] = make_password(password)

        return super(AdminUserSerializer, self).create(validated_data)
