from django.core.exceptions import ObjectDoesNotExist
from api_v1.utils.error_handler import errors


def get_model_object(model, column_name, column_value, **kwargs):
    """
    Gets model instance from the database by a crertain field.

    Args:
        model: Holds the model from which we want to query data
        column_name: Holds the model field to query data by from the model.
        column_value: Holds the value for the column_name.
        kwargs : Hold optional keyword arguments.
        message: Holds a custom error message(it's optional).
        error: Holds a error type to raise incase it's not GraphQlError
               (it's optional).

    Returns:
        model_instance: If the value exists.
        error: Else expection is raised with appropriate message.
    """
    try:
        model_instance = model.objects.get(**{column_name: column_value})
        return model_instance
    except ObjectDoesNotExist:
        message = kwargs.get('message', None)
        error_type = kwargs.get('error_type', None)
        if message is not None:
            errors.custom_message(message, error_type=error_type)
        errors.db_object_do_not_exists(
            model.__name__, column_name, column_value, error_type=error_type)
