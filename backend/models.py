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
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "employee_id": "EMP0001234",
                    "hours_worked": 40.00,
                    "hourly_rate": 25.50,
                    "tax_code": "US"
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
                            "tax_code": "US"
                        },
                        {
                            "employee_id": "EMP0005678",
                            "hours_worked": 35.50,
                            "hourly_rate": 30.00,
                            "tax_code": "US"
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
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "employee_id": "EMP0001234",
                    "gross_pay": 1020.00,
                    "federal_tax": 153.00,
                    "state_tax": 51.00,
                    "net_pay": 816.00,
                    "status": "OK"
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
                            "status": "OK"
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
