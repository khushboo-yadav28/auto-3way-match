import React, { useState, useRef, useEffect } from 'react';
import './App.css';

export default function App() {
  const [view, setView] = useState('login'); 
  const [activeTab, setActiveTab] = useState('data-entry'); 
  
  const [status, setStatus] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [rpaTriggered, setRpaTriggered] = useState(false);
  
  const [metrics, setMetrics] = useState({ processed: 0, value: 0.00, exceptions: 0 });
  
  const [auditLog, setAuditLog] = useState([
    { time: new Date().toLocaleTimeString(), msg: "System initialized. Waiting for Agentic RPA connection..." }
  ]);
  const logEndRef = useRef(null);

  const addLog = (msg) => {
    setAuditLog(prev => [...prev, { time: new Date().toLocaleTimeString(), msg }]);
  };

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [auditLog]);

  const handleAuth = (e) => {
    e.preventDefault();
    setIsLoggingIn(true);
    setTimeout(() => {
      setIsLoggingIn(false);
      setView('dashboard');
      addLog("Authentication successful. Secure session started.");
    }, 1500);
  };

  const handleTriggerRPA = () => {
    window.startRpaTyping = true; 
    setRpaTriggered(true);
    addLog("⚡ Autonomous Agent triggered. Awaiting data injection...");
  };

  const handleDownloadPDF = () => {
    addLog("User downloaded the source PDF for manual audit.");
    const link = document.createElement('a');
    link.href = '/invoice_techsolutions.pdf'; 
    link.download = 'Verified_Invoice_Copy.pdf'; 
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleViewPDF = () => {
    addLog("User opened source PDF in new tab.");
    window.open('/invoice_techsolutions.pdf', '_blank');
  };

  const handleException = () => {
    const id = document.getElementById('invoiceId').value || 'Unknown';
    addLog(`⚠️ DISCREPANCY FLAGGED: Three-Way Match failed for Invoice ${id}. Halted.`);
    setMetrics(prev => ({ ...prev, exceptions: prev.exceptions + 1 }));
    setStatus('🛑 Alert: Invoice rejected due to data mismatch.');
    
    document.getElementById("invoiceForm")?.reset();
    setRpaTriggered(false);
    window.startRpaTyping = false; 
    
    setTimeout(() => setStatus(''), 5000);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    addLog("Validating injected fields against ERP constraints...");
    
    const formData = new FormData(e.target);
    const amount = parseFloat(formData.get('totalAmount'));
    const id = formData.get('invoiceId');
    
    setTimeout(() => {
      if (!isNaN(amount)) {
        setMetrics(prev => ({ 
          ...prev, 
          processed: prev.processed + 1, 
          value: prev.value + amount 
        }));
      }
      
      setStatus('✅ Success: Three-Way Match Verified & Logged!');
      addLog(`✅ Invoice ${id} successfully recorded. Value: $${amount}`);
      
      setIsSubmitting(false);
      setRpaTriggered(false);
      window.startRpaTyping = false; 
      e.target.reset();
      
      setTimeout(() => setStatus(''), 5000);
    }, 1500);
  };

  if (view === 'login') {
    return (
      <div className="login-wrapper">
        <div className="auth-box glass-panel">
          <div className="logo-placeholder">🤖 Agentic AI</div>
          <h2>ERP Access Portal</h2>
          <p>Sign in to monitor autonomous workflows</p>
          <form onSubmit={handleAuth}>
            <input type="email" id="email" placeholder="Email Address" required disabled={isLoggingIn} />
            <input type="password" id="password" placeholder="Password" required disabled={isLoggingIn} />
            <button type="submit" id="authButton" className="btn-primary" disabled={isLoggingIn}>
              {isLoggingIn ? 'Authenticating...' : 'Secure Log In'}
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-layout">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>🤖 Nexus ERP</h2>
          <span className="badge">Agentic AI Node</span>
        </div>
        <nav className="sidebar-nav">
          <a href="#" className={activeTab === 'data-entry' ? "active" : ""} onClick={(e) => { e.preventDefault(); setActiveTab('data-entry'); }}>Data Entry</a>
          <a href="#" className={activeTab === 'purchase-orders' ? "active" : ""} onClick={(e) => { e.preventDefault(); setActiveTab('purchase-orders'); }}>Purchase Orders</a>
          <a href="#" className={activeTab === 'goods-received' ? "active" : ""} onClick={(e) => { e.preventDefault(); setActiveTab('goods-received'); }}>Goods Received</a>
        </nav>
        <button onClick={() => setView('login')} className="btn-logout">Disconnect</button>
      </aside>

      <main className="main-content">
        <header className="top-bar">
          <h1>Intelligent Accounts Payable</h1>
          <div className="user-profile">Admin User</div>
        </header>

        {/* Render content based on the active tab */}
        {activeTab === 'data-entry' && (
          <>
            <div className="analytics-grid">
              <div className="stat-card glass-panel">
                <div className="stat-icon blue">📄</div>
                <div className="stat-info">
                  <h3>Processed</h3>
                  <p className="stat-value">{metrics.processed}</p>
                </div>
              </div>
              <div className="stat-card glass-panel">
                <div className="stat-icon green">💰</div>
                <div className="stat-info">
                  <h3>Value Logged</h3>
                  <p className="stat-value">${metrics.value.toLocaleString(undefined, {minimumFractionDigits: 2})}</p>
                </div>
              </div>
              <div className="stat-card glass-panel exception-card">
                <div className="stat-icon red">⚠️</div>
                <div className="stat-info">
                  <h3>Exceptions</h3>
                  <p className="stat-value">{metrics.exceptions}</p>
                </div>
              </div>
            </div>

            <div className="content-grid">
              <div className="form-container glass-panel">
                <div className="form-header">
                  <h2>Invoice Auto-Entry</h2>
                  <div className="action-buttons">
                    {/* The buttons the bot will click */}
                    <button id="viewPdfBtn" onClick={handleViewPDF} className="btn-secondary">👁️ View PDF</button>
                    <button id="downloadPdfBtn" onClick={handleDownloadPDF} className="btn-secondary">📥 Download</button>
                    <button id="triggerRpaBtn" onClick={handleTriggerRPA} className={`btn-primary rpa-btn ${rpaTriggered ? 'active-pulse' : ''}`} disabled={rpaTriggered}>
                      {rpaTriggered ? '🤖 Agent Typing...' : '⚡ Trigger Agent'}
                    </button>
                  </div>
                </div>

                {status && <div className="status-banner" id="successBanner">{status}</div>}
                
                <form id="invoiceForm" onSubmit={handleSubmit}>
                  <div className="input-row">
                    <div className="input-group">
                      <label>Invoice ID</label>
                      <input type="text" id="invoiceId" name="invoiceId" required disabled={isSubmitting} />
                    </div>
                    <div className="input-group">
                      <label>Vendor Name</label>
                      <input type="text" id="vendorName" name="vendorName" required disabled={isSubmitting} />
                    </div>
                  </div>
                  <div className="input-row">
                    <div className="input-group">
                      <label>Item Quantities</label>
                      <input type="number" id="itemQuantities" name="itemQuantities" required disabled={isSubmitting} />
                    </div>
                    <div className="input-group">
                      <label>Unit Pricing ($)</label>
                      <input type="number" step="0.01" id="unitPricing" name="unitPricing" required disabled={isSubmitting} />
                    </div>
                  </div>
                  <div className="input-group full-width">
                    <label>Total Amount ($)</label>
                    <input type="number" step="0.01" id="totalAmount" name="totalAmount" required disabled={isSubmitting} />
                  </div>
                  
                  <div style={{ display: 'flex', gap: '16px', marginTop: '16px' }}>
                    <button type="submit" className="btn-submit" id="submitInvoice" disabled={isSubmitting} style={{ flex: 1 }}>
                      {isSubmitting ? 'Committing...' : 'Commit Record'}
                    </button>
                    <button type="button" id="logExceptionBtn" onClick={handleException} disabled={isSubmitting} style={{ flex: 1, padding: '14px', background: '#ef4444', color: 'white', borderRadius: '6px', fontWeight: '600', border: 'none', cursor: 'pointer' }}>
                      Flag Discrepancy
                    </button>
                  </div>
                </form>
              </div>

              <div className="audit-log glass-panel">
                <h2>Live System Audit Log</h2>
                <div className="log-window">
                  {auditLog.map((log, idx) => (
                    <div key={idx} className="log-entry">
                      <span className="log-time">[{log.time}]</span>
                      <span className="log-msg">{log.msg}</span>
                    </div>
                  ))}
                  <div ref={logEndRef} />
                </div>
              </div>
            </div>
          </>
        )}

        {/* Purchase Orders View */}
        {activeTab === 'purchase-orders' && (
          <div className="glass-panel" style={{ padding: '32px' }}>
            <h2 style={{ marginBottom: '8px' }}>Purchase Orders Directory</h2>
            <p style={{ color: '#6b7280', marginBottom: '32px' }}>Read-only view of approved vendor contracts and negotiated rates.</p>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #e5e7eb' }}>
                  <th style={{ padding: '12px 8px', color: '#374151' }}>PO ID</th>
                  <th style={{ padding: '12px 8px', color: '#374151' }}>Vendor Name</th>
                  <th style={{ padding: '12px 8px', color: '#374151' }}>Approved Qty</th>
                  <th style={{ padding: '12px 8px', color: '#374151' }}>Unit Price</th>
                  <th style={{ padding: '12px 8px', color: '#374151' }}>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr style={{ borderBottom: '1px solid #e5e7eb' }}>
                  <td style={{ padding: '16px 8px', fontWeight: '600' }}>PO-1001</td>
                  <td style={{ padding: '16px 8px' }}>TechSolutions Inc.</td>
                  <td style={{ padding: '16px 8px' }}>10</td>
                  <td style={{ padding: '16px 8px' }}>$1,000.00</td>
                  <td style={{ padding: '16px 8px' }}><span style={{ color: '#065f46', background: '#d1fae5', padding: '4px 12px', borderRadius: '12px', fontSize: '12px', fontWeight: 'bold' }}>Active</span></td>
                </tr>
                <tr style={{ borderBottom: '1px solid #e5e7eb' }}>
                  <td style={{ padding: '16px 8px', fontWeight: '600' }}>PO-1002</td>
                  <td style={{ padding: '16px 8px' }}>OfficePro Supplies</td>
                  <td style={{ padding: '16px 8px' }}>50</td>
                  <td style={{ padding: '16px 8px' }}>$20.00</td>
                  <td style={{ padding: '16px 8px' }}><span style={{ color: '#065f46', background: '#d1fae5', padding: '4px 12px', borderRadius: '12px', fontSize: '12px', fontWeight: 'bold' }}>Active</span></td>
                </tr>
                <tr>
                  <td style={{ padding: '16px 8px', fontWeight: '600' }}>PO-1003</td>
                  <td style={{ padding: '16px 8px' }}>GlobalHardware Corp</td>
                  <td style={{ padding: '16px 8px' }}>5</td>
                  <td style={{ padding: '16px 8px' }}>$500.00</td>
                  <td style={{ padding: '16px 8px' }}><span style={{ color: '#065f46', background: '#d1fae5', padding: '4px 12px', borderRadius: '12px', fontSize: '12px', fontWeight: 'bold' }}>Active</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        )}

        {/* Goods Received View */}
        {activeTab === 'goods-received' && (
          <div className="glass-panel" style={{ padding: '32px' }}>
            <h2 style={{ marginBottom: '8px' }}>Warehouse Goods Received (GRN)</h2>
            <p style={{ color: '#6b7280', marginBottom: '32px' }}>Warehouse delivery logs used for matching physical inventory to invoices.</p>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #e5e7eb' }}>
                  <th style={{ padding: '12px 8px', color: '#374151' }}>GRN ID</th>
                  <th style={{ padding: '12px 8px', color: '#374151' }}>Linked PO</th>
                  <th style={{ padding: '12px 8px', color: '#374151' }}>Vendor Name</th>
                  <th style={{ padding: '12px 8px', color: '#374151' }}>Physically Received</th>
                </tr>
              </thead>
              <tbody>
                <tr style={{ borderBottom: '1px solid #e5e7eb' }}>
                  <td style={{ padding: '16px 8px', fontWeight: '600' }}>GRN-5001</td>
                  <td style={{ padding: '16px 8px', color: '#3b82f6' }}>PO-1001</td>
                  <td style={{ padding: '16px 8px' }}>TechSolutions Inc.</td>
                  <td style={{ padding: '16px 8px', fontWeight: '600', color: '#111827' }}>10 units</td>
                </tr>
                <tr style={{ borderBottom: '1px solid #e5e7eb' }}>
                  <td style={{ padding: '16px 8px', fontWeight: '600' }}>GRN-5002</td>
                  <td style={{ padding: '16px 8px', color: '#3b82f6' }}>PO-1002</td>
                  <td style={{ padding: '16px 8px' }}>OfficePro Supplies</td>
                  <td style={{ padding: '16px 8px', fontWeight: '600', color: '#111827' }}>50 units</td>
                </tr>
                <tr>
                  <td style={{ padding: '16px 8px', fontWeight: '600' }}>GRN-5003</td>
                  <td style={{ padding: '16px 8px', color: '#3b82f6' }}>PO-1003</td>
                  <td style={{ padding: '16px 8px' }}>GlobalHardware Corp</td>
                  <td style={{ padding: '16px 8px', fontWeight: '600', color: '#111827' }}>5 units</td>
                </tr>
              </tbody>
            </table>
          </div>
        )}

      </main>
    </div>
  );
}