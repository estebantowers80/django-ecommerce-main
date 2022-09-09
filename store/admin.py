from django.contrib import admin
from .models import Category, Customer, Order, OrderItem, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)


##------ inicio para registrar un maestro detalle dentro del amdin
#detalle 
class Detalle_orden(admin.TabularInline):
    model = OrderItem

#indicamos las lineas de detalle 
class OrdenAdmin(admin.ModelAdmin):
    inlines = (Detalle_orden,)
    list_display=('id','customer','total','created')
    list_display_links = ('id', 'customer')
    list_filter = ('customer','id',)      
    list_per_page = 10
    search_fields = ('id','customer','created')
#registramos el modelo 
admin.site.register(Order, OrdenAdmin)
#------FIN para registrar un maestro detalle dentro del amdin


"""
list_display = ('id', 'title', 'description_1', 'list_date', 'is_published')
    list_display_links = ('id', 'title')
    list_filter = ('title',)
    list_editable = ('is_published',)
    list_per_page = 25
    search_fields = ('title', 'description_1', 'description_2', 'description_3', 'list_date')

customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=9, decimal_places=2)    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)	


"""

admin.site.site_header = "Villa store admin"
admin.site.index_title = "Panel de control"

#para la plantilla de admin
#https://dev.to/sm0ke/django-admin-dashboards-open-source-and-free-1o80
#Django Dashboards - Open-Source and Free
#A curated list with open-source admin panels coded in Django Framework on top of popular Ui Kits: material, black design, argon, light. 

