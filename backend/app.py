"""
Country Risk Model Backend API
Provides endpoints for country risk assessment data
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os

# Get the base directory (parent of backend)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Load countries data
def load_countries():
    countries_file = os.path.join(DATA_DIR, 'countries.json')
    with open(countries_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load risk data
def load_risk_data():
    risk_file = os.path.join(DATA_DIR, 'risk_data.json')
    if os.path.exists(risk_file):
        with open(risk_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Save risk data
def save_risk_data(data):
    risk_file = os.path.join(DATA_DIR, 'risk_data.json')
    with open(risk_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    """Serve the frontend landing page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/countries', methods=['GET'])
def get_countries():
    """Get list of all countries"""
    try:
        countries = load_countries()
        return jsonify({
            'success': True,
            'count': len(countries),
            'countries': countries
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    """Get details for a specific country"""
    try:
        countries = load_countries()
        country_code = country_code.upper()
        
        # Find country by alpha2 or alpha3 code
        country = next(
            (c for c in countries 
             if c['alpha2'] == country_code or c['alpha3'] == country_code),
            None
        )
        
        if not country:
            return jsonify({
                'success': False,
                'error': 'Country not found'
            }), 404
        
        # Get risk data for this country (always use alpha2 code)
        risk_data = load_risk_data()
        country_risk = risk_data.get(country['alpha2'], {})
        
        return jsonify({
            'success': True,
            'country': country,
            'risk_assessment': country_risk
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/risk-categories', methods=['GET'])
def get_risk_categories():
    """Get all risk factor categories"""
    categories = [
        {
            'id': 'money_laundering',
            'name': 'Money Laundering',
            'description': 'Risk of money laundering activities',
            'data_sources': ['FATF', 'Basel AML Index']
        },
        {
            'id': 'terrorism_financing',
            'name': 'Terrorism Financing',
            'description': 'Risk of terrorism financing activities',
            'data_sources': ['FATF', 'UN Security Council']
        },
        {
            'id': 'sanctions',
            'name': 'Sanctions and Evasion',
            'description': 'International sanctions and evasion risks',
            'data_sources': ['OFAC', 'UN', 'EU Sanctions']
        },
        {
            'id': 'transparency',
            'name': 'Transparency',
            'description': 'Government and financial transparency',
            'data_sources': ['Transparency International', 'World Bank']
        },
        {
            'id': 'corruption',
            'name': 'Corruption',
            'description': 'Corruption perception and risks',
            'data_sources': ['Corruption Perceptions Index']
        },
        {
            'id': 'regulatory_compliance',
            'name': 'Regulatory Compliance',
            'description': 'Adherence to international regulatory standards',
            'data_sources': ['World Bank', 'IMF']
        },
        {
            'id': 'political_stability',
            'name': 'Political Stability',
            'description': 'Political stability and governance',
            'data_sources': ['World Bank Governance Indicators']
        },
        {
            'id': 'economic_risk',
            'name': 'Economic Risk',
            'description': 'Economic stability and financial risks',
            'data_sources': ['IMF', 'World Bank', 'Credit Rating Agencies']
        }
    ]
    
    return jsonify({
        'success': True,
        'categories': categories
    })

@app.route('/api/countries/<country_code>/risk', methods=['GET'])
def get_country_risk(country_code):
    """Get risk assessment for a specific country"""
    try:
        countries = load_countries()
        risk_data = load_risk_data()
        country_code = country_code.upper()
        
        # Find country to get alpha2 code
        country = next(
            (c for c in countries 
             if c['alpha2'] == country_code or c['alpha3'] == country_code),
            None
        )
        
        if not country:
            return jsonify({
                'success': False,
                'error': 'Country not found'
            }), 404
        
        # Use alpha2 code for risk data lookup
        alpha2_code = country['alpha2']
        
        if alpha2_code not in risk_data:
            # Return default/placeholder data if no risk data exists
            return jsonify({
                'success': True,
                'country_code': alpha2_code,
                'risk_scores': {},
                'overall_risk': 'Not Assessed',
                'message': 'No risk data available for this country'
            })
        
        return jsonify({
            'success': True,
            'country_code': alpha2_code,
            'risk_assessment': risk_data[alpha2_code]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/countries/<country_code>/risk', methods=['POST'])
def update_country_risk(country_code):
    """Update risk assessment for a specific country"""
    try:
        countries = load_countries()
        country_code = country_code.upper()
        
        # Find country to get alpha2 code
        country = next(
            (c for c in countries 
             if c['alpha2'] == country_code or c['alpha3'] == country_code),
            None
        )
        
        if not country:
            return jsonify({
                'success': False,
                'error': 'Country not found'
            }), 404
        
        # Use alpha2 code for risk data storage
        alpha2_code = country['alpha2']
        risk_data = load_risk_data()
        
        # Get the request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Update risk data for this country
        risk_data[alpha2_code] = data
        save_risk_data(risk_data)
        
        return jsonify({
            'success': True,
            'message': 'Risk data updated successfully',
            'country_code': alpha2_code
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search', methods=['GET'])
def search_countries():
    """Search countries by name or code"""
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query required'
            }), 400
        
        countries = load_countries()
        results = [
            c for c in countries
            if query in c['name'].lower() 
            or query in c['alpha2'].lower()
            or query in c['alpha3'].lower()
        ]
        
        return jsonify({
            'success': True,
            'query': query,
            'count': len(results),
            'results': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    try:
        countries = load_countries()
        risk_data = load_risk_data()
        
        return jsonify({
            'success': True,
            'total_countries': len(countries),
            'assessed_countries': len(risk_data),
            'unassessed_countries': len(countries) - len(risk_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Create initial risk_data.json if it doesn't exist
    risk_file = os.path.join(DATA_DIR, 'risk_data.json')
    if not os.path.exists(risk_file):
        save_risk_data({})
    
    app.run(debug=True, host='0.0.0.0', port=5000)
