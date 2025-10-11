import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Breadcrumbs,
  Link,
  Chip,
  Divider,
} from '@mui/material';
import {
  Business as BusinessIcon,
  Visibility as ViewIcon,
  TrendingUp as ChartIcon,
} from '@mui/icons-material';
import { managementAPI, fundAPI } from '../services/api';

const ManagementEntityExplorer = () => {
  const { mgmtId: urlMgmtId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [managementEntities, setManagementEntities] = useState([]);
  const [selectedMgmtId, setSelectedMgmtId] = useState(urlMgmtId || '');
  const [selectedEntity, setSelectedEntity] = useState(null);
  const [funds, setFunds] = useState([]);

  const fetchManagementEntities = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await managementAPI.getAllManagementEntities(1, 100);
      setManagementEntities(response.data.management_entities || []);
      
      // If no mgmtId in URL, select first entity
      if (!selectedMgmtId && response.data.management_entities.length > 0) {
        setSelectedMgmtId(response.data.management_entities[0].mgmt_id);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch management entities');
    } finally {
      setLoading(false);
    }
  }, [selectedMgmtId]);

  const fetchEntityDetails = useCallback(async () => {
    try {
      const response = await managementAPI.getManagementEntityById(selectedMgmtId);
      setSelectedEntity(response.data);
    } catch (err) {
      console.error('Error fetching entity details:', err);
    }
  }, [selectedMgmtId]);

  const fetchFundsByManagement = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fundAPI.getFundsByManagementEntity(selectedMgmtId);
      setFunds(response.data.funds || []);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch funds');
    } finally {
      setLoading(false);
    }
  }, [selectedMgmtId]);

  useEffect(() => {
    fetchManagementEntities();
  }, [fetchManagementEntities]);

  useEffect(() => {
    if (selectedMgmtId) {
      fetchEntityDetails();
      fetchFundsByManagement();
    }
  }, [selectedMgmtId, fetchEntityDetails, fetchFundsByManagement]);

  const handleMgmtChange = (event) => {
    setSelectedMgmtId(event.target.value);
  };

  if (loading && !selectedEntity) {
    return (
      <Container maxWidth="xl" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs sx={{ mb: 2 }}>
        <Link underline="hover" color="inherit" onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>
          Home
        </Link>
        <Typography color="text.primary">Management Entity Explorer</Typography>
      </Breadcrumbs>

      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5">
          Management Entity Explorer
        </Typography>
        <FormControl sx={{ minWidth: 300 }}>
          <InputLabel>Select Management Entity</InputLabel>
          <Select
            value={selectedMgmtId}
            label="Select Management Entity"
            onChange={handleMgmtChange}
          >
            {managementEntities.map((entity) => (
              <MenuItem key={entity.mgmt_id} value={entity.mgmt_id}>
                {entity.mgmt_id} - {entity.registration_no}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Management Entity Details */}
      {selectedEntity && (
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <BusinessIcon sx={{ fontSize: 40, color: '#4caf50', mr: 2 }} />
            <Box>
              <Typography variant="h6">
                {selectedEntity.mgmt_id}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Management Entity Details
              </Typography>
            </Box>
          </Box>
          <Divider sx={{ mb: 2 }} />
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="body2" color="text.secondary">
                Registration Number
              </Typography>
              <Typography variant="body1">
                {selectedEntity.registration_no || 'N/A'}
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="body2" color="text.secondary">
                Entity Type
              </Typography>
              <Typography variant="body1">
                {selectedEntity.entity_type || 'N/A'}
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="body2" color="text.secondary">
                Domicile
              </Typography>
              <Typography variant="body1">
                {selectedEntity.domicile || 'N/A'}
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="body2" color="text.secondary">
                Status
              </Typography>
              <Chip
                label={selectedEntity.status || 'N/A'}
                color={selectedEntity.status === 'ACTIVE' ? 'success' : 'default'}
                size="small"
              />
            </Grid>
          </Grid>
        </Paper>
      )}

      {/* Funds Managed */}
      <Typography variant="h6" gutterBottom>
        Funds Managed ({funds.length})
      </Typography>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
          <CircularProgress />
        </Box>
      ) : funds.length === 0 ? (
        <Paper elevation={2} sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="body1" color="text.secondary">
            No funds found for this management entity
          </Typography>
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {funds.map((fund) => (
            <Grid item xs={12} sm={6} md={4} key={fund.fund_id}>
              <Card elevation={2}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 1 }}>
                    <Typography variant="h6" component="div" sx={{ fontSize: '1rem' }}>
                      {fund.fund_name}
                    </Typography>
                    <Chip
                      label={fund.status}
                      size="small"
                      color={fund.status === 'ACTIVE' ? 'success' : 'default'}
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    {fund.fund_code}
                  </Typography>
                  <Divider sx={{ my: 1 }} />
                  <Grid container spacing={1}>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">
                        Type
                      </Typography>
                      <Typography variant="body2">
                        {fund.fund_type}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">
                        Currency
                      </Typography>
                      <Typography variant="body2">
                        {fund.base_currency}
                      </Typography>
                    </Grid>
                    <Grid item xs={12}>
                      <Typography variant="caption" color="text.secondary">
                        Domicile
                      </Typography>
                      <Typography variant="body2">
                        {fund.domicile}
                      </Typography>
                    </Grid>
                    {fund.isin_master && (
                      <Grid item xs={12}>
                        <Typography variant="caption" color="text.secondary">
                          ISIN
                        </Typography>
                        <Typography variant="body2" sx={{ fontSize: '0.75rem' }}>
                          {fund.isin_master}
                        </Typography>
                      </Grid>
                    )}
                  </Grid>
                </CardContent>
                <CardActions sx={{ justifyContent: 'space-between', px: 2, pb: 2 }}>
                  <Button
                    size="small"
                    startIcon={<ViewIcon />}
                    onClick={() => navigate(`/fund/${fund.fund_id}`)}
                  >
                    Details
                  </Button>
                  <Button
                    size="small"
                    startIcon={<ChartIcon />}
                    onClick={() => navigate(`/visualization/${fund.fund_id}`)}
                  >
                    Visualize
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

export default ManagementEntityExplorer;
