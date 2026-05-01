from django import template
from clubs.models import Membership

register = template.Library()


@register.simple_tag
def is_member(user, club):
    if not user.is_authenticated:
        return False
    return Membership.objects.filter(user=user, club=club).exists()


@register.simple_tag
def is_club_admin(user, club):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return Membership.objects.filter(user=user, club=club, role__in=['admin', 'president']).exists()
