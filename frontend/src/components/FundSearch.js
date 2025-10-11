import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  TextField,
  Button,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Typography,
  Box,
  Chip,
  IconButton,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  Search as SearchIcon,
  Visibility as VisibilityIcon,
  FilterList as FilterListIcon,
  ExpandMore as ExpandMoreIcon,
  AccountTree as HierarchyIcon,
} from '@mui/icons-material';
import { fundAPI } from '../services/api';

const FundSearch = () => {
  const navigate = useNavigate();
  const [funds, setFunds] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [totalFunds, setTotalFunds] = useState(0);
  const [filterExpanded, setFilterExpanded] = useState(true);

  // Search filters
  const [filters, setFilters] = useState({
    fund_code: '',
    fund_id: '',
    isin: '',
    fund_type: '',
    status: '',
    mgmt_id: '',
  });

  const fundTypes = ['UCITS', 'AIF', 'ETF', 'MUTUAL_FUND', 'HEDGE_FUND'];
  const statuses = ['ACTIVE', 'CLOSED', 'SUSPENDED'];

  const searchFunds = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      // Filter out empty values
      const params = Object.fromEntries(
        Object.entries(filters).filter(([_, value]) => value !== '')
      );
      params.page = page + 1; // API pages are 1-indexed
      params.page_size = rowsPerPage;

      const response = await fundAPI.searchFunds(params);
      setFunds(response.data.funds || []);
      setTotalFunds(response.data.total || 0);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch funds');
      setFunds([]);
    } finally {
      setLoading(false);
    }
  }, [filters, page, rowsPerPage]);

  useEffect(() => {
    searchFunds();
  }, [searchFunds]);

  const handleFilterChange = (field, value) => {
    setFilters((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSearch = () => {
    setPage(0); // Reset to first page on new search
    searchFunds();
  };

  const handleClearFilters = () => {
    setFilters({
      fund_code: '',
      fund_id: '',
      isin: '',
      fund_type: '',
      status: '',
      mgmt_id: '',
    });
    setPage(0);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleViewDetails = (fund) => {
    navigate(`/fund/${fund.fund_id}`);
  };

  const handleViewHierarchy = (fund) => {
    navigate(`/visualization/${fund.fund_id}`);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'ACTIVE':
        return 'success';
      case 'CLOSED':
        return 'error';
      case 'SUSPENDED':
        return 'warning';
      default:
        return 'default';
    }
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Fund Search & Explorer
      </Typography>

      {/* Filters Section */}
      <Accordion
        expanded={filterExpanded}
        onChange={() => setFilterExpanded(!filterExpanded)}
        sx={{ mb: 3 }}
      >
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <FilterListIcon />
            <Typography variant="h6">Search Filters</Typography>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={4}>
              <TextField
                fullWidth
                label="Fund Code"
                value={filters.fund_code}
                onChange={(e) => handleFilterChange('fund_code', e.target.value)}
                placeholder="e.g., FUND001"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <TextField
                fullWidth
                label="Fund ID"
                value={filters.fund_id}
                onChange={(e) => handleFilterChange('fund_id', e.target.value)}
                placeholder="e.g., F000001"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <TextField
                fullWidth
                label="ISIN"
                value={filters.isin}
                onChange={(e) => handleFilterChange('isin', e.target.value)}
                placeholder="e.g., IE00B4L5Y983"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <FormControl fullWidth>
                <InputLabel>Fund Type</InputLabel>
                <Select
                  value={filters.fund_type}
                  label="Fund Type"
                  onChange={(e) => handleFilterChange('fund_type', e.target.value)}
                >
                  <MenuItem value="">All</MenuItem>
                  {fundTypes.map((type) => (
                    <MenuItem key={type} value={type}>
                      {type}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={filters.status}
                  label="Status"
                  onChange={(e) => handleFilterChange('status', e.target.value)}
                >
                  <MenuItem value="">All</MenuItem>
                  {statuses.map((status) => (
                    <MenuItem key={status} value={status}>
                      {status}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <TextField
                fullWidth
                label="Management Entity ID"
                value={filters.mgmt_id}
                onChange={(e) => handleFilterChange('mgmt_id', e.target.value)}
                placeholder="e.g., MG000001"
              />
            </Grid>
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button
                  variant="contained"
                  startIcon={<SearchIcon />}
                  onClick={handleSearch}
                  disabled={loading}
                >
                  Search
                </Button>
                <Button variant="outlined" onClick={handleClearFilters}>
                  Clear Filters
                </Button>
              </Box>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Results Table */}
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            <TableContainer sx={{ maxHeight: 600 }}>
              <Table stickyHeader>
                <TableHead>
                  <TableRow>
                    <TableCell><strong>Fund Code</strong></TableCell>
                    <TableCell><strong>Fund Name</strong></TableCell>
                    <TableCell><strong>Type</strong></TableCell>
                    <TableCell><strong>Currency</strong></TableCell>
                    <TableCell><strong>Status</strong></TableCell>
                    <TableCell><strong>ISIN</strong></TableCell>
                    <TableCell align="center"><strong>Actions</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {funds.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={7} align="center">
                        <Typography variant="body2" color="text.secondary" sx={{ py: 4 }}>
                          No funds found. Try adjusting your search filters.
                        </Typography>
                      </TableCell>
                    </TableRow>
                  ) : (
                    funds.map((fund) => (
                      <TableRow key={fund.fund_id} hover>
                        <TableCell>{fund.fund_code}</TableCell>
                        <TableCell>{fund.fund_name}</TableCell>
                        <TableCell>
                          <Chip label={fund.fund_type} size="small" variant="outlined" />
                        </TableCell>
                        <TableCell>{fund.base_currency}</TableCell>
                        <TableCell>
                          <Chip
                            label={fund.status}
                            size="small"
                            color={getStatusColor(fund.status)}
                          />
                        </TableCell>
                        <TableCell sx={{ fontSize: '0.875rem' }}>{fund.isin_master}</TableCell>
                        <TableCell align="center">
                          <IconButton
                            size="small"
                            color="primary"
                            onClick={() => handleViewDetails(fund)}
                            title="View Details"
                          >
                            <VisibilityIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            color="secondary"
                            onClick={() => handleViewHierarchy(fund)}
                            title="View Hierarchy"
                          >
                            <HierarchyIcon />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
            <TablePagination
              rowsPerPageOptions={[5, 10, 25, 50]}
              component="div"
              count={totalFunds}
              rowsPerPage={rowsPerPage}
              page={page}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
            />
          </>
        )}
      </Paper>
    </Container>
  );
};

export default FundSearch;