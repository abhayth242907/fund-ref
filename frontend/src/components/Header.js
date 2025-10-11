import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { 
  Dashboard as DashboardIcon, 
  Search as SearchIcon,
  Business as BusinessIcon,
  Add as AddIcon,
} from '@mui/icons-material';

const Header = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Fund Referential System
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button color="inherit" component={RouterLink} to="/" startIcon={<DashboardIcon />}>
            Dashboard
          </Button>
          <Button color="inherit" component={RouterLink} to="/search" startIcon={<SearchIcon />}>
            Search
          </Button>
          <Button color="inherit" component={RouterLink} to="/management" startIcon={<BusinessIcon />}>
            Management
          </Button>
          <Button color="inherit" component={RouterLink} to="/onboarding" startIcon={<AddIcon />}>
            Onboard Fund
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;