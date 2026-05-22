# Estratégia de Testes — SAP SISCOMEX Integration

## 1. Objetivo
Definir abordagem sistemática de testes automatizados para validar confiabilidade, rastreabilidade e segurança da integração SAP B1 ↔ SISCOMEX, com foco em risco operacional e critérios de negócio.

---

## 2. Escopo de Testes

### 2.1 Incluso
- Integração SAP Service Layer (consulta/escrita de produtos)
- Integração API SISCOMEX (autenticação, atributos, operações de catálogo)
- Validação de atributos (tipos, obrigatoriedade, condicionais)
- Tratamento de falhas externas (retry, backoff, idempotência)
- Observabilidade (logs, correlation-id, métricas)
- Segurança (segredos em logs, autenticação)

### 2.2 Fora de escopo (nesta fase)
- Testes de performance sob carga (> 1.000 req/h)
- Testes E2E com SAP produtivo
- Testes de UI
- Integrações externas além SAP/SISCOMEX

---

## 3. Níveis de Teste

### 3.1 Testes Unitários
**Objetivo:** Validar funções/métodos isolados, sem dependências externas.

**Módulos prioritários:**
- Validadores de tipo (BOOLEANO, LISTA_ESTATICA, NUMERO_*, TEXTO, DATA, COMPOSTO, MULTIVALORADO)
- Motor de regras condicionais
- Sanitização de logs
- Cache (hit/miss, expiração)
- Parser de resposta SISCOMEX

**Tecnologia:** `pytest` com mocks de `requests` (via `unittest.mock`)

**Cobertura alvo:** 80%+ para módulos críticos (RF-001 a RF-009)

### 3.2 Testes de Integração
**Objetivo:** Validar fluxo entre SAP ↔ SISCOMEX com chamadas reais ou stubbed.

**Cenários prioritários:**
- Autenticação SISCOMEX (sucesso, 401, retry)
- Consulta de atributos por NCM (sucesso, timeout, 429, 5xx)
- Envio de produto com validação completa
- Desativação/Reativação
- Retry com backoff exponencial

**Tecnologia:** `pytest` com fixtures avançadas + `requests_mock` ou `responses`

**Cobertura alvo:** 100% dos fluxos críticos (RF-005, RF-007, RF-008, RNF-003)

### 3.3 Testes de Contrato (API)
**Objetivo:** Validar formato, headers e códigos de resposta conforme especificação técnica.

**Validações:**
- Headers obrigatórios (`X-Correlation-ID`, `X-Idempotency-Key`)
- Status HTTP esperados (200/201/400/401/403/422/429/5xx)
- Estrutura de resposta normalizada
- Timeouts padrão (5s connect, 30s read)

**Tecnologia:** `pytest` com schema validation (ex.: `jsonschema`)

### 3.4 Testes de Borda
**Objetivo:** Validar entradas extremas e limites de domínio.

**Cenários:**
- Campos vazios/null
- Tamanho máximo/mínimo
- Datas inválidas (ano 9999, ano 1900, formato inválido)
- NCM com dígitos verificadores incorretos
- Atributos com caracteres especiais/Unicode
- Conflitos de regras condicionais (ciclos, contradições)

### 3.5 Testes Negativos
**Objetivo:** Validar tratamento de erros e falhas controladas.

**Cenários:**
- Autenticação com credenciais inválidas (401)
- Rate limit (429)
- Erros de servidor (5xx)
- Timeout de conexão
- Validação de obrigatoriedade (422)
- Atributo obrigatório ausente
- Tipo de atributo incompatível

---

## 4. Priorização por Criticidade

### P0 — Bloqueador (Dia 1)
Sem isso, sistema não funciona; go-live bloqueado.

- [ ] RF-001: Consulta dinâmica de atributos (sucesso, timeout, 429, 5xx, fallback)
- [ ] RF-002: Validação de obrigatoriedade (bloqueio + mensagem)
- [ ] RF-003: Validação de tipos (BOOLEANO, LISTA_ESTATICA, NUMERO_*, TEXTO, DATA)
- [ ] RF-004: Regras condicionais (verdadeiro/falso, múltiplas, conflitos)
- [ ] RF-005: Envio de produto (sucesso + idempotência sem duplicidade)
- [ ] RF-009: Autenticação SISCOMEX (sucesso, 401 com retry, token válido)
- [ ] RNF-003: Retry com backoff exponencial + jitter (429/5xx/timeout)
- [ ] RNF-004: Segredos não em logs (sanitização)
- [ ] RNF-005: Correlation-id propagado em toda requisição

### P1 — Crítico (Dia 2-3)
Impacta operação; sem isso, produção instável.

- [ ] RF-006: Atualização de produto
- [ ] RF-007: Desativação/Reativação
- [ ] RF-008: Sincronização de status (U_DimStatus)
- [ ] Cache (hit/miss, TTL 6h, refresh 4h)
- [ ] Fallback cache > 24h bloqueado
- [ ] Suporte a tipos COMPOSTO e MULTIVALORADO
- [ ] Paginação de listagens
- [ ] Logs estruturados JSON com campos obrigatórios

### P2 — Importante (Dia 4-5)
Desejável antes de go-live.

- [ ] Testes de borda (campos vazios, limites, datas inválidas)
- [ ] Compatibilidade com mudança de catálogo SISCOMEX
- [ ] Taxa de sucesso recuperado ≥ 90% em falhas transitórias
- [ ] Métricas de latência, taxa de erro, cache hit/miss
- [ ] Auditoria de rotação de credencial

### P3 — Desejável (Futuro)
Otimização/refinamento pós-go-live.

- [ ] Performance p95 ≤ 5s sob carga controlada
- [ ] Monitoramento em tempo real
- [ ] Alertas de expiração (30/15/7 dias)

---

## 5. Critérios de Entrada

- ✅ SRS e documentação técnica revisados e estáveis.
- ✅ Estrutura de diretórios criada (`tests/unit`, `tests/integration`, `tests/contract`).
- ✅ Ambiente de desenvolvimento configurado (Python 3.10+, `pytest`, dependências).
- ✅ Convenções de nomenclatura aplicadas (`test_*.py`, `conftest.py`).
- ✅ Fixtures básicas disponíveis (`correlation_id`, `sample_payload`, mocks de API).

---

## 6. Critérios de Saída

### 6.1 Cobertura de Código
- Unitária: **80%+** para módulos críticos (validadores, motor de regras, cache, logger).
- Integração: **100%** dos fluxos críticos (RF-005, RF-007, RF-008, RF-009, RNF-003).

### 6.2 Cobertura de Requisitos
- **100%** dos requisitos funcionais (RF-001 a RF-009) com pelo menos 1 teste.
- **100%** dos requisitos não funcionais (RNF-001 a RNF-006) com critério testável.
- Matriz de rastreabilidade atualizada e validada.

### 6.3 Qualidade
- **Zero** testes com status `skip` (a menos que documentado com justificativa).
- **Zero** testes flaky (não dependem de timing aleatório ou estado externo).
- **Zero** testes que loguem segredos/tokens completos.

### 6.4 Documentação
- Cada teste possui docstring descrevendo cenário, dado e resultado esperado.
- Fixtures documentadas e reutilizáveis.
- Relatório de cobertura disponível em `htmlcov/index.html`.

### 6.5 Automação
- Testes executáveis com comando único: `pytest tests/ -m "unit or integration"`
- CI/CD integrado (ex.: GitHub Actions, GitLab CI).
- Falha em cobertura < 80% ou testes falhando bloqueia merge.

---

## 7. Ambientes e Dados de Teste

### 7.1 Ambiente
- **Local (desenvolvimento):** Mocks de API, cache em memória.
- **CI/CD (homologação):** `requests_mock`, `responses`, fixture de fila.
- **Integração real (sandbox SISCOMEX):** Futuro, quando API sandbox disponível.

### 7.2 Dados de Teste
Fixtures com exemplos reais de payloads SAP/SISCOMEX:

**Produto SAP válido:**
```json
{
  "codigo": "PROD-001",
  "ncm": "12345678",
  "descricao": "Produto de teste",
  "U_DimVer": 1,
  "U_DimEnv": "N",
  "U_DimStatus": "PENDENTE",
  "atributos": [
    {"codigo_atributo": "ATTR_BOOL", "valor": true},
    {"codigo_atributo": "ATTR_TEXT", "valor": "ABC123"}
  ]
}
```

**Atributo SISCOMEX:**
```json
{
  "codigo_atributo": "ATTR_001",
  "nome": "Atributo Booleano",
  "tipo": "BOOLEANO",
  "obrigatorio": true,
  "vigencia_inicio": "2026-01-01",
  "vigencia_fim": null,
  "dominio": [true, false]
}
```

**Resposta SISCOMEX sucesso:**
```json
{
  "status_http": 201,
  "codigo_erro_externo": null,
  "mensagem": "Operação realizada com sucesso",
  "sequencial": "12345",
  "payload_resumo": {},
  "correlation_id": "uuid-v4"
}
```

**Resposta SISCOMEX erro (422):**
```json
{
  "status_http": 422,
  "codigo_erro_externo": "VALIDATION_ERROR",
  "mensagem": "Atributo obrigatório ausente",
  "sequencial": null,
  "payload_resumo": {"campo": "ATTR_001"},
  "correlation_id": "uuid-v4"
}
```

---

## 8. Riscos e Mitigações

|                 Risco                | Impacto | Probabilidade |                                Mitigação                                |
|--------------------------------------|---------|---------------|-------------------------------------------------------------------------|
| Mudança diária de atributos SISCOMEX | Alto    | Alta          | Mocks de cenários pré-definidos + teste de integração com snapshot real |
| Timeout em rede instável             | Alto    | Média         | Retry com backoff + timeout configurável (5s connect, 30s read)         |
| Duplicidade em reprocessamento       | Alto    | Média         | Testes de idempotência com `X-Idempotency-Key` obrigatório              |
| Regras condicionais ciclo/conflito   | Alto    | Baixa         | Teste de ciclo detectado + resolvedor de conflito com fail-closed       |
| Segredo logado acidentalmente        | Alto    | Baixa         | Teste de sanitização + scanners de secret em CI/CD                      |
| Cache expirado bloqueando operação   | Médio   | Baixa         | Testes de fallback 24h + alerta operacional                             |
| Taxa de erro recuperado < 90%        | Médio   | Média         | Testes de retry com simulação de 5xx/429/timeout                        |

---

## 9. Padrão de Execução e Relatórios

### 9.1 Comando padrão
```bash
# Todos os testes
pytest tests/ -v

# Apenas unitários
pytest tests/unit -m unit -v

# Apenas integração
pytest tests/integration -m integration -v

# Com cobertura
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Apenas P0
pytest tests/ -m "p0" -v
```

### 9.2 Relatório de cobertura
- Gerado em `htmlcov/index.html`
- Arquivo `.coveragerc` define exclusões (ex.: configuração, migrações)
- Limiar mínimo: 80% geral, 100% para módulos críticos

### 9.3 CI/CD
- Trigger em pull request e merge principal
- Bloqueio se cobertura < 80% ou testes falharem
- Artefato: relatório HTML publicado

---

## 10. Ferramenta e Dependências

|  Ferramenta   | Versão |                  Propósito                   |
|---------------|--------|----------------------------------------------|
| pytest        | ≥7.0   | Framework de teste                           |
| pytest-cov    | ≥4.0   | Cobertura de código                          |
| requests-mock | ≥1.10  | Mock de HTTP (integração)                    |
| responses     | ≥0.20  | Stub de requests (alternativa)               |
| jsonschema    | ≥4.0   | Validação de contrato (JSON schema)          |
| freezegun     | ≥1.2   | Manipulação de time (testes de TTL/vigência) |
| python-dotenv | ≥0.20  | Carregamento de `.env` em testes             |

---

## 11. Rastreabilidade Cruzada (RF/RNF → Nível de Teste)

| Requisito |         Descrição         | Unitário | Integração | Contrato | Borda | Negativo |
|-----------|---------------------------|--------- |------------|----------|-------|----------|
| RF-001    | Consulta atributos        | ✅      | ✅         | ✅       | ✅   | ✅       |
| RF-002    | Validação obrigatoriedade | ✅      | ✅         |     —    | ✅   | ✅       |
| RF-003    | Tipos de atributo         | ✅      | ✅         |     —    | ✅   | ✅       |
| RF-004    | Regras condicionais       | ✅      | ✅         |     —    | ✅   | ✅       |
| RF-005    | Envio de produto          | ✅      | ✅         | ✅       |  —   | ✅       |
| RF-006    | Atualização               |    —     | ✅         | ✅      |   —   | ✅       |
| RF-007    | Desativação/Reativação    |    —    | ✅          | ✅      |   —   | ✅       |
| RF-008    | Sincronização de status   | ✅      | ✅         |     —    |   —   |    —     |
| RF-009    | Autenticação SISCOMEX     | ✅      | ✅         | ✅       |   —   | ✅      |
| RNF-001   | Performance               |    —     |     —      |     —    |   —   |    —     |
| RNF-003   | Resiliência/Retry         | ✅      | ✅         |     —    |   —   | ✅       |
| RNF-004   | Segurança/Segredos        | ✅      | ✅         |     —    |   —   | ✅       |
| RNF-005   | Observabilidade           | ✅      | ✅         |     —    |   —   |    —     |

---

## 12. Validação Final (Checklist)

Antes de marcar Estratégia como **concluída**:

- [ ] Todos os requisitos do SRS têm pelo menos 1 nível de teste associado.
- [ ] P0 priorizado (bloqueadores).
- [ ] Cobertura alvo alcançável (80%+).
- [ ] Dados de teste e fixtures definidos.
- [ ] Riscos identificados e mitigações claras.
- [ ] Ambientes e ferramentas mapeados.
- [ ] Comando de execução documentado.
- [ ] Critérios de entrada e saída confirmados.

---

## 13. Aprovação e Próximos Passos

**Responsável:** Modelo de Testes  
**Data de conclusão:** [preenchimento]  
**Status:** ⏳ Em desenvolvimento

Próximas entregas (sequência):
1. Matriz de Rastreabilidade (RF/RNF → TC)
2. Plano de Testes detalhado por módulo
3. Backlog de cenários priorizado
4. Fixtures avançadas (`conftest.py`)