import React, { useState, useEffect } from 'react';
import { Settings, Save, CheckCircle, Mail, Key, Shield, Sparkles } from 'lucide-react';
import { api } from '../api/client';
import { useLanguage } from '../i18n/LanguageContext';

export default function AdminSettings() {
  const { t } = useLanguage();
  const [adminEmail, setAdminEmail] = useState('');
  const [geminiApiKey, setGeminiApiKey] = useState('');
  const [isGeminiActive, setIsGeminiActive] = useState(false);
  const [loading, setLoading] = useState(true);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      setLoading(true);
      const data = await api.getSettings();
      setAdminEmail(data.admin_notification_email || '');
      setGeminiApiKey(data.gemini_api_key || '');
      setIsGeminiActive(data.is_gemini_active);
    } catch (err) {
      console.error('Error fetching settings:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      await api.updateSettings({
        admin_notification_email: adminEmail,
        gemini_api_key: geminiApiKey,
      });
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 4000);
      loadSettings();
    } catch (err) {
      alert('Lỗi lưu cài đặt: ' + err.message);
    }
  };

  return (
    <div className="admin-page" style={{ maxWidth: 800 }}>
      <div className="page-header">
        <div>
          <h2>
            <Settings size={24} style={{ color: '#818cf8' }} />
            {t.settingsPageTitle}
          </h2>
          <p>{t.settingsPageSubtitle}</p>
        </div>
      </div>

      <div className="table-card" style={{ padding: 24 }}>
        <form onSubmit={handleSave}>
          {/* Email section */}
          <div style={{ marginBottom: 28 }}>
            <h3 style={{ fontSize: 16, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
              <Mail size={18} style={{ color: '#38bdf8' }} />
              {t.emailSectionTitle}
            </h3>
            <p style={{ fontSize: 13, color: '#94a3b8', marginBottom: 12 }}>
              {t.emailSectionDesc}
            </p>
            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                required
                className="form-control"
                value={adminEmail}
                onChange={(e) => setAdminEmail(e.target.value)}
                placeholder="chushop@gmail.com"
              />
            </div>
          </div>

          <hr style={{ borderColor: 'var(--border-color)', margin: '24px 0' }} />

          {/* Gemini AI section */}
          <div style={{ marginBottom: 28 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
              <h3 style={{ fontSize: 16, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: 8 }}>
                <Key size={18} style={{ color: '#f59e0b' }} />
                {t.geminiSectionTitle}
              </h3>
              <span className={`status-tag ${isGeminiActive ? 'confirmed' : 'pending'}`}>
                {isGeminiActive ? t.geminiActiveBadge : t.geminiFallbackBadge}
              </span>
            </div>
            <p style={{ fontSize: 13, color: '#94a3b8', marginBottom: 12 }}>
              Nhập API Key từ <a href="https://aistudio.google.com" target="_blank" rel="noreferrer" style={{ color: '#818cf8' }}>Google AI Studio</a>.
            </p>
            <div className="form-group">
              <label>Gemini API Key:</label>
              <input
                type="password"
                className="form-control"
                value={geminiApiKey}
                onChange={(e) => setGeminiApiKey(e.target.value)}
                placeholder="AIzaSy..."
              />
            </div>
          </div>

          {savedSuccess && (
            <div style={{ background: 'rgba(16, 185, 129, 0.15)', border: '1px solid #10b981', padding: 12, borderRadius: 8, color: '#34d399', fontSize: 14, display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
              <CheckCircle size={18} /> {t.saveSuccessMsg}
            </div>
          )}

          <button
            type="submit"
            className="btn-primary"
            style={{ width: '100%', justifyContent: 'center' }}
          >
            <Save size={18} /> {t.saveSettingsBtn}
          </button>
        </form>
      </div>
    </div>
  );
}
