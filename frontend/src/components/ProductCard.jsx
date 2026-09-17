import React from 'react';
import { ShoppingBag, Info } from 'lucide-react';
import { useLanguage } from '../i18n/LanguageContext';

export default function ProductCard({ product, onSelectProduct, onAskDetails }) {
  const { t } = useLanguage();
  if (!product) return null;

  const discountPercent = product.price && product.sale_price && product.price > product.sale_price
    ? Math.round(((product.price - product.sale_price) / product.price) * 100)
    : 0;

  return (
    <div className="inchat-product-card">
      <div className="inchat-img-wrap">
        <img
          src={product.image_url || 'https://images.unsplash.com/photo-1584990347449-3972626e27a9?auto=format&fit=crop&w=600&q=80'}
          alt={product.name}
          className="inchat-img"
          loading="lazy"
        />
        {discountPercent > 0 && (
          <span className="badge-discount">-{discountPercent}%</span>
        )}
      </div>

      <div className="inchat-body">
        <h4 className="inchat-title" title={product.name}>
          {product.name}
        </h4>

        <div className="inchat-pricing">
          <span className="price-current">
            {(product.sale_price || product.price || 0).toLocaleString('vi-VN')} đ
          </span>
          {discountPercent > 0 && (
            <span className="price-old">
              {product.price.toLocaleString('vi-VN')} đ
            </span>
          )}
        </div>

        <div className="inchat-actions">
          <button
            type="button"
            className="btn-buy-now"
            onClick={() => onSelectProduct && onSelectProduct(product)}
            title={t.btnBuyNow}
          >
            <ShoppingBag size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
            {t.btnBuyNow}
          </button>
          <button
            type="button"
            className="btn-detail"
            onClick={() => onAskDetails && onAskDetails(product)}
            title={t.btnDetail}
          >
            <Info size={14} style={{ display: 'inline', verticalAlign: 'middle' }} />
          </button>
        </div>
      </div>
    </div>
  );
}
