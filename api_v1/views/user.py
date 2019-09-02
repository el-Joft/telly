"""User endpoints."""
from django.contrib.auth.hashers import check_password
from django.contrib.auth import user_logged_in
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api_v1.models import Role, User
from api_v1.serializers.user import UsersSerializer
from api_v1.utils.database import get_model_object
from api_v1.utils.tokens import account_activation_token
from api_v1.utils.app_utils.send_mail import SendMail


class UserViewSet(ViewSet):
    """Users viewset."""
    serializer_class = UsersSerializer
    queryset = User.objects.all()

    def create(self, request):
        """
        Create a user

        If successful, response payload with:
            - status: 200
            - data

        If unsuccessful, a response payload with:
            - status: 400
            - error: Bad Request
            - message
            Status Code: 400
        Request
        -------
        method: post
        url: /api/v1/register/
        """
        serializer = UsersSerializer(
            data=request.data)
        current_site = get_current_site(request)
        if serializer.is_valid():
            role = get_model_object(Role, 'role_type', 'User')
            user_instance = serializer.save(role=role)
            user_instance.set_password(user_instance.password)
            token = account_activation_token.make_token(user_instance)
            user_instance.save()

            domain = current_site.domain
            # account verification
            uid = urlsafe_base64_encode(force_bytes(
                user_instance.pk))
            to_email = [
                user_instance.email,
            ]
            email_verify_template = \
                'auth/email_verification.html'
            subject = 'Telly Account Verification'
            verify_token = f"{domain}/api/v1/activate/{uid}/{token}"
            context = {
                'template_type': 'Verify your email',
                'small_text_detail': 'Thank you for '
                                     'creating a Telly account. '
                                     'Please verify your email '
                                     'address to set up your account.',
                'email': user_instance.email,
                'domain': domain,
                'uid': uid,
                'token': token,
                'verification_link': verify_token
            }
            send_mail = SendMail(
                email_verify_template, context, subject, to_email)
            send_mail.send()

            data = {
                'status': 'success',
                'data': serializer.data,
                'verification': verify_token
            }
            return Response(data, status=status.HTTP_201_CREATED)
        data = {
            'status': 'error',
            'data': serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def activate(self, request, uidb64, token):
        """
               Activate User token

               If successful, response payload with:
                   - status: 200
                   - data

               If unsuccessful, a response payload with:
                   - status: 400
                   - error: Bad Request
                   - message
                   Status Code: 400
               Request
               -------
               method: get
               url: /api/v1/activate/token
               """
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and \
                account_activation_token.check_token(user, token):
            user.active = True
            user.save()
            return Response(
                'Thank you for your email confirmation. '
                'Now you can login your account.')
        else:
            return Response('Activation link is invalid!')

    def login(self, request, *args, **kwargs):
        """
            Login User

              If successful, response payload with:
                  - status: 200
                  - token

              If unsuccessful, a response payload with:
                  - status: 403
                  - error: Unauthorize
                  - message
                  Status Code: 403
              Request
              -------
              method: post
              url: /api/v1/login
        """
        if not request.data:
            return Response(
                {'error': "Please provide username/password"},
                status=status.HTTP_400_BAD_REQUEST)
        username = request.data['username']
        password = request.data['password']

        try:
            user = User.objects.get(username=username)
            match_password = check_password(password, user.password)
            if not match_password:
                return Response({
                    'error': 'Invalid username/password',
                }, status=status.HTTP_400_BAD_REQUEST)

            if user is not None:
                if user.is_active:
                    payload = {
                        'email': user.email,
                        'role': user.role.role_type,
                        'username': user.username,
                        'firstName': user.first_name,
                        'lastName': user.last_name,
                        'mobileNumber': user.mobile_number
                    }
                    token = account_activation_token.encode_token(payload)
                    user.token = token
                    user.save()
                    jwt_token = {'token': token}
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)

                    return Response(data=jwt_token, status=status.HTTP_200_OK)
                else:
                    data = {
                        'error': 'Inactive account, '
                                 'check your mail to activate your account'
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({
                'error': 'Invalid username/password',
            }, status=status.HTTP_400_BAD_REQUEST)
