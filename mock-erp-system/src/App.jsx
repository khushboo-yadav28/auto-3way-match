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
    { time: new Date().toLocaleTimeString(), msg: "SYSTEM INIT: Agentic RPA node online and listening..." }
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
      addLog("Auth success. Secure uplink established.");
    }, 1500);
  };

  const handleTriggerRPA = () => {
    window.startRpaTyping = true; 
    setRpaTriggered(true);
    addLog("⚡ Autonomous Agent triggered. Awaiting UI injection...");
  };

  const handleDownloadPDF = () => {
    addLog("User downloaded source PDF. Audit trail logged.");
    const link = document.createElement('a');
    link.href = '/invoice_techsolutions.pdf'; 
    link.download = 'Verified_Invoice_Copy.pdf'; 
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleViewPDF = () => {
    addLog("Document requested: Opening secure viewer.");
    window.open('/invoice_techsolutions.pdf', '_blank');
  };

  const handleException = () => {
    const id = document.getElementById('invoiceId').value || 'Unknown';
    addLog(`⚠️ ANOMALY DETECTED: 3-Way Match failed for ${id}. Pipeline halted.`);
    
    setMetrics(prev => ({ ...prev, exceptions: prev.exceptions + 1 }));
    setStatus('🛑 ALERT: Data mismatch detected. Manager Override required.');
    
    setRpaTriggered(false);
    window.startRpaTyping = false; 
  };

  const handleOverride = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    addLog("🔒 MANAGER OVERRIDE: Verifying biometric/credential clearance...");
    
    const amount = parseFloat(document.getElementById('totalAmount').value);
    const id = document.getElementById('invoiceId').value;
    
    setTimeout(() => {
      if (!isNaN(amount)) {
        setMetrics(prev => ({ 
          ...prev, 
          processed: prev.processed + 1, 
          value: prev.value + amount,
          exceptions: prev.exceptions - 1 
        }));
      }
      
      setStatus('✅ OVERRIDE SUCCESS: Record forced to ledger.');
      addLog(`✅ Exception Cleared: Invoice ${id} manually forced. Value: $${amount}`);
      
      setIsSubmitting(false);
      document.getElementById("invoiceForm").reset();
      
      setTimeout(() => setStatus(''), 5000);
    }, 1500);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    addLog("Processing standard commit. Validating payload...");
    
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
      
      setStatus('✅ SUCCESS: 3-Way Match Verified & Logged!');
      addLog(`✅ Invoice ${id} securely committed. Value: $${amount}`);
      
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
        <div className="light-aurora-bg"></div>
        <div className="floating-orbs"></div>
        <div className="auth-box glass-panel">
          <div className="logo-placeholder"><span className="pulse-dot"></span> NEXUS AI</div>
          <h2>ERP Uplink</h2>
          <p>Agentic Process Automation Portal</p>
          <form onSubmit={handleAuth}>
            <input type="email" id="email" placeholder="Email Address" required disabled={isLoggingIn} />
            <input type="password" id="password" placeholder="Password" required disabled={isLoggingIn} />
            <button type="submit" id="authButton" className="btn-primary" disabled={isLoggingIn}>
              {isLoggingIn ? 'Establishing Connection...' : 'Initialize Session'}
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-layout">
      {/* Background Animations */}
      <div className="light-aurora-bg"></div>
      <div className="floating-orbs"></div>

      <aside className="sidebar glass-panel">
        <div className="sidebar-header">
          <h2>🤖 Nexus ERP</h2>
          <div className="system-status">
            <span className="pulse-dot"></span> Agent Node Active
          </div>
        </div>
        <nav className="sidebar-nav">
          <a href="#" className={activeTab === 'data-entry' ? "active" : ""} onClick={() => setActiveTab('data-entry')}>Data Entry</a>
          <a href="#" className={activeTab === 'purchase-orders' ? "active" : ""} onClick={() => setActiveTab('purchase-orders')}>Purchase Orders</a>
          <a href="#" className={activeTab === 'goods-received' ? "active" : ""} onClick={() => setActiveTab('goods-received')}>Goods Received</a>
        </nav>
        <button onClick={() => setView('login')} className="btn-logout">Terminate Uplink</button>
      </aside>

      <main className="main-content">
        <header className="top-bar glass-panel">
          <h1>Accounts Payable Command Center</h1>
          <div className="user-profile">Administrator</div>
        </header>

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
              <div className={`stat-card glass-panel ${metrics.exceptions > 0 ? 'exception-active' : ''}`}>
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
                  <h2>Invoice Injection Port</h2>
                  <div className="action-buttons">
                    <button id="viewPdfBtn" onClick={handleViewPDF} className="btn-secondary">👁️ View PDF</button>
                    <button id="downloadPdfBtn" onClick={handleDownloadPDF} className="btn-secondary">📥 Fetch File</button>
                    <button id="triggerRpaBtn" onClick={handleTriggerRPA} className={`btn-primary rpa-btn ${rpaTriggered ? 'active-pulse' : ''}`} disabled={rpaTriggered}>
                      {rpaTriggered ? '🤖 Agent Inbound...' : '⚡ Sync Agent'}
                    </button>
                  </div>
                </div>

                {status && (
                  <div className="status-banner" id="successBanner" 
                    style={{ 
                      background: status.includes('ALERT') ? 'rgba(254, 226, 226, 0.9)' : 'rgba(209, 250, 229, 0.9)', 
                      color: status.includes('ALERT') ? '#991b1b' : '#065f46', 
                      border: `1px solid ${status.includes('ALERT') ? '#f87171' : '#34d399'}` 
                    }}>
                    {status}
                  </div>
                )}
                
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
                  
                  <div style={{ display: 'flex', gap: '16px', marginTop: '24px' }}>
                    {status.includes('ALERT') ? (
                      <>
                        <button type="button" onClick={handleOverride} disabled={isSubmitting} className="btn-override">
                          {isSubmitting ? 'AUTHORIZING...' : '🚨 OVERRIDE: FORCE APPROVE'}
                        </button>
                        <button type="button" onClick={() => { setStatus(''); document.getElementById("invoiceForm").reset(); addLog("System cleared. Standing by."); }} disabled={isSubmitting} className="btn-reject">
                          REJECT & CLEAR
                        </button>
                      </>
                    ) : (
                      <>
                        <button type="submit" className="btn-submit" id="submitInvoice" disabled={isSubmitting} style={{ flex: 1 }}>
                          {isSubmitting ? 'COMMITTING...' : 'COMMIT RECORD'}
                        </button>
                        <button type="button" id="logExceptionBtn" onClick={handleException} disabled={isSubmitting} className="btn-flag">
                          FLAG ANOMALY
                        </button>
                      </>
                    )}
                  </div>
                </form>
              </div>

              <div className="audit-log glass-panel">
                <h2>Live Agent Telemetry</h2>
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

        {/* PO & GRN Views */}
        {(activeTab === 'purchase-orders' || activeTab === 'goods-received') && (
          <div className="glass-panel" style={{ padding: '32px' }}>
            <h2>{activeTab === 'purchase-orders' ? 'Secure Ledger: Purchase Orders' : 'Warehouse Node: Goods Received'}</h2>
            <p style={{ color: 'var(--text-muted)', marginBottom: '32px' }}>Read-only database view synchronized with main node.</p>
            <div className="placeholder-table" style={{ color: 'var(--text-main)' }}>Data connection established. Records encrypted.</div>
          </div>
        )}
      </main>
    </div>
  );
}