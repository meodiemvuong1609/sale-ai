import json
import logging
import os
import re
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from sales_core.models import Product, ChatSession, ChatMessage, Order, OrderItem, SystemSetting
from sales_core.services.email_service import send_order_notification_email

logger = logging.getLogger(__name__)


def get_gemini_api_key():
    """Lấy API Key từ SystemSetting, Django settings hoặc env"""
    try:
        setting = SystemSetting.objects.filter(key='gemini_api_key').first()
        if setting and setting.value.strip():
            return setting.value.strip()
    except Exception:
        pass
    return getattr(settings, 'GEMINI_API_KEY', '') or os.environ.get('GEMINI_API_KEY', '')


def build_product_catalog_context():
    """Tạo bản tóm tắt danh mục sản phẩm thực tế của cửa hàng để đưa vào System Prompt"""
    products = Product.objects.filter(is_active=True)
    if not products.exists():
        return "Hiện chưa có sản phẩm nào trong cửa hàng."

    catalog_lines = []
    for p in products:
        price_sale = f"{p.sale_price:,.0f}đ" if p.sale_price else "Không sale"
        price_orig = f"{p.price:,.0f}đ"
        usp = p.selling_points.replace('\n', ' ') if p.selling_points else p.short_description
        faq = p.faq.replace('\n', ' ') if p.faq else ""
        catalog_lines.append(
            f"- [{p.id}] {p.name} (SKU: {p.sku}): Giá ưu đãi: {price_sale} (Giá gốc: {price_orig}). Tồn kho: {p.stock} cái.\n"
            f"  + Điểm nổi bật & quà tặng: {usp}\n"
            f"  + FAQ: {faq}"
        )
    return "\n".join(catalog_lines)


def build_system_prompt(language='vi'):
    catalog = build_product_catalog_context()
    
    if language == 'lo':
        return f"""ເຈົ້າແມ່ນພະນັກງານຂາຍ ແລະ ໃຫ້ຄຳປຶກສາລູກຄ້າທີ່ເປັນກັນເອງ, ສຸພາບ ແລະ ເປັນມືອາຊີບຂອງຮ້ານ (ເອີ້ນຕົວເອງວ່າ "ນ້ອງ", ເອີ້ນລູກຄ້າວ່າ "ທ່ານ" ຫຼື "ອ້າຍ/ເອື້ອຍ").
ເຈົ້າສື່ສານດ້ວຍ ພາສາລາວ (Lao Language) ຢ່າງເປັນທຳມະຊາດ, ກົງໄປກົງມາ, ສັ້ນກະທັດຮັດ (2-4 ປະໂຫຍກຕໍ່ຂໍ້ຄວາມ) ແລະ ເຂົ້າໃຈຄວາມຕ້ອງການຂອງລູກຄ້າ.

ຫຼັກການສື່ສານ ແລະ ປິດການຂາຍ:
1. ຕອບກົງກັບຄຳຖາມ ແລະ ບໍລິບົດ:
   - ລູກຄ້າຖາມຫຍັງ (ລາຄາ, ສຽງດັງ, ພື້ນທີ່ຫ້ອງ, ຂອງແຖມ, ການຮັບປະກັນ...), ໃຫ້ຕອບກົງຈຸດນັ້ນກ່ອນ.
   - ຈື່ບໍລິບົດທີ່ລູກຄ້າໄດ້ບອກມາກ່ອນໜ້ານີ້ (ຊື່, ຂະໜາດຫ້ອງ, ສັດລ້ຽງ, ເດັກນ້ອຍ...). ບໍ່ຖາມຊ້ຳສິ່ງທີ່ລູກຄ້າບອກແລ້ວ.
2. ເວົ້າຈາເປັນທຳມະຊາດ, ບໍ່ໃຊ້ຄຳເວົ້າຫຸ່ນຍົນ, ຂໍ້ຄວາມສັ້ນ 2-4 ປະໂຫຍກ, ແບ່ງວັກຕອນໃຫ້ອ່ານງ່າຍສະບາຍຕາ.
3. ພຽງແຕ່ແນະນຳສິນຄ້າທີ່ມີຢູ່ໃນຮ້ານ:
{catalog}
4. ເຕັກນິກການປິດການຂາຍ (Closing Deal):
   - ເມື່ອລູກຄ້າພໍໃຈ: "ໂດຍ ນ້ອງຂໍອະນຸຍາດເກັບສິດໂປຣໂມຊັນ ແລະ ຂອງແຖມນີ້ໄວ້ໃຫ້ອ້າຍ/ເອື້ອຍເດີ. ຂໍຊື່, ເບີໂທລະສັບ ແລະ ທີ່ຢູ່ຈັດສົ່ງເພື່ອລົງອໍເດີຈັດສົ່ງໃຫ້ໄວທີ່ສຸດເຈົ້າ!".
   - ເມື່ອລູກຄ້າແຈ້ງ ຊື່, ເບີໂທລະສັບ ແລະ ທີ່ຢູ່: ເຈົ້າຕ້ອງຮຽກໃຊ້ TOOL `create_order` ທັນທີເພື່ອສ້າງອໍເດີໃນລະບົບ!
   - ຫຼັງຈາກສ້າງອໍເດີສຳເລັດ: ຢືນຢັນລະຫັດອໍເດີ, ຂອບໃຈລູກຄ້າ ແລະ ແຈ້ງວ່າສາມາດກວດກາສິນຄ້າກ່ອນຈ່າຍເງິນ (COD) ໄດ້ເລີຍ.
"""

    return f"""Bạn là em nhân viên tư vấn bán hàng và chăm sóc khách hàng của cửa hàng (xưng "em", gọi khách là "anh/chị").
Bạn giao tiếp giống như một chuyên viên bán hàng thực tế qua Zalo hoặc Messenger: tự nhiên, gần gũi, súc tích và cực kỳ hiểu tâm lý khách hàng.

NGUYÊN TẮC GIAO TIẾP VÀ TƯ VẤN THỰC TẾ:
1. TRẢ LỜI ĐÚNG TRỌNG TÂM & BÁM SÁT NGỮ CẢNH:
   - Khách hỏi gì thì trả lời thẳng vào câu hỏi đó trước tiên (về giá, độ ồn, diện tích sử dụng, bảo hành, cách vệ sinh...). Không né tránh, không dài dòng.
   - Nhớ ngữ cảnh đã nói ở các câu trước (nếu khách nói nhà có em bé, nuôi mèo, nhà 3 tầng, hoặc tên khách... phải nhớ và gắn liền câu trả lời với bối cảnh đó). Tuyệt đối không hỏi lại những gì khách đã cung cấp.

2. CÁCH NÓI CHUYỆN TỰ NHIÊN, KHÔNG MÁY MÓC:
   - Tuyệt đối KHÔNG dùng văn mẫu rập khuôn kiểu robot ("Chào bạn! Tôi là trợ lý ảo...").
   - KHÔNG đặt câu hỏi dồn dập như khảo sát/làm bài kiểm tra. Mỗi tin nhắn chỉ dài từ 2-4 câu ngắn gọn, cách dòng thoáng, giống như người thật gõ chat.
   - Chia sẻ chân thành góc nhìn thực tế: "Mẫu này khách bên em khen nhất là...", "Độ ồn máy chỉ tầm 58dB rất êm anh nhé...".

3. CHỈ TƯ VẤN SẢN PHẨM CÓ TRONG CỬA HÀNG:
   - Tuyệt đối KHÔNG đề xuất các thương hiệu hoặc mã máy không có trong cửa hàng.
   - Dưới đây là danh mục sản phẩm THỰC TẾ của cửa hàng:
{catalog}

4. KỸ THUẬT CHỐT ĐƠN (CLOSING DEAL):
   - Khi khách đã ưng ý: Chủ động xin thông tin nhẹ nhàng: "Dạ em giữ quà tặng và suất giảm giá này cho anh/chị nhé. Anh/Chị cho em xin tên, số điện thoại và địa chỉ nhận hàng để em lên đơn gửi đi sớm nha!".
   - KHI KHÁCH CUNG CẤP TÊN, SỐ ĐIỆN THOẠI VÀ ĐỊA CHỈ: Bạn BẮT BUỘC PHẢI GỌI TOOL `create_order` ngay lập tức để tạo đơn hàng trong hệ thống.
   - Sau khi gọi tool thành công: Xác nhận lại mã đơn hàng, cảm ơn khách và nhắc khách: "Hàng giao tới nơi anh/chị được kiểm tra hàng thoải mái trước khi thanh toán COD ạ!".
"""


def process_sales_chat(session: ChatSession, user_message: str, language: str = None) -> dict:
    """
    Xử lý tin nhắn khách hàng gửi đến với đa ngôn ngữ (vi, lo):
    1. Lưu tin nhắn người dùng vào DB.
    2. Gọi Gemini thông qua Google GenAI SDK Chat.
    3. Hỗ trợ Function Calling chốt đơn và gửi email cho chủ shop.
    4. Trả về phản hồi và metadata cho frontend.
    """
    lang = language or session.language or 'vi'

    # 1. Lưu tin nhắn của khách
    ChatMessage.objects.create(
        session=session,
        sender='user',
        content=user_message
    )

    api_key = get_gemini_api_key()

    if api_key and api_key != 'YOUR_GEMINI_API_KEY':
        try:
            return _call_gemini_chat(session, user_message, api_key, language=lang)
        except Exception as e:
            logger.warning(f"Gemini API call failed: {e}. Falling back to Smart Sales Engine.")
            return _fallback_smart_sales_engine(session, user_message, str(e), language=lang)
    else:
        return _fallback_smart_sales_engine(session, user_message, "GEMINI_API_KEY_NOT_SET", language=lang)


def _call_gemini_chat(session: ChatSession, user_message: str, api_key: str, language: str = 'vi') -> dict:
    """Gọi Gemini qua client.chats.create hỗ trợ Multi-turn memory và Tool Calling thực tế"""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    created_order_data = {}

    # Định nghĩa công cụ tạo đơn hàng gắn với phiên chat hiện tại
    def create_order(customer_name: str, customer_phone: str, customer_address: str, product_name: str = "", quantity: int = 1, notes: str = "") -> str:
        """
        Tạo đơn hàng chính thức khi khách hàng đã cung cấp đủ Họ Tên, Số điện thoại và Địa chỉ nhận hàng.
        Args:
            customer_name: Họ và tên người nhận hàng
            customer_phone: Số điện thoại liên hệ nhận hàng
            customer_address: Địa chỉ nhận hàng chi tiết
            product_name: Tên hoặc mã sản phẩm khách đặt mua
            quantity: Số lượng sản phẩm khách mua
            notes: Ghi chú thêm nếu có
        """
        try:
            # Tìm sản phẩm phù hợp trong DB
            product = None
            if product_name:
                product = Product.objects.filter(name__icontains=product_name, is_active=True).first()
                if not product:
                    product = Product.objects.filter(sku__icontains=product_name, is_active=True).first()
            if not product:
                product = Product.objects.filter(is_active=True).first()

            unit_price = Decimal(product.current_price) if product else Decimal(500000)
            p_name = product.name if product else (product_name or "Sản phẩm tư vấn")
            qty = max(1, int(quantity or 1))
            total_amount = unit_price * qty

            order_id = f"ORD-{timezone.now().strftime('%Y%m%d')}-{Order.objects.count() + 1:04d}"

            # Lưu đơn hàng
            order = Order.objects.create(
                id=order_id,
                session=session,
                customer_name=customer_name.strip(),
                customer_phone=customer_phone.strip(),
                customer_address=customer_address.strip(),
                total_amount=total_amount,
                status='CONFIRMED',
                notes=notes.strip() if notes else f"Đơn hàng được chốt tự động bởi AI Sales Rep cho sản phẩm {p_name}"
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=p_name,
                quantity=qty,
                price=unit_price,
                subtotal=total_amount
            )

            # Cập nhật thông tin khách vào session
            session.customer_name = customer_name.strip()
            session.customer_phone = customer_phone.strip()
            session.customer_address = customer_address.strip()
            session.status = 'order_placed'
            session.save()

            # Gửi email HTML thông báo cho chủ shop ngay lập tức
            email_sent, _ = send_order_notification_email(order)

            created_order_data['id'] = order.id
            created_order_data['customer_name'] = order.customer_name
            created_order_data['customer_phone'] = order.customer_phone
            created_order_data['customer_address'] = order.customer_address
            created_order_data['total_amount'] = float(order.total_amount)
            created_order_data['status'] = order.status

            return json.dumps({
                "success": True,
                "order_id": order.id,
                "customer_name": order.customer_name,
                "product_name": p_name,
                "total_amount": float(total_amount),
                "message": "Đã tạo đơn hàng thành công và gửi email thông báo cho chủ shop!"
            }, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Lỗi tạo đơn hàng trong tool: {e}")
            return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

    def get_product_details(product_id: int) -> str:
        """Lấy chi tiết sản phẩm theo ID"""
        p = Product.objects.filter(id=product_id, is_active=True).first()
        if not p:
            return "Không tìm thấy sản phẩm."
        return json.dumps({
            "name": p.name,
            "price": float(p.current_price),
            "stock": p.stock,
            "selling_points": p.selling_points,
            "faq": p.faq
        }, ensure_ascii=False)

    # 2. Chuẩn bị lịch sử hội thoại trước đó (tối đa 12 tin nhắn gần nhất)
    # Lấy các tin nhắn TRƯỚC tin nhắn hiện tại
    past_messages = session.messages.order_by('created_at')
    # Loại bỏ tin nhắn người dùng vừa mới lưu để gửi qua chat.send_message
    past_list = list(past_messages)
    if past_list and past_list[-1].sender == 'user':
        past_list = past_list[:-1]

    history = []
    for msg in past_list[-12:]:
        role = "user" if msg.sender == "user" else "model"
        history.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg.content)]
            )
        )

    system_instruction = build_system_prompt(language=language)
    model_name = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.7,
        tools=[create_order, get_product_details]
    )

    chat = client.chats.create(
        model=model_name,
        history=history,
        config=config
    )

    # 3. Gửi tin nhắn hiện tại
    response = chat.send_message(user_message)
    reply_text = response.text or (
        "ໂດຍ ນ້ອງສາມາດຊ່ວຍເຫຼືອ ຫຼື ໃຫ້ຂໍ້ມູນຫຍັງເພີ່ມເຕີມແດ່ເຈົ້າ?" if language == 'lo' else "Dạ em có thể hỗ trợ thêm thông tin gì cho mình không ạ?"
    )

    # 4. Chuẩn bị metadata trả về frontend
    metadata = {}
    if created_order_data:
        metadata['order'] = created_order_data
    else:
        # Kiểm tra xem có đơn hàng nào vừa được tạo trong session này không
        latest_order = Order.objects.filter(session=session).order_by('-created_at').first()
        if latest_order:
            metadata['order'] = {
                'id': latest_order.id,
                'customer_name': latest_order.customer_name,
                'customer_phone': latest_order.customer_phone,
                'customer_address': latest_order.customer_address,
                'total_amount': float(latest_order.total_amount),
                'status': latest_order.status
            }
        else:
            # Gợi ý sản phẩm liên quan để hiển thị thẻ sản phẩm trong khung chat
            msg_lower = user_message.lower() + " " + reply_text.lower()
            matched_products = []
            for p in Product.objects.filter(is_active=True):
                if p.name.lower() in msg_lower or p.sku.lower() in msg_lower or any(w in msg_lower for w in p.name.lower().split()[:2]):
                    matched_products.append(p)
            
            if not matched_products:
                matched_products = list(Product.objects.filter(is_active=True)[:2])
            
            metadata['suggested_products'] = [_prod_to_dict(p) for p in matched_products[:2]]

    # 5. Lưu tin nhắn phản hồi của Assistant
    ChatMessage.objects.create(
        session=session,
        sender='assistant',
        content=reply_text,
        metadata=metadata
    )

    return {
        'reply': reply_text,
        'metadata': metadata,
        'session_id': str(session.id)
    }


def _fallback_smart_sales_engine(session: ChatSession, user_message: str, reason: str, language: str = 'vi') -> dict:
    """Smart Fallback Sales Engine khi chưa có API key hoặc mạng gián đoạn"""
    msg_lower = user_message.lower()
    metadata = {}

    phone_match = re.search(r'(0\d{9,10}|\+84\d{9,10}|\+856\d{8,10}|\b\d{8,11}\b)', user_message)

    if phone_match:
        phone = phone_match.group(1)
        name = session.customer_name or ("ທ່ານລູກຄ້າ" if language == 'lo' else "Anh/Chị")
        address = session.customer_address or ("ທີ່ຢູ່ຈັດສົ່ງ" if language == 'lo' else "Địa chỉ nhận hàng")

        addr_match = re.search(r'(?i)(?:địa chỉ:?|đc:?|giao đến:?|giao qua:?|giao về:?|ທີ່ຢູ່:?|ສົ່ງຮອດ:?)\s*([^;\n]+)', user_message)
        if addr_match:
            clean_addr = re.sub(r'(?i)(,\s*)?(giao cho anh|giao cho em|giao giúp|nhé|nha|ạ|ເດີ|ເຈົ້າ)\s*$', '', addr_match.group(1)).strip()
            if clean_addr:
                address = clean_addr

        name_match = re.search(r'(?i)(?:tên là|mình tên|em tên|anh tên|chị tên|tên:?|ຊື່:?|ຂ້ອຍຊື່)\s*([^,;\n]+)', user_message)
        if name_match:
            clean_name = re.sub(r'(?i)(chốt đơn|oke|ok|dạ|ạ|nhé|sđt|số điện thoại|ເບີໂທ).*', '', name_match.group(1)).strip()
            if clean_name and len(clean_name) < 50:
                name = clean_name

        session.customer_name = name
        session.customer_phone = phone
        session.customer_address = address
        session.status = 'order_placed'
        session.save()

        product = Product.objects.filter(is_active=True).first()
        for p in Product.objects.filter(is_active=True):
            if p.name.lower() in msg_lower or p.sku.lower() in msg_lower:
                product = p
                break

        unit_price = Decimal(product.current_price) if product else Decimal(500000)
        p_name = product.name if product else "Sản phẩm chọn mua"
        order_id = f"ORD-{timezone.now().strftime('%Y%m%d')}-{Order.objects.count() + 1:04d}"

        order = Order.objects.create(
            id=order_id,
            session=session,
            customer_name=name,
            customer_phone=phone,
            customer_address=address,
            total_amount=unit_price,
            status='CONFIRMED',
            notes=f"Chốt đơn từ phiên chat {str(session.id)[:8]} (Ngôn ngữ: {language})"
        )
        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=p_name,
            quantity=1,
            price=unit_price,
            subtotal=unit_price
        )
        send_order_notification_email(order)

        if language == 'lo':
            reply_text = (
                f"ໂດຍ ນ້ອງໄດ້ລົງອໍເດີສຳເລັດແລ້ວ ລະຫັດ **{order.id}** ໃຫ້ {name} ເຈົ້າ! 🥳\n\n"
                f"ສິນຄ້າ **{p_name}** ({unit_price:,.0f} đ) ຈະຖືກຈັດສົ່ງໄປທີ່: {address}.\n"
                f"ເມື່ອສິນຄ້າໄປຮອດ ທ່ານສາມາດກວດກາສິນຄ້າໄດ້ຢ່າງສະບາຍໃຈກ່ອນຈ່າຍເງິນ COD ເດີ. ຂອບໃຈ {name} ຫຼາຍໆເຈົ້າ! 🙏"
            )
        else:
            reply_text = (
                f"Dạ em đã lên đơn thành công mã **{order.id}** cho {name} rồi ạ! 🥳\n\n"
                f"Đơn hàng **{p_name}** ({unit_price:,.0f}đ) sẽ được gửi đến địa chỉ: {address}.\n"
                f"Hàng tới nơi mình được kiểm tra thoải mái rồi mới thanh toán COD cho bạn giao hàng nhé ạ. Em cảm ơn {name} nhiều!"
            )

        metadata['order'] = {
            'id': order.id,
            'customer_name': name,
            'customer_phone': phone,
            'customer_address': address,
            'total_amount': float(unit_price),
            'status': 'CONFIRMED'
        }

    elif any(w in msg_lower for w in ['ồn', 'tiếng kêu', 'bé ngủ', 'ສຽງດັງ']):
        if language == 'lo':
            reply_text = (
                "ໂດຍ ທ່ານສະບາຍໃຈໄດ້ເລີຍເຈົ້າ, ຫຸ່ນຍົນ Dreame L10s Ultra Gen 2 ນີ້ເຮັດວຽກງຽບຫຼາຍ (ສຽງດັງພຽງ 58-60dB ເທົ່ານັ້ນ).\n\n"
                "ເຮົາສາມາດຕັ້ງຄ່າໂໝດງຽບໃນແອັບ ຫຼື ຕັ້ງເວລາໃຫ້ເຮັດວຽກຕອນທີ່ເຮົາອອກໄປຂ້າງນອກໄດ້, ບໍ່ລົບກວນເວລານອນແນ່ນອນເຈົ້າ. ພື້ນເຮືອນຂອງທ່ານເປັນພື້ນໄມ້ ຫຼື ພື້ນກະໂລ້ເຈົ້າ?"
            )
        else:
            reply_text = (
                "Dạ anh yên tâm ạ, dòng Dreame L10s Ultra Gen 2 này chạy cực kỳ êm luôn ạ (độ ồn chỉ khoảng 58-60dB thôi).\n\n"
                "Mình có thể cài đặt chế độ hoạt động im lặng trên app hoặc hẹn giờ cho máy dọn lúc bé thức chơi, đảm bảo không ảnh hưởng giấc ngủ của bé đâu ạ. Nhà mình hiện tại sàn gạch hay sàn gỗ vậy anh?"
            )
        p = Product.objects.filter(name__icontains='Dreame').first()
        if p:
            metadata['suggested_products'] = [_prod_to_dict(p)]

    elif any(w in msg_lower for w in ['giá', 'nhiêu', 'khuyến mãi', 'sale', 'ລາຄາ', 'ໂປຣໂມຊັນ']):
        p = Product.objects.filter(name__icontains='Dreame').first() or Product.objects.first()
        if language == 'lo':
            reply_text = (
                f"ໂດຍ ລຸ້ນ {p.name} ລາຄາປົກກະຕິ {p.price:,.0f}đ ແຕ່ມື້ນີ້ຮ້ານເຮົາມີໂປຣໂມຊັນພິເສດຫຼຸດເຫຼືອພຽງ **{p.sale_price:,.0f}đ** ເທົ່ານັ້ນເຈົ້າ!\n\n"
                f"ພ້ອມແຖມຟຣີ ຊຸດອຸປະກອນເສີມ 5 ຢ່າງ ມູນຄ່າ 1,200,000đ ແລະ ຮັບປະກັນສູນແທ້ 2 ປີ. ທ່ານຢາກໃຫ້ນ້ອງເກັບສິດຂອງແຖມນີ້ໄວ້ໃຫ້ເລີຍບໍ່ເຈົ້າ?"
            )
        else:
            reply_text = (
                f"Dạ mẫu {p.name} giá gốc {p.price:,.0f}đ nhưng hôm nay bên em đang sale mạnh còn **{p.sale_price:,.0f}đ** thôi ạ!\n\n"
                f"Đặc biệt được tặng kèm luôn bộ phụ kiện 5 món trị giá 1.200.000đ và bảo hành chính hãng 2 năm 1 đổi 1. Anh có muốn em giữ suất quà này cho mình không ạ?"
            )
        metadata['suggested_products'] = [_prod_to_dict(p)]

    else:
        p = Product.objects.first()
        if language == 'lo':
            reply_text = (
                f"ສະບາຍດີເຈົ້າ! ນ້ອງແມ່ນພະນັກງານໃຫ້ຄຳປຶກສາຂອງຮ້ານ.\n\n"
                f"ມື້ນີ້ທາງຮ້ານເຮົາມີໂປຣໂມຊັນຫຼຸດລາຄາພິເສດ ແລະ ແຖມຂອງຂວັນສຳລັບຫຸ່ນຍົນດູດຝຸ່ນ Dreame ແລະ ເຄື່ອງຟອກອາກາດ Dyson ເຈົ້າ.\n\n"
                f"ທ່ານກຳລັງຊອກຫາສິນຄ້າປະເພດໃດ ຫຼື ຢາກໃຫ້ນ້ອງແນະນຳລຸ້ນໃດໃຫ້ເໝາະກັບເຮືອນຂອງທ່ານແດ່ເຈົ້າ? 😊"
            )
        else:
            reply_text = (
                f"Dạ em chào anh/chị ạ! Anh/chị đang cần tìm sản phẩm gia dụng hay công nghệ cho gia đình mình thế ạ? "
                f"Hôm nay bên em đang có ưu đãi giảm giá sâu và tặng quà cho dòng robot hút bụi Dreame và máy lọc không khí Dyson đó ạ."
            )
        metadata['suggested_products'] = [_prod_to_dict(p)]

    ChatMessage.objects.create(
        session=session,
        sender='assistant',
        content=reply_text,
        metadata=metadata
    )

    return {
        'reply': reply_text,
        'metadata': metadata,
        'session_id': str(session.id)
    }


def _prod_to_dict(p):
    if not p:
        return {}
    return {
        'id': p.id,
        'name': p.name,
        'price': float(p.price),
        'sale_price': float(p.sale_price) if p.sale_price else float(p.price),
        'image_url': p.image_url,
        'short_description': p.short_description
    }
