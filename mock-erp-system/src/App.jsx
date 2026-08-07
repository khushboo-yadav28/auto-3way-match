import React, { useState } from 'react';
import './App.css';

export default function App() {
  const [view, setView] = useState('login'); 
  const [status, setStatus] = useState('');
  
  // State for Analytics Dashboard
  const [metrics, setMetrics] = useState({
    processed: 142,
    value: 12450.00,
    exceptions: 3
  });

  const handleAuth = (e) => {
    e.preventDefault();
    setView('dashboard');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Dynamically update analytics metrics on successful RPA entry
    const formData = new FormData(e.target);
    const amount = parseFloat(formData.get('totalAmount'));
    
    if (!isNaN(amount)) {
      setMetrics(prev => ({
        ...prev,
        processed: prev.processed + 1,
        value: prev.value + amount
      }));
    }

    setStatus('✅ Success: Invoice Data Structured and Validated!');
    setTimeout(() => setStatus(''), 4000);
    e.target.reset();
  };

  if (view === 'login') {
    return (
      <div className="erp-container auth-mode">
        <div className="auth-box">
          <h2>System Login</h2>
          <form onSubmit={handleAuth}>
            <input type="email" id="email" placeholder="Email Address" required />
            <input type="password" id="password" placeholder="Password" required />
            <button type="submit" id="authButton">Log In</button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="erp-container">
      <nav className="erp-nav">
        <h1>Intelligent ERP Dashboard</h1>
        <button onClick={() => setView('login')} className="logout-btn">Log Out</button>
      </nav>
      
      <main className="erp-content">
        {/* Analytics Panel */}
        <div className="analytics-panel">
          <div className="stat-card">
            <h3>Invoices Processed</h3>
            <p className="stat-value">{metrics.processed}</p>
          </div>
          <div className="stat-card">
            <h3>Total Value Logged</h3>
            <p className="stat-value">${metrics.value.toLocaleString(undefined, {minimumFractionDigits: 2})}</p>
          </div>
          <div className="stat-card exception">
            <h3>Exceptions Caught</h3>
            <p className="stat-value">{metrics.exceptions}</p>
          </div>
        </div>

        {/* Invoice Data Entry Form */}
        <div className="form-wrapper">
          <h2>Invoice Data Entry</h2>
          {status && <div className="status-banner" id="successBanner">{status}</div>}
          <form id="invoiceForm" onSubmit={handleSubmit}>
            <div className="input-group">
              <label htmlFor="invoiceId">Invoice ID</label>
              <input type="text" id="invoiceId" name="invoiceId" required />
            </div>
            <div className="input-group">
              <label htmlFor="vendorName">Vendor Name</label>
              <input type="text" id="vendorName" name="vendorName" required />
            </div>
            <div className="input-group">
              <label htmlFor="itemQuantities">Item Quantities</label>
              <input type="number" id="itemQuantities" name="itemQuantities" required />
            </div>
            <div className="input-group">
              <label htmlFor="unitPricing">Unit Pricing</label>
              <input type="number" step="0.01" id="unitPricing" name="unitPricing" required />
            </div>
            <div className="input-group full-width">
              <label htmlFor="totalAmount">Total Amount</label>
              <input type="number" step="0.01" id="totalAmount" name="totalAmount" required />
            </div>
            <button type="submit" className="submit-btn" id="submitInvoice">Enter to ERP</button>
          </form>
        </div>
      </main>
    </div>
  );
}