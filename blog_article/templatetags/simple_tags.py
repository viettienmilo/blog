from django import template

register = template.Library()

RATINGS = {
		0: '☆☆☆☆☆',
		1: '★☆☆☆☆',
		2: '★★☆☆☆',
		3: '★★★☆☆',
		4: '★★★★☆',
		5: '★★★★★',
}


@register.simple_tag
def star_rating(rating):
	return RATINGS[rating]


@register.simple_tag
def average_rating(rates):
	if not rates:
		return 0
	rating_list = [rate.rating for rate in rates]
	ave_rating = sum(rating_list)/len(rating_list)
	ave_rating = round(ave_rating)
	return RATINGS[ave_rating]
