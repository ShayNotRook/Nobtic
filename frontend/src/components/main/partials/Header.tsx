// import React from 'react'
import './Header.css';
import { AppBar } from '@mui/material';
import { Box } from '@mui/material';
import { Toolbar } from '@mui/material';
// import { Typography } from '@mui/material';
import { Button } from '@mui/material';
import {Link as RouterLink } from 'react-router-dom';

interface HeaderProps {
  access: boolean;
  onLogout: () => void;
}

const Header: React.FC<HeaderProps> = ({ access, onLogout }) => {

  return (

    <AppBar position="static">
      <Toolbar>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button color="inherit" component={RouterLink} to="/">
            Home
          </Button>
          {access ? (
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Button color="inherit" component={RouterLink} to="/dashboard">
                Dashboard
              </Button>
              <Button color="inherit" onClick={onLogout}>
                Logout
              </Button>
            </Box>
          ) : (
            <Button color="inherit" component={RouterLink} to="/login">
              Login
            </Button>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  )
}

export default Header;