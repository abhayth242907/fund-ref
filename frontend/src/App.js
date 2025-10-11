import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import FundSearch from './components/FundSearch';
import FundDetails from './components/FundDetails';
import FundVisualization from './components/FundVisualization';
import FundOnboarding from './components/FundOnboarding';
import ManagementEntityExplorer from './components/ManagementEntityExplorer';
import SubFundDetails from './components/SubFundDetails';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/search" element={<FundSearch />} />
          <Route path="/fund/:fundId" element={<FundDetails />} />
          <Route path="/subfund/:subfundId" element={<SubFundDetails />} />
          <Route path="/visualization/:fundId" element={<FundVisualization />} />
          <Route path="/onboarding" element={<FundOnboarding />} />
          <Route path="/management" element={<ManagementEntityExplorer />} />
          <Route path="/management/:mgmtId" element={<ManagementEntityExplorer />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;