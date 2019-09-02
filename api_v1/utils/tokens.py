import datetime
import jwt
from rest_framework import exceptions
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.conf import settings


class TokenGenerator(PasswordResetTokenGenerator):
    """
        This cal
    """
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )

    def encode_token(self, payload: dict) -> str:
        return jwt.encode(
            {'data': payload, 'iat': datetime.datetime.utcnow(),
             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2)},
            settings.SECRET, algorithm='HS256')

    def decode_token(self, token: str):
        try:
            return jwt.decode(token, settings.SECRET)
        except jwt.InvalidSignatureError as e:
            raise exceptions.AuthenticationFailed(e)


account_activation_token = TokenGenerator()
