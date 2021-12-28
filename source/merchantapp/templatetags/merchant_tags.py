from django import template
register = template.Library()


@register.filter
def redeemable_count(rewards):
    return rewards.filter(redeemed=False).count()
