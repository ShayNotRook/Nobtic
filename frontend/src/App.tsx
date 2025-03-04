import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

import Header from './components/main/partials/Header';
import Dashboard from './components/dashboard/Dashboard';
import LoginForm from './components/auth/Login';
import { useState } from 'react';


function App() {
  const [accessToken, setAccessToken] = useState<string | null>(localStorage.getItem("accessToken"));

  const handleLogin = (access: string, refresh: string) => {
    localStorage.setItem("accessToken", access);
    localStorage.setItem("refreshToken", refresh);
    setAccessToken(access);
  };

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    setAccessToken(null);
  };

  return (
    <Router>
      <div className='App'>
        <Header access={!!accessToken} onLogout={handleLogout} />
        <div className='main'>
          <Routes>
            <Route path="/" element={!accessToken ? <LoginForm onLogin={handleLogin} /> :
                                 <Dashboard availableAccess={accessToken} />} />
            {/* <Route path='dashboard/' element={<Dashboard />} /> */}
            {/* <Route path='/login' element={<LoginForm onLogin={handleLogin} />} /> */}
          </Routes>
        </div>
        {/* <Footer /> */}
      </div>
    </Router>
  )
}

export default App
