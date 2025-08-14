from django import template
from library.utils import is_librarian as util_is_librarian, is_member as util_is_member

register = template.Library()


@register.filter(name='is_librarian')
def is_librarian_filter(user):
	return util_is_librarian(user)


@register.filter(name='is_member')
def is_member_filter(user):
	return util_is_member(user) 