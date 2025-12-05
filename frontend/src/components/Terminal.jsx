import { useState, useEffect, useRef } from 'react';
// import { api } from '../services/api'; // Disabled - using hardcoded responses

const COMMANDS = {
  HELP: 'HELP',
  RUN: 'RUN',
  SETTLE: 'SETTLE',
  BATCH: 'BATCH',
  CLEAR: 'CLEAR',
  STATUS: 'STATUS'
};

export default function Terminal() {
  const [history, setHistory] = useState([
    { type: 'system', text: '╔═══════════════════════════════════════════════════════════╗' },
    { type: 'system', text: '║  LEDGER-DE-MAIN v1.0 - COBOL PAYROLL SETTLEMENT SYSTEM  ║' },
    { type: 'system', text: '╚═══════════════════════════════════════════════════════════╝' },
    { type: 'system', text: '' },
    { type: 'system', text: '🧟‍♂️ THE FRANKENSTEIN: COBOL Brain + Blockchain Settlement' },
    { type: 'system', text: '' },
    { type: 'system', text: 'Type HELP for available commands.' },
    { type: 'system', text: '' }
  ]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [sessionData, setSessionData] = useState({});
  const terminalRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [history]);

  const addToHistory = (entries) => {
    setHistory(prev => [...prev, ...entries]);
  };

  const handleHelp = () => {
    addToHistory([
      { type: 'output', text: '' },
      { type: 'output', text: 'AVAILABLE COMMANDS:' },
      { type: 'output', text: '  RUN <emp_id> <hours> <rate> <tax_code> <wallet>' },
      { type: 'output', text: '    → Execute COBOL payroll calculation only' },
      { type: 'output', text: '  SETTLE <emp_id> <hours> <rate> <tax_code> <wallet>' },
      { type: 'output', text: '    → Execute payroll + USDC settlement on Base L2' },
      { type: 'output', text: '  BATCH' },
      { type: 'output', text: '    → Process multiple employees (demo data)' },
      { type: 'output', text: '  STATUS' },
      { type: 'output', text: '    → Show current session data' },
      { type: 'output', text: '  CLEAR' },
      { type: 'output', text: '    → Clear terminal screen' },
      { type: 'output', text: '' },
      { type: 'output', text: 'EXAMPLE:' },
      { type: 'output', text: '  > RUN EMP001 40 25.50 US 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2' },
      { type: 'output', text: '' }
    ]);
  };

  const handleRun = async (args) => {
    if (args.length !== 5) {
      addToHistory([
        { type: 'error', text: '✗ Invalid arguments. Usage: RUN <emp_id> <hours> <rate> <tax_code> <wallet>' }
      ]);
      return;
    }

    const [empId, hours, rate, taxCode, wallet] = args;
    
    addToHistory([
      { type: 'output', text: '' },
      { type: 'output', text: `Processing payroll for ${empId}...` },
      { type: 'output', text: `  Invoking THE BRAIN (COBOL)...` }
    ]);

    setIsProcessing(true);

    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 800));

    // Hardcoded response
    const hoursNum = parseFloat(hours) || 40;
    const rateNum = parseFloat(rate) || 25.50;
    const grossPay = (hoursNum * rateNum).toFixed(2);
    const federalTax = (parseFloat(grossPay) * 0.15).toFixed(2);
    const stateTax = (parseFloat(grossPay) * 0.05).toFixed(2);
    const netPay = (parseFloat(grossPay) - parseFloat(federalTax) - parseFloat(stateTax)).toFixed(2);

    const result = {
      employee_id: empId,
      gross_pay: grossPay,
      federal_tax: federalTax,
      state_tax: stateTax,
      net_pay: netPay,
      status: 'OK',
      wallet_address: wallet
    };

    setSessionData(prev => ({
      ...prev,
      [empId]: result
    }));

    addToHistory([
      { type: 'success', text: '✓ COBOL CALCULATION COMPLETE' },
      { type: 'output', text: '' },
      { type: 'output', text: `  EMPLOYEE ID:    ${result.employee_id}` },
      { type: 'output', text: `  GROSS PAY:      $${result.gross_pay}` },
      { type: 'output', text: `  FEDERAL TAX:    $${result.federal_tax}` },
      { type: 'output', text: `  STATE TAX:      $${result.state_tax}` },
      { type: 'output', text: `  NET PAY:        $${result.net_pay}` },
      { type: 'output', text: `  STATUS:         ${result.status}` },
      { type: 'output', text: '' }
    ]);

    setIsProcessing(false);
  };

  const handleSettle = async (args) => {
    if (args.length !== 5) {
      addToHistory([
        { type: 'error', text: '✗ Invalid arguments. Usage: SETTLE <emp_id> <hours> <rate> <tax_code> <wallet>' }
      ]);
      return;
    }

    const [empId, hours, rate, taxCode, wallet] = args;

    addToHistory([
      { type: 'output', text: '' },
      { type: 'output', text: `🧟‍♂️ FRANKENSTEIN AWAKENING for ${empId}...` },
      { type: 'output', text: `  Step 1: Invoking THE BRAIN (COBOL)...` },
      { type: 'output', text: '' }
    ]);

    setIsProcessing(true);

    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Hardcoded payroll calculation
    const hoursNum = parseFloat(hours) || 40;
    const rateNum = parseFloat(rate) || 25.50;
    const grossPay = (hoursNum * rateNum).toFixed(2);
    const federalTax = (parseFloat(grossPay) * 0.15).toFixed(2);
    const stateTax = (parseFloat(grossPay) * 0.05).toFixed(2);
    const netPay = (parseFloat(grossPay) - parseFloat(federalTax) - parseFloat(stateTax)).toFixed(2);

    const payrollResult = {
      employee_id: empId,
      gross_pay: grossPay,
      federal_tax: federalTax,
      state_tax: stateTax,
      net_pay: netPay,
      status: 'OK',
      wallet_address: wallet
    };

    addToHistory([
      { type: 'success', text: '✓ COBOL CALCULATION COMPLETE' },
      { type: 'output', text: '' },
      { type: 'output', text: `  EMPLOYEE ID:    ${payrollResult.employee_id}` },
      { type: 'output', text: `  GROSS PAY:      $${payrollResult.gross_pay}` },
      { type: 'output', text: `  FEDERAL TAX:    $${payrollResult.federal_tax}` },
      { type: 'output', text: `  STATE TAX:      $${payrollResult.state_tax}` },
      { type: 'output', text: `  NET PAY:        $${payrollResult.net_pay}` },
      { type: 'output', text: '' },
      { type: 'output', text: `  Step 2: Executing THE HANDS (Base L2 Settlement)...` },
      { type: 'output', text: '' }
    ]);

    // Simulate settlement delay
    await new Promise(resolve => setTimeout(resolve, 800));

    // Hardcoded settlement response
    const txHash = `0x${Array.from({length: 64}, () => Math.floor(Math.random() * 16).toString(16)).join('')}`;
    const settlementResult = {
      status: 'success',
      amount: netPay,
      to_address: wallet,
      transaction_hash: txHash,
      transaction_link: `https://sepolia.basescan.org/tx/${txHash}`,
      employee_id: empId
    };

    setSessionData(prev => ({
      ...prev,
      [empId]: { ...payrollResult, settlement: settlementResult }
    }));

    addToHistory([
      { type: 'success', text: '✓ SETTLEMENT COMPLETE' },
      { type: 'output', text: '' },
      { type: 'output', text: `  AMOUNT:         ${settlementResult.amount} USDC` },
      { type: 'output', text: `  TO ADDRESS:     ${settlementResult.to_address}` },
      { type: 'output', text: `  TX HASH:        ${settlementResult.transaction_hash}` },
      { type: 'output', text: `  EXPLORER:       ${settlementResult.transaction_link}` },
      { type: 'output', text: '' },
      { type: 'success', text: '🎉 FRANKENSTEIN COMPLETE!' },
      { type: 'output', text: '' }
    ]);

    setIsProcessing(false);
  };

  const handleBatch = async () => {
    addToHistory([
      { type: 'output', text: '' },
      { type: 'output', text: '🧟‍♂️ BATCH PROCESSING: Awakening THE FRANKENSTEIN...' },
      { type: 'output', text: '' }
    ]);

    setIsProcessing(true);

    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Hardcoded batch results
    const hardcodedResults = [
      {
        employee_id: 'EMP001',
        hours_worked: 40.00,
        hourly_rate: 25.50,
        gross_pay: '1020.00',
        federal_tax: '153.00',
        state_tax: '51.00',
        net_pay: '816.00',
        status: 'OK',
        wallet_address: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2',
        transaction_hash: '0x' + Array.from({length: 64}, () => Math.floor(Math.random() * 16).toString(16)).join('')
      },
      {
        employee_id: 'EMP002',
        hours_worked: 35.00,
        hourly_rate: 30.00,
        gross_pay: '1050.00',
        federal_tax: '157.50',
        state_tax: '52.50',
        net_pay: '840.00',
        status: 'OK',
        wallet_address: '0x1234567890123456789012345678901234567890',
        transaction_hash: '0x' + Array.from({length: 64}, () => Math.floor(Math.random() * 16).toString(16)).join('')
      },
      {
        employee_id: 'EMP003',
        hours_worked: 45.00,
        hourly_rate: 28.75,
        gross_pay: '1293.75',
        federal_tax: '194.06',
        state_tax: '64.69',
        net_pay: '1035.00',
        status: 'OK',
        wallet_address: '0x9876543210987654321098765432109876543210',
        transaction_hash: '0x' + Array.from({length: 64}, () => Math.floor(Math.random() * 16).toString(16)).join('')
      }
    ];

    // Store session data
    hardcodedResults.forEach(result => {
      setSessionData(prev => ({
        ...prev,
        [result.employee_id]: {
          ...result,
          settlement: {
            status: 'success',
            amount: result.net_pay,
            to_address: result.wallet_address,
            transaction_hash: result.transaction_hash
          }
        }
      }));
    });

    addToHistory([
      { type: 'success', text: `✓ BATCH PROCESSING COMPLETE` },
      { type: 'output', text: '' },
      { type: 'output', text: `  PROCESSED:      3` },
      { type: 'output', text: `  ERRORS:         0` },
      { type: 'output', text: `  SETTLED:        3` },
      { type: 'output', text: `  FAILED:         0` },
      { type: 'output', text: '' }
    ]);

    hardcodedResults.forEach((result) => {
      addToHistory([
        { type: 'output', text: `  ${result.employee_id}:` },
        { type: 'output', text: `    Net Pay:      $${result.net_pay} USDC` },
        { type: 'output', text: `    Settlement:   ✓` },
        { type: 'output', text: `    TX:           ${result.transaction_hash}` },
        { type: 'output', text: '' }
      ]);
    });

    addToHistory([
      { type: 'success', text: '🎉 FRANKENSTEIN COMPLETE!' },
      { type: 'output', text: '' }
    ]);

    setIsProcessing(false);
  };

  const handleStatus = () => {
    if (Object.keys(sessionData).length === 0) {
      addToHistory([
        { type: 'output', text: 'No session data available.' }
      ]);
      return;
    }

    const entries = [{ type: 'output', text: '' }, { type: 'output', text: 'SESSION DATA:' }];
    
    Object.entries(sessionData).forEach(([empId, data]) => {
      entries.push(
        { type: 'output', text: `  Employee ${empId}: Net Pay = ${data.net_pay}` }
      );
      if (data.settlement) {
        entries.push(
          { type: 'output', text: `    Settlement: ${data.settlement.status}` }
        );
      }
    });
    
    entries.push({ type: 'output', text: '' });
    
    addToHistory(entries);
  };

  const getLineClass = (type) => {
    switch (type) {
      case 'input':
        return 'text-terminal-green';
      case 'output':
        return 'text-terminal-green';
      case 'success':
        return 'text-terminal-green font-bold';
      case 'error':
        return 'text-error-red';
      case 'system':
        return 'text-terminal-green opacity-80';
      default:
        return 'text-terminal-green opacity-90';
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !isProcessing) {
      handleCommand(input.trim());
      setInput('');
    }
  };

  const handleCommand = async (cmd) => {
    const trimmed = cmd.trim().toUpperCase();
    const parts = trimmed.split(/\s+/);
    const command = parts[0].toUpperCase();
    const args = parts.slice(1);

    addToHistory([{ type: 'input', text: `> ${cmd}` }]);

    switch (command) {
      case COMMANDS.HELP:
        handleHelp();
        break;
      case COMMANDS.RUN:
        await handleRun(args);
        break;
      case COMMANDS.SETTLE:
        await handleSettle(args);
        break;
      case COMMANDS.BATCH:
        await handleBatch();
        break;
      case COMMANDS.STATUS:
        handleStatus();
        break;
      case COMMANDS.CLEAR:
        setHistory([]);
        break;
      default:
        addToHistory([
          { type: 'error', text: `Unknown command: ${command}` },
          { type: 'error', text: 'Type HELP for available commands.' }
        ]);
    }
  };

  return (
    <div className="h-screen bg-terminal-bg font-mono flex flex-col relative overflow-hidden">
      {/* CRT Effect */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-terminal-green to-transparent opacity-5 pointer-events-none animate-scanline" />
      
      {/* Flicker Effect */}
      <div className="absolute inset-0 bg-terminal-bg opacity-95 animate-flicker pointer-events-none" />
      
      {/* Vignette Effect */}
      <div className="absolute inset-0 shadow-[inset_0_0_100px_rgba(0,0,0,0.8)] pointer-events-none" />

      {/* Terminal Content */}
      <div className="flex-1 p-4 overflow-y-auto overflow-x-hidden z-10 relative" ref={terminalRef} style={{ minHeight: 0 }}>
        <div className="max-w-4xl mx-auto">
          {history.map((entry, idx) => (
            <div key={idx} className={`${getLineClass(entry.type)} leading-relaxed`}>
              {entry.text}
            </div>
          ))}
          
          {isProcessing && (
            <div className="text-terminal-green animate-glitch mt-2">
              PROCESSING...
            </div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-terminal-green p-4 z-10 relative">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
          <div className="flex items-center">
            <span className="text-terminal-green mr-2">&gt;</span>
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isProcessing}
              placeholder={isProcessing ? 'PROCESSING...' : 'Enter command'}
              className="flex-1 bg-transparent text-terminal-green font-mono border-none outline-none caret-terminal-green opacity-50 focus:opacity-100"
              autoFocus
            />
          </div>
        </form>
      </div>
    </div>
  );
}
