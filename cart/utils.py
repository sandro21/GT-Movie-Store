def calculate_cart_total(cart, movies_in_cart):
    total = 0
    for m in movies_in_cart:
        qty = int(cart[str(m.id)])
        total += m.price * qty
    return total
