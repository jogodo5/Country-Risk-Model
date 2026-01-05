# Country Risk Model 🌍

A comprehensive web-based platform for assessing country-level risks across multiple dimensions including money laundering, terrorism financing, sanctions, transparency, corruption, and more.

## Features

### Risk Assessment Categories
- **💰 Money Laundering**: Assessment of AML risks and controls
- **⚠️ Terrorism Financing**: Analysis of CFT vulnerabilities
- **🚫 Sanctions and Evasion**: International sanctions monitoring
- **🔍 Transparency**: Government and financial transparency metrics
- **⚖️ Corruption**: Corruption perception analysis
- **📋 Regulatory Compliance**: International regulatory standards adherence
- **🏛️ Political Stability**: Political stability and governance indicators
- **📊 Economic Risk**: Economic stability and financial health assessment

### Data
- **Country List**: Comprehensive list of 195+ countries with ISO codes (Alpha-2, Alpha-3, Numeric)
- **Local Storage**: All country data stored locally for offline access
- **External Data Integration**: Framework for collecting data from international sources (FATF, Transparency International, World Bank, IMF, etc.)

## Project Structure

```
Country-Risk-Model/
├── backend/
│   └── app.py              # Flask API server
├── frontend/
│   ├── index.html          # Landing page
│   ├── countries.html      # Countries list page
│   ├── country.html        # Country detail page
│   ├── risk-factors.html   # Risk factors information
│   ├── about.html          # About page
│   ├── styles.css          # Styling
│   └── app.js              # Frontend utilities
├── data/
│   ├── countries.json      # Country list with ISO codes
│   └── risk_data.json      # Risk assessment data (auto-generated)
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/jogodo5/Country-Risk-Model.git
   cd Country-Risk-Model
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   cd backend
   python app.py
   ```

4. **Access the application**
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## API Endpoints

### Countries
- `GET /api/countries` - Get all countries
- `GET /api/countries/<code>` - Get specific country details
- `GET /api/search?q=<query>` - Search countries

### Risk Assessment
- `GET /api/risk-categories` - Get all risk categories
- `GET /api/countries/<code>/risk` - Get country risk assessment
- `POST /api/countries/<code>/risk` - Update country risk assessment

### Statistics
- `GET /api/stats` - Get platform statistics

## Usage

### Viewing Countries
1. Navigate to the "Countries" page
2. Browse or search for specific countries
3. Click on a country to view detailed risk assessment

### Risk Assessment
Each country can be assessed across 8 risk categories with scores from 0-10:
- **0-3**: Low Risk (Green)
- **4-6**: Medium Risk (Orange)
- **7-10**: High Risk (Red)

### Adding Risk Data
Risk data can be added via the API:
```bash
curl -X POST http://localhost:5000/api/countries/US/risk \
  -H "Content-Type: application/json" \
  -d '{
    "money_laundering": 3.5,
    "terrorism_financing": 2.8,
    "sanctions": 1.5,
    "transparency": 7.2,
    "corruption": 6.8,
    "regulatory_compliance": 8.5,
    "political_stability": 7.0,
    "economic_risk": 4.2
  }'
```

## Data Sources

The platform is designed to integrate data from:
- Financial Action Task Force (FATF)
- Basel AML Index
- Transparency International
- World Bank Governance Indicators
- International Monetary Fund (IMF)
- OFAC (Office of Foreign Assets Control)
- UN Security Council
- EU Sanctions Database

## Deployment

### For Production Hosting

1. **Set Flask to production mode**
   ```bash
   # Set environment variable before running
   export FLASK_ENV=production
   cd backend
   python app.py
   ```
   
   Or use a production WSGI server (recommended):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
   ```
2. **Set up reverse proxy** (nginx example)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Hosting Options
- **Heroku**: Use `Procfile` with gunicorn
- **AWS**: Deploy on EC2 or Elastic Beanstalk
- **DigitalOcean**: App Platform or Droplet
- **PythonAnywhere**: Free tier available
- **Vercel/Netlify**: For static frontend with serverless backend

## Development

### Adding New Risk Categories
1. Update the risk categories in `backend/app.py` in the `get_risk_categories()` function
2. Add corresponding UI elements in the frontend pages
3. Update the documentation

### Integrating External Data Sources
Create a data collection script:
```python
# backend/data_collector.py
import requests
from app import save_risk_data, load_risk_data

def collect_fatf_data():
    # Implement data collection logic
    pass

def update_risk_scores():
    # Update risk_data.json with collected data
    pass
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

The information provided on this platform is for informational purposes only. Risk assessments should not be used as the sole basis for making business or financial decisions. Always conduct your own due diligence and consult with appropriate professionals.

## Support

For issues, questions, or contributions, please open an issue on GitHub.
