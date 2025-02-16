from types import FunctionType


NO_QUERYSET_ACTION_ATTRIBUTE = "no_queryset_action"


def is_no_queryset_action(function: FunctionType) -> bool:
    return getattr(function, NO_QUERYSET_ACTION_ATTRIBUTE, False)


def mark_as_no_queryset_action(function: FunctionType):
    setattr(function, NO_QUERYSET_ACTION_ATTRIBUTE, True)
