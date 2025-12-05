# Product Spec: Ledger-De-Main

## 🎯 Vision
Build a hybrid Payroll System that leverages the decimal precision of COBOL for calculations and the speed of Base (L2) for settlement. The user experience should feel like "Booting up an old mainframe that has connected to the blockchain."

## 👥 User Personas
1.  **The Operator (User):** A startup founder or HR manager. They want the UI to look "Hackerman" cool but need the math to be "CPA" safe.
2.  **The Auditor (Passive):** Requires that all logic impacting money is written in COBOL, not a modern dynamic language.

## 🛠 Core Features

### 1. The Payroll Engine (COBOL)
* **Input:** Employee ID, Hours Worked, Hourly Rate, Tax Code.
* **Process:**
    * Calculate Gross Pay.
    * Calculate Federal Tax (15%).
    * Calculate State Tax (5%).
    * Calculate Net Pay.
* **Output:** A trusted data structure with exact 2-decimal precision.

### 2. The Bridge (Python)
* Must abstract the COBOL complexity away from the Frontend.
* Must validate JSON inputs before converting them to Fixed-Width text for COBOL.
* **Frankenstein Hook:** The Python models must dynamically update if the COBOL structure changes.

### 3. Settlement (Base L2 via Coinbase SDK)
* **Library:** `cdp-sdk` (Coinbase Developer Platform).
* **Asset:** USDC on Base.
* **Logic:**
    1. Receive verified Net Pay from COBOL.
    2. Initialize CDP Wallet.
    3. Execute Transfer (Gasless if possible).
    4. Return Transaction Hash to UI.

### 4. Interface (React)
* **Theme:** "Retro Terminal" / "Cyber-Gothic".
* **Visuals:** Green text, black background, scanlines, CRT flicker effects.
* **Interaction:** Command-line style input (e.g., `> INITIATE_TRANSFER`).