"""User endpoints."""
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from api_v1.models import User
from api_v1.models import Role
from api_v1.serializers.user import UsersSerializer
from api_v1.utils.database import get_model_object


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
        if serializer.is_valid():
            role = get_model_object(Role, 'role_type', 'User')
            user_instance = serializer.save(role=role)
            user_instance.set_password(user_instance.password)
            user_instance.save()
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
