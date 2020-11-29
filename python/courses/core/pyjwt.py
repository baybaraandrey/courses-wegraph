import jwt
from jwt.exceptions import InvalidTokenError as PyJWTInvalidTokenError


class InvalidJWTTokenError(Exception):
    pass


def encode(payload, key, **kwargs):
    return jwt.encode(
        payload=payload,
        key=key,
        algorithm='HS256',
        **kwargs,
    ).decode('ascii')


def decode(jwt_token, key, **kwargs):
    try:
        return jwt.decode(
            jwt=jwt_token,
            key=key,
            verify=True,
            algorithms=['HS256', 'HS384', 'HS512'],
            **kwargs,
        )
    except PyJWTInvalidTokenError as e:
        raise InvalidJWTTokenError from e
