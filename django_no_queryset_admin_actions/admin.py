from types import FunctionType

from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.http import HttpRequest, HttpResponseRedirect
from django.http.request import QueryDict
from django.utils.translation import gettext as _

from .decorators import no_queryset_action, NO_QUERYSET_ACTION_ATTRIBUTE


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

    def get_actions(self, request: HttpRequest):
        no_queryset_actions = [
            action.__name__ if callable(action) else action
            for action in self.no_queryset_actions or []
        ]

        return {
            name: (
                (no_queryset_action(function), name, description)
                if name in no_queryset_actions
                and not getattr(function, NO_QUERYSET_ACTION_ATTRIBUTE, False)
                else (function, name, description)
            )
            for function, name, description in super().get_actions(request).values()
        }

    def changelist_view(self, request: HttpRequest, extra_context=None):
        if "action" not in request.POST:
            return super().changelist_view(request, extra_context)

        action_name = request.POST.get("action", "")
        action = self.get_actions(request).get(action_name)
        if action is None or not getattr(
            action[0], NO_QUERYSET_ACTION_ATTRIBUTE, False
        ):
            return super().changelist_view(request, extra_context)

        selected: "list[str]" = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)
        select_across: bool = request.POST.get("select_across", "0") == "1"

        if selected or select_across:
            self.message_user(
                request,
                _("No items must be selected in order to perform this action."),
                messages.WARNING,
            )
            return HttpResponseRedirect(request.get_full_path())

        # Monkey-patch `getlist` method on `QueryDict` to pass check for selected items
        request.POST.getlist = patched_getlist.__get__(request.POST, QueryDict)

        return super().changelist_view(request, extra_context)
