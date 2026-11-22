# MIMCP API Specification - Perguntas Frequentes

## FAQ

**Q: Quantas tools estao disponiveis?**  
A: 12 tools divididas em 3 niveis (P0: 5 tools essenciais, P1: 5 tools avancadas, P2: 2 tools opcionais), todas acessiveis via JSON-RPC 2.0 em POST /mcp/json-rpc.

**Q: Qual o formato de requisicao?**  
A: JSON-RPC 2.0 padrao. Requisições devem conter jsonrpc, method, params e id. O header Content-Type: application/json e o endpoint /mcp/json-rpc sao obrigatorios.

**Q: Como lidar com erros?**  
A: Erros seguem o padrao JSON-RPC 2.0 com codigos -32600 a -32603. Codigos customizados como VALIDATION_ERROR fornecem detalhes adicionais no campo data. Always check the error field quando success for false.

**Q: Onde encontrar documentacao completa?**  
A: Consulte MIMCP_API_SPEC.md este arquivo, ou acesse a documentacao gerada automaticamente em POST /mcp/json-rpc com method: math_evaluate como exemplo inicial.

---

## JSON-RPC 2.0 Endpoint

```
POST /mcp/json-rpc
Content-Type: application/json
```

---

## Estrutura da Requisicao

```json
{
  "jsonrpc": "2.0",
  "method": "nome_da_tool",
  "params": {/* parametros especificos }},
  "id": 1
}
```

### Parametros Padrao Obrigatorios

| Campo | Descricao | Obrigatorio |
|-------|-----------|------------|
| jsonrpc | Versao do protocolo | Sim |
| method | Nome da tool/ metodo | Sim |
| params | Objeto com parametros da tool | Sim |
| id | Identificador da requisicao | Sim |

---

## Ferramentas Disponiveis (12 Tools P0-P2)

### Nivel P0 - Ferramentas Essenciais (5 tools)

#### Como usar o math_evaluate?

A: Avalie expressoes matematicas padrao. Exemplo: math_evaluate({expression: "2 + 2 * 3"}) retorna success: true, data: 8.

| Parametro | Tipo | Descricao | Padrao |
|-----------|------|-----------|--------|
| expression | string | Expressao mathematica valida | Obrigatorio |

Resposta de sucesso:
```json
{"jsonrpc":"2.0","result":{"success":true,"data":8,"expression":"2 + 2 * 3"},"id":1}
```

Resposta de erro:
```json
{"jsonrpc":"2.0","error":{"code":-32602,"message":"Invalid parameters"},"id":1}
```

---

#### Como usar o math_explain?

A: Explicar conceitos matematicos de forma estruturada. Niveis disponiveis: basic, intermediate, advanced, expert.

| Parametro | Tipo | Descricao | Obrigatorio |
|-----------|------|-----------|------------|
| topic | string | Conceito a explicar | Sim |
| level | string | Nivel de detalhe | Nao |

Resposta de sucesso:
```json
{"jsonrpc":"2.0","result":{"success":true,"data":"A derivada mede a taxa...","topic":"derivada","level":"basic","formatted":true},"id":1}
```

---

#### Como usar o math_optimize?

A: Otimizar expressoes algebricas para forma simplificada. Exemplo: x * x + 2 * x + 1 -> (x + 1)^2.

| Parametro | Tipo | Descricao | Obrigatorio |
|-----------|------|-----------|------------|
| expression | string | Expressao a otimizar | Sim |

Resposta de sucesso:
```json
{"jsonrpc":"2.0","result":{"success":true,"data":"(x + 1)2","expression":"x * x + 2 * x + 1","optimized":true},"id":1}
```

---

#### Como usar o result_verify?

A: Verificar se um resultado de calculo esta correto. Confidence scale: 0.0 a 1.0.

| Parametro | Tipo | Descricao | Obrigatorio |
|-----------|------|-----------|------------|
| expression | string | Expressao original | Sim |
| result | string | Resultado a verificar | Sim |

Resposta de sucesso:
```json
{"jsonrpc":"2.0","result":{"success":true,"verified":true,"expression":"integral(x^2)","result":"x^3/3","confidence":0.95},"id":1}
```

---

#### Como usar o memory_profile?

A: Perfilagem de consumo de memoria durante operacoes.

| Parametro | Tipo | Descricao | Obrigatorio |
|-----------|------|-----------|------------|
| operation | string | Nome da operacao | Sim |
| duration_ms | number | Duracao em milissegundos | Sim |

Resposta de sucesso:
```json
{"jsonrpc":"2.0","result":{"success":true,"data":{"peak_mb":45.2,"average_mb":32.1},"operation":"search","duration_ms":150},"id":1}
```

---

### Nivel P1 - Ferramentas Avancadas (5 tools)

13. formula_engine
14. symbolic_solver
15. calculus_operations
16. linear_algebra
17. statistical_analysis

---

### Nivel P2 - Ferramentas Opcionais (2 tools)

18. advanced_cryptography
19. pattern_recognition

---

## Requisicoes de Exemplo

### Exemplo 1: Avaliar expressao

```bash
curl -X POST http://localhost:8000/mcp/json-rpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"math_evaluate","params":{"expression":"(5 + 3) * 2"},"id":1}'
```

### Exemplo 2: Explicar conceito

```bash
curl -X POST http://localhost:8000/mcp/json-rpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"math_explain","params":{"topic":"integral definida","level":"intermediate"},"id":2}'
```

### Exemplo 3: Verificar resultado

```bash
curl -X POST http://localhost:8000/mcp/json-rpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"result_verify","params":{"expression":"derivada de x3","result":"3x2"},"id":3}'
```

### Exemplo 4: Perfilagem de memoria

```bash
curl -X POST http://localhost:8000/mcp/json-rpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"memory_profile","params":{"operation":"calculus","duration_ms":5000},"id":4}'
```

---

## Códigos de Erro

| Código | Significado | Resolucao |
|--------|-------------|-----------|
| -32600 | Parse error | Formato JSON invalido |
| -32601 | Method not found | Método inexistente; consulte lista de tools disponiveis |
| -32602 | Invalid parameters | Parâmetros invalidos; verifique tipos e estrutura |
| -32603 | Internal error | Erro interno do servidor; consulte logs |
| VALIDATION_ERROR | Erro de validação | Corrija os parâmetros conforme especificação |

---

## Segurança e Rate Limiting

- **Rate Limit**: 100 requisições por minuto por IP
- **Autenticação**: Sem auth para desenvolvimento; tokens Bearer disponiveis para produção
- **HTTPS**: Obrigatório em produção; HTTP permitido apenas em localhost
- **CORS**: Configurado para localhost:8000 e render.com

---

## Versionamento

- Versão Atual: 0.1.0
- Data: 15 de janeiro de 2024
- Especificação JSON-RPC: 2.0
- Compatibilidade: Versões anteriores mantidas por 12 meses

---

## Ultima atualizacao

15 de janeiro de 2024

Versao

0.1.0