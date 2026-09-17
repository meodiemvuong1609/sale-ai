import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, Sparkles, RefreshCw, ShoppingCart, ShieldCheck, Flame } from 'lucide-react';
import { api } from '../api/client';
import ProductCard from './ProductCard';
import OrderSuccessCard from './OrderSuccessCard';
import { useLanguage } from '../i18n/LanguageContext';

function renderFormattedMessage(content) {
  if (!content) return '';
  const lines = content.split('\n');
  return lines.map((line, idx) => {
    const parts = line.split(/(\*\*.*?\*\*)/g);
    return (
      <span key={idx} style={{ display: 'block', minHeight: line.trim() === '' ? 10 : 'auto' }}>
        {parts.map((part, pIdx) => {
          if (part.startsWith('**') && part.endsWith('**')) {
            return <strong key={pIdx} style={{ color: '#818cf8' }}>{part.slice(2, -2)}</strong>;
          }
          return part;
        })}
      </span>
    );
  });
}

export default function ChatInterface() {
  const { lang, t } = useLanguage();
  const [sessionId, setSessionId] = useState(() => localStorage.getItem('sale_ai_session_id') || '');
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [sidebarProducts, setSidebarProducts] = useState([]);
  const messagesEndRef = useRef(null);

  const quickPrompts = [
    { text: t.prompt1, icon: Flame },
    { text: t.prompt2, icon: Sparkles },
    { text: t.prompt3, icon: ShieldCheck },
    { text: t.prompt4, icon: ShoppingCart },
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    initChat();
    loadSidebarProducts();
  }, [lang]);

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const initChat = async () => {
    try {
      const storedId = localStorage.getItem('sale_ai_session_id');
      const session = await api.startChat(storedId || null, lang);
      setSessionId(session.id);
      localStorage.setItem('sale_ai_session_id', session.id);

      if (session.messages && session.messages.length > 0) {
        setMessages(session.messages);
      } else {
        // Tin nhắn chào mừng ban đầu theo ngôn ngữ đã chọn
        setMessages([
          {
            id: 'init-msg',
            sender: 'assistant',
            content: t.initialGreeting,
            metadata: {
              showWelcome: true,
            },
            created_at: new Date().toISOString(),
          },
        ]);
      }
    } catch (err) {
      console.error('Failed to init chat session:', err);
    }
  };

  const loadSidebarProducts = async () => {
    try {
      const prods = await api.getProducts();
      setSidebarProducts(prods.slice(0, 6));
    } catch (err) {
      console.error('Failed to load products for sidebar:', err);
    }
  };

  const handleResetChat = async () => {
    localStorage.removeItem('sale_ai_session_id');
    setMessages([]);
    initChat();
  };

  const handleSendMessage = async (textToSend = null) => {
    const text = (textToSend || inputText).trim();
    if (!text || loading) return;

    // Add user message to state immediately
    const tempUserMsg = {
      id: 'temp-user-' + Date.now(),
      sender: 'user',
      content: text,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, tempUserMsg]);
    setInputText('');
    setLoading(true);

    try {
      const response = await api.sendMessage(sessionId, text, lang);
      const aiReplyMsg = {
        id: 'ai-' + Date.now(),
        sender: 'assistant',
        content: response.reply,
        metadata: response.metadata || {},
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, aiReplyMsg]);
    } catch (err) {
      const errorMsg = {
        id: 'err-' + Date.now(),
        sender: 'assistant',
        content: lang === 'lo'
          ? 'ຂໍອະໄພຫຼາຍໆ ການເຊື່ອມຕໍ່ຂັດຂ້ອງເລັກນ້ອຍ. ກະລຸນາສົ່ງຂໍ້ຄວາມອີກຄັ້ງແດ່ເຈົ້າ!'
          : 'Dạ em xin lỗi, kết nối bị gián đoạn đôi chút. Anh/Chị vui lòng gửi lại tin nhắn giúp em nhé!',
        metadata: {},
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSelectProduct = (product) => {
    const text = `${t.buyNowPrefix}${product.name}${t.buyNowSuffix}`;
    handleSendMessage(text);
  };

  const handleAskDetails = (product) => {
    const text = `${t.askDetailsPrefix}${product.name}`;
    handleSendMessage(text);
  };

  return (
    <div className="chat-page">
      {/* Sidebar: Danh mục sản phẩm nổi bật */}
      <aside className="chat-sidebar">
        <div className="sidebar-title">
          <Sparkles size={18} style={{ color: '#818cf8' }} />
          <span>{t.hotDealsTitle}</span>
        </div>

        <div className="product-mini-list">
          {sidebarProducts.map((p) => (
            <div
              key={p.id}
              className="product-mini-card"
              onClick={() => handleAskDetails(p)}
              title={t.askDetailsPrefix + p.name}
            >
              <img
                src={p.image_url || 'https://images.unsplash.com/photo-1584990347449-3972626e27a9?auto=format&fit=crop&w=200&q=80'}
                alt={p.name}
                className="mini-thumb"
              />
              <div className="mini-info">
                <div className="mini-name">{p.name}</div>
                <div className="mini-price">
                  {(p.sale_price || p.price).toLocaleString('vi-VN')} đ
                </div>
              </div>
            </div>
          ))}
        </div>

        <button
          type="button"
          className="btn-secondary"
          style={{ width: '100%', justifyContent: 'center', fontSize: 13 }}
          onClick={handleResetChat}
        >
          <RefreshCw size={14} /> {t.resetChat}
        </button>
      </aside>

      {/* Main Chat Window */}
      <div className="chat-container">
        <div className="chat-window-header">
          <div className="agent-profile">
            <div className="agent-avatar">
              <Bot size={22} color="#ffffff" />
            </div>
            <div className="agent-meta">
              <h3>{t.aiTitle}</h3>
              <p>{t.aiSubtitle}</p>
            </div>
          </div>
          <div>
            <span className="brand-badge">{t.readyToClose}</span>
          </div>
        </div>

        {/* Viewport */}
        <div className="messages-viewport">
          <div className="welcome-banner">
            <h4>{t.welcomeBannerTitle}</h4>
            <p>{t.welcomeBannerDesc}</p>
          </div>

          {messages.map((msg) => (
            <div key={msg.id} className={`message-row ${msg.sender}`}>
              <div className="message-bubble">
                <div className="bubble-text">{renderFormattedMessage(msg.content)}</div>

                {/* Hiển thị thẻ đơn hàng thành công nếu có */}
                {msg.metadata?.order && (
                  <OrderSuccessCard order={msg.metadata.order} />
                )}

                {/* Hiển thị thẻ sản phẩm gợi ý nếu có */}
                {msg.metadata?.suggested_products && msg.metadata.suggested_products.length > 0 && (
                  <div className="inchat-products-grid">
                    {msg.metadata.suggested_products.map((p) => (
                      <ProductCard
                        key={p.id}
                        product={p}
                        onSelectProduct={handleSelectProduct}
                        onAskDetails={handleAskDetails}
                      />
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row assistant">
              <div className="typing-bubble">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Quick Prompts Bar */}
        <div className="quick-prompts-bar">
          {quickPrompts.map((qp, idx) => {
            const Icon = qp.icon;
            return (
              <button
                key={idx}
                type="button"
                className="prompt-chip"
                onClick={() => handleSendMessage(qp.text)}
              >
                <Icon size={14} />
                <span>{qp.text}</span>
              </button>
            );
          })}
        </div>

        {/* Chat Input Bar */}
        <div className="chat-input-bar">
          <form
            className="chat-input-form"
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
          >
            <div className="input-wrapper">
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={t.inputPlaceholder}
                rows={1}
                className="chat-textarea"
              />
            </div>
            <button
              type="submit"
              disabled={!inputText.trim() || loading}
              className="btn-send"
              title="Send"
            >
              <Send size={18} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
