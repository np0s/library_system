from django import template
from library.utils import is_librarian as _is_librarian, is_member as _is_member

register = template.Library()


@register.filter
def is_librarian(user):
	return _is_librarian(user)


@register.filter
def is_member(user):
	return _is_member(user) 