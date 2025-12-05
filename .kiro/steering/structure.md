# Directory Structure

/
├── .kiro/
│   ├── hooks/
│   │   └── cobol_stitcher.py  # The "Frankenstein" Hook
│   ├── steering/
│   │   └── tech.md            # The "Rules of the Monster"
│   └── specs/
│       └── product.md
│
├── cobol/                     # THE BRAIN (Legacy)
│   ├── payroll.cbl            # Main logic file
│   └── bin/                   # Compiled binaries (gitignored)
│
├── backend/                   # THE BODY (Python/FastAPI)
│   ├── main.py                # API Entry point
│   ├── bridge.py              # Handles subprocess calls to COBOL
│   ├── models.py              # Pydantic models (Auto-updated by Hook)
│   ├── coinbase_client.py     # Base L2 Integration (CDP SDK)
│   └── key_manager.py         # Loads CDP API Key Name/Private Key
│
├── frontend/                  # THE FACE (React + Tailwind)
│   ├── src/
│   │   ├── components/
│   │   │   └── Terminal.jsx   # Main UI component
│   │   └── services/
│   │       └── api.js
│   └── public/
│
├── data/                      # SHARED STATE
│   ├── input.dat              # Python writes here -> COBOL reads
│   └── output.rpt             # COBOL writes here -> Python reads
│
└── README.md