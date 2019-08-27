from rest_framework import serializers
from rest_framework import status


class ErrorHandler():
    '''Raise errors'''

    def check_conflict(self, model, field, value, error_type=None):
        # Database integrity error
        message = f'{model} with {field} {value}, already exists!'
        if error_type is not None:
            raise error_type({'error': message})
        raise serializers.ValidationError(message)

    def db_object_do_not_exists(self, model, field, value, error_type=None):
        error = {
            'status': status.HTTP_404_NOT_FOUND,
            'message': f'{model} with { field } { value } does not exist.',
        }

        if error_type is not None:
            raise error_type({'error': error})
        raise serializers.ValidationError(
            error, status.HTTP_404_NOT_FOUND)

    def custom_message(self, message, error_type=None):
        # custom message error
        if error_type is not None:
            raise error_type({'error': message})
        raise serializers.ValidationError(message)


errors = ErrorHandler()
