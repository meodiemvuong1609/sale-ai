from django.core.management.base import BaseCommand
from sales_core.models import Product


SAMPLE_PRODUCTS = [
    {
        "name": "Robot hút bụi lau nhà Dreame L10s Ultra Gen 2",
        "sku": "DREAME-L10S-GEN2",
        "category": "Gia dụng thông minh",
        "price": 18990000,
        "sale_price": 14990000,
        "stock": 15,
        "short_description": "Lực hút siêu khủng 10.000Pa, tự động giặt giẻ nước nóng 60°C và sấy khô, tự đổ rác 75 ngày.",
        "description": "Dreame L10s Ultra Gen 2 là siêu phẩm robot hút bụi thông minh bậc nhất hiện nay. Trạm sạc all-in-one tự động hút bụi vào túi chứa 3.2L, tự pha dung dịch lau sàn, tự giặt giẻ bằng nước nóng 60°C diệt khuẩn 99.9% và sấy khô bằng khí nóng chống ẩm mốc. Công nghệ camera AI kết hợp laser 3D tránh chướng ngại vật chuẩn xác.",
        "selling_points": "• Giảm ngay 4 triệu trong tuần lễ tri ân\n• Tặng kèm bộ phụ kiện 5 món trị giá 1.200.000đ (chổi + 4 giẻ lau + nước lau sàn chuyên dụng)\n• Miễn phí vận chuyển toàn quốc & lắp đặt hướng dẫn tại nhà\n• Bảo hành chính hãng 24 tháng 1 đổi 1 trong 30 ngày nếu lỗi NSX",
        "faq": "Q: Nhà có nhiều tầng robot có lưu bản đồ được không?\nA: Dạ robot lưu được tối đa 4 tầng bản đồ riêng biệt rất tiện lợi ạ!\nQ: Có tự động nâng giẻ khi lên thảm không?\nA: Dạ có, cảm biến siêu âm phát hiện thảm và tự nâng giẻ 10.5mm để thảm không bị ướt.",
        "image_url": "https://images.unsplash.com/photo-1616401784845-180882ba9ba8?auto=format&fit=crop&w=800&q=80",
        "is_active": True
    },
    {
        "name": "Máy lọc không khí Dyson Purifier Cool Formaldehyde TP09",
        "sku": "DYSON-TP09-GOLD",
        "category": "Không gian sống & Sức khỏe",
        "price": 21500000,
        "sale_price": 17900000,
        "stock": 8,
        "short_description": "Lọc sạch 99.95% bụi siêu mịn PM0.1, tiêu hủy formaldehyde liên tục trọn đời máy, kèm quạt làm mát dịu nhẹ.",
        "description": "Dyson TP09 tích hợp cảm biến formaldehyde thể rắn chính xác tuyệt đối, bộ lọc xúc tác Cryptomic phá hủy vĩnh viễn phân tử formaldehyde thành nước và CO2 mà không cần thay lõi lọc xúc tác. Toàn bộ máy đạt tiêu chuẩn khép kín HEPA H13, ngăn ngừa bụi bẩn rò rỉ ngược ra phòng.",
        "selling_points": "• Giá ưu đãi độc quyền rẻ hơn thị trường 3.6 triệu\n• Tặng voucher 500.000đ trừ trực tiếp khi thanh toán\n• Trả góp 0% lãi suất qua thẻ tín dụng\n• Bảo hành 2 năm chính hãng Dyson Việt Nam tận nhà",
        "faq": "Q: Phòng 40m2 dùng có đủ tải không?\nA: Dạ công nghệ Air Multiplier khuếch tán luồng gió tinh khiết 290 lít/giây, phủ đều phòng tới 50m2 rất nhanh chỉ sau 15-20 phút!",
        "image_url": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?auto=format&fit=crop&w=800&q=80",
        "is_active": True
    },
    {
        "name": "Bàn chải điện Oral-B iO Series 9 AI",
        "sku": "ORALB-IO-9",
        "category": "Chăm sóc cá nhân",
        "price": 6500000,
        "sale_price": 4890000,
        "stock": 25,
        "short_description": "Trí tuệ nhân tạo theo dõi 16 vùng răng theo thời gian thực 3D, màn hình màu tương tác, cảm biến lực thông minh.",
        "description": "Oral-B iO Series 9 kết hợp đầu tròn độc quyền với rung vi mô từ tính êm ái, mang lại cảm giác sạch bóng chuẩn nha khoa. Cảm biến lực bảo vệ nướu bằng đèn cảnh báo đỏ (quá mạnh), trắng (quá nhẹ), xanh lá (hoàn hảo). Đi kèm hộp sạc du lịch sạc cùng lúc cả bàn chải và điện thoại.",
        "selling_points": "• Tặng 2 đầu bàn chải thay thế chính hãng iO Ultimate Clean trị giá 450.000đ\n• Bảo hành 1 đổi 1 trong 12 tháng\n• Ship hoả tốc 2 giờ nội thành",
        "faq": "Q: Răng nhạy cảm hay chảy máu chân răng có dùng được không?\nA: Dạ máy có riêng chế độ Super Sensitive cực kỳ êm ái cho răng nướu nhạy cảm, cải thiện sức khỏe nướu rõ rệt sau 1 tuần dùng.",
        "image_url": "https://images.unsplash.com/photo-1559591937-e11a3b379b18?auto=format&fit=crop&w=800&q=80",
        "is_active": True
    },
    {
        "name": "Nồi chiên không dầu kết hợp hấp Philips Airfryer XXL Combi HD9880",
        "sku": "PHILIPS-HD9880",
        "category": "Nhà bếp hiện đại",
        "price": 12990000,
        "sale_price": 9990000,
        "stock": 12,
        "short_description": "Dung tích khủng 8.3L (2kg thực phẩm), công nghệ Rapid CombiAir kết hợp chiên nướng hấp mọng nước bên trong giòn rụm bên ngoài.",
        "description": "Philips HD9880 7000 Series tích hợp nhiệt kế thực phẩm Food Thermometer thông minh tự động căn độ chín hoàn hảo cho bít tết hoặc gà nguyên con. 22 chức năng nấu trong 1 thiết bị, kết nối app HomeID với hơn 500 công thức chuẩn bếp trưởng.",
        "selling_points": "• Giảm sốc 3.000.000đ cho 10 khách hàng đầu tiên trong ngày\n• Tặng sách 100 công thức nấu ăn bằng nồi chiên và nhiệt kế thức ăn trị giá 600.000đ\n• Bảo hành toàn cầu 2 năm",
        "faq": "Q: Nướng gà nguyên con vừa không?\nA: Dạ dung tích XXL 8.3L chứa vừa gà nguyên con 2.2kg hoặc khẩu phần cho 7-8 người ăn thoải mái ạ.",
        "image_url": "https://images.unsplash.com/photo-1584990347449-3972626e27a9?auto=format&fit=crop&w=800&q=80",
        "is_active": True
    },
    {
        "name": "Máy ép chậm trục đứng Hurom H400 Easy Clean",
        "sku": "HUROM-H400",
        "category": "Nhà bếp hiện đại",
        "price": 11500000,
        "sale_price": 8900000,
        "stock": 20,
        "short_description": "Khoang chứa cực lớn ép nguyên trái không cần cắt nhỏ, trục ép tích hợp dao cắt thế hệ mới, tháo rửa vệ sinh chỉ trong 1 phút.",
        "description": "Hurom H400 sử dụng công nghệ vắt lấy nước chậm SST 70 vòng/phút giúp nước ép không bị sinh nhiệt, giữ nguyên 98% enzyme và vitamin. Trục ép cải tiến 2 trong 1 không dùng lưới lọc kim loại nên không bị kẹt bã, xả dưới vòi nước là sạch bong.",
        "selling_points": "• Tiết kiệm 2.600.000đ so với giá niêm yết\n• Tặng set 3 ly thủy tinh chịu nhiệt Hurom cao cấp\n• Động cơ AC siêu bền bỉ bảo hành tới 10 năm",
        "faq": "Q: Có ép được cần tây và rau má nhiều xơ không?\nA: Dạ máy thiết kế riêng dao cắt đảo chiều tự động nghiền nát rau xơ như cần tây, cải xoăn mà không lo tắc kẹt máy ạ!",
        "image_url": "https://images.unsplash.com/photo-1589733955941-5eeaf752f6dd?auto=format&fit=crop&w=800&q=80",
        "is_active": True
    }
]


class Command(BaseCommand):
    help = "Khởi tạo dữ liệu sản phẩm mẫu chất lượng cao cho AI Sales"

    def handle(self, *args, **options):
        count = 0
        for item in SAMPLE_PRODUCTS:
            product, created = Product.objects.update_or_create(
                sku=item["sku"],
                defaults=item
            )
            if created:
                count += 1
                self.stdout.write(self.style.SUCCESS(f"Đã tạo: {product.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Đã cập nhật: {product.name}"))

        self.stdout.write(self.style.SUCCESS(f"Hoàn tất nạp dữ liệu: {count} sản phẩm mới đã tạo."))
