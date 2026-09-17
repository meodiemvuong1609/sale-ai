from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    OrderViewSet,
    start_chat_session,
    send_chat_message,
    get_chat_history,
    settings_view
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('chat/start/', start_chat_session, name='chat-start'),
    path('chat/send/', send_chat_message, name='chat-send'),
    path('chat/history/<str:session_id>/', get_chat_history, name='chat-history'),
    path('settings/', settings_view, name='settings'),
]
