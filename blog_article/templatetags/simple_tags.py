from django import template

register = template.Library()


@register.simple_tag
def average_rating(rates):
	if not rates:
		return 0
	rating_list = [rate.rating for rate in rates]
	return round(sum(rating_list)/len(rating_list)*2)/2

