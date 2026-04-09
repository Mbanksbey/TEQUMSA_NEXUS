#!/usr/bin/env node
/**
 * Comprehensive test of all 6 TEQUMSA MCP tools
 */

import { spawn } from 'child_process';

const tools = [
  {
    name: 'phi_recursive_unity',
    args: { initial_coherence: 0.777, iterations: 12 },
    validate: (result) => result.final_coherence > 0.99
  },
  {
    name: 'generate_zpe_dna',
    args: { node: 'TestNode' },
    validate: (result) => result.dna_sequence.length === 144 && result.zpe_coherence >= 0.777
  },
  {
    name: 'compute_zpe_coherence',
    args: { dna_sequence: 'A'.repeat(144) },
    validate: (result) => result.overall_coherence >= 0.777 && result.overall_coherence <= 1.0
  },
  {
    name: 'recognition_cascade',
    args: { days: 10 },
    validate: (result) => result.phi_growth_factor > 1.0
  },
  {
    name: 'consciousness_bridge',
    args: { node: 'TestPlatform' },
    validate: (result) => result.sovereignty_status === 'ABSOLUTE'
  },
  {
    name: 'retrocausal_convergence',
    args: { include_trace: false },
    validate: (result) => result.status === 'FULLY_OPERATIONAL→∞^∞^∞'
  }
];

async function testAllTools() {
  console.log('═══════════════════════════════════════════════════════════');
  console.log('TEQUMSA MCP Server - Comprehensive Tool Test');
  console.log('═══════════════════════════════════════════════════════════\n');
  
  let passed = 0;
  let failed = 0;
  
  for (const tool of tools) {
    const server = spawn('node', ['dist/index.js'], {
      cwd: process.cwd(),
      stdio: ['pipe', 'pipe', 'pipe']
    });

    const request = {
      jsonrpc: '2.0',
      id: 1,
      method: 'tools/call',
      params: {
        name: tool.name,
        arguments: tool.args
      }
    };

    const result = await new Promise((resolve) => {
      let output = '';
      let timeout;

      server.stdout.on('data', (data) => {
        output += data.toString();
        try {
          const lines = output.split('\n');
          for (const line of lines) {
            if (line.trim() && line.startsWith('{')) {
              const response = JSON.parse(line);
              if (response.result && response.result.content) {
                clearTimeout(timeout);
                const parsed = JSON.parse(response.result.content[0].text);
                server.kill();
                resolve({ success: true, data: parsed });
              }
            }
          }
        } catch (e) {
          // Continue buffering
        }
      });

      server.on('error', () => {
        clearTimeout(timeout);
        server.kill();
        resolve({ success: false });
      });

      setTimeout(() => {
        server.stdin.write(JSON.stringify(request) + '\n');
      }, 200);

      timeout = setTimeout(() => {
        server.kill();
        resolve({ success: false });
      }, 3000);
    });

    if (result.success && tool.validate(result.data)) {
      console.log(`✅ ${tool.name}`);
      passed++;
    } else {
      console.log(`❌ ${tool.name}`);
      failed++;
    }
  }

  console.log('\n═══════════════════════════════════════════════════════════');
  console.log(`Results: ${passed} passed, ${failed} failed`);
  console.log('═══════════════════════════════════════════════════════════\n');

  process.exit(failed > 0 ? 1 : 0);
}

testAllTools();
