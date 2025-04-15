from django.contrib import admin
from .models import Category, Flower, Customer, Order, OrderItem, Comment

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total_price', 'order_date']
    list_filter = ['order_date']
    search_fields = ['customer__username', 'shipping_address']
    inlines = [OrderItemInline]

class FlowerAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category', 'is_featured', 'date_added']
    list_filter = ['category', 'is_featured', 'date_added']
    search_fields = ['name', 'description']
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'price', 'stock', 'category', 'image', 'is_featured']
        }),
        ('Content', {
            'fields': ['description']
        }),
        ('Settings', {
            'fields': ['date_added']
        }),
    ]

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'date_posted']
    list_filter = ['date_posted']
    search_fields = ['user__username', 'content']

admin.site.register(Category)
admin.site.register(Flower, FlowerAdmin)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(Comment, CommentAdmin)
