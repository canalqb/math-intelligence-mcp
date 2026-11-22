import { ModuleMetadata, Component } from '@angular/core';
import { Router } from '@angular/router';

// Este é um exemplo de metadado para o módulo Math Intelligence
// Será usado pela integração Angular do agente IA

export const MATH_INTELLIGENCE_CONFIG = {
  name: 'math-intelligence',
  version: '0.1.0',
  description: 'Mathematical Intelligence capabilities for AI agents',
  tools: [
    'math_evaluate',
    'math_explain', 
    'math_optimize',
    'result_verify',
    'memory_profile'
  ],
  endpoints: {
    json_rpc: 'http://localhost:8000/mcp/json-rpc',
    stdio: true
  }
};