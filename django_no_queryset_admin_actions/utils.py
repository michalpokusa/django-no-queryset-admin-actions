from types import FunctionType


NO_QUERYSET_ACTION_ATTRIBUTE = "no_queryset_action"
OPTIONAL_QUERYSET_ACTION_ATTRIBUTE = "optional_queryset_action"


def is_no_queryset_action(function: FunctionType) -> bool:
    return getattr(function, NO_QUERYSET_ACTION_ATTRIBUTE, False)


def is_optional_queryset_action(function: FunctionType) -> bool:
    return getattr(function, OPTIONAL_QUERYSET_ACTION_ATTRIBUTE, False)


def mark_as_no_queryset_action(function: FunctionType):
    setattr(function, NO_QUERYSET_ACTION_ATTRIBUTE, True)


def mark_as_optional_queryset_action(function: FunctionType):
    setattr(function, OPTIONAL_QUERYSET_ACTION_ATTRIBUTE, True)
