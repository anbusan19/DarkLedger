# Ledger-De-Main 🧟‍♂️💰
> **"The only payroll platform your Accountant AND your Crypto-Bro CTO will agree on."**

![Kiroween Hackathon](https://img.shields.io/badge/Kiroween-Frankenstein_Track-purple)
![Tech Stack](https://img.shields.io/badge/COBOL-Base_L2-blue)

## 💀 The Concept (Frankenstein Category)
Ledger-De-Main is a **chimera**: a monstrous stitching of 1960s mainframe technology with 2025 Web3 settlement.

We use **COBOL** for the math (because floating-point errors in Python/JS are dangerous) and **Base (L2)** for the money (because it's fast and cheap).

## 🩸 The Problem
In JavaScript, Python, and Solidity, `0.1 + 0.2` often equals `0.30000000000000004`.
In a $10M payroll run, those tiny errors add up to lawsuits and tax audits.

## ⚡ The Solution
We refuse to modernize the math. We run the core payroll logic in **COBOL**—the same language that powers 95% of the world's ATM swipes. We then use a **Python Bridge** to "stitch" this legacy brain to the **Coinbase SDK** for instant settlement.

**Audit-proof math. Instant global settlement.**

## 🏗 Architecture
1.  **The Brain (COBOL):** Calculates Gross-to-Net, taxes, and deductions using fixed-point arithmetic.
2.  **The Stitch (Python/FastAPI):** Acts as the nervous system. Uses a custom **Kiro Hook** (`.kiro/hooks/cobol_stitcher.py`) to auto-compile COBOL and update API schemas in real-time.
3.  **The Hands (Base L2):** Uses the **Coinbase CDP SDK** to execute USDC transfers based on the trusted COBOL output.
4.  **The Face (React):** A retro-terminal interface for the user.

## 🚀 Getting Started

### Prerequisites
* `gnucobol` (compiler)
* `python 3.9+`
* `node 18+`
* `coinbase-cdp-sdk` (pip install cdp-sdk)

### Quick Start

**Option 1: Use the startup scripts (Windows)**
```bash
# Terminal 1: Start backend
start_backend.bat

# Terminal 2: Start frontend
start_frontend.bat
```

**Option 2: Manual start**
```bash
# Terminal 1: Start the backend
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Start the frontend
cd frontend
npm install  # First time only
npm run dev
```

Then open http://localhost:5173/ in your browser.

### Using the Terminal Interface

The UI is a retro terminal with green text on black background. Available commands:

* `HELP` - Show all commands
* `RUN <emp_id> <hours> <rate> <tax_code> <wallet>` - Process payroll only
* `SETTLE <emp_id> <hours> <rate> <tax_code> <wallet>` - Process + settle on Base L2
* `BATCH` - Process multiple employees (demo)
* `STATUS` - Show session data
* `CLEAR` - Clear screen

**Example:**
```
> RUN EMP001 40 25.50 US 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2
```

For detailed integration guide, see [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)

## 👻 Kiro Implementation
This project was built using Kiro's **Agentic Workflow**:
* **Vibe Coding:** Used to generate valid COBOL syntax without prior knowledge.
* **Steering:** `.kiro/steering/tech.md` enforces strict separation of "Legacy" vs "Modern" code.
* **Hooks:** Custom hooks handle the compilation and bridging of COBOL to Python automatically on save.

---
*Submitted for the Kiroween Hackathon 2025*