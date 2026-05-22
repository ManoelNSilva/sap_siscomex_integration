# Cenários de Teste — SAP SISCOMEX Integration

## 1. Objetivo

Registrar cenários de teste (base e incrementais) com prioridade e vínculo com arquivo real de teste, sem criar novos requisitos fora do SRS.

Referências:
- `docs/project/software_requirements.md` (**fonte oficial**)
- `docs/test/traceability_matrix.md`
- `docs/test/test_plan.md`
- `docs/technical/siscomex_api_implementation.md`

---

## 2. Convenções

- Formato: **Dado / Quando / Então**
- Priorização: P0/P1/P2/P3 (igual matriz e plano)
- IDs:
  - Base: `TC-RF-xxx-01` / `TC-RNF-xxx-01`
  - Incrementais: `...-02`, `...-03`, ...

---

## 3. Cenários base (obrigatórios por requisito)

|      ID       | Requisito | Prioridade |        Nível        |                                Arquivo de Teste                                  |                        Cenário resumido                         |
|---------------|-----------|------------|---------------------|-----------------------------------------------------------------------------------|-----------------------------------------------------------------|
| TC-RF-001-01  | RF-001    | P0         | Integração          | `tests/integration/test_siscomex_integration.py`                                  | Consulta de atributos por NCM com retorno válido.               |
| TC-RF-002-01  | RF-002    | P0         | Unitário            | `tests/unit/test_product_manager.py`                                              | Bloqueio quando obrigatório ausente.                            |
| TC-RF-003-01  | RF-003    | P0         | Unitário            | `tests/unit/test_siscomex_utils.py`                                               | Validação de tipos, incluindo **COMPOSTO** e **MULTIVALORADO**. |
| TC-RF-004-01  | RF-004    | P0         | Unitário            | `tests/unit/test_product_manager.py`                                              | Aplicação de regra condicional com fail-closed em conflito.     |
| TC-RF-005-01  | RF-005    | P0         | Integração          | `tests/integration/test_siscomex_integration.py`                                  | Envio de produto com idempotência.                              |
| TC-RF-006-01  | RF-006    | P1         | Unitário/Integração | `tests/unit/test_version_control.py`; `tests/integration/test_sap_integration.py` | Atualização com controle de versão.                             |
| TC-RF-007-01  | RF-007    | P1         | Integração          | `tests/integration/test_sap_integration.py`                                       | Desativar/reativar sem duplicidade.                             |
| TC-RF-008-01  | RF-008    | P1         | Unitário/Integração | `tests/unit/test_sap_utils.py`; `tests/integration/test_sap_integration.py`       | Sincronização de status entre sistemas.                         |
| TC-RF-009-01  | RF-009    | P0         | Unitário/Integração | `tests/unit/test_api_client.py`; `tests/integration/test_siscomex_integration.py` | Autenticação e renovação controlada.                            |
| TC-RNF-001-01 | RNF-001   | P1         | Integração          | `tests/integration/test_siscomex_integration.py`                                  | SLA de resposta conforme SRS.                                   |
| TC-RNF-002-01 | RNF-002   | P2         | Integração          | `tests/integration/test_sap_integration.py`                                       | Comportamento estável em volume operacional.                    |
| TC-RNF-003-01 | RNF-003   | P0         | Unitário/Integração | `tests/unit/test_api_client.py`; `tests/integration/test_siscomex_integration.py` | Retry/backoff/jitter para falha transitória.                    |
| TC-RNF-004-01 | RNF-004   | P0         | Unitário            | `tests/unit/test_logger.py`                                                       | Sigilo e mascaramento de credenciais nos logs.                  |
| TC-RNF-005-01 | RNF-005   | P0         | Unitário            | `tests/unit/test_logger.py`                                                       | Log estruturado com correlation_id.                             |
| TC-RNF-006-01 | RNF-006   | P2         | Integração          | `tests/integration/test_sap_integration.py`                                       | Evidência de trilha auditável e retenção.                       |


---

## 4. Cenários incrementais (P0/P1/P2/P3)

|      ID       | Requisito | Prioridade |   Nível    |                 Arquivo de Teste                 |                     Cenário resumido                     |
|---------------|-----------|------------|------------|--------------------------------------------------|----------------------------------------------------------|
| TC-RF-001-02  | RF-001    | P0         | Integração | `tests/integration/test_siscomex_integration.py` | Timeout/429/5xx com fallback seguro.                     |
| TC-RF-003-02  | RF-003    | P0         | Unitário   | `tests/unit/test_siscomex_utils.py`              | Estrutura inválida de **COMPOSTO** é rejeitada.          |
| TC-RF-003-03  | RF-003    | P0         | Unitário   | `tests/unit/test_siscomex_utils.py`              | Cardinalidade inválida de **MULTIVALORADO** é rejeitada. |
| TC-RF-005-02  | RF-005    | P0         | Integração | `tests/integration/test_siscomex_integration.py` | Reenvio com mesma `X-Idempotency-Key` não duplica.       |
| TC-RF-009-02  | RF-009    | P0         | Integração | `tests/integration/test_siscomex_integration.py` | 401 → reauth 1x + retry 1x.                              |
| TC-RNF-003-02 | RNF-003   | P0         | Unitário   | `tests/unit/test_api_client.py`                  | Limite de tentativas e jitter aplicados corretamente.    |
| TC-RNF-005-02 | RNF-005   | P0         | Unitário   | `tests/unit/test_logger.py`                      | Propagação de `correlation_id` em eventos críticos.      |
| TC-RF-008-02  | RF-008    | P1         | Integração | `tests/integration/test_sap_integration.py`      | Reconciliação de status divergente SAP/SISCOMEX.         |
| TC-RNF-001-02 | RNF-001   | P1         | Integração | `tests/integration/test_siscomex_integration.py` | Alerta quando latência ultrapassa janela definida.       |
| TC-RNF-006-02 | RNF-006   | P2         | Integração | `tests/integration/test_sap_integration.py`      | Consulta auditável por período/produto/status.           |

---

## 5. Critérios de aceite do documento

- Todos os RF/RNF do SRS aparecem com pelo menos 1 cenário.
- Cada cenário possui ID, prioridade, nível e arquivo de teste.
- Priorização coerente com matriz e plano.
- Sem criação de requisitos novos.

---

## 6. Cobertura-alvo (alinhamento)

- **P0/P1: 80%**
- **P2/P3: 60%**

---

## 7. Status

**Status:** Finalizado (conteúdo)  
**Situação:** Em revisão integrada com matriz e plano