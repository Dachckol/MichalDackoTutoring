from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
 
register = template.Library()
 
@register.filter
def pound(pounds):
    if pounds:
        pounds = round(float(pounds), 2)
        return "%s%s" % (intcomma(int(pounds)), ("%0.2f" % pounds)[-3:])
    else:
        return ''