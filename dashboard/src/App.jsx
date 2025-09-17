import React, { useState } from 'react'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [password, setPassword] = useState('')

  const handleLogin = (e) => {
    e.preventDefault()
    // Simple password check - replace with proper auth later
    if (password === 'admin123') {
      setIsAuthenticated(true)
    } else {
      alert('Invalid password')
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="login-container">
        <div className="login-box">
          <h1>MYTA Dashboard</h1>
          <p>Admin Access Required</p>
          <form onSubmit={handleLogin}>
            <input
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="password-input"
            />
            <button type="submit" className="login-btn">
              Access Dashboard
            </button>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>🎯 MYTA Production Dashboard</h1>
        <button 
          onClick={() => setIsAuthenticated(false)}
          className="logout-btn"
        >
          Logout
        </button>
      </header>
      
      <main className="dashboard-content">
        <div className="coming-soon">
          <h2>🚧 Dashboard Coming Soon</h2>
          <p>Production monitoring dashboard is being built.</p>
          
          <div className="placeholder-metrics">
            <div className="metric-card">
              <h3>Active Users</h3>
              <div className="metric-value">--</div>
            </div>
            <div className="metric-card">
              <h3>AI Agents Active</h3>
              <div className="metric-value">--</div>
            </div>
            <div className="metric-card">
              <h3>System Health</h3>
              <div className="metric-value">🟢 Ready</div>
            </div>
          </div>
          
          <p className="status">
            ✅ Domain configured<br/>
            ✅ Authentication working<br/>
            🔄 Metrics integration pending
          </p>
        </div>
      </main>
    </div>
  )
}

export default App
