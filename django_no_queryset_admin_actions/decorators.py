from functools import wraps
from types import FunctionType
from typing import overload

from django.contrib.admin import ModelAdmin
from django.db.models import QuerySet
from django.http import HttpRequest

from .utils import (
    is_no_queryset_action,
    mark_as_no_queryset_action,
)


@overload
def no_queryset_action(function: FunctionType) -> FunctionType: ...


@overload
def no_queryset_action(
    *, permissions: "list[str] | None" = None, description: "str | None" = None
) -> FunctionType: ...


def no_queryset_action(
    function: "FunctionType | None" = None,
    *,
    permissions: "list[str] | None" = None,
    description: "str | None" = None,
):
    """
    Decorator that removes `queryset` parameter from being passed to action function.
    """

    def decorator(action_function):
        if is_no_queryset_action(action_function):
            return action_function

        @wraps(action_function)
        def wrapper(*args):

            # Compatibility with django-admin-action-forms
            modeladmin: ModelAdmin = args[0]
            request: HttpRequest = args[1]
            rest = [arg for arg in args[2:] if not isinstance(arg, QuerySet)]

            return action_function(modeladmin, request, *rest)

        mark_as_no_queryset_action(wrapper)

        if permissions is not None:
            setattr(wrapper, "allowed_permissions", permissions)

        if description is not None:
            setattr(wrapper, "short_description", description)

        return wrapper

    if function is None:
        return decorator
    else:
        return decorator(function)
