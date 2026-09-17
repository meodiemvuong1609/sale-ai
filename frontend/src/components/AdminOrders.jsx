import React, { useState, useEffect } from 'react';
import { PackageCheck, Mail, Phone, MapPin, RefreshCw, Eye, X } from 'lucide-react';
import { api } from '../api/client';
import { useLanguage } from '../i18n/LanguageContext';

export default function AdminOrders() {
  const { t } = useLanguage();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState(null);

  useEffect(() => {
    loadOrders();
    const interval = setInterval(loadOrders, 8000); // Tự động làm mới mỗi 8 giây
    return () => clearInterval(interval);
  }, []);

  const loadOrders = async () => {
    try {
      const data = await api.getOrders();
      setOrders(data);
    } catch (err) {
      console.error('Error fetching orders:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-page">
      <div className="page-header">
        <div>
          <h2>
            <PackageCheck size={24} style={{ color: '#10b981' }} />
            {t.ordersPageTitle}
          </h2>
          <p>{t.ordersPageSubtitle}</p>
        </div>
        <button
          type="button"
          className="btn-secondary"
          onClick={loadOrders}
        >
          <RefreshCw size={16} /> {t.refreshBtn}
        </button>
      </div>

      <div className="table-card">
        <table className="custom-table">
          <thead>
            <tr>
              <th>{t.thOrderId}</th>
              <th>{t.thTime}</th>
              <th>{t.thCustomer}</th>
              <th>{t.thPhone}</th>
              <th>{t.thTotal}</th>
              <th>{t.thStatus}</th>
              <th>{t.thEmailStatus}</th>
              <th style={{ textAlign: 'right' }}>{t.thView}</th>
            </tr>
          </thead>
          <tbody>
            {loading && orders.length === 0 ? (
              <tr>
                <td colSpan="8" style={{ textAlign: 'center', padding: 30 }}>
                  Đang tải danh sách đơn hàng...
                </td>
              </tr>
            ) : orders.length === 0 ? (
              <tr>
                <td colSpan="8" style={{ textAlign: 'center', padding: 40, color: '#94a3b8' }}>
                  Chưa có đơn hàng nào được chốt. Hãy thử trò chuyện với AI tại mục "Khách Hàng Chat" để chốt đơn!
                </td>
              </tr>
            ) : (
              orders.map((o) => (
                <tr key={o.id}>
                  <td>
                    <strong style={{ color: '#38bdf8' }}>{o.id}</strong>
                  </td>
                  <td style={{ fontSize: 13, color: '#94a3b8' }}>
                    {new Date(o.created_at).toLocaleString('vi-VN')}
                  </td>
                  <td style={{ fontWeight: 600 }}>{o.customer_name}</td>
                  <td>
                    <a
                      href={`tel:${o.customer_phone}`}
                      style={{ color: '#818cf8', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 4 }}
                    >
                      <Phone size={13} /> {o.customer_phone}
                    </a>
                  </td>
                  <td style={{ fontWeight: 700, color: '#34d399' }}>
                    {(o.total_amount || 0).toLocaleString('vi-VN')} đ
                  </td>
                  <td>
                    <span className="status-tag confirmed">
                      {o.status}
                    </span>
                  </td>
                  <td>
                    <span className={`status-tag ${o.email_sent ? 'email-sent' : 'pending'}`}>
                      <Mail size={12} /> {o.email_sent ? t.emailSentBadge : t.emailPendingBadge}
                    </span>
                  </td>
                  <td style={{ textAlign: 'right' }}>
                    <button
                      type="button"
                      className="btn-secondary"
                      style={{ padding: '6px 12px', display: 'inline-flex', fontSize: 13 }}
                      onClick={() => setSelectedOrder(o)}
                    >
                      <Eye size={14} style={{ marginRight: 4 }} /> {t.thView}
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Order Detail Modal */}
      {selectedOrder && (
        <div className="modal-overlay" onClick={() => setSelectedOrder(null)}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Chi Tiết Đơn Hàng #{selectedOrder.id}</h3>
              <button
                type="button"
                onClick={() => setSelectedOrder(null)}
                style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer' }}
              >
                <X size={20} />
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              <div style={{ background: '#182236', padding: 16, borderRadius: 12, border: '1px solid var(--border-color)' }}>
                <h4 style={{ color: '#818cf8', marginBottom: 8 }}>Thông Tin Giao Hàng</h4>
                <div style={{ fontSize: 14, marginBottom: 4 }}>
                  <strong>Người nhận:</strong> {selectedOrder.customer_name}
                </div>
                <div style={{ fontSize: 14, marginBottom: 4 }}>
                  <strong>Số điện thoại:</strong>{' '}
                  <a href={`tel:${selectedOrder.customer_phone}`} style={{ color: '#38bdf8' }}>
                    {selectedOrder.customer_phone}
                  </a>
                </div>
                <div style={{ fontSize: 14 }}>
                  <strong>Địa chỉ giao hàng:</strong> {selectedOrder.customer_address}
                </div>
              </div>

              <div>
                <h4 style={{ marginBottom: 10, color: '#f8fafc' }}>Sản Phẩm Đặt Mua</h4>
                <div style={{ background: '#131b2e', borderRadius: 8, overflow: 'hidden', border: '1px solid var(--border-color)' }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
                    <thead>
                      <tr style={{ background: '#1e293b', textAlign: 'left' }}>
                        <th style={{ padding: 10 }}>Sản phẩm</th>
                        <th style={{ padding: 10, textAlign: 'center' }}>SL</th>
                        <th style={{ padding: 10, textAlign: 'right' }}>Đơn giá</th>
                        <th style={{ padding: 10, textAlign: 'right' }}>Thành tiền</th>
                      </tr>
                    </thead>
                    <tbody>
                      {selectedOrder.items && selectedOrder.items.length > 0 ? (
                        selectedOrder.items.map((item) => (
                          <tr key={item.id} style={{ borderBottom: '1px solid #1e293b' }}>
                            <td style={{ padding: 10 }}>{item.product_name}</td>
                            <td style={{ padding: 10, textAlign: 'center' }}>{item.quantity}</td>
                            <td style={{ padding: 10, textAlign: 'right' }}>{Number(item.price).toLocaleString('vi-VN')} đ</td>
                            <td style={{ padding: 10, textAlign: 'right', fontWeight: 600 }}>{Number(item.subtotal).toLocaleString('vi-VN')} đ</td>
                          </tr>
                        ))
                      ) : (
                        <tr>
                          <td colSpan="4" style={{ padding: 14, textAlign: 'center', color: '#94a3b8' }}>
                            Sản phẩm được chốt từ cuộc trò chuyện của khách
                          </td>
                        </tr>
                      )}
                      <tr style={{ fontWeight: 700, fontSize: 15, background: '#182236' }}>
                        <td colSpan="3" style={{ padding: 12 }}>TỔNG THANH TOÁN:</td>
                        <td style={{ padding: 12, textAlign: 'right', color: '#34d399' }}>
                          {Number(selectedOrder.total_amount).toLocaleString('vi-VN')} đ
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              {selectedOrder.notes && (
                <div style={{ background: '#242014', border: '1px solid #78350f', padding: 12, borderRadius: 8, fontSize: 13, color: '#fde68a' }}>
                  <strong>📝 Ghi chú từ cuộc trò chuyện:</strong>
                  <p style={{ marginTop: 4 }}>{selectedOrder.notes}</p>
                </div>
              )}

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 10 }}>
                <span style={{ fontSize: 12, color: '#94a3b8' }}>
                  Email chủ shop: <strong>{selectedOrder.email_sent ? 'Đã gửi thành công' : 'Chờ gửi'}</strong>
                </span>
                <a
                  href={`tel:${selectedOrder.customer_phone}`}
                  className="btn-primary"
                  style={{ textDecoration: 'none', background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)' }}
                >
                  <Phone size={16} /> {t.btnCallCustomer}
                </a>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
