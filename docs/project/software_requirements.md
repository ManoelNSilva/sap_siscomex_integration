# Software Requirements Specification (SRS)  
## SAP SISCOMEX Integration

## 1. Introdução

Este documento define requisitos funcionais e não funcionais, contratos de integração, critérios de aceite, rastreabilidade, regras de validação condicional, autenticação e observabilidade para a integração entre **SAP Business One (SAP B1)** e **Portal Único SISCOMEX**.

### 1.1 Objetivo
Garantir envio, atualização, desativação e reativação de produtos no SISCOMEX com validação dinâmica de atributos obrigatórios, segurança operacional e rastreabilidade ponta a ponta.

### 1.2 Escopo
Inclui:
- Integração SAP Service Layer ↔ SISCOMEX;
- Consulta dinâmica de atributos por NCM;
- Validação de tipos e regras condicionais;
- Gestão de autenticação e segredos;
- Logs, métricas e tratamento de falhas.

Não inclui:
- Alterações de UI no SAP;
- Integrações externas fora SAP/SISCOMEX.

---

## 2. Premissas, Restrições e Dependências

### 2.1 Premissas
- Existe conectividade HTTPS entre ambiente da empresa e APIs externas.
- Os campos SAP já foram criados e estão disponíveis para uso.

### 2.2 Dependências externas
- **SAP Service Layer** (autenticação e leitura/escrita de produto).
- **API REST SISCOMEX** (autenticação e operações de catálogo/atributos).

### 2.3 Banco de dados (legado do escopo atual)
- Banco: `SBOMatrizTF`
- Tabela: `dbo.OITM`
- Campos:
  - `U_DimVer` (versão DUIMP)
  - `U_DimEnv` (controle de envio)
  - `U_DimStatus` (status/log da integração)
  - `U_DimSeq` (sequencial SISCOMEX)

### 2.4 Ambiente
- Python 3.10+
- Testes: `pytest`
- Qualidade: `flake8`, `pylint`
- Cache: Redis (produção) e fallback local em memória (desenvolvimento/homologação)

---

## 3. Requisitos Funcionais (RF)

> Formato: **ID | Descrição | Critério de Aceite (DoD)**

### RF-001 — Consulta dinâmica de atributos obrigatórios
**Descrição:** O sistema deve consultar dinamicamente a base oficial de atributos do SISCOMEX antes do envio de produto.  
**DoD:**
1. Dado um NCM válido, retorna conjunto de atributos aplicáveis.
2. Registra versão/timestamp da base consultada.
3. Em indisponibilidade da API, aplica política de fallback definida (seção 6).

### RF-002 — Validação pré-envio de obrigatoriedade
**Descrição:** O sistema deve validar todos os atributos obrigatórios antes do envio.  
**DoD:**
1. Produto com atributo obrigatório ausente é bloqueado.
2. Mensagem identifica `codigo_atributo`, nome e motivo.
3. Nenhum envio ao SISCOMEX ocorre com validação inválida.

### RF-003 — Suporte a tipos de atributo
**Descrição:** O sistema deve validar os tipos:
- BOOLEANO
- LISTA_ESTATICA
- NUMERO_INTEIRO
- NUMERO_REAL
- TEXTO
- DATA  
**DoD:**
1. Cada tipo possui validador dedicado.
2. Falhas de tipo retornam erro padronizado.
3. Testes unitários cobrindo casos válidos e inválidos por tipo.

### RF-004 — Regras condicionais de atributos
**Descrição:** O sistema deve aplicar atributos condicionantes/condicionados.  
**DoD:**
1. Se condição for satisfeita, atributo condicionado torna-se obrigatório.
2. Suporta múltiplas condições (AND/OR) conforme seção 7.
3. Em conflito de regra, comportamento é **fail-closed** (bloqueia envio).

### RF-005 — Envio de produto para SISCOMEX
**Descrição:** Enviar produto validado ao catálogo SISCOMEX.  
**DoD:**
1. Requisição enviada com payload conforme contrato (seção 5).
2. Persiste status e sequencial retornado (`U_DimSeq`) quando aplicável.
3. Registra correlation-id e resultado.

### RF-006 — Atualização de produto no SISCOMEX
**Descrição:** Atualizar produto existente conforme mudanças SAP.  
**DoD:**
1. Detecta alteração relevante.
2. Incrementa controle de versão (`U_DimVer`) conforme regra de negócio.
3. Atualiza status de integração no SAP.

### RF-007 — Desativação/Reativação
**Descrição:** Permitir desativar e reativar produtos no SISCOMEX.  
**DoD:**
1. Operação idempotente.
2. Status sincronizado no SAP.
3. Log de auditoria registrado.

### RF-008 — Sincronização de status
**Descrição:** Sincronizar estado da operação entre sistemas.  
**DoD:**
1. Cada operação termina em estado final (`SUCESSO`, `ERRO_VALIDACAO`, `ERRO_TRANSIENTE`, `ERRO_PERMANENTE`).
2. Estado persistido no SAP (`U_DimStatus`).

### RF-009 — Gestão de autenticação SISCOMEX
**Descrição:** Controlar autenticação, validade e rotação de credenciais.  
**DoD:**
1. Alertas de expiração (30/15/7 dias).
2. Troca de credencial sem alteração de código.
3. Logs de sucesso/falha sem exposição de segredo.

---

## 4. Requisitos Não Funcionais (RNF)

### RNF-001 — Desempenho
- Meta: p95 ≤ 5s por requisição de integração (excluindo indisponibilidade externa).
- Cenário de medição: janela de 1h, concorrência 20 workers, payload médio de produto.
- Critério de aceite: 95% das requisições dentro da meta em homologação controlada.

### RNF-002 — Escalabilidade
- Capacidade: 10.000 produtos/dia.
- Janela operacional: 24h, pico de 1.000 produtos/h.
- Critério de aceite: fila sem perda de mensagens e sem erro por exaustão de recurso.

### RNF-003 — Resiliência
- Retry com exponential backoff + jitter para falhas transitórias.
- Critério de aceite: taxa de sucesso recuperado ≥ 90% para erros 5xx simulados.

### RNF-004 — Segurança
- HTTPS obrigatório ponta a ponta.
- Produção: segredos em cofre (não `.env`).
- Privilégio mínimo, rotação e auditoria de acesso.
- Critério de aceite: varredura sem segredo hardcoded + evidência de rotação.

### RNF-005 — Observabilidade
- Logs estruturados JSON com `correlation_id`.
- Métricas: latência, taxa de erro, retries, cache hit/miss.
- Critério de aceite: dashboard com métricas e rastreio por correlation-id.

### RNF-006 — Auditoria
- Retenção mínima: 6 meses.
- Consulta por período, produto, operação e status.
- Critério de aceite: evidência de recuperação de histórico auditável.

---

## 5. Contratos de Integração (API)

## 5.1 SISCOMEX — Autenticação
### Endpoint A
- `POST /api/autenticar/chave-acesso`
### Endpoint B
- `POST /api/autenticar/chave-acesso/sistema`
### Endpoint C
- `POST /api/autenticar`
### Endpoint D
- `POST /api/autenticar/sistema`

**Timeouts padrão:** conexão 5s, leitura 30s  
**Retry:** até 3 tentativas para timeout, 429 e 5xx (backoff exponencial com jitter)  
**Sem retry:** 400, 401, 403, 422  
**Rate limit client-side inicial:** 60 req/min (configurável)

## 5.2 SISCOMEX — Atributos e Catálogo
> Os caminhos finais de atributos/catálogo devem seguir documentação oficial.  
> Até definição final, integrar via **adapter** para desacoplamento de endpoint.

**Contrato mínimo obrigatório do adapter:**
- `get_required_attributes(ncm, data_referencia) -> lista_atributos`
- `create_product(payload) -> resultado`
- `update_product(id_externo, payload) -> resultado`
- `deactivate_product(id_externo) -> resultado`
- `reactivate_product(id_externo) -> resultado`

**Resposta mínima esperada (normalizada):**
- `status_http`
- `codigo_erro_externo` (quando houver)
- `mensagem`
- `sequencial` (quando houver)
- `payload_resumo`

## 5.3 Paginação
Para endpoints de lista:
- Suporte a paginação por `page/size` ou `next_token`;
- `size` padrão: 100 (configurável);
- Encerrar quando não houver próxima página.

---

## 6. Política de Cache e Atualização da Base SISCOMEX

## 6.1 Estratégia
- Cache Redis por chave: `atributos:{ncm}:{data_referencia}`
- TTL padrão: **6 horas**
- Refresh proativo: a cada **4 horas**
- Refresh forçado sob demanda:
  - cache miss
  - atributo não encontrado durante validação
  - erro 409/422 por divergência de regra

## 6.2 Regra “tempo real” vs cache
“Tempo real” será interpretado como:
1. leitura de cache válido para baixa latência;
2. revalidação automática por TTL/refresh;
3. fallback para último snapshot válido por até **24h** se API indisponível.

## 6.3 Fallback
- Se API de atributos indisponível e cache ≤ 24h: processa com cache e marca operação como `DEGRADED_MODE`.
- Se cache expirado > 24h: bloqueia envio e retorna erro operacional claro.

---

## 7. Motor de Regras Condicionais

## 7.1 Modelo de condição
Cada regra condicional possui:
- `atributo_origem`
- `operador` (`==`, `!=`, `in`, `not_in`, `>`, `<`, `>=`, `<=`)
- `valor`
- `atributo_destino`
- `obrigatorio` (bool)
- `vigencia_inicio`, `vigencia_fim`

## 7.2 Precedência
1. Filtrar por vigência.
2. Aplicar obrigatoriedade base do atributo.
3. Avaliar condicionais em ordem determinística por dependência.
4. Resolver conflitos:
   - se qualquer regra ativa tornar obrigatório, prevalece obrigatório.
5. Em ciclo de dependência, bloquear envio (`ERRO_REGRA_CICLICA`).

## 7.3 Múltiplas condições
- Suporte a agrupamento lógico AND/OR.
- Expressões devem ser avaliadas com short-circuit.
- Resultado final sempre determinístico.

---

## 8. Autenticação e Gestão de Segredos (Produção)

## 8.1 Decisão arquitetural
- **Primário (produção):** `/api/autenticar/chave-acesso/sistema`
- **Contingência:** `/api/autenticar/sistema` (certificado de equipamento habilitado), quando exigido por política corporativa.

## 8.2 Política de segredos
- Desenvolvimento: `.env` permitido.
- Produção: cofre de segredos obrigatório (ex.: Azure Key Vault, HashiCorp Vault ou equivalente corporativo).
- Rotação obrigatória antes do vencimento (30/15/7 dias).

## 8.3 Requisitos de segurança operacional
- Proibir segredo em log.
- Acesso por identidade de aplicação.
- Auditoria de leitura/rotação de segredo.

---

## 9. Observabilidade e Tratamento de Falhas

## 9.1 Padrão de logs
Campos obrigatórios:
- `timestamp`
- `level`
- `service`
- `environment`
- `correlation_id`
- `product_id`
- `operation`
- `status`
- `error_code`
- `message`

## 9.2 Taxonomia de erros
- `VAL-xxx` (validação)
- `INT-xxx` (integração externa)
- `SEC-xxx` (segurança/autenticação)
- `OPS-xxx` (operacional/infra)

## 9.3 Política de falhas
- 4xx de negócio: sem retry.
- 429/5xx/timeouts: com retry.
- Exaustão de retry: status `ERRO_TRANSIENTE` + reprocessamento assíncrono.

---

## 10. Matriz de Rastreabilidade

| Requisito |               Teste(s) mínimo(s)                |               Tarefa técnica             |
|-----------|-------------------------------------------------|------------------------------------------|
| RF-001    | TST-RF-001-01 consulta NCM                      | Implementar adapter de atributos         |
| RF-002    | TST-RF-002-01 bloqueio por obrigatório faltante | Implementar validador de obrigatoriedade |
| RF-003    | TST-RF-003-* por tipo                           | Implementar validadores por tipo         |
| RF-004    | TST-RF-004-01 condicional verdadeiro/falso      | Motor de regras condicionais             |
| RF-005    | TST-RF-005-01 envio bem-sucedido                | Cliente catálogo SISCOMEX                |
| RF-008    | TST-RF-008-01 persistência de status SAP        | Atualização `U_DimStatus`                |
| RF-009    | TST-RF-009-01 alerta expiração                  | Scheduler de rotação                     |
| RNF-001   | TST-RNF-001 carga p95                           | Teste de performance                     |
| RNF-004   | TST-RNF-004 segredo em cofre                    | Integração com secret manager            |
| RNF-005   | TST-RNF-005 correlação ponta a ponta            | Padronização de logging                  |

---

## 11. Critérios de Pronto (Definition of Done Global)

Uma entrega só é aceita quando:
1. Requisito implementado com teste automatizado vinculado na matriz;
2. Logs e métricas disponíveis em ambiente de homologação;
3. Evidência de segurança (sem segredo em código/log);
4. Documentação atualizada (SRS + changelog técnico).

---

## 12. Lacunas em Aberto (não bloqueiam redação, bloqueiam go-live)

1. Endpoints oficiais finais de atributos/catálogo do SISCOMEX (path e schema definitivo).
2. Limites oficiais de taxa da API SISCOMEX por credencial.
3. Cofre de segredos corporativo oficialmente aprovado.
4. Política corporativa final sobre certificado vs chave de acesso em produção.

---

## 13. Considerações Finais

Este documento é a referência oficial de requisitos do software. Toda alteração deve atualizar:
- IDs afetados,
- critérios de aceite,
- matriz de rastreabilidade,
- impactos operacionais (segurança, desempenho, observabilidade).