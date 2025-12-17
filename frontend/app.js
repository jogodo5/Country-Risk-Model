// Shared JavaScript utilities for Country Risk Model

// API base URL
const API_BASE = window.location.hostname === 'localhost' ? 'http://localhost:5000' : '';

// Fetch helper with error handling
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API fetch error:', error);
        throw error;
    }
}

// Format risk score
function formatRiskScore(score) {
    if (!score || score === 'N/A') return 'N/A';
    return typeof score === 'number' ? score.toFixed(1) : score;
}

// Get risk level class
function getRiskLevelClass(score) {
    if (!score || score === 'N/A') return 'risk-not-assessed';
    const numScore = typeof score === 'string' ? parseFloat(score) : score;
    if (numScore >= 7) return 'risk-high';
    if (numScore >= 4) return 'risk-medium';
    return 'risk-low';
}

// Show loading state
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="loading"></div>';
    }
}

// Show error message
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<div class="error-message">${message}</div>`;
    }
}

// Export for use in other scripts
window.AppUtils = {
    API_BASE,
    fetchAPI,
    formatRiskScore,
    getRiskLevelClass,
    showLoading,
    showError
};
