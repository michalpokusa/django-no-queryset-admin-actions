
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

It does one thing and one thing only.

- [🔌 Installation](#-installation)
- [✏️ Example](#️-example)


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

## ✏️ Example

Let's say you have an action that fetches external orders from an API. You don't need a queryset to run this action, but Django requires it by default. By using this extension, you can bypass that, and create actions that can be run without selecting any objects.

<img src="https://raw.githubusercontent.com/michalpokusa/django-no-queryset-admin-actions/main/resources/example.gif" width="100%"></img>

```python
from django.contrib.admin import ModelAdmin, register, action

from django_no_queryset_admin_actions import NoQuerySetAdminActionsMixin


@register(ExternalOrder)
class ExternalOrderAdmin(NoQuerySetAdminActionsMixin, ModelAdmin):

    ...

    @action(description="Fetch external orders")
    def fetch_external_orders(self, request): # <- No `queryset` parameter
        ...

    actions = ["fetch_external_orders"]

    no_queryset_actions = ["fetch_external_orders"]
```
