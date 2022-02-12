from django.contrib.auth.models import User, Permission
from django.db import models

from .managers import StateManager


class State(models.Model):
    name = models.CharField(max_length=32, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    objects = StateManager()

    class Meta:
        ordering = ['-priority']

    def __str__(self):
        return self.name

    def available_to_user(self, user):
        return self in State.objects.available_to_user(user)
        
    
def get_guest_state():
    try:
        return State.objects.get(name='Guest')
    except State.DoesNotExist:
        return State.objects.create(name='Guest', priority=0, public=True)


def get_guest_state_pk():
    return get_guest_state().pk


class Employees(models.Model):
    class Meta:
        default_permissions = ('change',)

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.SET_DEFAULT, default=get_guest_state_pk)
    e_id = models.CharField(max_length=64)
    hire_date = models.DateTimeField(null=True, blank=True)

    def assign_state(self, state=None, commit=True):
        if not state:
            state = State.objects.get_for_user(self.user)
        if self.state != state:
            self.state = state
            if commit:
                self.save(update_fields=['state'])

    def __str__(self):
        return str(self.user)