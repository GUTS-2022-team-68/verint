from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, Permission

from .models import Employees



class StateBackend(ModelBackend):
    @staticmethod
    def _get_state_permissions(user_obj):
        """returns permissions for state of given user object"""
        if hasattr(user_obj, "profile") and user_obj.profile:
            return Permission.objects.filter(state=user_obj.profile.state)
        else:
            return Permission.objects.none()

    def get_state_permissions(self, user_obj, obj=None):
        return self._get_permissions(user_obj, obj, 'state')

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = self.get_user_permissions(user_obj)
            user_obj._perm_cache.update(self.get_group_permissions(user_obj))
            user_obj._perm_cache.update(self.get_state_permissions(user_obj))
        return user_obj._perm_cache


    def create_user(self, token):
        user = "TODO"
        """TODO"""
        return user

    @staticmethod
    def iterate_username(name):
        name = str.replace(name, "'", "")
        name = str.replace(name, ' ', '_')
        if User.objects.filter(username__startswith=name).exists():
            u = User.objects.filter(username__startswith=name)
            num = len(u)
            username = f"{name}_{num}"
            while u.filter(username=username).exists():
                num += 1
                username = f"{name}_{num}"
        else:
            username = name
        return username
