// API Service Layer
// Real work is done by the backend (Python + COBOL binary)

// Use environment variable if provided, otherwise:
// - In development: use localhost
// - In production (served from same domain): use relative URLs (empty string)
const API_BASE = import.meta.env.VITE_API_BASE_URL !== undefined 
    ? import.meta.env.VITE_API_BASE_URL
    : (import.meta.env.DEV ? 'http://127.0.0.1:8000' : '');

export const api = {
  /**
   * Process payroll using COBOL engine (batch)
   * @param {Array} employees - Array of { employee_id, hours_worked, hourly_rate, tax_code, wallet_address }
   * @returns {Promise<Object>} Payroll results from COBOL
   */
  async processPayroll(employees) {
    const response = await fetch(`${API_BASE}/api/payroll/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ employees })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Payroll processing failed');
    }
    
    return response.json();
  },

  /**
   * Process payroll AND execute settlement (combined)
   * @param {Array} employees - Array of { employee_id, hours_worked, hourly_rate, tax_code, wallet_address }
   * @returns {Promise<Object>} Combined payroll and settlement results
   */
  async processAndSettle(employees) {
    const response = await fetch(`${API_BASE}/api/payroll/process-and-settle`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ employees })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Process and settle failed');
    }
    
    return response.json();
  },

  /**
   * Health check
   */
  async ping() {
    const response = await fetch(`${API_BASE}/health`);
    return response.json();
  }
};
