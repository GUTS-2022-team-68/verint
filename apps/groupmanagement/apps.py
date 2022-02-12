from django.apps import AppConfig


class GroupManagementConfig(AppConfig):
    name = 'verint.apps.groupmanagement'
    label = 'groupmanagement'
    verbose_name = 'Group Management'
    
    def ready(self):
    from . import signals