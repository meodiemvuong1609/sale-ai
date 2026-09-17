import uuid
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, ChatSession, ChatMessage, Order, SystemSetting
from .serializers import (
    ProductSerializer,
    ChatSessionSerializer,
    ChatMessageSerializer,
    OrderSerializer,
    SystemSettingSerializer
)
from .services.gemini_sales import process_sales_chat, get_gemini_api_key
from .services.email_service import get_admin_notification_email


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer


@api_view(['POST'])
def start_chat_session(request):
    """Bắt đầu phiên chat mới hoặc khôi phục phiên chat có sẵn"""
    session_id = request.data.get('session_id')
    language = request.data.get('language', 'vi')
    if session_id:
        try:
            session = ChatSession.objects.get(id=session_id)
            if language and session.language != language:
                session.language = language
                session.save(update_fields=['language'])
            serializer = ChatSessionSerializer(session)
            return Response(serializer.data)
        except ChatSession.DoesNotExist:
            pass

    session = ChatSession.objects.create(language=language)
    serializer = ChatSessionSerializer(session)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def send_chat_message(request):
    """Gửi tin nhắn của khách hàng và nhận phản hồi chốt đơn từ AI Sales Rep"""
    session_id = request.data.get('session_id')
    message_text = request.data.get('message', '').strip()
    language = request.data.get('language')

    if not session_id or not message_text:
        return Response(
            {'error': 'session_id và message là bắt buộc'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        session = ChatSession.objects.get(id=session_id)
    except ChatSession.DoesNotExist:
        session = ChatSession.objects.create(
            id=uuid.UUID(session_id) if len(session_id) == 36 else uuid.uuid4(),
            language=language or 'vi'
        )

    if language and session.language != language:
        session.language = language
        session.save(update_fields=['language'])

    response_data = process_sales_chat(session, message_text, language=session.language)
    return Response(response_data)


@api_view(['GET'])
def get_chat_history(request, session_id):
    """Lấy toàn bộ lịch sử tin nhắn của một phiên chat"""
    try:
        session = ChatSession.objects.get(id=session_id)
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data)
    except ChatSession.DoesNotExist:
        return Response({'error': 'Không tìm thấy phiên chat'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def settings_view(request):
    """Lấy hoặc cập nhật cấu hình hệ thống (Email nhận đơn, Gemini API Key)"""
    if request.method == 'GET':
        admin_email = get_admin_notification_email()
        api_key = get_gemini_api_key()
        masked_key = (api_key[:8] + '...' + api_key[-4:]) if (api_key and len(api_key) > 12) else (api_key or '')
        
        return Response({
            'admin_notification_email': admin_email,
            'gemini_api_key': masked_key,
            'is_gemini_active': bool(api_key and api_key != 'YOUR_GEMINI_API_KEY')
        })

    elif request.method == 'POST':
        admin_email = request.data.get('admin_notification_email')
        gemini_api_key = request.data.get('gemini_api_key')

        if admin_email is not None:
            SystemSetting.objects.update_or_create(
                key='admin_notification_email',
                defaults={'value': admin_email.strip(), 'description': 'Email chủ shop nhận thông báo đơn hàng'}
            )

        if gemini_api_key is not None and gemini_api_key.strip():
            # Không cập nhật nếu người dùng gửi lại masked string
            if '...' not in gemini_api_key:
                SystemSetting.objects.update_or_create(
                    key='gemini_api_key',
                    defaults={'value': gemini_api_key.strip(), 'description': 'Google Gemini API Key'}
                )

        return Response({'message': 'Cập nhật cấu hình thành công!'})
