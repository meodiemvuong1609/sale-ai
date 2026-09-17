import React, { useState, useEffect } from 'react';
import { Plus, Edit2, Trash2, Search, Sparkles, X, Check } from 'lucide-react';
import { api } from '../api/client';
import { useLanguage } from '../i18n/LanguageContext';

export default function AdminProducts() {
  const { t } = useLanguage();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);

  const initialForm = {
    name: '',
    sku: '',
    category: 'Gia dụng thông minh',
    price: '',
    sale_price: '',
    stock: 10,
    short_description: '',
    description: '',
    selling_points: '',
    faq: '',
    image_url: '',
    is_active: true,
  };

  const [formData, setFormData] = useState(initialForm);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const data = await api.getProducts();
      setProducts(data);
    } catch (err) {
      console.error('Error fetching products:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = (prod = null) => {
    if (prod) {
      setEditingProduct(prod);
      setFormData({
        ...prod,
        price: prod.price || '',
        sale_price: prod.sale_price || '',
      });
    } else {
      setEditingProduct(null);
      setFormData({
        ...initialForm,
        sku: 'SKU-' + Date.now().toString().slice(-6),
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingProduct(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        price: Number(formData.price),
        sale_price: formData.sale_price ? Number(formData.sale_price) : null,
        stock: Number(formData.stock),
      };

      if (editingProduct) {
        await api.updateProduct(editingProduct.id, payload);
      } else {
        await api.createProduct(payload);
      }

      handleCloseModal();
      loadProducts();
    } catch (err) {
      alert('Lỗi lưu sản phẩm: ' + err.message);
    }
  };

  const handleDelete = async (id, name) => {
    if (window.confirm(`Bạn có chắc muốn xóa sản phẩm "${name}"?`)) {
      try {
        await api.deleteProduct(id);
        loadProducts();
      } catch (err) {
        alert('Lỗi xóa sản phẩm: ' + err.message);
      }
    }
  };

  const categories = ['ALL', ...new Set(products.map((p) => p.category).filter(Boolean))];

  const filteredProducts = products.filter((p) => {
    const matchSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.sku.toLowerCase().includes(searchTerm.toLowerCase());
    const matchCategory = selectedCategory === 'ALL' || p.category === selectedCategory;
    return matchSearch && matchCategory;
  });

  return (
    <div className="admin-page">
      <div className="page-header">
        <div>
          <h2>
            <Sparkles size={24} style={{ color: '#818cf8' }} />
            {t.productsPageTitle}
          </h2>
          <p>{t.productsPageSubtitle}</p>
        </div>
        <button
          type="button"
          className="btn-primary"
          onClick={() => handleOpenModal()}
        >
          <Plus size={18} /> {t.addProductBtn}
        </button>
      </div>

      {/* Filter & Search Bar */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 20, flexWrap: 'wrap' }}>
        <div style={{ position: 'relative', flex: 1, minWidth: 260 }}>
          <Search size={18} style={{ position: 'absolute', left: 12, top: 12, color: '#94a3b8' }} />
          <input
            type="text"
            className="form-control"
            style={{ paddingLeft: 38 }}
            placeholder={t.searchPlaceholder}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <select
          className="form-control"
          style={{ width: 220 }}
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
        >
          {categories.map((c) => (
            <option key={c} value={c}>
              {c === 'ALL' ? t.allCategories : c}
            </option>
          ))}
        </select>
      </div>

      {/* Product Table */}
      <div className="table-card">
        <table className="custom-table">
          <thead>
            <tr>
              <th>{t.thImage}</th>
              <th>{t.thNameSku}</th>
              <th>{t.thCategory}</th>
              <th>{t.thOriginalPrice}</th>
              <th>{t.thSalePrice}</th>
              <th>{t.thStock}</th>
              <th>{t.thStatus}</th>
              <th style={{ textAlign: 'right' }}>{t.thActions}</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="8" style={{ textAlign: 'center', padding: 30 }}>
                  Đang tải dữ liệu sản phẩm...
                </td>
              </tr>
            ) : filteredProducts.length === 0 ? (
              <tr>
                <td colSpan="8" style={{ textAlign: 'center', padding: 40, color: '#94a3b8' }}>
                  Chưa có sản phẩm nào phù hợp. Hãy bấm "Thêm Sản Phẩm Mới" để nạp dữ liệu!
                </td>
              </tr>
            ) : (
              filteredProducts.map((p) => (
                <tr key={p.id}>
                  <td>
                    <img
                      src={p.image_url || 'https://images.unsplash.com/photo-1584990347449-3972626e27a9?auto=format&fit=crop&w=120&q=80'}
                      alt={p.name}
                      style={{ width: 48, height: 48, borderRadius: 8, objectFit: 'cover' }}
                    />
                  </td>
                  <td>
                    <div style={{ fontWeight: 600, color: '#f8fafc' }}>{p.name}</div>
                    <div style={{ fontSize: 12, color: '#64748b' }}>Mã: {p.sku}</div>
                  </td>
                  <td>
                    <span style={{ background: '#1e293b', padding: '4px 8px', borderRadius: 6, fontSize: 12 }}>
                      {p.category}
                    </span>
                  </td>
                  <td style={{ textDecoration: p.sale_price ? 'line-through' : 'none', color: p.sale_price ? '#64748b' : '#f8fafc' }}>
                    {p.price.toLocaleString('vi-VN')} đ
                  </td>
                  <td style={{ fontWeight: 700, color: '#38bdf8' }}>
                    {p.sale_price ? `${p.sale_price.toLocaleString('vi-VN')} đ` : '-'}
                  </td>
                  <td>
                    <span style={{ color: p.stock > 5 ? '#34d399' : '#f87171', fontWeight: 600 }}>
                      {p.stock} cái
                    </span>
                  </td>
                  <td>
                    <span className={`status-tag ${p.is_active ? 'confirmed' : 'pending'}`}>
                      {p.is_active ? 'Đang bán' : 'Tạm dừng'}
                    </span>
                  </td>
                  <td style={{ textAlign: 'right' }}>
                    <button
                      type="button"
                      className="btn-secondary"
                      style={{ padding: '6px 10px', marginRight: 6, display: 'inline-flex' }}
                      onClick={() => handleOpenModal(p)}
                      title="Chỉnh sửa sản phẩm"
                    >
                      <Edit2 size={14} />
                    </button>
                    <button
                      type="button"
                      className="btn-secondary"
                      style={{ padding: '6px 10px', color: '#f87171', display: 'inline-flex' }}
                      onClick={() => handleDelete(p.id, p.name)}
                      title="Xóa sản phẩm"
                    >
                      <Trash2 size={14} />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Modal Ingestion Form */}
      {isModalOpen && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{editingProduct ? 'Chỉnh Sửa Dữ Liệu Sản Phẩm' : 'Nạp Dữ Liệu Sản Phẩm Mới'}</h3>
              <button
                type="button"
                onClick={handleCloseModal}
                style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer' }}
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Tên sản phẩm *</label>
                <input
                  type="text"
                  required
                  className="form-control"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="VD: Robot hút bụi lau nhà Dreame L10s Ultra Gen 2"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Mã SKU *</label>
                  <input
                    type="text"
                    required
                    className="form-control"
                    value={formData.sku}
                    onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
                    placeholder="VD: DREAME-L10S"
                  />
                </div>
                <div className="form-group">
                  <label>Danh mục</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    placeholder="VD: Gia dụng thông minh"
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Giá niêm yết (VNĐ) *</label>
                  <input
                    type="number"
                    required
                    min="0"
                    className="form-control"
                    value={formData.price}
                    onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                    placeholder="VD: 18990000"
                  />
                </div>
                <div className="form-group">
                  <label>Giá khuyến mãi / Sale (VNĐ)</label>
                  <input
                    type="number"
                    min="0"
                    className="form-control"
                    value={formData.sale_price}
                    onChange={(e) => setFormData({ ...formData, sale_price: e.target.value })}
                    placeholder="VD: 14990000 (Để trống nếu không sale)"
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Số lượng tồn kho</label>
                  <input
                    type="number"
                    min="0"
                    className="form-control"
                    value={formData.stock}
                    onChange={(e) => setFormData({ ...formData, stock: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Đường dẫn hình ảnh (URL)</label>
                  <input
                    type="url"
                    className="form-control"
                    value={formData.image_url}
                    onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                    placeholder="https://..."
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Mô tả ngắn (1-2 câu tóm tắt điểm mạnh nhất)</label>
                <input
                  type="text"
                  className="form-control"
                  value={formData.short_description}
                  onChange={(e) => setFormData({ ...formData, short_description: e.target.value })}
                  placeholder="Lực hút siêu khỏe 10.000Pa, giặt giẻ nước nóng diệt khuẩn..."
                />
              </div>

              <div className="form-group">
                <label>Điểm bán hàng cốt lõi (USP, Quà tặng, Cam kết bảo hành - Gemini dùng để chốt đơn)</label>
                <textarea
                  rows={3}
                  className="form-control"
                  value={formData.selling_points}
                  onChange={(e) => setFormData({ ...formData, selling_points: e.target.value })}
                  placeholder="• Giảm ngay 4 triệu trong tuần lễ này&#10;• Tặng kèm bộ phụ kiện 5 món trị giá 1.200.000đ&#10;• Bảo hành 2 năm chính hãng 1 đổi 1..."
                />
              </div>

              <div className="form-group">
                <label>FAQ Thường gặp & Giải đáp mẫu</label>
                <textarea
                  rows={2}
                  className="form-control"
                  value={formData.faq}
                  onChange={(e) => setFormData({ ...formData, faq: e.target.value })}
                  placeholder="Q: Nhà nhiều tầng có lưu bản đồ được không?&#10;A: Lưu được 4 tầng riêng biệt ạ!"
                />
              </div>

              <div className="modal-actions">
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={handleCloseModal}
                >
                  Hủy Bỏ
                </button>
                <button
                  type="submit"
                  className="btn-primary"
                >
                  <Check size={16} /> Lưu Sản Phẩm
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
