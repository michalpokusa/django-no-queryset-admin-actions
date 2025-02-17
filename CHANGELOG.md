# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.2.0] - 2025-02-17

### Fixed

- Regression with `django-admin-action-forms==1.3.0` where `@no_queryset_action` decorator was not working correctly with `@action_with_form` decorator due to missing `'index'` key in `request.POST`

### Added

- `@optional_queryset_action` decorator for actions that can run regardless of whether a queryset is selected or not

## [1.1.0] - 2024-10-01

### Changed

- `@no_queryset_action` decorator accepts `permissions` and `description` arguments and can be used before or after `@action_with_form` decorator from `django-admin-action-forms` package

## [1.0.2] - 2024-09-12

### Changed

- Renamed and moved `@no_queryset_action` decorator to `decorators.py` module

## [1.0.1] - 2024-08-28

### Added

- Mention about working with `django-admin-action-forms` package in README.md

## [1.0.0] - 2024-08-28

### Added

- `NoQuerySetAdminActionsMixin` class that allows `no_queryset_action` attribute to be used in `ModelAdmin` classes for specifying actions that do not require a queryset
- README.md file with instalation instructions and example

[1.2.0]: https://github.com/michalpokusa/django-no-queryset-admin-actions/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/michalpokusa/django-no-queryset-admin-actions/compare/1.0.2...1.1.0
[1.0.2]: https://github.com/michalpokusa/django-no-queryset-admin-actions/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/michalpokusa/django-no-queryset-admin-actions/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/michalpokusa/django-no-queryset-admin-actions/tree/1.0.0
