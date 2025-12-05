# Design Document: Python Bridge

## Overview

The Python Bridge is a FastAPI-based REST API that serves as the integration layer between the React frontend and the COBOL Payroll Engine. It handles bidirectional data transformation (JSON ↔ Fixed-Width), subprocess management for COBOL execution, and secure credential management for blockchain settlement.

The design follows a modular architecture with clear separation of concerns: API routing, data validation, format conversion, subprocess execution, and configuration management. This approach ensures maintainability, testability, and adherence to the "Frankenstein" philosophy where Python acts as the nervous system connecting the legacy brain (COBOL) to the modern face (React).

## Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/JSON
                     ↓
┌─────────────────────────────────────────────────────────┐
│                  Python Bridge (FastAPI)                 │
│  ┌──────────────────────────────────────────────────┐  │
│  │  main.py (API Routes & CORS)                     │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                        │
│  ┌──────────────↓───────────────────────────────────┐  │
│  │  models.py (Pydantic Validation)                 │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                        │
│  ┌──────────────↓───────────────────────────────────┐  │
│  │  bridge.py (Format Conversion & COBOL Execution) │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                        │
│  ┌──────────────↓───────────────────────────────────┐  │
│  │  key_manager.py (Credential Loading)             │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────┘
                      │ Subprocess
                      ↓
┌─────────────────────────────────────────────────────────┐
│              COBOL Payroll Engine (Binary)               │
└─────────────────────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────┐
│              File System (data/*.dat, *.rpt)             │
└─────────────────────────────────────────────────────────┘
```

### Request Flow

```
1. Frontend sends POST /api/payroll/process with JSON
   ↓
2. FastAPI validates request against Pydantic model
   ↓
3. bridge.py converts JSON to fixed-width format
   ↓
4. bridge.py writes data/input.dat
   ↓
5. bridge.py executes cobol/bin/payroll via subprocess
   ↓
6. COBOL reads input.dat, processes, writes output.rpt
   ↓
7. bridge.py reads data/output.rpt
   ↓
8. bridge.py parses fixed-width to Python dict
   ↓
9. FastAPI serializes response to JSON
   ↓
10. Frontend receives JSON response
```

## Components and Interfaces

### 1. main.py - API Entry Point

**Responsibilities:**
- Initialize FastAPI application
- Configure CORS middleware
- Define API routes
- Handle HTTP request/response lifecycle
- Serve OpenAPI documentation

**Key Endpoints:**

```python
POST /api/payroll/process
- Request Body: PayrollRequest (JSON)
- Response: PayrollResponse (JSON)
- Status Codes: 200 (success), 422 (validation error), 500 (processing error)

GET /docs
- Interactive Swagger UI documentation

GET /health
- Health check endpoint
- Returns: {"status": "healthy"}
```

**CORS Configuration:**
```python
origins = [
    "http://localhost:3000",  # React dev server
    "http://localhost:5173",  # Vite dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. models.py - Data Validation

**Responsibilities:**
- Define Pydantic models for request/response
- Validate input data types and constraints
- Provide automatic JSON serialization/deserialization
- Generate OpenAPI schema

**Data Models:**

```python
class EmployeePayrollInput(BaseModel):
    """Single employee payroll input"""
    employee_id: str = Field(..., min_length=1, max_length=10)
    hours_worked: Decimal = Field(..., gt=0, max_digits=5, decimal_places=2)
    hourly_rate: Decimal = Field(..., gt=0, max_digits=6, decimal_places=2)
    tax_code: str = Field(default="US", min_length=2, max_length=2)
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP0001234",
                "hours_worked": 40.00,
                "hourly_rate": 25.50,
                "tax_code": "US"
            }
        }

class PayrollRequest(BaseModel):
    """Request body for payroll processing"""
    employees: List[EmployeePayrollInput] = Field(..., min_items=1)

class EmployeePayrollOutput(BaseModel):
    """Single employee payroll output"""
    employee_id: str
    gross_pay: Decimal
    federal_tax: Decimal
    state_tax: Decimal
    net_pay: Decimal
    status: str  # "OK" or "ER"

class PayrollResponse(BaseModel):
    """Response body for payroll processing"""
    results: List[EmployeePayrollOutput]
    summary: dict  # {"processed": int, "errors": int}
```

### 3. bridge.py - Format Conversion & Execution

**Responsibilities:**
- Convert JSON to fixed-width format
- Write input.dat file
- Execute COBOL binary via subprocess
- Read output.rpt file
- Parse fixed-width to Python dict
- Handle file I/O errors
- Log execution details

**Key Functions:**

```python
def json_to_fixed_width(employee: EmployeePayrollInput) -> str:
    """
    Convert JSON employee data to 23-byte fixed-width record.
    
    Format:
    - Employee ID: positions 1-10 (left-aligned, space-padded)
    - Hours Worked: positions 11-15 (99999, implied 2 decimals)
    - Hourly Rate: positions 16-21 (999999, implied 2 decimals)
    - Tax Code: positions 22-23 (left-aligned)
    
    Example:
    Input: {"employee_id": "EMP001", "hours_worked": 40.00, ...}
    Output: "EMP001    0400002550US"
    """
    pass

def write_input_file(employees: List[EmployeePayrollInput]) -> None:
    """
    Write all employee records to data/input.dat.
    Each record is 23 bytes + newline.
    """
    pass

def execute_cobol() -> subprocess.CompletedProcess:
    """
    Execute the COBOL binary with timeout and error handling.
    
    Returns CompletedProcess with stdout, stderr, and returncode.
    Raises subprocess.TimeoutExpired if execution exceeds 30 seconds.
    Raises FileNotFoundError if binary doesn't exist.
    """
    pass

def read_output_file() -> List[str]:
    """
    Read all lines from data/output.rpt.
    Returns list of lines (excluding summary line).
    """
    pass

def parse_output_line(line: str) -> dict:
    """
    Parse a 60-byte fixed-width output record.
    
    Format:
    - Employee ID: positions 1-10
    - Gross Pay: positions 11-22 (99999999V99)
    - Federal Tax: positions 23-34 (99999999V99)
    - State Tax: positions 35-46 (99999999V99)
    - Net Pay: positions 47-58 (99999999V99)
    - Status: positions 59-60 ("OK" or "ER")
    
    Returns dict with parsed values as Decimal types.
    """
    pass

def parse_summary_line(line: str) -> dict:
    """
    Parse summary line: "SUMMARY: PROCESSED=nnnnn ERRORS=nnnnn"
    Returns: {"processed": int, "errors": int}
    """
    pass

def process_payroll(request: PayrollRequest) -> PayrollResponse:
    """
    Main orchestration function.
    
    Steps:
    1. Convert JSON to fixed-width
    2. Write input.dat
    3. Execute COBOL binary
    4. Read output.rpt
    5. Parse results
    6. Return PayrollResponse
    
    Handles all errors and logs execution details.
    """
    pass
```

### 4. key_manager.py - Credential Management

**Responsibilities:**
- Load Coinbase API credentials from environment
- Validate credential presence
- Provide secure access to credentials
- Raise errors for missing configuration

**Implementation:**

```python
import os
from typing import Tuple

class KeyManager:
    """Manages secure loading of Coinbase API credentials."""
    
    def __init__(self):
        self.api_key_name = os.getenv("COINBASE_API_KEY_NAME")
        self.private_key = os.getenv("COINBASE_PRIVATE_KEY")
        
        if not self.api_key_name or not self.private_key:
            raise ValueError(
                "Missing required environment variables: "
                "COINBASE_API_KEY_NAME and COINBASE_PRIVATE_KEY"
            )
    
    def get_credentials(self) -> Tuple[str, str]:
        """Returns (api_key_name, private_key)"""
        return self.api_key_name, self.private_key
    
    def __repr__(self):
        """Never expose credentials in logs"""
        return f"KeyManager(api_key_name={'***' if self.api_key_name else None})"

# Singleton instance
key_manager = KeyManager()
```

## Data Models

### Fixed-Width Format Specifications

**Input Record (23 bytes):**
```
Position  Length  Field           Format      Example
1-10      10      Employee ID     X(10)       "EMP0001234"
11-15     5       Hours Worked    999V99      "04000" (40.00)
16-21     6       Hourly Rate     9999V99     "002550" (25.50)
22-23     2       Tax Code        XX          "US"
```

**Output Record (60 bytes):**
```
Position  Length  Field           Format          Example
1-10      10      Employee ID     X(10)           "EMP0001234"
11-22     12      Gross Pay       9(8)V99         "000001020.00"
23-34     12      Federal Tax     9(8)V99         "000000153.00"
35-46     12      State Tax       9(8)V99         "000000051.00"
47-58     12      Net Pay         9(8)V99         "000000816.00"
59-60     2       Status          XX              "OK"
```

### Decimal Precision Handling

Python's `Decimal` type is used throughout to maintain precision:

```python
from decimal import Decimal, ROUND_HALF_EVEN

# Configure decimal context
getcontext().prec = 10
getcontext().rounding = ROUND_HALF_EVEN

# Example conversion
hours = Decimal("40.00")
rate = Decimal("25.50")
gross = (hours * rate).quantize(Decimal("0.01"))
```

## Error Handling

### Error Categories

1. **Validation Errors (HTTP 422)**
   - Invalid employee ID format
   - Negative or zero hours/rate
   - Missing required fields
   - Handled automatically by Pydantic

2. **File I/O Errors (HTTP 500)**
   - Cannot write input.dat
   - Cannot read output.rpt
   - Insufficient permissions

3. **Subprocess Errors (HTTP 500)**
   - COBOL binary not found
   - Execution timeout (>30s)
   - Non-zero exit code

4. **Parsing Errors (HTTP 500)**
   - Malformed output.rpt
   - Unexpected line length
   - Invalid numeric values

5. **Configuration Errors (Startup)**
   - Missing environment variables
   - Invalid COBOL binary path

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong",
  "error_type": "ValidationError|FileIOError|SubprocessError|ParsingError",
  "timestamp": "2025-12-05T10:30:00Z"
}
```

### Logging Strategy

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("payroll_bridge")

# Log levels:
# DEBUG: Detailed execution flow
# INFO: Normal operations (file writes, subprocess calls)
# WARNING: Recoverable issues
# ERROR: Processing failures
# CRITICAL: Configuration errors
```

## Testing Strategy

### Unit Tests

1. **Format Conversion Tests**
   - Test `json_to_fixed_width()` with various inputs
   - Verify correct padding and alignment
   - Test decimal precision handling

2. **Parsing Tests**
   - Test `parse_output_line()` with valid records
   - Test error handling for malformed lines
   - Test summary line parsing

3. **Validation Tests**
   - Test Pydantic model validation
   - Test boundary conditions (min/max values)
   - Test required field enforcement

### Integration Tests

4. **End-to-End Processing**
   - Mock COBOL execution with pre-generated output.rpt
   - Verify complete request → response flow
   - Test error propagation

5. **File I/O Tests**
   - Test file creation and cleanup
   - Test handling of missing directories
   - Test concurrent access scenarios

### API Tests

6. **Endpoint Tests**
   - Test POST /api/payroll/process with valid data
   - Test error responses (422, 500)
   - Test CORS headers
   - Test OpenAPI documentation generation

## Performance Considerations

### Throughput

- Target: Process 100 employees per request
- Expected latency: < 2 seconds for 100 employees
- COBOL execution: ~500ms for 100 records
- File I/O overhead: ~100ms
- JSON serialization: ~50ms

### Optimization Strategies

1. **Batch Processing**
   - Process multiple employees in single COBOL execution
   - Minimize subprocess overhead

2. **File Buffering**
   - Use buffered I/O for large batches
   - Write input.dat in single operation

3. **Async Considerations**
   - Current design is synchronous (COBOL is blocking)
   - Future: Use asyncio for concurrent requests
   - Use background tasks for long-running batches

### Resource Management

```python
# Ensure files are cleaned up
try:
    write_input_file(employees)
    result = execute_cobol()
    output = read_output_file()
finally:
    # Optional: Clean up input.dat after processing
    if os.path.exists("data/input.dat"):
        os.remove("data/input.dat")
```

## Security Considerations

### Input Sanitization

- Pydantic validates all inputs before processing
- No shell injection risk (subprocess uses list args, not shell=True)
- Employee ID limited to 10 characters (prevents buffer overflow in COBOL)

### Credential Security

- Never log API keys or private keys
- Load from environment variables only
- Use key_manager module for centralized access
- Validate credentials on startup (fail fast)

### File System Security

- Restrict file permissions on data/ directory
- Validate file paths to prevent directory traversal
- Use absolute paths for COBOL binary

### API Security

- Enable CORS only for trusted origins
- Consider adding API key authentication (future)
- Rate limiting for production deployment (future)

## Deployment

### Dependencies

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
```

### Environment Variables

```bash
# Required for Coinbase integration
export COINBASE_API_KEY_NAME="your-api-key-name"
export COINBASE_PRIVATE_KEY="your-private-key"

# Optional configuration
export COBOL_BINARY_PATH="cobol/bin/payroll"
export DATA_DIR="data"
export LOG_LEVEL="INFO"
```

### Running the Server

```bash
# Development
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Health Checks

```bash
# Check API is running
curl http://localhost:8000/health

# Check OpenAPI docs
curl http://localhost:8000/docs
```

## Integration Points

### Frontend Integration

The React frontend will call the API using fetch or axios:

```javascript
// frontend/src/services/api.js
async function processPayroll(employees) {
  const response = await fetch('http://localhost:8000/api/payroll/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ employees })
  });
  
  if (!response.ok) {
    throw new Error(`Payroll processing failed: ${response.statusText}`);
  }
  
  return await response.json();
}
```

### COBOL Integration

The bridge assumes the COBOL binary:
- Exists at `cobol/bin/payroll`
- Reads from `data/input.dat`
- Writes to `data/output.rpt`
- Exits with code 0 on success

### Coinbase SDK Integration

The key_manager provides credentials for future Coinbase integration:

```python
from backend.key_manager import key_manager
from cdp import Cdp

# Initialize CDP SDK
api_key_name, private_key = key_manager.get_credentials()
Cdp.configure(api_key_name, private_key)
```

## Future Enhancements

### Async Processing

Convert to async/await for better concurrency:

```python
@app.post("/api/payroll/process")
async def process_payroll_async(request: PayrollRequest):
    # Use asyncio.create_subprocess_exec for non-blocking COBOL execution
    pass
```

### Batch Job Queue

For large payroll runs, use background task queue:

```python
from fastapi import BackgroundTasks

@app.post("/api/payroll/batch")
async def process_payroll_batch(request: PayrollRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_large_batch, request)
    return {"job_id": "...", "status": "queued"}
```

### Caching

Cache COBOL results for idempotent requests:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_result(request_hash: str):
    pass
```

### Monitoring

Add metrics and tracing:

```python
from prometheus_client import Counter, Histogram

payroll_requests = Counter('payroll_requests_total', 'Total payroll requests')
payroll_duration = Histogram('payroll_duration_seconds', 'Payroll processing duration')
```
