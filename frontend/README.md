# Fund Referential System - Frontend

A comprehensive React-based frontend application for managing and visualizing fund hierarchies, built with Material-UI and ReactFlow.

## Features

### 1. Dashboard
- **Overview Statistics**: Total funds, active/inactive counts
- **Visual Analytics**: Pie charts and bar charts showing fund distribution by type
- **Recent Funds**: Quick access to recently added funds
- **Quick Actions**: Navigate to search or onboarding

### 2. Fund Search
- **Advanced Filtering**: Search by fund code, fund ID, ISIN, fund type, status, and management entity
- **Pagination**: Browse through large datasets efficiently
- **Expandable Filters**: Clean UI with collapsible filter section
- **Quick Navigation**: Click on any fund to view details or visualize hierarchy

### 3. Fund Details
- **Comprehensive Information**: View all fund attributes including:
  - Basic info (code, name, type, currency, domicile, ISIN, status)
  - Management entity details
  - Share classes with distribution and currency info
  - SubFunds hierarchy
- **Navigation**: Breadcrumbs and buttons to easily navigate between views
- **Visualization Link**: Direct access to hierarchy visualization

### 4. Fund Hierarchy Visualization
- **Interactive Graph**: Built with ReactFlow for smooth pan, zoom, and node interaction
- **Color-Coded Nodes**:
  - Blue: Fund
  - Green: Management Entity
  - Orange: Share Class
  - Purple: SubFund
- **Configurable Depth**: Choose hierarchy depth (1-3 levels)
- **MiniMap**: Overview of entire graph structure
- **Node Details**: Click nodes to see detailed information

### 5. Fund Onboarding
- **Multi-Step Form**: Wizard-style interface with 3 steps:
  1. Basic Information (code, name, type, currency, etc.)
  2. Management & Legal entities
  3. Additional details (inception date, AUM, expense ratio)
- **Validation**: Required field validation
- **Pre-populated Options**: Dropdowns populated from existing management and legal entities
- **Auto-navigation**: Redirects to fund details upon successful creation

### 6. Management Entity Explorer
- **Entity Selection**: Dropdown to select any management entity
- **Entity Details**: View registration number, type, domicile, status
- **Associated Funds**: Grid of all funds managed by the selected entity
- **Fund Cards**: Each card shows:
  - Fund name, code, status
  - Type, currency, domicile
  - ISIN (if available)
  - Quick links to details and visualization

## Technology Stack

- **React 18.2.0**: Core framework
- **Material-UI 5.14.14**: UI component library
- **ReactFlow**: Interactive node-based visualization
- **Recharts**: Charts and data visualization
- **React Router 6.17.0**: Client-side routing
- **Axios 1.5.1**: HTTP client for API communication

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Dashboard.js           # Main dashboard with statistics
│   │   ├── FundSearch.js          # Advanced search with filters
│   │   ├── FundDetails.js         # Detailed fund view
│   │   ├── FundVisualization.js   # Interactive hierarchy graph
│   │   ├── FundOnboarding.js      # Multi-step fund creation form
│   │   ├── ManagementEntityExplorer.js # Management entity viewer
│   │   └── Header.js              # Navigation header
│   ├── services/
│   │   └── api.js                 # API service layer
│   ├── App.js                     # Main app with routing
│   └── index.js                   # Entry point
├── package.json
└── README.md
```

## Installation

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm start
   ```

   The application will open at `http://localhost:3000`

## Configuration

### API Base URL
The frontend connects to the backend API at `http://localhost:8000`. Update this in `src/services/api.js` if your backend runs on a different port.

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## Available Routes

- `/` - Dashboard (home page)
- `/search` - Fund search with filters
- `/fund/:fundId` - Detailed fund view
- `/visualization/:fundId` - Interactive hierarchy visualization
- `/onboarding` - Create new fund form
- `/management` - Management entity explorer
- `/management/:mgmtId` - Management entity with specific ID

## API Integration

The frontend communicates with the backend through a centralized API service (`src/services/api.js`) with the following endpoints:

### Fund API
- `searchFunds(filters, page, pageSize)` - Search funds with filters
- `getFundByCode(fundCode)` - Get fund by code
- `getFundById(fundId)` - Get fund by ID
- `createFund(fundData)` - Create new fund
- `getFundHierarchyChildren(fundId, depth)` - Get child hierarchy
- `getFundHierarchyParents(fundId, depth)` - Get parent hierarchy
- `getFundsByManagementEntity(mgmtId)` - Get all funds by management entity

### Management Entity API
- `getAllManagementEntities(page, pageSize)` - List all entities
- `getManagementEntityById(mgmtId)` - Get entity details

### SubFund API
- `getAllSubFunds(page, pageSize)` - List all subfunds
- `getSubFundById(subfundId)` - Get subfund details

### Share Class API
- `getAllShareClasses(page, pageSize)` - List all share classes
- `getShareClassById(scId)` - Get share class details

### Legal Entity API
- `getAllLegalEntities(page, pageSize)` - List all legal entities
- `getLegalEntityById(leId)` - Get legal entity details

## Features Implementation

### Search Functionality
The search component supports multiple filter criteria:
- Fund Code (exact or partial match)
- Fund ID (exact match)
- ISIN (exact or partial match)
- Fund Type (dropdown: UCITS, AIF, ETF, etc.)
- Status (dropdown: ACTIVE, INACTIVE, etc.)
- Management Entity ID (exact match)

Filters can be combined for precise searches.

### Hierarchy Visualization
The visualization uses ReactFlow to create an interactive graph:
- Nodes represent funds, subfunds, management entities, and share classes
- Edges show relationships (manages, parent-child, has class)
- Pan and zoom for navigation
- Mini-map for overview
- Configurable depth for performance

### Form Validation
The onboarding form includes:
- Required field validation
- Type-specific inputs (date picker, number inputs)
- Dropdown menus populated from database
- Multi-step wizard with back/forward navigation

## Styling

The application uses Material-UI's theming system with a custom theme:
- Primary color: Blue (#1976d2)
- Secondary color: Red (#dc004e)
- Consistent spacing and typography
- Responsive design for mobile and desktop

## Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development Tips

1. **Hot Reload**: Changes to source files will automatically reload the browser
2. **Error Overlay**: Compilation errors appear as an overlay in the browser
3. **Console Logging**: Use browser DevTools to debug API calls and component state
4. **React DevTools**: Install the React Developer Tools extension for debugging

## Troubleshooting

### Backend Connection Issues
If you see "Network Error" or "Failed to fetch":
1. Ensure the backend is running at `http://localhost:8000`
2. Check CORS settings in the backend
3. Verify API endpoints in `src/services/api.js`

### Missing Data
If dropdowns are empty or data doesn't load:
1. Check that the Neo4j database is populated
2. Verify backend API responses in browser DevTools Network tab
3. Check console for error messages

### Visualization Not Rendering
If the hierarchy visualization is blank:
1. Ensure ReactFlow styles are imported in `FundVisualization.js`
2. Check that the fund has related entities (management, share classes, subfunds)
3. Verify the hierarchy API returns valid data

## Future Enhancements

- Natural language search using AI
- Real-time fund updates with WebSockets
- Export functionality (PDF, Excel)
- Advanced analytics and reporting
- Multi-language support
- Dark mode theme
- Mobile-optimized views
- Bulk fund import
- Fund comparison tool
- Historical data tracking

## License

MIT License - see LICENSE file for details
