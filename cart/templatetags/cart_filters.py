from django import template
register = template.Library()

@register.filter(name='get_quantity')
def get_cart_quantity(cart, movie_id):
    return cart.get(str(movie_id), 0)
