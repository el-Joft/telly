"""User endpoints."""
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template import loader
from django.template.loader import render_to_string
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
            user_instance.save()

            domain = current_site.domain
            # account verification
            token = account_activation_token.make_token(user_instance)
            uid = urlsafe_base64_encode(force_bytes(
                user_instance.pk))
            to_email = [
                user_instance.email,
            ]
            email_verify_template = \
                'auth/email_verification.html'
            subject = 'Telly Account Verification'
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
                'verification_link': f"{domain}/api/v1/activate/{uid}/{token}"
            }
            send_mail = SendMail(
                email_verify_template, context, subject, to_email)
            send_mail.send()

            data = {
                'status': 'success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        data = {
            'status': 'error',
            'data': serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def activate(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return Response('Thank you for your email confirmation. Now you can login your account.')
        else:
            return Response('Activation link is invalid!')
