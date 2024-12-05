from django.contrib import admin
from.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','qtty','size')
    search_fields = ('name',)



