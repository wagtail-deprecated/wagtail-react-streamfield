from django.apps import AppConfig

from .monkey_patch import patch


class WagtailReactStreamFieldConfig(AppConfig):
    name = 'wagtail_react_streamfield'

    def ready(self):
        patch()
