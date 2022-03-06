from django import template
from django.db.models import Q

from merchantapp.models import Merchant, Branch, Program

register = template.Library()


@register.filter
def redeemable_count(rewards, merchant_employee):
    merchant = Merchant.objects.filter(Q(director=merchant_employee) | Q(employees=merchant_employee)).first()
    branches = Branch.objects.filter(merchant=merchant)
    programs = Program.objects.filter(branch__in=branches)
    return rewards.filter(redeemed=False, program__in=programs).count()


@register.filter
def total_count(objects, merchant_employee):
    merchant = Merchant.objects.filter(Q(director=merchant_employee) | Q(employees=merchant_employee)).first()
    branches = Branch.objects.filter(merchant=merchant)
    programs = Program.objects.filter(branch__in=branches)
    return objects.filter(program__in=programs).count()
