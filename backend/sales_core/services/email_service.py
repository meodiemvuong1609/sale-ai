import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from sales_core.models import SystemSetting

logger = logging.getLogger(__name__)


def get_admin_notification_email():
    """Lấy email nhận thông báo từ SystemSetting hoặc Django settings"""
    try:
        setting = SystemSetting.objects.filter(key='admin_notification_email').first()
        if setting and setting.value.strip():
            return setting.value.strip()
    except Exception:
        pass
    return getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', 'admin@sale-ai.vn')


def send_order_notification_email(order):
    """Gửi email HTML chi tiết đơn hàng đến cho chủ shop"""
    recipient_email = get_admin_notification_email()
    subject = f"🔥 [ĐƠN HÀNG MỚI #{order.id}] {order.customer_name} - {order.total_amount:,.0f} đ"

    context = {
        'order': order,
    }

    try:
        html_content = render_to_string('emails/order_notification.html', context)
        text_content = strip_tags(html_content)

        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@sale-ai.vn')

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[recipient_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

        order.email_sent = True
        order.save(update_fields=['email_sent'])
        logger.info(f"Đã gửi email thông báo đơn hàng {order.id} tới {recipient_email}")
        return True, f"Email sent successfully to {recipient_email}"
    except Exception as e:
        logger.error(f"Lỗi khi gửi email đơn hàng {order.id}: {str(e)}")
        return False, str(e)
