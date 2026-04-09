#!/usr/bin/env node
/**
 * Simple test to verify MCP server tool registration
 */

import { spawn } from 'child_process';

async function testMCPServer() {
  console.log('Starting MCP Server test...\n');
  
  const server = spawn('node', ['dist/index.js'], {
    cwd: process.cwd(),
    stdio: ['pipe', 'pipe', 'pipe']
  });

  // Send tools/list request
  const listToolsRequest = {
    jsonrpc: '2.0',
    id: 1,
    method: 'tools/list',
    params: {}
  };

  let output = '';
  let errorOutput = '';
  let receivedResponse = false;

  server.stdout.on('data', (data) => {
    output += data.toString();
    try {
      const lines = output.split('\n');
      for (const line of lines) {
        if (line.trim() && line.startsWith('{')) {
          const response = JSON.parse(line);
          if (response.result && response.result.tools) {
            console.log('✅ MCP Server is running and responding!');
            console.log('\nAvailable tools:');
            response.result.tools.forEach((tool, idx) => {
              console.log(`${idx + 1}. ${tool.name} - ${tool.description.substring(0, 80)}...`);
            });
            console.log(`\nTotal tools: ${response.result.tools.length}`);
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
    errorOutput += data.toString();
  });

  server.on('close', (code) => {
    if (!receivedResponse) {
      console.log('❌ Server did not respond as expected');
      console.log('\nStderr output:');
      console.log(errorOutput);
    }
    process.exit(receivedResponse ? 0 : 1);
  });

  // Give the server time to start
  setTimeout(() => {
    server.stdin.write(JSON.stringify(listToolsRequest) + '\n');
  }, 500);

  // Timeout after 5 seconds
  setTimeout(() => {
    if (!receivedResponse) {
      console.log('❌ Test timed out');
      server.kill();
      process.exit(1);
    }
  }, 5000);
}

testMCPServer();
