from .cart import Cart

def shopping_cart(request):
    return {'shopping_cart': Cart(request)}