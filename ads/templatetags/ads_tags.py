from django import template

from ..models import ExchangeProposal

register = template.Library()


@register.simple_tag
def number_pending_proposals(request):
    number = ExchangeProposal.objects.filter(ad_receiver__user=request.user, status='pending').count()
    return number or ''


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
