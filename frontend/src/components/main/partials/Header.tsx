// import React from 'react'
import './Header.css'


const Header = () => {
  const access = localStorage.getItem('accessToken');

  return (
    <nav className="header">
      <h1>Scheduler</h1>
      <div className="nav-links">
        <a href="/">Home</a>
        { access ?  <div className='user-links'>
                    <a href="/dashboard">Dashboard</a> 
                    <a href="/logout">Logout</a></div>
                    : <a className='login' href="/login">Login</a>}
      </div>
    </nav>
  )
}

export default Header;