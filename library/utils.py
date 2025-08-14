from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib import messages


def is_librarian(user):
    """Check if user is a librarian"""
    if not user.is_authenticated:
        return False
    return user.groups.filter(name='Librarian').exists()


def is_member(user):
    """Check if user is a member"""
    if not user.is_authenticated:
        return False
    return user.groups.filter(name='Member').exists() or hasattr(user, 'member_profile')


def librarian_required(view_func):
    """Decorator to ensure only librarians can access a view"""
    from django.contrib.auth.decorators import user_passes_test
    return user_passes_test(is_librarian, login_url='/login/')(view_func)


def member_required(view_func):
    """Decorator to ensure only members can access a view"""
    from django.contrib.auth.decorators import user_passes_test
    return user_passes_test(is_member, login_url='/login/')(view_func)


def get_user_role(user):
    """Get the user's role as a string"""
    if is_librarian(user):
        return 'librarian'
    elif is_member(user):
        return 'member'
    else:
        return 'guest'


def create_default_groups():
    """Create default groups if they don't exist"""
    librarian_group, created = Group.objects.get_or_create(name='Librarian')
    member_group, created = Group.objects.get_or_create(name='Member')
    return librarian_group, member_group 