
from unicodedata import name
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('product-detail/<int:product_id>/', views.product_detail, name='productDetail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view_function, name='login'),
    path('logout/', views.logout_view_function, name= 'logout'),
    path('add-item/', views.add_item_to_cart, name='addItem'),
    path('remove-item/', views.remove_item_from_cart, name='removeItem'),
    path('process-order/', views.process_order, name='processOrder'),
    path('top_producto/', views.productos_top, name='topProducto'),
    path('historico/', views.historico_pedidos, name='historico'),
]