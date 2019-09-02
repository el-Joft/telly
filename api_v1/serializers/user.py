from api_v1.models.user import User
# rest_framework
from rest_framework import serializers
from api_v1.models.role import Role
import re


class RolesSerializer(serializers.ModelSerializer):
    """Roles Model Serializer."""

    class Meta:
        """Access fields and create returned object."""

        model = Role
        fields = ('role_type',)


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    """
    Users Model Serializer.
    """
    role = RolesSerializer(read_only=True)
    # this code was commented out intensionally
    # role_id = serializers.SlugRelatedField(
    #     queryset=Role.objects.all(),
    #     slug_field='pk', write_only=True, source='role',
    #     required=True)

    class Meta:
        """Access fields and create returned object."""
        model = User
        fields = ('id', 'first_name', 'email', 'role', 'mobile_number',
                  'last_name', 'username', 'password', 'token',
                  'created_at', 'updated_at',)
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, validated_data):
        errors = []
        for (key, value) in validated_data.items():
            if key == 'password':
                if re.match('^([a-z]*|[A-Z]*|[0-9]*|.{0,7})$', value):
                    errors.append(
                        "Password must contain a Number,"
                        + " a letter and 8 charcters long"
                    )
            if key == 'mobile_number':
                if not re.match(
                    "^(\(?\+?[0-9]*\)?)?[0-9_\- \(\)]*$", value):  # noqa: E731
                    errors.append(
                        "Mobile Number must be valid e.g. (+44)(0)20-12341234"
                    )
        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return validated_data
