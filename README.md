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

### Usage
1.  **Start the Brain:** `uvicorn backend.main:app --reload`
2.  **Start the Face:** `npm start`
3.  **Run Payroll:**
    * Navigate to the terminal UI.
    * Type: `RUN PAYROLL --BATCH 2025-10-31`
    * Watch the ghost in the machine work.

## 👻 Kiro Implementation
This project was built using Kiro's **Agentic Workflow**:
* **Vibe Coding:** Used to generate valid COBOL syntax without prior knowledge.
* **Steering:** `.kiro/steering/tech.md` enforces strict separation of "Legacy" vs "Modern" code.
* **Hooks:** Custom hooks handle the compilation and bridging of COBOL to Python automatically on save.

---
*Submitted for the Kiroween Hackathon 2025*