from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .managers import GroupManager
from .models import GroupRequest


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_management(request):
    acceptrequests = []
    leaverequests = []

    base_group_query = GroupRequest.objects.select_related('user', 'group')
    if GroupManager.has_management_permission(request.user):
        # Full access
        group_requests = base_group_query.all()
    else:
        # Group specific leader
        users__groups = GroupManager.get_group_leaders_groups(request.user)
        group_requests = base_group_query.filter(group__in=users__groups)

    for grouprequest in group_requests:
        if grouprequest.leave_request:
            leaverequests.append(grouprequest)
        else:
            acceptrequests.append(grouprequest)

    render_items = {
        'acceptrequests': acceptrequests,
        'leaverequests': leaverequests,
        'auto_leave': getattr(settings, 'GROUPMANAGEMENT_AUTO_LEAVE', False),
    }

    return render(request, 'groupmanagement/index.html', context=render_items)


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_membership(request):
    # Get all open and closed groups
    if GroupManager.has_management_permission(request.user):
        # Full access
        groups = GroupManager.get_all_non_internal_groups()
    else:
        # Group leader specific
        groups = GroupManager.get_group_leaders_groups(request.user)

    groups = groups.exclude(authgroup__internal=True).annotate(num_members=Count('user')).order_by('name')

    render_items = {'groups': groups}

    return render(request, 'groupmanagement/groupmembership.html', context=render_items)


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_membership_list(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    try:

        # Check its a joinable group i.e. not corp or internal
        # And the user has permission to manage it
        if (not GroupManager.check_internal_group(group)
            or not GroupManager.can_manage_group(request.user, group)
        ):
            raise PermissionDenied

    except ObjectDoesNotExist:
        raise Http404("Group does not exist")

    group_leaders = group.authgroup.group_leaders.all()
    members = list()
    for member in \
        group.user_set\
            .all():

        members.append({
            'user': member,
            'is_leader': member in group_leaders
        })

    render_items = {'group': group, 'members': members}

    return render(
        request, 'groupmanagement/groupmembers.html',
        context=render_items
    )


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_membership_remove(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id)
    try:
        # Check its a joinable group i.e. not corp or internal
        # And the user has permission to manage it
        if not GroupManager.check_internal_group(group) or not GroupManager.can_manage_group(request.user, group):
            raise PermissionDenied

        try:
            user = group.user_set.get(id=user_id)
            user.groups.remove(group)
            messages.success(request, ("Removed user %(user)s from group %(group)s.") % {"user": user, "group": group})
        except ObjectDoesNotExist:
            messages.warning(request, ("User does not exist in that group"))

    except ObjectDoesNotExist:
        messages.warning(request, ("Group does not exist"))

    return redirect('groupmanagement:membership', group_id)


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_accept_request(request, group_request_id):
    group_request = get_object_or_404(GroupRequest, id=group_request_id)
    try:
        group, created = Group.objects.get_or_create(name=group_request.group.name)

        if not GroupManager.joinable_group(group_request.group, group_request.user.profile.state) or \
                not GroupManager.can_manage_group(request.user, group_request.group):
            raise PermissionDenied

        group_request.user.groups.add(group)
        group_request.user.save()
        group_request.delete()
        messages.success(request,
                        ('Accepted application from %(user)s to %(group)s.') % {"user": group_request.user, "group": group_request.group})

    except PermissionDenied as p:
        raise p
    except:
        messages.error(request, ('An unhandled error occurred while processing the application from %(user)s to %(group)s.') % {"user": group_request.user, "group": group_request.group})
        pass

    return redirect("groupmanagement:management")


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_reject_request(request, group_request_id):
    group_request = get_object_or_404(GroupRequest, id=group_request_id)
    try:
        if not GroupManager.can_manage_group(request.user, group_request.group):
            raise PermissionDenied

        if group_request:
            group_request.delete()
            messages.success(request,
                            ('Rejected application from %(user)s to %(group)s.') % {"user": group_request.user, "group": group_request.group})

    except PermissionDenied as p:
        raise p
    except:
        messages.error(request, ('An unhandled error occurred while processing the application from %(user)s to %(group)s.') % {"user": group_request.user, "group": group_request.group})
        pass

    return redirect("groupmanagement:management")


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_leave_accept_request(request, group_request_id):
    group_request = get_object_or_404(GroupRequest, id=group_request_id)
    try:
        if not GroupManager.can_manage_group(request.user, group_request.group):
            raise PermissionDenied

        group, created = Group.objects.get_or_create(name=group_request.group.name)
        group_request.user.groups.remove(group)
        group_request.user.save()
        group_request.delete()
        messages.success(request,
                        ('Accepted application from %(user)s to leave %(group)s.') % {"user": group_request.user, "group": group_request.group})
    except PermissionDenied as p:
        raise p
    except:
        messages.error(request, ('An unhandled error occurred while processing the application from %(user)s to leave %(group)s.') % {
            "user": group_request.user, "group": group_request.group})
        pass

    return redirect("groupmanagement:management")


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_leave_reject_request(request, group_request_id):
    group_request = get_object_or_404(GroupRequest, id=group_request_id)
    try:
        if not GroupManager.can_manage_group(request.user, group_request.group):
            raise PermissionDenied

        if group_request:
            group_request.delete()
            messages.success(request, ('Rejected application from %(user)s to leave %(group)s.') % {
                "user": group_request.user, "group": group_request.group})
    except PermissionDenied as p:
        raise p
    except:
        messages.error(request, ('An unhandled error occurred while processing the application from %(user)s to leave %(group)s.') % {
            "user": group_request.user, "group": group_request.group})
        pass

    return redirect("groupmanagement:management")


@login_required
def groups_view(request):
    groups_qs = GroupManager.get_joinable_groups_for_user(
        request.user, include_hidden=False
    )
    groups_qs = groups_qs.order_by('name')
    groups = []
    for group in groups_qs:
        group_request = GroupRequest.objects\
            .filter(user=request.user)\
            .filter(group=group)
        groups.append({
            'group': group,
            'request': group_request[0] if group_request else None
        })

    context = {'groups': groups}
    return render(request, 'groupmanagement/groups.html', context=context)


@login_required
def group_request_add(request, group_id):
    group = Group.objects.get(id=group_id)
    state = request.user.profile.state
    if not GroupManager.joinable_group(group, state):
        messages.warning(request, ("You cannot join that group"))
        return redirect('groupmanagement:groups')
    if group in request.user.groups.all():
        # User is already a member of this group.
        messages.warning(request, ("You are already a member of that group."))
        return redirect('groupmanagement:groups')
    if not request.user.has_perm('groupmanagement.request_groups') and not group.authgroup.public:
        # Does not have the required permission, trying to join a non-public group
        messages.warning(request, ("You cannot join that group"))
        return redirect('groupmanagement:groups')
    if group.authgroup.open:
        request.user.groups.add(group)
        return redirect("groupmanagement:groups")
    req = GroupRequest.objects.filter(user=request.user, group=group)
    if len(req) > 0:
        messages.warning(request, ("You already have a pending application for that group."))
        return redirect("groupmanagement:groups")
    grouprequest = GroupRequest()
    grouprequest.group = group
    grouprequest.user = request.user
    grouprequest.leave_request = False
    grouprequest.save()
    messages.success(request, ('Applied to group %(group)s.') % {"group": group})
    return redirect("groupmanagement:groups")


@login_required
def group_request_leave(request, group_id):
    group = Group.objects.get(id=group_id)
    if not GroupManager.check_internal_group(group):
        messages.warning(request, ("You cannot leave that group"))
        return redirect('groupmanagement:groups')
    if group not in request.user.groups.all():
        messages.warning(request, ("You are not a member of that group"))
        return redirect('groupmanagement:groups')
    if group.authgroup.open:
        request.user.groups.remove(group)
        return redirect("groupmanagement:groups")
    req = GroupRequest.objects.filter(user=request.user, group=group)
    if len(req) > 0:
        messages.warning(request, ("You already have a pending leave request for that group."))
        return redirect("groupmanagement:groups")
    if getattr(settings, 'GROUPMANAGEMENT_AUTO_LEAVE', False):
        request.user.groups.remove(group)
        return redirect('groupmanagement:groups')
    grouprequest = GroupRequest()
    grouprequest.group = group
    grouprequest.user = request.user
    grouprequest.leave_request = True
    grouprequest.save()
    messages.success(request, ('Applied to leave group %(group)s.') % {"group": group})
    return redirect("groupmanagement:groups")
