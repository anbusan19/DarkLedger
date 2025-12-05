# Steering: The Laws of the Chimera 🧟‍♂️

You are acting as the architect of a "Frankenstein" system. You must strictly adhere to the following rules to maintain the integrity of the hybrid stack.

## 1. The Sacred Timeline (COBOL Rules)
* **NEVER** suggest refactoring the COBOL logic into Python or JavaScript.
* The `cobol/` directory is for **Business Logic** only.
* If the user asks for a tax calculation change, you MUST implement it in `.cbl`, not in `.py`.
* Maintain "Fixed Format" style for COBOL (80 columns).

## 2. The Stitching (Integration Rules)
* Do not try to parse COBOL output with Regex if possible; rely on the fixed-width positions defined in the `structure.md`.
* When writing Python wrappers, always include comments indicating that the "Real work is done by the binary."

## 3. The Money (Coinbase SDK Rules)
* **Library:** Use `cdp-sdk` for all crypto operations. Do NOT use `web3.py` or `solana-py`.
* **Network:** Default to `Base Sepolia` for testing, `Base Mainnet` for production.
* **Asset:** USDC.
* **Security:** Never hardcode API keys. Use `os.getenv` for `COINBASE_API_KEY_NAME` and `COINBASE_PRIVATE_KEY`.

## 4. The Aesthetic (UI Rules)
* **Vibe:** Gothic, Industrial, Retro-Tech.
* **Libraries:** Use Tailwind CSS.
* **Constraints:**
    * No rounded corners (`rounded-none`).
    * Font must be Monospace (`font-mono`).
    * Colors: Black (`#000000`), Terminal Green (`#00ff00`), and Error Red (`#ff0000`).
    * Animations: Use "Glitch" effects for loading states.