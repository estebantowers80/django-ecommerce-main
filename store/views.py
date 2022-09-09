from .models import *
#------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from .forms import SignUpForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import json
from .cart import Cart
from django.db import transaction
from django.db.models import Q, Sum
import datetime



#para envio de correos
#Fuente: https://www.iteramos.com/pregunta/98870/como-enviar-correo-electronico-html-con-django-con-contenido-dinamico
from django.core.mail import send_mail
from django.template.loader import render_to_string 
from django.utils.html import strip_tags


def index(request):
    txt_buscar = request.GET.get("search")
    if txt_buscar :
        products = Product.objects.filter( 
            (
            Q(name__icontains = txt_buscar) |
            Q(description__icontains = txt_buscar)
            ) & 
            Q(is_active = True)
        ).distinct()
    else:
        products = Product.objects.filter(is_active = True)


        #probar correo
        #enviar_email_en_html(request,'Confirmacion de pedido','estebantowers@gmail.com','ESTEBAN TORRES','4545')
        #enviar_email(request, 'Confirmación de Pedido', men  ,'estebantowers@gmail.com')

        #probar suma de articulos 
        #print(OrderItem.objects.values('product__id','product__name','product__description','product__image').annotate(cantidad_venta=Sum('quantity')).order_by('-cantidad_venta'))
        #probar listado de ordenes
        #print(Customer.objects.values('order__customer','id','identification','full_name','order__total','order__created'))
    return render(request, 'store.html', {'products': products})

def product_detail(request, product_id):
    if product_id>25:
        raise Http404('The product does not exist')
    else:
        context = {'productId': product_id}
        return render(request, 'product_detail.html', context)

def cart(request):
    shopping_cart = Cart(request)
    total_cart = sum(item['subtotal'] for item in shopping_cart)
    return render(request, 'cart.html', context = {'shopping_cart': shopping_cart, 'total_cart': total_cart})

def checkout(request): 
    shopping_cart = Cart(request)
    total_cart = sum(item['subtotal'] for item in shopping_cart)    
    return render(request, 'checkout.html', context = {'shopping_cart': shopping_cart, 'total_cart': total_cart})

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Se ha registrado exitosamente.") 
            return redirect("index")

    form = SignUpForm()
    return render(request, 'signup.html', context = { 'signup_form': form })

def login_view_function(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Ha iniciado sesión exitosamente como: {username}.")
                return redirect("index")
            else:
                messages.error(request, "Usuario o contraseña inválidos.")
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
    
    form = AuthenticationForm()
    return render(request, "login.html", context={'login_form': form})

def logout_view_function(request): 
    logout(request)
    messages.info(request, "Ha cerrado la sesión exitosamente.") 
    return redirect("index")

def add_item_to_cart(request):
    cart = Cart(request)

    data = json.loads(request.body)
    product_id = int(data.get('product_id'))
    quantity = int(data.get('quantity'))
    get_object_or_404(Product, id=product_id)
    
    cart.add(product_id, quantity)
    return JsonResponse({"added": True, "total_items": cart.__len__()})

def remove_item_from_cart(request):    
    cart = Cart(request)
    data = json.loads(request.body)
    product_id = int(data.get('product_id'))

    cart.delete(product_id=product_id)
    return JsonResponse({"deleted": True, "total_items": cart.__len__()})


@transaction.atomic
def process_order(request):
    try:
        if request.method == "POST":
            
            cart = Cart(request)

            data = json.loads(request.body)
            identification = data.get('identification')
            full_name = data.get('full_name')
            email = data.get('email')
            city = data.get('city')
            address = data.get('address')
            cellphone = data.get('cellphone')
            cart_total = sum(item.get('subtotal') for item in cart)

            mensaje = 'Estimado se tiene un pedido a nombre de ' + full_name + '<br> detalle'

            print('Los campos recibidos son: ', data)
            print('Los items del carrito son: ', cart.__len__())

            try:
                customer = Customer.objects.get(identification=identification)
                customer.full_name = full_name
                customer.email = email
                customer.phone = cellphone
                customer.save(update_fields=['full_name', 'email', 'phone'])
            except Customer.DoesNotExist:
                customer = Customer(user=request.user,
                                    identification=identification,
                                    full_name=full_name,
                                    email=email,
                                    phone=cellphone)
                customer.save()

            order = Order(  customer=customer,
                            complete=True,
                            total=cart_total)
            order.save()

            for item in cart:
                order_item = OrderItem( order=order,
                                        product=item.get('product'),
                                        quantity=item.get('quantity'))
                order_item.save()

            shippingAddress = ShippingAddress(  order=order,
                                                city=city,
                                                address=address,
                                                phone=cellphone)
            shippingAddress.save()
            
            cart.clear()
   
            
            enviar_email_en_html(request, 'Confirmación de Pedido',email,full_name,cellphone,order.id)

            #enviar_email(request, 'Confirmación de Pedido', mensaje  ,email)                
            #print('PASA')

            return JsonResponse({"order_id": order.id}, status=201)
    except Exception as error:
        print('Ocurrió un error al generar el pedido: ', repr(error))
        return JsonResponse({"error_msg": "Opps, su pedido no pudo ser ingresado. " + repr(error)}, status=500)

def search(request):    
    if request.method == "GET":
        form = AuthenticationForm(request, data= request.GET)
        if form.is_valid():
            form.save()
            messages.info(request, "Se ha registrado exitosamente.") 
            return redirect("index")

    form = SignUpForm()
    return render(request, 'signup.html', context = { 'signup_form': form })


#para enviar correos
def enviar_email(request, vs_asunto,vs_mensaje,vs_to):
    print("enviar correo")
    send_mail(vs_asunto,vs_mensaje,'estebantowers@gmail.com', [vs_to], fail_silently=True )    

    # https://github.com/sukanya-pai/Django-Email-Sender


#para enviar correos con formato html
def enviar_email_en_html(request, vs_asunto,vs_to,vs_nombre,vs_telefono,vs_num_pedido):
    print("enviar correo")

    context = {
                    'nombre': vs_nombre,
                    'telefono': vs_telefono,
                    'correo': vs_to,
                    'num_pedido':vs_num_pedido
            }

    html_message = render_to_string('mail_template.html',context)
    plain_message = strip_tags(html_message)

    send_mail(vs_asunto,plain_message,'estebantowers@gmail.com', [vs_to], html_message=html_message )    

    # https://github.com/sukanya-pai/Django-Email-Sender
    # https://www.fullstackpython.com/django-template-loader-render-to-string-examples.html
    # https://github.com/dccnconf/dccnsys/tree/master/wwwdccn/auth_app


def productos_top(request):
    producto = OrderItem.objects.values('product__id','product__name','product__description','product__price','product__image').annotate(cantidad_venta=Sum('quantity')).order_by('-cantidad_venta')
    return render(request, 'top_producto.html', {'products': producto})    

def historico_pedidos(request):

    historico_ventas = Customer.objects.values('order__customer','id','identification','full_name','order__total','order__created')
    return render(request,'historico.html',{'historico': historico_ventas})
    