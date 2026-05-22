# SISCOMEX API — Implementação Técnica

## 1. Introdução

Este documento descreve a implementação técnica da integração com a API SISCOMEX (endpoints, headers, timeouts, erros, idempotência e observabilidade), alinhada ao SRS em `docs/project/software_requirements.md`.

---

## 2. Configuração e Segurança

### 2.1 Variáveis de ambiente

```env
CPF_CNPJ_RAIZ=<seu_cnpj_raiz>

# Autenticação por chave de acesso (modo atual)
CLIENT_ID=<sua_chave_de_acesso>

# Opcional: somente para outros modos de autenticação, se aplicável
CLIENT_SECRET=<seu_segredo_de_acesso_opcional>

LINK_PROD=https://portalunico.siscomex.gov.br/catp
PREFIX_CATP=/api
URL_AUTH=https://portalunico.siscomex.gov.br/portal/api/autenticar/chave-acesso

ROLE_TYPE=IMPEXP
PRODUTO_TESTE=<codigo_produto_teste>
```

### 2.2 Modelo real de autenticação (corrigido)

- **Modo atualmente implementado:** `/portal/api/autenticar/chave-acesso`
- **Payload utilizado:** `chaveAcesso + cnpjRaiz`
- **Uso de `CLIENT_SECRET`:** **não utilizado** neste modo.
- Se a equipe migrar para outro modo que exija segredo/certificado, atualizar este documento e o SRS.

### 2.3 Regras obrigatórias

1. `.env` no `.gitignore`.
2. Produção com cofre de segredos.
3. Rotação de credenciais conforme SRS.
4. Nunca logar segredo/token completo.

---

## 3. Padrões Técnicos Globais

### 3.1 Timeout padrão (padronizado)

- **Padrão único:** `timeout=(5, 30)` (connect, read) para todas as chamadas.
- Exceção explícita: exportações grandes podem usar `timeout=(10, 60)`.

### 3.2 Correlation ID (formalizado)

- Gerar `correlation_id` por operação (UUID v4).
- Propagar em headers internos e logs.
- Sempre incluir no resultado normalizado.

**Header recomendado:**
- `X-Correlation-ID: <uuid>`

### 3.3 Idempotência para operações não idempotentes (POST)

Para `create_product`, `link_manufacturer` e criação de operador:

1. Enviar `X-Idempotency-Key` por requisição.
2. Persistir chave por janela mínima de 24h.
3. Em retry, reutilizar a mesma chave.
4. Se API não suportar chave idempotente:
   - fazer verificação prévia (consulta por identificador natural),
   - só então executar POST.

---

## 4. Autenticação

### 4.1 Endpoint

**POST** `https://portalunico.siscomex.gov.br/portal/api/autenticar/chave-acesso`

**Body:**
```json
{
  "chaveAcesso": "<CLIENT_ID_from_env>",
  "cnpjRaiz": "<CPF_CNPJ_RAIZ_from_env>"
}
```

**Timeout:** `(5, 30)`

### 4.2 Política para HTTP 401 (corrigida)

Política única:
1. Ao receber 401, renovar autenticação **1 vez**.
2. Reexecutar a mesma requisição **1 vez**, quando seguro.
3. Se falhar novamente, erro final `SEC-401-AUTH-FAILED`.

---

## 5. Endpoints — Produtos

### 5.1 Consulta de produtos (GET)

`GET {LINK_PROD}/api/v1/ext/produto`

- Query: `cpfCnpjRaiz` (obrigatório), `codigo` (opcional)
- Timeout: `(5, 30)`

**Mapeamento SRS (corrigido):**
- **Não é RF-001**.
- Relaciona-se a suporte operacional para **RF-008** (sincronização/consulta de estado) e diagnóstico técnico.

### 5.2 Inclusão de produto (POST)

`POST {LINK_PROD}/api/v1/ext/produto`

- Timeout: `(5, 30)`
- Exigir idempotência (seção 3.3)

**Mapeamento SRS:** **RF-005**

### 5.3 Desativação de produto (PUT)

`PUT {LINK_PROD}/api/v1/ext/produto/desativar/{cpfCnpjRaiz}/{codigo}`

- Timeout: `(5, 30)`

**Mapeamento SRS:** **RF-007**

### 5.4 Desativação em lote

- Chamada item a item do endpoint 5.3.
- Falhas isoladas não interrompem lote.

**Mapeamento SRS:** **RF-007 + RF-008**

---

## 6. Endpoints — Operador Estrangeiro

### 6.1 Inclusão (POST)

`POST {LINK_PROD}/api/v1/ext/operador-estrangeiro`  
Timeout `(5, 30)` + idempotência.

### 6.2 Consulta (GET)

`GET {LINK_PROD}/api/v1/ext/operador-estrangeiro`  
Timeout `(5, 30)`.

### 6.3 Desativação (PUT)

`PUT {LINK_PROD}/api/v1/ext/operador-estrangeiro/desativar/{cpfCnpjRaiz}/{codigoPais}/{codigo}/{versao}`  
Timeout `(5, 30)`.

**Mapeamento SRS:** operação complementar (fora RF principal atual).

---

## 7. Endpoints — Fabricante (Vínculo)

### 7.1 Vínculo (POST)

`POST {LINK_PROD}/api/v1/ext/fabricante`  
Timeout `(5, 30)` + idempotência.

### 7.2 Desvínculo (PUT)

`PUT {LINK_PROD}/api/v1/ext/fabricante/{cpfCnpjRaiz}`  
Timeout `(5, 30)`.

### 7.3 Exportação de vínculos (GET)

`GET {LINK_PROD}/api/v1/ext/fabricante/exportar/{cpfCnpjRaiz}`  
Timeout `(10, 60)` quando volume alto.

**Mapeamento SRS:** operação complementar (fora RF principal atual).

---

## 8. Consulta de Atributos Obrigatórios (RF-001)

> O endpoint oficial pode variar conforme documentação do SISCOMEX. Implementar via adapter.

**Contrato obrigatório do adapter:**
- `get_required_attributes(ncm, data_referencia)`

**Mapeamento SRS:** **RF-001**, **RF-002**, **RF-003**, **RF-004**

---

## 9. Paginação e Limites (formalizado)

Para endpoints de listagem:
- parâmetros preferenciais: `page` e `size` (quando suportado)
- `size` padrão: 100
- `size` máximo recomendado: 500
- interromper em ausência de próxima página/token

Se endpoint não suportar paginação explícita, registrar limitação técnica.

---

## 10. Tratamento de Erros e Retry

### 10.1 Matriz única de decisão (corrigida)

| HTTP/Erro | Retry | Ação |
|---|---:|---|
| 200/201 | Não | Sucesso |
| 400 | Não | Corrigir payload |
| 401 | Condicional | Reautenticar 1x + retry 1x |
| 403 | Não | Verificar permissão/perfil |
| 404 | Não | Verificar recurso |
| 409 | Não | Tratar conflito de negócio |
| 422 | Não | Corrigir validação |
| 429 | Sim | Backoff exponencial + jitter |
| 5xx | Sim | Backoff exponencial + jitter |
| Timeout | Sim | Backoff exponencial + jitter |

### 10.2 Regras de retry

- Máximo 3 tentativas para 429/5xx/timeout.
- Para POST não idempotente: só retry com `X-Idempotency-Key` e controle local.
- Para 401: fluxo especial da seção 4.2.

---

## 11. Taxonomia de erros internos (nova seção)

- `SEC-xxx`: autenticação/segurança
- `INT-xxx`: integração externa/transporte
- `VAL-xxx`: validação de negócio
- `OPS-xxx`: operação/infraestrutura

**Exemplos:**
- `SEC-401-AUTH-FAILED`
- `INT-429-RATE-LIMIT`
- `INT-5XX-UPSTREAM`
- `VAL-ATTR-REQUIRED-MISSING`
- `OPS-TIMEOUT-UPSTREAM`

---

## 12. Resposta normalizada (adapter)

```json
{
  "status_http": 201,
  "codigo_erro_externo": null,
  "codigo_erro_interno": null,
  "mensagem": "Operação realizada com sucesso",
  "sequencial": "12345",
  "payload_resumo": {},
  "correlation_id": "uuid-v4"
}
```

---

## 13. Mapeamento SRS consolidado (corrigido)

| Operação técnica | Mapeamento SRS |
|---|---|
| Autenticação SISCOMEX | RF-009, RNF-004 |
| Consulta atributos obrigatórios por NCM (adapter) | RF-001 |
| Validação de obrigatoriedade | RF-002 |
| Validação de tipos | RF-003 |
| Regras condicionais | RF-004 |
| Inclusão de produto | RF-005 |
| Atualização de produto (quando implementada) | RF-006 |
| Desativação/Reativação | RF-007 |
| Consulta/sincronização de estado | RF-008 |
| Logs/correlation_id/métricas | RNF-005 |
| Retry/resiliência | RNF-003 |
| Timeout/performance | RNF-001 |
| Segredos/rotação | RNF-004 |

---

## 14. Correções de redação aplicadas

- `reauthenticar` → **reautenticar**
- `desvincar` → **desvincular**

---

## 15. Referências

- SRS: `docs/project/software_requirements.md`
- Segurança corporativa: política de segredos e rotação