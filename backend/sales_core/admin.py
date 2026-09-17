from django.contrib import admin
from .models import Product, ChatSession, ChatMessage, Order, OrderItem, SystemSetting


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'sale_price', 'stock', 'is_active')
    search_fields = ('name', 'sku', 'category')
    list_filter = ('category', 'is_active')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'total_amount', 'status', 'email_sent', 'created_at')
    list_filter = ('status', 'email_sent', 'created_at')
    search_fields = ('id', 'customer_name', 'customer_phone')
    inlines = [OrderItemInline]


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('sender', 'content', 'created_at')


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'status', 'created_at', 'updated_at')
    search_fields = ('customer_name', 'customer_phone')
    list_filter = ('status', 'created_at')
    inlines = [ChatMessageInline]


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description')
