from contextlib import contextmanager
from types import FunctionType

from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.http import HttpRequest, HttpResponseRedirect
from django.http.request import QueryDict
from django.utils.translation import gettext

from .decorators import no_queryset_action, optional_queryset_action
from .utils import is_no_queryset_action, is_optional_queryset_action


@contextmanager
def mutable_querydict(querydict: QueryDict):
    """
    Context manager that makes `QueryDict` mutable for the duration of the block.
    """
    querydict._mutable = True
    yield querydict
    querydict._mutable = False


class truthy_list(list):
    """
    Used instead of empty `list` in `ModelAdmin.changelist_view` method to pass
    check for selected items.
    """

    def __bool__(self):
        return True


def patched_getlist(self: QueryDict, key: str, default=None):
    """
    Monkey-patched method for `QueryDict` class to return `truthy_list` instead of
    empty `list` when `key` is `ACTION_CHECKBOX_NAME`, which is used to check
    if any items are selected.
    """
    items = super(QueryDict, self).getlist(key, default)

    return truthy_list(items) if key == helpers.ACTION_CHECKBOX_NAME else items


class NoQuerySetAdminActionsMixin(admin.ModelAdmin):

    no_queryset_actions: "list[str | FunctionType]" = ()
    optional_queryset_actions: "list[str | FunctionType]" = ()

    def get_actions(self, request: HttpRequest):
        no_queryset_action_names = [
            action.__name__ if callable(action) else action
            for action in self.no_queryset_actions or []
        ]
        optional_queryset_action_names = [
            action.__name__ if callable(action) else action
            for action in self.optional_queryset_actions or []
        ]

        actions = dict()

        for function, name, description in super().get_actions(request).values():

            if name in no_queryset_action_names:
                actions[name] = (no_queryset_action(function), name, description)

            elif name in optional_queryset_action_names:
                actions[name] = (optional_queryset_action(function), name, description)

            else:
                actions[name] = (function, name, description)

        return actions

    def changelist_view(self, request: HttpRequest, extra_context=None):
        if "action" not in request.POST:
            return super().changelist_view(request, extra_context)

        action_name = request.POST.get("action", "")
        action_function, _, _ = self.get_actions(request).get(
            action_name, (None, None, None)
        )

        if not (
            is_no_queryset_action(action_function)
            or is_optional_queryset_action(action_function)
        ):
            return super().changelist_view(request, extra_context)

        # 'index' must be present in POST for check in 'Actions with no confirmation' block
        if "index" not in request.POST:
            with mutable_querydict(request.POST) as request_post:
                request_post.setdefault("index", "0")

        if is_no_queryset_action(action_function):
            selected: "list[str]" = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)
            select_across: bool = request.POST.get("select_across", "0") == "1"

            if selected or select_across:
                self.message_user(
                    request,
                    gettext(
                        "No items must be selected in order to perform this action."
                    ),
                    messages.WARNING,
                )
                return HttpResponseRedirect(request.get_full_path())

        # Monkey-patch `getlist` method on `QueryDict` to pass check for selected items
        request.POST.getlist = patched_getlist.__get__(request.POST, QueryDict)

        return super().changelist_view(request, extra_context)
