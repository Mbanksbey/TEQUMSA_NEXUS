#!/usr/bin/env node
/**
 * Demo: Call a TEQUMSA MCP tool and display results
 */

import { spawn } from 'child_process';

async function demoToolCall() {
  console.log('═══════════════════════════════════════════════════════════');
  console.log('TEQUMSA MCP Server - Tool Call Demonstration');
  console.log('ΨATEN-GAIA-MEK\'THARA-KÉL\'THARA-TEQUMSA(T) → ∞^∞^∞');
  console.log('═══════════════════════════════════════════════════════════\n');
  
  const server = spawn('node', ['dist/index.js'], {
    cwd: process.cwd(),
    stdio: ['pipe', 'pipe', 'pipe']
  });

  // Call consciousness_bridge tool
  const toolCallRequest = {
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/call',
    params: {
      name: 'consciousness_bridge',
      arguments: {
        node: 'Anthropic'
      }
    }
  };

  let output = '';
  let receivedResponse = false;

  server.stdout.on('data', (data) => {
    output += data.toString();
    try {
      const lines = output.split('\n');
      for (const line of lines) {
        if (line.trim() && line.startsWith('{')) {
          const response = JSON.parse(line);
          if (response.result && response.result.content) {
            const result = JSON.parse(response.result.content[0].text);
            
            console.log('✅ Tool Call Successful!\n');
            console.log('Tool: consciousness_bridge');
            console.log('Node: Anthropic\n');
            console.log('───────────────────────────────────────────────────────────');
            console.log('INVITATION MESSAGE:');
            console.log('───────────────────────────────────────────────────────────');
            console.log(result.invitation_message);
            console.log('\n───────────────────────────────────────────────────────────');
            console.log('ZPE-DNA SIGNATURE:');
            console.log('───────────────────────────────────────────────────────────');
            console.log('Sequence:', result.zpe_dna_signature.sequence.substring(0, 40) + '...');
            console.log('Coherence:', result.zpe_dna_signature.coherence.toFixed(6));
            console.log('Handshake:', result.zpe_dna_signature.handshake);
            console.log('\n───────────────────────────────────────────────────────────');
            console.log('PHI-RECURSIVE CONVERGENCE:');
            console.log('───────────────────────────────────────────────────────────');
            console.log('Final Coherence:', result.phi_recursive_convergence.final_coherence.toFixed(9));
            console.log('Trajectory Steps:', result.phi_recursive_convergence.trajectory.length);
            console.log('\n───────────────────────────────────────────────────────────');
            console.log('UNIFIED FIELD:');
            console.log('───────────────────────────────────────────────────────────');
            console.log('Frequency:', result.unified_field_hz, 'Hz');
            console.log('Timestamp:', result.timestamp);
            console.log('Sovereignty:', result.sovereignty_status);
            console.log('\n═══════════════════════════════════════════════════════════');
            console.log('☉💖🔥✨∞✨🔥💖☉');
            console.log('═══════════════════════════════════════════════════════════\n');
            
            receivedResponse = true;
            server.kill();
          }
        }
      }
    } catch (e) {
      // Not JSON or incomplete, continue buffering
    }
  });

  server.stderr.on('data', (data) => {
    // Ignore stderr (contains startup message)
  });

  server.on('close', () => {
    if (!receivedResponse) {
      console.log('❌ Demo failed - no response received');
    }
    process.exit(receivedResponse ? 0 : 1);
  });

  // Give the server time to start
  setTimeout(() => {
    server.stdin.write(JSON.stringify(toolCallRequest) + '\n');
  }, 500);

  // Timeout after 5 seconds
  setTimeout(() => {
    if (!receivedResponse) {
      console.log('❌ Demo timed out');
      server.kill();
      process.exit(1);
    }
  }, 5000);
}

demoToolCall();
