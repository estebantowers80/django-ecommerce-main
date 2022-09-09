from django.conf import settings
from .models import Product

class Cart:

    """Inicializando el cart"""
    def __init__(self, request):        
        self.session = request.session
        cart_tmp = self.session.get(settings.CART_SESSION_ID)
        if not cart_tmp:
            cart_tmp = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart_tmp


    """Agregar item al cart"""
    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": quantity}
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()


    """Actualizar cantidad de item en el cart"""
    def update(self, product_id, quantity):
        product_id = str(product_id)

        if product_id in self.cart:
            self.cart[product_id]["quantity"] = quantity

        self.save()


    """Quitar item del cart"""
    def delete(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def save(self):
        self.session.modified = True


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    """Contabilizar todas las unidades agregadas al carrito"""
    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())
   
    def __iter__(self):        
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_tmp = self.cart.copy()

        for product in products:            
            cart_tmp[str(product.id)]["product"] = product
            
        for item in cart_tmp.values():
            item["subtotal"] = item["product"].price * item["quantity"]
            yield item  