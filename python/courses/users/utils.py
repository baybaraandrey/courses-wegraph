from datetime import datetime, timedelta
from functools import partial
from urllib.parse import urlencode

from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken

from courses.core.pyjwt import decode, encode


PASSWORD_RECOVERY_AUD = 'PASSWORD_RECOVERY'


def _encode(
        ttl,
        now,
        audience,
        uid,
        sub,
        key=settings.JWT_SECRET_KEY,
        **kwargs,
):
    return encode(
        payload={
            'aud': audience,
            'exp': now + ttl,
            'iat': now,
            'uid': uid,
            'sub': sub,
        },
        key=key,
        **kwargs,
    )


def _decode(
        jwt_token,
        audience,
        key=settings.JWT_SECRET_KEY,
        **kwargs,
):
    return decode(
        jwt_token=jwt_token,
        audience=audience,
        key=key,
        **kwargs,
    )


encode_password_recovery_token = partial(
    _encode, audience=[PASSWORD_RECOVERY_AUD])
decode_password_recovery_token = partial(
    _decode, audience=[PASSWORD_RECOVERY_AUD])


def create_password_recovery_link(uid, sub):
    ttl = timedelta(
        minutes=settings.JWT_RECOVERY_PASSWORD_TOKEN_LIFETIME,
    )
    return '%s?%s' % (
        settings.RECOVERY_PASSWORD_REDIRECT_URL,
        urlencode(
            {
                'token': encode_password_recovery_token(
                    uid=uid,
                    sub=sub,
                    now=datetime.utcnow(),
                    ttl=ttl,
                    key=settings.JWT_SECRET_KEY,
                ),
            },
        ),
    )


def payload_from_token(token):
    return decode_password_recovery_token(
        token,
        key=settings.JWT_SECRET_KEY,
    )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
