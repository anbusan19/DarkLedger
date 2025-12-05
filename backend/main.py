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
from backend.coinbase_client import CoinbaseClient

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


@app.post("/api/payroll/process-and-settle")
async def process_and_settle_endpoint(request: PayrollRequest):
    """
    Process payroll and execute blockchain settlement in one operation.
    
    THE COMPLETE FLOW: This endpoint orchestrates the entire Frankenstein system:
    1. Validates JSON input (automatic via Pydantic)
    2. Processes payroll through COBOL (THE BRAIN does the calculations)
    3. Executes USDC transfers on Base L2 (THE BODY settles on blockchain)
    4. Returns combined payroll and settlement results
    
    This is the ultimate integration of legacy precision with modern settlement speed.
    
    Args:
        request: PayrollRequest containing employees with wallet addresses
        
    Returns:
        dict: Combined response with payroll results and settlement summary
        
    Raises:
        HTTPException 422: Validation error (automatic via Pydantic)
        HTTPException 500: Processing or settlement error
    
    Example:
        POST /api/payroll/process-and-settle
        {
            "employees": [
                {
                    "employee_id": "EMP0001234",
                    "hours_worked": 40.00,
                    "hourly_rate": 25.50,
                    "tax_code": "US",
                    "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
                }
            ]
        }
        
        Response:
        {
            "payroll": {
                "results": [...],
                "summary": {"processed": 1, "errors": 0}
            },
            "settlement": {
                "total_processed": 1,
                "total_succeeded": 1,
                "total_failed": 0,
                "results": [...]
            }
        }
    """
    logger.info(
        f"🧟‍♂️ FRANKENSTEIN AWAKENS: Processing and settling payroll for "
        f"{len(request.employees)} employees"
    )
    
    try:
        # Step 1: Process payroll through COBOL
        # THE BRAIN: COBOL handles all calculations with exact decimal precision
        logger.info("🧠 THE BRAIN: Processing payroll through COBOL...")
        payroll_response = process_payroll(request)
        
        logger.info(
            f"✅ Payroll processing completed: "
            f"{payroll_response.summary['processed']} processed, "
            f"{payroll_response.summary['errors']} errors"
        )
        
        # Step 2: Execute settlement on blockchain
        # THE BODY: Execute USDC transfers on Base L2
        logger.info("💸 THE BODY: Executing blockchain settlement...")
        try:
            client = CoinbaseClient()
            settlement_summary = client.batch_settle(payroll_response)
            
            logger.info(
                f"✅ Settlement completed: "
                f"{settlement_summary['total_succeeded']} succeeded, "
                f"{settlement_summary['total_failed']} failed"
            )
            
        except Exception as e:
            # Settlement error - payroll succeeded but settlement failed
            error_msg = f"Settlement failed after successful payroll processing: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(
                status_code=500,
                detail={
                    "error": error_msg,
                    "error_type": "SettlementError",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "payroll": payroll_response.model_dump()
                }
            )
        
        # Step 3: Return combined response
        combined_response = {
            "payroll": payroll_response.model_dump(),
            "settlement": settlement_summary
        }
        
        logger.info(
            f"🎉 FRANKENSTEIN COMPLETE: Payroll processed and settled successfully"
        )
        
        return combined_response
        
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
        error_msg = f"Unexpected error during process-and-settle: {str(e)}"
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
