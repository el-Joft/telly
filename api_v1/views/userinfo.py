"""User endpoints."""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api_v1.models import User
from api_v1.serializers.user import UsersSerializer


class UserInfoViewSet(ViewSet):
    """UserInfo viewset."""
    permission_classes = (IsAuthenticated,)
    serializer_class = UsersSerializer
    queryset = User.objects.all()

    def list(self, request):
        """
        List all users

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
        print(request.user)

        return Response({}, status=status.HTTP_200_OK)
