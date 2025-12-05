# Ledger-De-Main Terminal UI

Retro-terminal interface with cyber-gothic aesthetic for the COBOL payroll settlement system.

## Setup

```bash
npm install
npm run dev
```

## Commands

- `HELP` - Show available commands
- `CALCULATE <emp_id> <hours> <rate> <tax_code>` - Execute COBOL payroll calculation
- `INITIATE_TRANSFER <emp_id> <address>` - Send USDC on Base L2
- `STATUS` - Show current session data
- `CLEAR` - Clear terminal

## Design Rules

- No rounded corners (rounded-none)
- Monospace font only
- Colors: Black (#000000), Terminal Green (#00ff00), Error Red (#ff0000)
- Glitch effects for loading states
- CRT scanline and flicker animations
