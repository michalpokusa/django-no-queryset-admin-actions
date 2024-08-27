from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.http import HttpRequest, HttpResponseRedirect
from django.http.request import QueryDict
from django.utils.translation import gettext as _


class truthy_list(list):
    """
    Used instead of empty `list` in `ModelAdmin.changelist_view` method to pass
    check for selected items.
    """

    def __bool__(self):
        return True


def getlist(self, key, default=None):
    """
    Monkey-patched method for `QueryDict` class to return `truthy_list` instead of
    empty `list` when `key` is `ACTION_CHECKBOX_NAME`, which is used to check
    if any items are selected.
    """

    if key == helpers.ACTION_CHECKBOX_NAME:
        return truthy_list()

    return super(QueryDict, self).getlist(key, default)


def remove_action_queryset_parameter(action_function):
    """
    Decorator to remove `queryset` parameter from being passed to action function.
    """

    def wrapper2(*args, **kwargs):
        modeladmin, request, queryset, *rest = args

        result = action_function(modeladmin, request, *rest, **kwargs)
        return result

    return wrapper2


class NoQuerySetAdminActionsMixin(admin.ModelAdmin):

    no_queryset_actions: "list[str] | tuple[str]" = ()

    def _get_no_queryset_actions(self) -> "list[str]":
        return (self.get_action(action) for action in self.no_queryset_actions or [])

    def get_actions(self, request: HttpRequest):
        return {
            name: (
                (remove_action_queryset_parameter(callable), name, description)
                if name in (name for _, name, _ in self._get_no_queryset_actions())
                else (callable, name, description)
            )
            for callable, name, description in super().get_actions(request).values()
        }

    def changelist_view(self, request: HttpRequest, extra_context=None):
        if "action" not in request.POST:
            return super().changelist_view(request, extra_context)

        action_name = request.POST.get("action", "")
        if action_name not in (name for _, name, _ in self._get_no_queryset_actions()):
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

        request.POST.getlist = getlist.__get__(request.POST, QueryDict)

        return super().changelist_view(request, extra_context)
