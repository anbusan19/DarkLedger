"""
Ledger-De-Main API - FastAPI Entry Point

THE FACE: This is the modern REST API that fronts the legacy COBOL brain.
Real work is done by the COBOL binary - this just provides a clean HTTP interface.
"""

import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import PayrollRequest, PayrollResponse
from backend.bridge import process_payroll

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("payroll_api")

# Initialize FastAPI application
app = FastAPI(
    title="Ledger-De-Main API",
    version="1.0.0",
    description="Hybrid Payroll System: COBOL precision meets blockchain settlement",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware for frontend integration
# Allow React dev server (port 3000) and Vite dev server (port 5173)
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

logger.info("Ledger-De-Main API initialized successfully")


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns a simple status indicator to verify the API is running.
    Useful for monitoring, load balancers, and deployment verification.
    
    Returns:
        dict: Status indicator with "healthy" value
    """
    return {"status": "healthy"}


@app.post("/api/payroll/process", response_model=PayrollResponse)
async def process_payroll_endpoint(request: PayrollRequest):
    """
    Process payroll for a batch of employees.
    
    THE STITCHING: This endpoint orchestrates the entire payroll flow:
    1. Validates JSON input (automatic via Pydantic)
    2. Converts to fixed-width format
    3. Invokes COBOL binary (where the real work happens)
    4. Parses results back to JSON
    5. Returns structured response
    
    The COBOL engine performs all calculations with exact decimal precision.
    This endpoint just handles the translation between modern JSON and legacy formats.
    
    Args:
        request: PayrollRequest containing list of employees to process
        
    Returns:
        PayrollResponse: Processed payroll results with summary statistics
        
    Raises:
        HTTPException 422: Validation error (automatic via Pydantic)
        HTTPException 500: Processing error (file I/O, COBOL execution, parsing)
    
    Example:
        POST /api/payroll/process
        {
            "employees": [
                {
                    "employee_id": "EMP0001234",
                    "hours_worked": 40.00,
                    "hourly_rate": 25.50,
                    "tax_code": "US"
                }
            ]
        }
        
        Response:
        {
            "results": [
                {
                    "employee_id": "EMP0001234",
                    "gross_pay": 1020.00,
                    "federal_tax": 153.00,
                    "state_tax": 51.00,
                    "net_pay": 816.00,
                    "status": "OK"
                }
            ],
            "summary": {
                "processed": 1,
                "errors": 0
            }
        }
    """
    logger.info(f"Received payroll processing request for {len(request.employees)} employees")
    
    try:
        # Call the bridge module to process payroll
        # THE BRAIN DOES THE WORK: COBOL handles all calculations
        response = process_payroll(request)
        
        logger.info(
            f"Payroll processing completed: "
            f"{response.summary['processed']} processed, "
            f"{response.summary['errors']} errors"
        )
        
        return response
        
    except FileNotFoundError as e:
        # COBOL binary or output file not found
        error_msg = f"COBOL binary or required files not found: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail={
                "error": error_msg,
                "error_type": "FileNotFoundError",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
    
    except IOError as e:
        # File I/O error (input.dat write or output.rpt read)
        error_msg = f"File I/O error during payroll processing: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail={
                "error": error_msg,
                "error_type": "FileIOError",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
    
    except ValueError as e:
        # Parsing error (malformed output.rpt)
        error_msg = f"Failed to parse COBOL output: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail={
                "error": error_msg,
                "error_type": "ParsingError",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
    
    except Exception as e:
        # Catch-all for unexpected errors
        error_msg = f"Unexpected error during payroll processing: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail={
                "error": error_msg,
                "error_type": "UnexpectedError",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    logger.info("=" * 60)
    logger.info("Ledger-De-Main API Starting Up")
    logger.info("THE FRANKENSTEIN AWAKENS: Connecting COBOL brain to REST API")
    logger.info("=" * 60)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information."""
    logger.info("Ledger-De-Main API shutting down")
