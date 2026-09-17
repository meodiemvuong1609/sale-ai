import React, { createContext, useContext, useState, useEffect } from 'react';
import { translations } from './translations';

const LanguageContext = createContext();

export function LanguageProvider({ children }) {
  const [lang, setLangState] = useState(() => {
    return localStorage.getItem('sale_ai_lang') || 'vi';
  });

  const setLang = (newLang) => {
    setLangState(newLang);
    localStorage.setItem('sale_ai_lang', newLang);
  };

  const t = translations[lang] || translations.vi;

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}
