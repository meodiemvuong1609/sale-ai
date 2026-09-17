import uuid
from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tên sản phẩm")
    sku = models.CharField(max_length=100, unique=True, verbose_name="Mã SKU")
    category = models.CharField(max_length=100, default="Chung", verbose_name="Danh mục")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá niêm yết (VNĐ)")
    sale_price = models.DecimalField(
        max_digits=12, decimal_places=0, null=True, blank=True, verbose_name="Giá khuyến mãi (VNĐ)"
    )
    stock = models.IntegerField(default=10, verbose_name="Số lượng tồn kho")
    short_description = models.CharField(max_length=500, blank=True, verbose_name="Mô tả ngắn")
    description = models.TextField(blank=True, verbose_name="Mô tả chi tiết")
    selling_points = models.TextField(
        blank=True,
        help_text="Các điểm bán hàng vượt trội (USP), quà tặng kèm, ưu đãi đặc biệt để AI thuyết phục khách",
        verbose_name="Điểm nhấn bán hàng (USP)"
    )
    faq = models.TextField(
        blank=True,
        help_text="Câu hỏi thường gặp và giải đáp mẫu",
        verbose_name="FAQ thường gặp"
    )
    image_url = models.URLField(max_length=1000, blank=True, verbose_name="Đường dẫn ảnh")
    is_active = models.BooleanField(default=True, verbose_name="Đang kinh doanh")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Danh sách sản phẩm"

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def current_price(self):
        return self.sale_price if self.sale_price is not None and self.sale_price > 0 else self.price


class ChatSession(models.Model):
    STATUS_CHOICES = (
        ('active', 'Đang trò chuyện'),
        ('order_placed', 'Đã chốt đơn'),
        ('closed', 'Đã đóng'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=150, blank=True, default="")
    customer_phone = models.CharField(max_length=50, blank=True, default="")
    customer_address = models.TextField(blank=True, default="")
    language = models.CharField(max_length=10, default='vi', verbose_name="Ngôn ngữ")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Phiên chat"
        verbose_name_plural = "Danh sách phiên chat"

    def __str__(self):
        return f"Chat {str(self.id)[:8]} - {self.customer_name or 'Khách vãng lai'}"


class ChatMessage(models.Model):
    SENDER_CHOICES = (
        ('user', 'Khách hàng'),
        ('assistant', 'AI Sales Rep'),
        ('system', 'Hệ thống'),
    )

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.sender}] {self.content[:40]}..."


class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Chờ xác nhận'),
        ('CONFIRMED', 'Đã chốt đơn'),
        ('SHIPPING', 'Đang giao hàng'),
        ('COMPLETED', 'Hoàn tất'),
        ('CANCELLED', 'Đã hủy'),
    )

    id = models.CharField(max_length=50, primary_key=True, verbose_name="Mã đơn hàng")
    session = models.ForeignKey(
        ChatSession, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders'
    )
    customer_name = models.CharField(max_length=200, verbose_name="Tên khách hàng")
    customer_phone = models.CharField(max_length=50, verbose_name="Số điện thoại")
    customer_address = models.TextField(verbose_name="Địa chỉ nhận hàng")
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Tổng tiền (VNĐ)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED', verbose_name="Trạng thái")
    notes = models.TextField(blank=True, default="", verbose_name="Ghi chú đơn hàng")
    email_sent = models.BooleanField(default=False, verbose_name="Đã gửi email thông báo")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Thời gian tạo")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Danh sách đơn hàng"

    def __str__(self):
        return f"{self.id} - {self.customer_name} ({self.total_amount:,.0f} đ)"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=0)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"


class SystemSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True, default="")
    description = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return f"{self.key}: {self.value[:30]}"
