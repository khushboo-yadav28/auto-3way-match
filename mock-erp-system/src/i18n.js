import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: {
    translation: {
      title: "Kinetix ERP Command Center",
      pendingInvoices: "Pending Invoices",
      overrideApprove: "Override: Force Approve",
      mismatchDetected: "Discrepancy Detected",
      languageSelect: "Language"
    }
  },
  hi: {
    translation: {
      title: "किनेटिक्स ईआरपी कमांड सेंटर",
      pendingInvoices: "लंबित चालान",
      overrideApprove: "ओवरराइड: फोर्स स्वीकृत करें",
      mismatchDetected: "विसंगति का पता चला",
      languageSelect: "भाषा"
    }
  },
  gu: {
    translation: {
      title: "किनेटिक्स ERP કમાન્ડ સેન્ટર",
      pendingInvoices: "પેન્ડિંગ ઇનવોઇસ",
      overrideApprove: "ઓવરરાઇડ: મંજૂર કરો",
      mismatchDetected: "विसंगति मळिया",
      languageSelect: "ભાષા"
    }
  }
};

i18n.use(initReactI18next).init({
  resources,
  lng: "en",
  interpolation: { escapeValue: false }
});

export default i18n;