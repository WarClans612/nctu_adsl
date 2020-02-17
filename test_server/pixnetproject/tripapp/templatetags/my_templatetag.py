from django import template
register = template.Library()

@register.filter
def times(value):
    return range(value)

@register.filter
def list_item(lis, val):
	return lis[val]

@register.filter
def length(value):
 	return len(value) 

@register.filter
def len_range(value):
 	return range(len(value)) 

