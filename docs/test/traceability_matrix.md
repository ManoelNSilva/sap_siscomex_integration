# Matriz de Rastreabilidade — SAP SISCOMEX Integration

## 1. Objetivo

Garantir rastreabilidade completa **Requisito → Caso de Teste → Nível → Arquivo de Teste → Critério de Aceite** para os requisitos oficiais do SRS.

Referências:
- `docs/project/software_requirements.md` (**fonte oficial**)
- `docs/technical/siscomex_api_implementation.md`
- `docs/test/test_strategy.md`
- `docs/project/structure.md`
- `README.md`

---

## 2. Política de Prioridade

- **P0 (Bloqueador)**: impede operação/go-live.
- **P1 (Crítico)**: alto impacto operacional.
- **P2 (Importante)**: impacto relevante em estabilidade/confiabilidade.
- **P3 (Desejável)**: melhoria evolutiva.

---

## 3. Cobertura-alvo

- **Críticos (P0/P1): 80%**
- **Auxiliares (P2/P3): 60%**
- **Rastreabilidade RF/RNF: 100%**

---

## 4. Matriz consolidada (RF e RNF)

| Requisito | Prioridade | Caso de Teste |   Nível de Teste    |                                  Arquivo de Teste                                 |                   Critério de Aceite (resumo)                    |
|-----------|------------|---------------|---------------------|-----------------------------------------------------------------------------------|------------------------------------------------------------------|
| RF-001    | P0         | TC-RF-001-01  | Integração          | `tests/integration/test_siscomex_integration.py`                                  | Cons. de atrib. por NCM retorna estrutura válida e tratativa de falha/caching. |
| RF-002    | P0         | TC-RF-002-01  | Unitário            | `tests/unit/test_product_manager.py`                                              | Bloqueia envio sem atributo obrigatório e retorna erro de validação claro. |
| RF-003    | P0         | TC-RF-003-01  | Unitário            | `tests/unit/test_siscomex_utils.py`                                               | Valida tipos: BOOLEANO, LISTA_ESTATICA, NUMERO_*, TEXTO, DATA, **COMPOSTO**, **MULTIVALORADO**. |
| RF-004    | P0         | TC-RF-004-01  | Unitário            | `tests/unit/test_product_manager.py`                                              | Aplica regras condicionais com comportamento determinístico e fail-closed em conflito. |
| RF-005    | P0         | TC-RF-005-01  | Integração          | `tests/integration/test_siscomex_integration.py`                                  | Envio de produto com idempotência, persistindo status e referência externa. |
| RF-006    | P1         | TC-RF-006-01  | Unitário/Integração | `tests/unit/test_version_control.py`; `tests/integration/test_sap_integration.py` | Atualização com controle de versão e sincronização de estado. |
| RF-007    | P1         | TC-RF-007-01  | Integração          | `tests/integration/test_sap_integration.py`                                       | Desativação/reativação com comportamento idempotente e rastreável. |
| RF-008    | P1         | TC-RF-008-01  | Unitário/Integração | `tests/unit/test_sap_utils.py`; `tests/integration/test_sap_integration.py`       | Sincronização de status SAP/SISCOMEX com mapeamento consistente. |
| RF-009    | P0         | TC-RF-009-01  | Unitário/Integração | `tests/unit/test_api_client.py`; `tests/integration/test_siscomex_integration.py` | Autenticação e renovação 401 (reauth 1x + retry 1x) sem vazamento em logs. |
| RNF-001   | P1         | TC-RNF-001-01 | Integração          | `tests/integration/test_siscomex_integration.py`                                  | Tempo de resposta operacional dentro do SLA definido no SRS. |
| RNF-002   | P2         | TC-RNF-002-01 | Integração          | `tests/integration/test_sap_integration.py`                                       | Suporte a volume sem perda de consistência funcional. |
| RNF-003   | P0         | TC-RNF-003-01 | Unitário/Integração | `tests/unit/test_api_client.py`; `tests/integration/test_siscomex_integration.py` | Retry com backoff+jitter para 429/5xx/timeout com limite controlado. |
| RNF-004   | P0         | TC-RNF-004-01 | Unitário            | `tests/unit/test_logger.py`                                                       | Segredos mascarados em logs e ausência de credenciais expostas. |
| RNF-005   | P0         | TC-RNF-005-01 | Unitário            | `tests/unit/test_logger.py`                                                       | Logs estruturados com `correlation_id` e campos mínimos de observabilidade. |
| RNF-006   | P2         | TC-RNF-006-01 | Integração          | `tests/integration/test_sap_integration.py`                                       | Trilha auditável e consultável conforme retenção definida no SRS. |

---

## 5. Catálogo oficial de casos (base)

### RF
- TC-RF-001-01, TC-RF-002-01, TC-RF-003-01, TC-RF-004-01, TC-RF-005-01, TC-RF-006-01, TC-RF-007-01, TC-RF-008-01, TC-RF-009-01

### RNF
- TC-RNF-001-01, TC-RNF-002-01, TC-RNF-003-01, TC-RNF-004-01, TC-RNF-005-01, TC-RNF-006-01

> Casos incrementais estão em `docs/test/test_scenarios.md`.

---

## 6. Status

- Rastreabilidade RF/RNF: **concluída**
- Alinhamento com arquivos reais em `tests/`: **concluído**
- Situação: **Em revisão integrada (matriz + plano + cenários)**