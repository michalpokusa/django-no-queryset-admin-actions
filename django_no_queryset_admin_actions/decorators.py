from functools import wraps
from types import FunctionType


NO_QUERYSET_ACTION_ATTRIBUTE = "no_queryset_action"


def no_queryset_action(action_function: FunctionType):
    """
    Decorator to remove `queryset` parameter from being passed to action function.
    """

    if getattr(action_function, NO_QUERYSET_ACTION_ATTRIBUTE, None) is not None:
        return action_function

    @wraps(action_function)
    def wrapper(*args, **kwargs):
        modeladmin, request, queryset, *rest = args
        return action_function(modeladmin, request, *rest, **kwargs)

    setattr(wrapper, NO_QUERYSET_ACTION_ATTRIBUTE, True)

    return wrapper
