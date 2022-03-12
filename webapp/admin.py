from django.contrib import admin
from webapp.models import Product, Review


# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'text', 'rating']
    list_filter = ['text']
    search_fields = ['text']
    fields = ['id', 'author', 'text', 'rating', 'product']
    readonly_fields = ['id']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'description', 'category', 'picture']
    list_filter = ['product']
    search_fields = ['product']
    fields = ['id', 'product', 'description', 'category', 'picture']
    readonly_fields = ['id']


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
