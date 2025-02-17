
# django-no-queryset-admin-actions

<p float="left">
    <a href="https://pypi.org/project/django-no-queryset-admin-actions/">
        <img src="https://img.shields.io/pypi/v/django-no-queryset-admin-actions?color=0073b7"/>
    </a>
    <a href="https://www.djangoproject.com/">
        <img src="https://img.shields.io/badge/3.2.x, 4.x.x, 5.x.x-a?style=flat&logo=django&label=django&labelColor=0c4b33&color=616161">
    </a>
</p>

Extension for the Django admin panel that makes it possible to add actions that do not require a queryset to run.

Works with [django-admin-action-forms](https://pypi.org/project/django-admin-action-forms/).

- [🔌 Installation](#-installation)
- [✏️ Examples](#️-examples)
  - [No queryset actions](#no-queryset-actions)
  - [Optional queryset actions](#optional-queryset-actions)


## 🔌 Installation

1. Install using ``pip``:

    ```bash
    $ pip3 install django-no-queryset-admin-actions
    ```


2. Add `'django_no_queryset_admin_actions'` to your `INSTALLED_APPS` setting.
    ```python
    INSTALLED_APPS = [
        ...
        'django_no_queryset_admin_actions',
    ]
    ```

## ✏️ Examples

### No queryset actions

Let's say you have an action that fetches external orders from an API. You don't need a queryset to run this action,
but Django requires it by default. By using the `@no_queryset_action`, you can bypass that, and create actions that can
be run without selecting any objects.

<img src="https://raw.githubusercontent.com/michalpokusa/django-no-queryset-admin-actions/main/resources/example.gif" width="100%"></img>

```python
from django.contrib.admin import ModelAdmin, register

from django_no_queryset_admin_actions import NoQuerySetAdminActionsMixin, no_queryset_action


@register(ExternalOrder)
class ExternalOrderAdmin(NoQuerySetAdminActionsMixin, ModelAdmin):

    @no_queryset_action(description="Fetch external orders")
    def fetch_external_orders(self, request): # <- No `queryset` parameter
        ...

    actions = [fetch_external_orders]
```

### Optional queryset actions

Another use case is when you have an action that can be run on a specific queryset, but you also want to allow running it without selecting any objects.

This type of action could be used to e.g.:
- default to all, or a filtered subset of objects when no selection is made
- choose a random object if no specific item is selected

Leveraging the `@optional_queryset_action` decorator, you can create actions that run whether or not objects are selected.

Let's say, that `ExternalOrder` objects fetched in the previous example may sometimes need updating. In this example, if no objects are selected, `queryset` will be empty, and the action will default to updating all `ExternalOrder` objects.

```python
from django.contrib.admin import ModelAdmin, register

from django_no_queryset_admin_actions import NoQuerySetAdminActionsMixin, optional_queryset_action


@register(ExternalOrder)
class ExternalOrderAdmin(NoQuerySetAdminActionsMixin, ModelAdmin):

    @optional_queryset_action(description="Update external orders")
    def update_external_orders(self, request, queryset): # <- `queryset` can be empty

        if not queryset:
            queryset = ExternalOrder.objects.all()

        ...

    actions = [update_external_orders]
```
