import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Stepper,
  Step,
  StepLabel,
  Button,
  TextField,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Breadcrumbs,
  Link,
} from '@mui/material';
import {
  Save as SaveIcon,
  ArrowBack as BackIcon,
  ArrowForward as ForwardIcon,
} from '@mui/icons-material';
import { fundAPI, managementAPI, legalEntityAPI } from '../services/api';

const steps = ['Basic Information', 'Management & Legal', 'Additional Details'];

const FundOnboarding = () => {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [managementEntities, setManagementEntities] = useState([]);
  const [legalEntities, setLegalEntities] = useState([]);

  const [formData, setFormData] = useState({
    fund_code: '',
    fund_name: '',
    fund_type: 'UCITS',
    base_currency: 'USD',
    domicile: '',
    isin_master: '',
    status: 'ACTIVE',
    mgmt_id: '',
    le_id: '',
    inception_date: '',
    aum: '',
    expense_ratio: '',
  });

  useEffect(() => {
    fetchReferenceData();
  }, []);

  const fetchReferenceData = async () => {
    try {
      const mgmtResponse = await managementAPI.getAllManagementEntities(1, 100);
      setManagementEntities(mgmtResponse.data.management_entities || []);

      const leResponse = await legalEntityAPI.getAllLegalEntities(1, 100);
      setLegalEntities(leResponse.data.legal_entities || []);
    } catch (err) {
      console.error('Error fetching reference data:', err);
    }
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    try {
      // Create the fund
      const response = await fundAPI.createFund(formData);
      setSuccess(true);
      
      setTimeout(() => {
        navigate(`/fund/${response.data.fund_id}`);
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create fund');
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                required
                fullWidth
                name="fund_code"
                label="Fund Code"
                value={formData.fund_code}
                onChange={handleChange}
                helperText="Unique identifier for the fund"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                required
                fullWidth
                name="fund_name"
                label="Fund Name"
                value={formData.fund_name}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Fund Type</InputLabel>
                <Select
                  name="fund_type"
                  value={formData.fund_type}
                  label="Fund Type"
                  onChange={handleChange}
                >
                  <MenuItem value="UCITS">UCITS</MenuItem>
                  <MenuItem value="AIF">AIF</MenuItem>
                  <MenuItem value="ETF">ETF</MenuItem>
                  <MenuItem value="HEDGE">Hedge Fund</MenuItem>
                  <MenuItem value="PENSION">Pension Fund</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Base Currency</InputLabel>
                <Select
                  name="base_currency"
                  value={formData.base_currency}
                  label="Base Currency"
                  onChange={handleChange}
                >
                  <MenuItem value="USD">USD</MenuItem>
                  <MenuItem value="EUR">EUR</MenuItem>
                  <MenuItem value="GBP">GBP</MenuItem>
                  <MenuItem value="CHF">CHF</MenuItem>
                  <MenuItem value="JPY">JPY</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                required
                fullWidth
                name="domicile"
                label="Domicile"
                value={formData.domicile}
                onChange={handleChange}
                helperText="Country of registration"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                name="isin_master"
                label="ISIN Master"
                value={formData.isin_master}
                onChange={handleChange}
                helperText="International Securities Identification Number"
              />
            </Grid>
          </Grid>
        );

      case 1:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Management Entity</InputLabel>
                <Select
                  name="mgmt_id"
                  value={formData.mgmt_id}
                  label="Management Entity"
                  onChange={handleChange}
                >
                  {managementEntities.map((entity) => (
                    <MenuItem key={entity.mgmt_id} value={entity.mgmt_id}>
                      {entity.mgmt_id} - {entity.registration_no}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Legal Entity</InputLabel>
                <Select
                  name="le_id"
                  value={formData.le_id}
                  label="Legal Entity"
                  onChange={handleChange}
                >
                  {legalEntities.map((entity) => (
                    <MenuItem key={entity.le_id} value={entity.le_id}>
                      {entity.le_id} - {entity.lei}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Status</InputLabel>
                <Select
                  name="status"
                  value={formData.status}
                  label="Status"
                  onChange={handleChange}
                >
                  <MenuItem value="ACTIVE">Active</MenuItem>
                  <MenuItem value="INACTIVE">Inactive</MenuItem>
                  <MenuItem value="PENDING">Pending</MenuItem>
                  <MenuItem value="CLOSED">Closed</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        );

      case 2:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                name="inception_date"
                label="Inception Date"
                type="date"
                value={formData.inception_date}
                onChange={handleChange}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                name="aum"
                label="Assets Under Management (AUM)"
                type="number"
                value={formData.aum}
                onChange={handleChange}
                helperText="In base currency"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                name="expense_ratio"
                label="Expense Ratio (%)"
                type="number"
                value={formData.expense_ratio}
                onChange={handleChange}
                inputProps={{ step: '0.01', min: '0', max: '100' }}
              />
            </Grid>
          </Grid>
        );

      default:
        return 'Unknown step';
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs sx={{ mb: 2 }}>
        <Link underline="hover" color="inherit" onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>
          Home
        </Link>
        <Typography color="text.primary">Fund Onboarding</Typography>
      </Breadcrumbs>

      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h5" gutterBottom>
          Onboard New Fund
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
          Complete all steps to add a new fund to the system
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert severity="success" sx={{ mb: 3 }}>
            Fund created successfully! Redirecting to fund details...
          </Alert>
        )}

        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        <Box sx={{ mb: 4 }}>
          {renderStepContent(activeStep)}
        </Box>

        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
          <Button
            onClick={() => navigate('/')}
            startIcon={<BackIcon />}
            disabled={loading}
          >
            Cancel
          </Button>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              disabled={activeStep === 0 || loading}
              onClick={handleBack}
            >
              Back
            </Button>
            {activeStep === steps.length - 1 ? (
              <Button
                variant="contained"
                onClick={handleSubmit}
                startIcon={loading ? <CircularProgress size={20} /> : <SaveIcon />}
                disabled={loading || success}
              >
                {loading ? 'Creating...' : 'Create Fund'}
              </Button>
            ) : (
              <Button
                variant="contained"
                onClick={handleNext}
                endIcon={<ForwardIcon />}
              >
                Next
              </Button>
            )}
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default FundOnboarding;
