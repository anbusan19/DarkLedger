# Implementation Plan: Settlement Integration

- [x] 1. Set up CDP SDK and project dependencies





  - Add `cdp-sdk` to `requirements.txt`
  - Install CDP SDK: `pip install cdp-sdk`
  - Verify key_manager module exists in backend/
  - _Requirements: 1.1, 1.2_

- [x] 2. Implement CoinbaseClient class structure






  - [x] 2.1 Create coinbase_client.py with class initialization

    - Define `CoinbaseClient` class with `__init__(network: str = "base-sepolia")`
    - Store network as instance variable
    - Initialize wallet as None
    - _Requirements: 1.1, 9.1, 9.2, 9.3_

  - [x] 2.2 Implement SDK configuration method


    - Create `_configure_sdk()` method that imports key_manager
    - Call `key_manager.get_credentials()` to get api_key_name and private_key
    - Call `Cdp.configure(api_key_name, private_key)`
    - Handle ValueError if credentials are missing
    - Log network being used (with warning if mainnet)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 9.4_

- [x] 3. Implement wallet management methods






  - [x] 3.1 Implement wallet creation




    - Create `create_wallet()` method that calls `Wallet.create()`
    - Store wallet in self.wallet
    - Log wallet ID for persistence

    - Return wallet instance
    - _Requirements: 2.2_
  - [x] 3.2 Implement wallet loading by ID





    - Create `load_wallet(wallet_id: str)` method that calls `Wallet.fetch(wallet_id)`

    - Store wallet in self.wallet
    - Return wallet instance
    - _Requirements: 2.3_
  - [x] 3.3 Implement wallet loading from seed

    - Create `load_wallet_from_seed(seed: str)` method that imports wallet from seed
    - Store wallet in self.wallet
    - Return wallet instance
    - _Requirements: 2.4_
  - [x] 3.4 Implement wallet initialization helper










    - Create `_ensure_wallet()` method that checks if self.wallet is None
    - Try loading from PAYROLL_WALLET_ID environment variable
    - Try loading from PAYROLL_WALLET_SEED environment variable
    - Create new wallet if neither is set
    - Log wallet initialization method used
    - _Requirements: 2.2, 2.3, 2.4, 2.5_

- [x] 4. Implement wallet utility methods






  - [x] 4.1 Implement balance checking

    - Create `get_balance(asset: str = "usdc")` method
    - Call `_ensure_wallet()` first
    - Get balance from wallet for specified asset
    - Return balance as Decimal
    - _Requirements: 4.3_

  - [x] 4.2 Implement faucet request for testnet





    - Create `request_faucet(asset: str = "usdc")` method
    - Check if network is "base-sepolia" (raise error if mainnet)
    - Call `_ensure_wallet()` first
    - Call `wallet.faucet(asset).wait()`
    - Log faucet request and wait for completion
    - _Requirements: 4.2, 9.5_

- [x] 5. Implement address validation







  - [x] 5.1 Create address validation method


    - Implement `_is_valid_address(address: str)` method
    - Check address is not empty
    - Use regex pattern `^0x[a-fA-F0-9]{40}$` to validate format
    - Return True if valid, False otherwise
    - _Requirements: 8.4_

- [ ] 6. Implement USDC transfer method








  - [x] 6.1 Create transfer_usdc method

    - Define `transfer_usdc(to_address: str, amount: Decimal, employee_id: str = None)` method
    - Call `_ensure_wallet()` first
    - Validate address using `_is_valid_address()`, raise InvalidAddressError if invalid
    - Validate amount is positive, raise ValueError if not
    - Check balance using `get_balance()`, raise InsufficientFundsError if insufficient
    - Log transfer initiation with employee_id, amount, and address
    - _Requirements: 3.1, 3.2, 7.1, 7.2, 8.4, 8.5_

  - [x] 6.2 Execute transfer and handle confirmation





    - Call `wallet.transfer(amount=float(amount), asset_id="usdc", destination=to_address)`
    - Call `.wait()` on transfer object to wait for confirmation
    - Extract transaction_hash and transaction_link from transfer object
    - Calculate execution duration
    - Log successful transfer with transaction hash and duration

    --_Requirements: 3.3, 3.4, 3.5, 5.1, 5.2, 5.3, 5.4, 5.
5_
  - [x] 6.3 Implement error handling and result formatting








    - Wrap transfer execution in try-except block
    - Catch all exceptions and log error with employee_id context
    - Return dict with transaction_hash, transaction_link, status, timestamp, amount, to_address, employee_id
    - Return status="success" on success, status="failed" with error field on failure
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 7.1, 7.2, 7.3, 7.4, 7.5_
- [x] 7. Implement batch settlement method






- [ ] 7. Implement batch settlement method






-

  - [x] 7.1 Create batch_settle method structure


    - Define `batch_settle(payroll_response: PayrollResponse)` method
    - Initialize results list and counters (succeeded=0, failed=0)
    - Filter payroll_response.results for status="OK" only
    - Log batch settlement start with count of valid results

    - _Requirements: 6.1, 6.2, 6.3, 10.1, 10.2_
  - [x] 7.2 Implement batch processing loop




    - Iterate through filtered valid results
    - For each result, call `transfer_usdc(result.wallet_address, result.net_pay, result.employee_id)`
    - Append settlement result to results list
    - Increment succeeded or failed counter based on status

    - Continue processing even if one transfer fails (error isolation)

    - _Requirements: 6.4, 6.5, 10.2, 10.3, 10.5_
  - [x] 7.3 Return batch settlement summary







    - Build summary dict with total_processed, total_succeeded, total_failed, and results list
    - Log batch settlement completion with success/failure counts
    - Return summary dict
    - _Requirements: 10.3, 10.4_

- [x] 8. Implement custom exception classes








  - [x] 8.1 Create settlement exception hierarchy

    - Define `SettlementError(Exception)` base class
    - Define `InsufficientFundsError(SettlementError)` for low balance
    - Define `InvalidAddressError(SettlementError)` for bad addresses
    - Define `TransactionFailedError(SettlementError)` for blockchain failures
    - _Requirements: 7.1, 7.2, 7.3, 7.4_


- [ ] 9. Implement logging and audit trail
  - [ ] 9.1 Set up logging configuration
    - Import logging module and create logger for "settlement"
    - Configure log format with timestamp, logger name, level, and message
    - Set log level to INFO
    - _Requirements: 5.5, 7.5_
  - [ ] 9.2 Add comprehensive logging throughout
    - Log SDK configuration and network selection
    - Log wallet initialization method
    - Log each transfer initiation and completion
    - Log all errors with full context
    - Log batch settlement start and completion
    - _Requirements: 4.5, 5.5, 7.5, 9.4_

- [ ] 10. Create test scripts and documentation
  - [ ] 10.1 Create testnet setup script
    - Create `backend/setup_testnet_wallet.py` script
    - Initialize CoinbaseClient with base-sepolia
    - Create new wallet and print wallet ID
    - Request faucet funds
    - Check and print balance
    - _Requirements: 4.2, 4.3_
  - [ ] 10.2 Create manual transfer test script
    - Create `backend/test_settlement.py` script
    - Load wallet from environment variable
    - Execute test transfer to a known test address
    - Print transaction hash and link
    - Verify transaction on Basescan
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 5.1, 5.2_
  - [ ] 10.3 Create batch settlement test
    - Create mock PayrollResponse with 3 employees
    - Include valid wallet addresses for testnet
    - Call batch_settle() and print summary
    - Verify all transactions on Basescan
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 11. Integrate with Python Bridge
  - [ ] 11.1 Extend PayrollRequest and PayrollResponse models
    - Add wallet_address field to EmployeePayrollInput in models.py
    - Add wallet_address field to EmployeePayrollOutput in models.py
    - Update example schemas to include wallet addresses
    - _Requirements: 6.1_
  - [ ] 11.2 Create combined payroll and settlement endpoint
    - Add POST /api/payroll/process-and-settle endpoint in main.py
    - Call process_payroll() to get PayrollResponse
    - Initialize CoinbaseClient
    - Call batch_settle() with PayrollResponse
    - Return combined response with payroll and settlement data
    - Handle errors and return appropriate HTTP status codes
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 12. Verify end-to-end settlement flow
  - [ ] 12.1 Test testnet wallet setup
    - Run setup_testnet_wallet.py script
    - Verify wallet is created and funded
    - Save wallet ID to environment variable
    - Confirm balance is sufficient for testing
    - _Requirements: 2.2, 4.2, 4.3_
  - [ ] 12.2 Test single transfer
    - Run test_settlement.py with test address
    - Verify transaction completes successfully
    - Check transaction on Basescan explorer
    - Verify funds received at destination
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 5.1, 5.2, 5.3, 5.4, 5.5_
  - [ ] 12.3 Test batch settlement
    - Create test PayrollRequest with 3 employees and wallet addresses
    - Send POST to /api/payroll/process-and-settle
    - Verify all transfers execute successfully
    - Check all transactions on Basescan
    - Verify settlement summary is accurate
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 10.1, 10.2, 10.3, 10.4, 10.5_
  - [ ] 12.4 Test error handling
    - Test with invalid wallet address (should fail validation)
    - Test with insufficient balance (should fail with InsufficientFundsError)
    - Test with missing credentials (should fail on startup)
    - Verify errors are logged and returned properly
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_
