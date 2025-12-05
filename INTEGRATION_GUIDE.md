# Frontend-Backend Integration Guide

## 🧟‍♂️ The Frankenstein System

This guide explains how to run the complete Ledger-De-Main system with frontend and backend integrated.

## Architecture Overview

```
┌─────────────────┐
│   React UI      │  Terminal interface (Gothic/Retro theme)
│  (Port 5173)    │  
└────────┬────────┘
         │ HTTP/JSON
         ▼
┌─────────────────┐
│  FastAPI        │  REST API + CORS enabled
│  (Port 8000)    │  
└────────┬────────┘
         │ subprocess
         ▼
┌─────────────────┐
│  COBOL Binary   │  Payroll calculations (THE BRAIN)
│  payroll.exe    │  
└────────┬────────┘
         │ Fixed-width files
         ▼
┌─────────────────┐
│  Coinbase SDK   │  USDC settlement on Base L2
│  (cdp-sdk)      │  
└─────────────────┘
```

## Prerequisites

1. **Python 3.9+** with dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **Node.js 18+** with npm

3. **COBOL Compiler** (GnuCOBOL) - Already compiled binary should exist

4. **Coinbase API Keys** (for settlement):
   - Set `COINBASE_API_KEY_NAME` environment variable
   - Set `COINBASE_PRIVATE_KEY` environment variable

## Quick Start

### Step 1: Compile COBOL (if needed)

```bash
cd cobol
compile.bat
```

This creates `cobol/bin/payroll.exe`

### Step 2: Start Backend

```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Ledger-De-Main API initialized successfully
```

### Step 3: Test Backend (Optional)

In a new terminal:
```bash
python test_frontend_integration.py
```

### Step 4: Start Frontend

In a new terminal:
```bash
cd frontend
npm install  # First time only
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:5173/
```

### Step 5: Open Browser

Navigate to: http://localhost:5173/

You should see the terminal interface with green text on black background.

## Using the Terminal

### Available Commands

1. **HELP** - Show all commands
   ```
   > HELP
   ```

2. **RUN** - Process payroll only (no settlement)
   ```
   > RUN EMP001 40 25.50 US 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2
   ```
   
   Format: `RUN <emp_id> <hours> <rate> <tax_code> <wallet>`

3. **SETTLE** - Process payroll AND execute blockchain settlement
   ```
   > SETTLE EMP001 40 25.50 US 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2
   ```
   
   Format: `SETTLE <emp_id> <hours> <rate> <tax_code> <wallet>`

4. **BATCH** - Process multiple employees (demo data)
   ```
   > BATCH
   ```

5. **STATUS** - Show current session data
   ```
   > STATUS
   ```

6. **CLEAR** - Clear terminal screen
   ```
   > CLEAR
   ```

## API Endpoints

The backend exposes these endpoints:

### Health Check
```
GET /health
```

### Process Payroll Only
```
POST /api/payroll/process
Content-Type: application/json

{
  "employees": [
    {
      "employee_id": "EMP001",
      "hours_worked": "40.00",
      "hourly_rate": "25.50",
      "tax_code": "US",
      "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2"
    }
  ]
}
```

### Process and Settle
```
POST /api/payroll/process-and-settle
Content-Type: application/json

{
  "employees": [
    {
      "employee_id": "EMP001",
      "hours_worked": "40.00",
      "hourly_rate": "25.50",
      "tax_code": "US",
      "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2"
    }
  ]
}
```

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000` (React dev server)
- `http://localhost:5173` (Vite dev server)

If you need to add more origins, edit `backend/main.py`:

```python
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://your-custom-origin:port"
]
```

## Troubleshooting

### Backend won't start
- Check if port 8000 is already in use
- Verify Python dependencies are installed: `pip install -r requirements.txt`
- Check COBOL binary exists: `cobol/bin/payroll.exe`

### Frontend won't connect to backend
- Verify backend is running on http://127.0.0.1:8000
- Check browser console for CORS errors
- Verify API_BASE in `frontend/src/services/api.js` matches backend URL

### COBOL errors
- Recompile: `cd cobol && compile.bat`
- Check `data/input.dat` and `data/output.rpt` permissions
- Verify COBOL binary path in `backend/bridge.py`

### Settlement errors
- Verify Coinbase API keys are set as environment variables
- Check network (Base Sepolia for testnet)
- Ensure wallet has sufficient USDC balance

## Development Tips

### Hot Reload
Both frontend and backend support hot reload:
- **Backend**: Uses `--reload` flag with uvicorn
- **Frontend**: Vite automatically reloads on file changes

### Viewing Logs
- **Backend**: Logs appear in the terminal running uvicorn
- **Frontend**: Check browser console (F12)

### Testing API Directly
Use the interactive docs at http://127.0.0.1:8000/docs

## Production Deployment

For production:

1. Build frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. Serve static files from `frontend/dist/`

3. Run backend with production ASGI server:
   ```bash
   gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

4. Use environment variables for configuration
5. Enable HTTPS
6. Configure proper CORS origins
7. Set up monitoring and logging

## The Aesthetic

The UI follows "The Laws of the Chimera":
- **Colors**: Black background (#000000), Terminal Green (#00ff00), Error Red (#ff0000)
- **Font**: Monospace (Courier New)
- **Effects**: CRT scanlines, glitch animations, flicker
- **Style**: No rounded corners, sharp edges, retro-tech vibe

This is THE FRANKENSTEIN - where 1960s COBOL precision meets 2024 blockchain speed. 🧟‍♂️
