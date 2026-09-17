import React from 'react';
import { CheckCircle, Mail, MapPin, Phone, User, Package } from 'lucide-react';
import { useLanguage } from '../i18n/LanguageContext';

export default function OrderSuccessCard({ order }) {
  const { t } = useLanguage();
  if (!order) return null;

  return (
    <div className="order-success-card">
      <div className="success-header">
        <div className="success-icon">
          <CheckCircle size={22} />
        </div>
        <div>
          <h4>{t.orderSuccessTitle}</h4>
          <span style={{ fontSize: 12, color: '#6ee7b7' }}>
            {t.orderCodeLabel} <strong>{order.id}</strong>
          </span>
        </div>
      </div>

      <div className="order-detail-rows">
        <div className="order-row">
          <span><User size={14} style={{ verticalAlign: 'middle', marginRight: 4 }} /> {t.recipientLabel}</span>
          <span>{order.customer_name}</span>
        </div>
        <div className="order-row">
          <span><Phone size={14} style={{ verticalAlign: 'middle', marginRight: 4 }} /> {t.phoneLabel}</span>
          <span>{order.customer_phone}</span>
        </div>
        <div className="order-row">
          <span><MapPin size={14} style={{ verticalAlign: 'middle', marginRight: 4 }} /> {t.addressLabel}</span>
          <span style={{ textAlign: 'right', maxWidth: '60%' }}>{order.customer_address}</span>
        </div>
        <div className="order-row total-amount">
          <span><Package size={14} style={{ verticalAlign: 'middle', marginRight: 4 }} /> {t.totalPaymentLabel}</span>
          <span>{(order.total_amount || 0).toLocaleString('vi-VN')} VNĐ</span>
        </div>
      </div>

      <div className="order-notice">
        <Mail size={15} style={{ color: '#10b981' }} />
        <span>{t.emailNoticeText}</span>
      </div>
    </div>
  );
}
