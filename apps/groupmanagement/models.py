from typing import Set

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db import models

from verint.apps.employees.models import State


class GroupRequest(models.Model):
    leave_request = models.BooleanField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ":" + self.group.name
    

class AuthGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    internal = models.BooleanField(
        default=True,
        help_text=(
            "Internal group, users cannot see, join or request to join this group.<br>"
            "Used for groups such as Employee, Admins, etc.<br>"
            "<b>Overrides Hidden and Open options when selected.</b>"
        )
    )
    hidden = models.BooleanField(
        default=True,
        help_text=(
            "Group is hidden from users but can still join with the correct link."
        )
    )
    open = models.BooleanField(
        default=False,
        help_text=(
            "Group is open and users will be automatically added upon request.<br>"
            "If the group is not open users will need their request manually approved."
        )
    )
    public = models.BooleanField(
        default=False,
        help_text=(
            "Group is public. Any registered user is able to join this group, with "
            "visibility based on the other options set for this group.<br>"
            "Auth will not remove users from this group automatically when they "
            "are no longer authenticated."
        )
    )
    group_leaders = models.ManyToManyField(
        User,
        related_name='leads_groups',
        blank=True,
        help_text=(
            "Group leaders can process requests for this group. "
            "Use the <code>auth.group_management</code> permission to allow "
            "a user to manage all groups.<br>"
        )
    )
    group_leader_groups = models.ManyToManyField(
        Group,
        related_name='leads_group_groups',
        blank=True,
        help_text=(
            "Members of leader groups can process requests for this group. "
            "Use the <code>auth.group_management</code> permission "
            "to allow a user to manage all groups.<br>")
    )
    states = models.ManyToManyField(
        State,
        related_name='valid_states',
        blank=True,
        help_text=(
            "States listed here will have the ability to join this group provided "
            "they have the proper permissions.<br>"
        )
    )
    description = models.TextField(
        max_length=512,
        blank=True,
        help_text=(
            "Short description <i>(max. 512 characters)</i> "
            "of the group shown to users."
        )
    )

    class Meta:
        permissions = (
            ("request_groups", ("Can request non-public groups")),
        )
        default_permissions = tuple()

    def __str__(self):
        return self.group.name

    def group_request_approvers(self) -> Set[User]:
        """Return all users who can approve a group request."""
        return set(
            self.group_leaders.all()
            | User.objects.filter(groups__in=list(self.group_leader_groups.all()))
        )
