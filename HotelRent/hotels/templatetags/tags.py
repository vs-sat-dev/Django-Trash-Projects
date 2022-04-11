from django import template
from math import ceil


register = template.Library()


@register.filter
def batch(lst, batch_size):
    limit = ceil(len(lst) / batch_size)
    for i in range(limit):
        yield lst[batch_size * i:batch_size * (i + 1)]

