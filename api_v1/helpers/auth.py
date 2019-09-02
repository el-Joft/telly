import jwt
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.authentication import (
    get_authorization_header, BaseAuthentication)
from api_v1.models.user import User
from api_v1.utils.tokens import account_activation_token


class TokenAuthentication(BaseAuthentication):
    """
      A class used for Token Authentication
      ...

      Attributes
      ----------
      request : dict
         request sent from the client
      token: str
         jwt token generated sent by the client
      Methods
      -------
      authenticate(request)
          checks the token sent by the client
      authenticate_credentials(request)
        checks the payload contained in the user token
      """

    def authenticate(self, request):
        """
        Method to authenticate the user token
        :param request: dict which is sent by the client
        :return: user and token generated
        """
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'bearer':
            return None

        if len(auth) < 2:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, token):
        """
        Validates the user payload in the token
        :param token: string
        :return: user and token generated
        """
        payload = account_activation_token.decode_token(token)
        email = payload['data']['email']
        username = payload['data']['username']
        first_name = payload['data']['firstName']
        last_name = payload['data']['lastName']
        mobile_number = payload['data']['mobileNumber']
        msg = {'Error': "Token mismatch", 'status': "401"}
        try:
            user = User.objects.get(
                email=email, first_name=first_name,
                last_name=last_name,
                username=username, mobile_number=mobile_number,
                active=True
            )
            if not eval(user.token) == token:
                raise exceptions.AuthenticationFailed(msg)

        except jwt.ExpiredSignature or jwt.DecodeError or \
                jwt.InvalidTokenError:
            return Response(
                {'Error': "Token is invalid"},
                status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response(
                {'Error': "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return user, token
