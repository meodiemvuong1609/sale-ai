from rest_framework import serializers
from .models import Product, ChatSession, ChatMessage, Order, OrderItem, SystemSetting


class ProductSerializer(serializers.ModelSerializer):
    current_price = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'category', 'price', 'sale_price', 'current_price',
            'stock', 'short_description', 'description', 'selling_points',
            'faq', 'image_url', 'is_active', 'created_at', 'updated_at'
        ]


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'session', 'sender', 'content', 'metadata', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = [
            'id', 'customer_name', 'customer_phone', 'customer_address',
            'language', 'status', 'created_at', 'updated_at', 'messages'
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'session', 'customer_name', 'customer_phone', 'customer_address',
            'total_amount', 'status', 'notes', 'email_sent', 'created_at', 'items'
        ]


class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = ['key', 'value', 'description']
