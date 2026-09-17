import React, { useState } from 'react';
import { MessageSquare, Package, ShoppingCart, Settings, Globe } from 'lucide-react';
import ChatInterface from './components/ChatInterface';
import AdminProducts from './components/AdminProducts';
import AdminOrders from './components/AdminOrders';
import AdminSettings from './components/AdminSettings';
import { LanguageProvider, useLanguage } from './i18n/LanguageContext';

function AppContent() {
  const [activeTab, setActiveTab] = useState('chat');
  const { lang, setLang, t } = useLanguage();

  return (
    <div className="app-container">
      {/* App Header */}
      <header className="app-header">
        <div className="brand-section">
          <div className="brand-logo">⚡</div>
          <div>
            <div className="brand-title">
              {t.brandTitle} <span className="brand-badge">{t.brandBadge}</span>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="nav-tabs">
          <button
            type="button"
            className={`nav-tab ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            <MessageSquare size={16} />
            <span>{t.tabChat}</span>
          </button>
          <button
            type="button"
            className={`nav-tab ${activeTab === 'products' ? 'active' : ''}`}
            onClick={() => setActiveTab('products')}
          >
            <Package size={16} />
            <span>{t.tabProducts}</span>
          </button>
          <button
            type="button"
            className={`nav-tab ${activeTab === 'orders' ? 'active' : ''}`}
            onClick={() => setActiveTab('orders')}
          >
            <ShoppingCart size={16} />
            <span>{t.tabOrders}</span>
          </button>
          <button
            type="button"
            className={`nav-tab ${activeTab === 'settings' ? 'active' : ''}`}
            onClick={() => setActiveTab('settings')}
          >
            <Settings size={16} />
            <span>{t.tabSettings}</span>
          </button>
        </nav>

        {/* Right Header Section: Language Selector & Live Status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          {/* Language Switcher */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, background: 'rgba(255, 255, 255, 0.06)', padding: '4px 8px', borderRadius: 20, border: '1px solid var(--border-color)' }}>
            <Globe size={14} style={{ color: '#818cf8' }} />
            <select
              value={lang}
              onChange={(e) => setLang(e.target.value)}
              style={{
                background: 'transparent',
                border: 'none',
                color: '#f8fafc',
                fontSize: 13,
                fontWeight: 600,
                outline: 'none',
                cursor: 'pointer',
              }}
            >
              <option value="vi" style={{ background: '#1e293b' }}>🇻🇳 Tiếng Việt</option>
              <option value="lo" style={{ background: '#1e293b' }}>🇱🇦 ພາສາລາວ</option>
            </select>
          </div>

          <div className="header-status">
            <div className="pulse-dot"></div>
            <span>{t.aiOnline}</span>
          </div>
        </div>
      </header>

      {/* Main View Area */}
      <main className="main-content">
        {activeTab === 'chat' && <ChatInterface />}
        {activeTab === 'products' && <AdminProducts />}
        {activeTab === 'orders' && <AdminOrders />}
        {activeTab === 'settings' && <AdminSettings />}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <AppContent />
    </LanguageProvider>
  );
}
