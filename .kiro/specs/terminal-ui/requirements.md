# Requirements Document

## Introduction

The Terminal UI is the face of Ledger-De-Main—a retro-futuristic interface that makes payroll processing feel like hacking into a 1970s mainframe that somehow got connected to Web3. This component provides the user experience layer where operators input employee data, trigger payroll calculations, and watch USDC settlements happen in real-time. The aesthetic is deliberately anachronistic: terminal green on black, monospace fonts, CRT scanlines, and glitch effects that make you feel like you're operating forbidden technology.

## Glossary

- **Terminal UI**: The React-based frontend interface styled as a retro computer terminal
- **Command Input**: Text input field where users type commands to interact with the system
- **Output Display**: Scrolling text area that shows system responses and processing logs
- **Scanlines**: Visual effect simulating CRT monitor horizontal lines
- **Glitch Effect**: CSS animation that creates digital distortion during loading states
- **Terminal Green**: The signature color (#00ff00) used for text and UI elements
- **Monospace Font**: Fixed-width font (font-mono) required for authentic terminal aesthetic
- **Boot Sequence**: Animated startup sequence that displays system initialization messages
- **Command Parser**: Logic that interprets user commands and triggers appropriate actions
- **Payroll Session**: Active state where employee data is being entered and processed

## Requirements

### Requirement 1

**User Story:** As an Operator, I want a terminal-style interface with gothic aesthetics, so that the system feels like authentic retro-tech.

#### Acceptance Criteria

1. THE Terminal UI SHALL use a black background (#000000) for all main interface areas
2. THE Terminal UI SHALL use terminal green (#00ff00) for all primary text and UI elements
3. THE Terminal UI SHALL use error red (#ff0000) for error messages and warnings
4. THE Terminal UI SHALL use monospace font (font-mono) for all text
5. THE Terminal UI SHALL apply rounded-none class to all elements (no rounded corners)

### Requirement 2

**User Story:** As an Operator, I want CRT-style visual effects, so that the interface feels like an old mainframe terminal.

#### Acceptance Criteria

1. THE Terminal UI SHALL display horizontal scanlines across the entire interface
2. THE Terminal UI SHALL apply a subtle screen flicker animation
3. THE Terminal UI SHALL show a CRT screen curvature effect (optional vignette)
4. THE Terminal UI SHALL use glitch animations during loading states
5. THE Terminal UI SHALL maintain 60fps performance despite visual effects

### Requirement 3

**User Story:** As an Operator, I want a boot sequence when the app loads, so that it feels like powering up a mainframe.

#### Acceptance Criteria

1. WHEN the application starts, THE Terminal UI SHALL display a boot sequence animation
2. THE Terminal UI SHALL show system initialization messages line-by-line
3. THE Terminal UI SHALL display ASCII art logo for Ledger-De-Main
4. THE Terminal UI SHALL show "SYSTEM READY" message when boot completes
5. THE Terminal UI SHALL complete boot sequence within 3 seconds

### Requirement 4

**User Story:** As an Operator, I want to enter commands via a terminal prompt, so that I can interact with the system naturally.

#### Acceptance Criteria

1. THE Terminal UI SHALL display a command prompt with format "> " at the bottom of the screen
2. THE Terminal UI SHALL accept text input for commands
3. THE Terminal UI SHALL display entered commands in the output display
4. THE Terminal UI SHALL support command history navigation with up/down arrow keys
5. THE Terminal UI SHALL clear input field after command submission

### Requirement 5

**User Story:** As an Operator, I want to add employee payroll data via commands, so that I can build a payroll batch.

#### Acceptance Criteria

1. THE Terminal UI SHALL recognize "ADD_EMPLOYEE" command
2. THE Terminal UI SHALL prompt for employee_id, hours_worked, hourly_rate, wallet_address
3. THE Terminal UI SHALL validate input data and show errors for invalid entries
4. THE Terminal UI SHALL display confirmation when employee is added to batch
5. THE Terminal UI SHALL maintain a list of added employees in the current session

### Requirement 6

**User Story:** As an Operator, I want to view the current payroll batch, so that I can verify data before processing.

#### Acceptance Criteria

1. THE Terminal UI SHALL recognize "LIST_EMPLOYEES" command
2. THE Terminal UI SHALL display all employees in current batch in a formatted table
3. THE Terminal UI SHALL show employee_id, hours, rate, and wallet_address for each entry
4. THE Terminal UI SHALL display "No employees in batch" if batch is empty
5. THE Terminal UI SHALL format monetary values with 2 decimal places

### Requirement 7

**User Story:** As an Operator, I want to process payroll and see results in real-time, so that I can monitor the calculation and settlement.

#### Acceptance Criteria

1. THE Terminal UI SHALL recognize "RUN_PAYROLL" command
2. WHEN payroll processing starts, THE Terminal UI SHALL display loading animation with glitch effects
3. THE Terminal UI SHALL show progress messages during COBOL execution
4. THE Terminal UI SHALL display calculation results (gross, taxes, net) for each employee
5. THE Terminal UI SHALL show settlement transaction hashes and links when transfers complete

### Requirement 8

**User Story:** As an Operator, I want to see transaction links I can click, so that I can verify settlements on the blockchain.

#### Acceptance Criteria

1. THE Terminal UI SHALL display transaction hashes as clickable links
2. THE Terminal UI SHALL open Basescan block explorer in new tab when link is clicked
3. THE Terminal UI SHALL style links in terminal green with underline on hover
4. THE Terminal UI SHALL display full transaction hash (not truncated)
5. THE Terminal UI SHALL show network indicator (Sepolia/Mainnet) next to transaction links

### Requirement 9

**User Story:** As an Operator, I want helpful commands and error messages, so that I can learn the system without documentation.

#### Acceptance Criteria

1. THE Terminal UI SHALL recognize "HELP" command and display available commands
2. THE Terminal UI SHALL show command syntax and examples for each command
3. WHEN an unknown command is entered, THE Terminal UI SHALL display "UNKNOWN COMMAND" error
4. WHEN a command has invalid syntax, THE Terminal UI SHALL display usage help
5. THE Terminal UI SHALL display error messages in error red (#ff0000)

### Requirement 10

**User Story:** As an Operator, I want to clear the terminal output, so that I can start fresh without clutter.

#### Acceptance Criteria

1. THE Terminal UI SHALL recognize "CLEAR" command
2. WHEN CLEAR is executed, THE Terminal UI SHALL remove all output lines
3. THE Terminal UI SHALL preserve the current payroll batch (only clear display)
4. THE Terminal UI SHALL display command prompt immediately after clearing
5. THE Terminal UI SHALL support "CLS" as an alias for "CLEAR"

### Requirement 11

**User Story:** As a Developer, I want the UI built with React and Tailwind CSS, so that it's maintainable and follows the tech stack.

#### Acceptance Criteria

1. THE Terminal UI SHALL be implemented as React functional components
2. THE Terminal UI SHALL use Tailwind CSS for all styling
3. THE Terminal UI SHALL use React hooks (useState, useEffect, useRef) for state management
4. THE Terminal UI SHALL organize components in a logical file structure
5. THE Terminal UI SHALL avoid inline styles (use Tailwind classes only)

### Requirement 12

**User Story:** As an Operator, I want the terminal to auto-scroll to new output, so that I always see the latest messages.

#### Acceptance Criteria

1. WHEN new output is added, THE Terminal UI SHALL automatically scroll to the bottom
2. THE Terminal UI SHALL maintain scroll position if user manually scrolls up
3. THE Terminal UI SHALL resume auto-scroll when user scrolls to bottom
4. THE Terminal UI SHALL use smooth scrolling behavior
5. THE Terminal UI SHALL focus the command input after each command execution

### Requirement 13

**User Story:** As an Operator, I want visual feedback during API calls, so that I know the system is working.

#### Acceptance Criteria

1. WHEN an API call is in progress, THE Terminal UI SHALL display a loading indicator
2. THE Terminal UI SHALL show animated dots or spinner in terminal green
3. THE Terminal UI SHALL display status messages during long operations
4. THE Terminal UI SHALL disable command input during processing
5. THE Terminal UI SHALL re-enable input when operation completes

### Requirement 14

**User Story:** As an Operator, I want keyboard shortcuts for common actions, so that I can work efficiently.

#### Acceptance Criteria

1. THE Terminal UI SHALL support Ctrl+L to clear the terminal
2. THE Terminal UI SHALL support Ctrl+C to cancel current operation
3. THE Terminal UI SHALL support Up/Down arrows for command history
4. THE Terminal UI SHALL support Tab for command auto-completion (future)
5. THE Terminal UI SHALL display keyboard shortcuts in HELP command output
