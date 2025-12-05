"""
Pydantic models for payroll API request/response validation.
These models define the JSON schema for the REST API.
"""

from decimal import Decimal
from typing import List
from pydantic import BaseModel, Field


class EmployeePayrollInput(BaseModel):
    """Single employee payroll input for processing."""
    
    employee_id: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Unique employee identifier (max 10 characters)"
    )
    hours_worked: Decimal = Field(
        ...,
        gt=0,
        max_digits=5,
        decimal_places=2,
        description="Hours worked in the pay period (must be positive)"
    )
    hourly_rate: Decimal = Field(
        ...,
        gt=0,
        max_digits=6,
        decimal_places=2,
        description="Hourly rate in dollars (must be positive)"
    )
    tax_code: str = Field(
        default="US",
        min_length=2,
        max_length=2,
        description="Two-character tax jurisdiction code"
    )
    wallet_address: str = Field(
        ...,
        min_length=42,
        max_length=42,
        description="Ethereum wallet address for settlement (0x + 40 hex chars)"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "employee_id": "EMP0001234",
                    "hours_worked": 40.00,
                    "hourly_rate": 25.50,
                    "tax_code": "US",
                    "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
                }
            ]
        }
    }


class PayrollRequest(BaseModel):
    """Request body for payroll processing endpoint."""
    
    employees: List[EmployeePayrollInput] = Field(
        ...,
        min_length=1,
        description="List of employees to process (minimum 1 required)"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "employees": [
                        {
                            "employee_id": "EMP0001234",
                            "hours_worked": 40.00,
                            "hourly_rate": 25.50,
                            "tax_code": "US",
                            "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
                        },
                        {
                            "employee_id": "EMP0005678",
                            "hours_worked": 35.50,
                            "hourly_rate": 30.00,
                            "tax_code": "US",
                            "wallet_address": "0x8B3a3b8e9c7d6f5e4d3c2b1a0987654321fedcba"
                        }
                    ]
                }
            ]
        }
    }


class EmployeePayrollOutput(BaseModel):
    """Single employee payroll output after COBOL processing."""
    
    employee_id: str = Field(
        ...,
        description="Employee identifier from input"
    )
    gross_pay: Decimal = Field(
        ...,
        decimal_places=2,
        description="Total pay before taxes"
    )
    federal_tax: Decimal = Field(
        ...,
        decimal_places=2,
        description="Federal tax withheld (15%)"
    )
    state_tax: Decimal = Field(
        ...,
        decimal_places=2,
        description="State tax withheld (5%)"
    )
    net_pay: Decimal = Field(
        ...,
        decimal_places=2,
        description="Final pay after all deductions"
    )
    status: str = Field(
        ...,
        description="Processing status: 'OK' for success, 'ER' for error"
    )
    wallet_address: str = Field(
        ...,
        description="Ethereum wallet address for settlement"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "employee_id": "EMP0001234",
                    "gross_pay": 1020.00,
                    "federal_tax": 153.00,
                    "state_tax": 51.00,
                    "net_pay": 816.00,
                    "status": "OK",
                    "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
                }
            ]
        }
    }


class PayrollResponse(BaseModel):
    """Response body for payroll processing endpoint."""
    
    results: List[EmployeePayrollOutput] = Field(
        ...,
        description="List of processed employee payroll results"
    )
    summary: dict = Field(
        ...,
        description="Processing summary with counts"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "results": [
                        {
                            "employee_id": "EMP0001234",
                            "gross_pay": 1020.00,
                            "federal_tax": 153.00,
                            "state_tax": 51.00,
                            "net_pay": 816.00,
                            "status": "OK",
                            "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
                        }
                    ],
                    "summary": {
                        "processed": 1,
                        "errors": 0
                    }
                }
            ]
        }
    }
