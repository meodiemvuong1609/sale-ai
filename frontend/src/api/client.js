const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const api = {
  // Products
  async getProducts() {
    const res = await fetch(`${API_BASE_URL}/products/`);
    if (!res.ok) throw new Error('Không thể tải danh sách sản phẩm');
    return res.json();
  },

  async createProduct(productData) {
    const res = await fetch(`${API_BASE_URL}/products/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(productData),
    });
    if (!res.ok) throw new Error('Không thể tạo sản phẩm mới');
    return res.json();
  },

  async updateProduct(id, productData) {
    const res = await fetch(`${API_BASE_URL}/products/${id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(productData),
    });
    if (!res.ok) throw new Error('Không thể cập nhật sản phẩm');
    return res.json();
  },

  async deleteProduct(id) {
    const res = await fetch(`${API_BASE_URL}/products/${id}/`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Không thể xóa sản phẩm');
    return true;
  },

  // Chat
  async startChat(sessionId = null, language = 'vi') {
    const res = await fetch(`${API_BASE_URL}/chat/start/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, language }),
    });
    if (!res.ok) throw new Error('Không thể khởi tạo phiên chat');
    return res.json();
  },

  async sendMessage(sessionId, message, language = 'vi') {
    const res = await fetch(`${API_BASE_URL}/chat/send/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, message, language }),
    });
    if (!res.ok) throw new Error('Không thể gửi tin nhắn');
    return res.json();
  },

  async getChatHistory(sessionId) {
    const res = await fetch(`${API_BASE_URL}/chat/history/${sessionId}/`);
    if (!res.ok) throw new Error('Không thể tải lịch sử chat');
    return res.json();
  },

  // Orders
  async getOrders() {
    const res = await fetch(`${API_BASE_URL}/orders/`);
    if (!res.ok) throw new Error('Không thể tải danh sách đơn hàng');
    return res.json();
  },

  // Settings
  async getSettings() {
    const res = await fetch(`${API_BASE_URL}/settings/`);
    if (!res.ok) throw new Error('Không thể tải cài đặt hệ thống');
    return res.json();
  },

  async updateSettings(settingsData) {
    const res = await fetch(`${API_BASE_URL}/settings/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settingsData),
    });
    if (!res.ok) throw new Error('Không thể cập nhật cài đặt');
    return res.json();
  },
};
