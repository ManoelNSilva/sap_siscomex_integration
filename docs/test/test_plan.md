# Plano de Testes — SAP SISCOMEX Integration

## 1. Objetivo

Definir abordagem executiva de testes para validar RF-001..RF-009 e RNF-001..RNF-006, com rastreabilidade até os arquivos reais em `tests/`.

Referências:
- `docs/project/software_requirements.md` (**fonte oficial**)
- `docs/technical/siscomex_api_implementation.md`
- `docs/test/test_strategy.md`
- `docs/test/traceability_matrix.md`
- `docs/project/naming_conventions.md`
- `docs/project/structure.md`
- `README.md`

---

## 2. Escopo

### 2.1 Incluso
- Rastreamento requisito → caso → nível → arquivo.
- Execução em:
  - Local (Windows, mock/stub)
  - CI/CD (GitHub Actions, mock/stub)
  - Homologação SAP/SISCOMEX (smoke e contrato crítico)
- Cobertura-alvo por criticidade:
  - **P0/P1: 80%**
  - **P2/P3: 60%**

### 2.2 Fora do escopo
- Teste de carga massiva de longa duração.
- Benchmark de performance fora da janela da fase 1.3.

---

## 3. Arquivos reais de teste (alinhamento com repositório)

### 3.1 Unitários
- `tests/unit/test_api_client.py`
- `tests/unit/test_logger.py`
- `tests/unit/test_product_manager.py`
- `tests/unit/test_sap_utils.py`
- `tests/unit/test_service_layer.py`
- `tests/unit/test_siscomex_utils.py`
- `tests/unit/test_version_control.py`

### 3.2 Integração
- `tests/integration/test_siscomex_integration.py`
- `tests/integration/test_sap_integration.py`

---

## 4. Mapeamento executivo (requisito → arquivo)

| Requisito | Prioridade |   Caso base   |   Nível de Teste    |                                  Arquivo de Teste                                 |
|-----------|------------|---------------|---------------------|-----------------------------------------------------------------------------------|
| RF-001    | P0         | TC-RF-001-01  | Integração          | `tests/integration/test_siscomex_integration.py`                                  |
| RF-002    | P0         | TC-RF-002-01  | Unitário            | `tests/unit/test_product_manager.py`                                              |
| RF-003    | P0         | TC-RF-003-01  | Unitário            | `tests/unit/test_siscomex_utils.py`                                               |
| RF-004    | P0         | TC-RF-004-01  | Unitário            | `tests/unit/test_product_manager.py`                                              |
| RF-005    | P0         | TC-RF-005-01  | Integração          | `tests/integration/test_siscomex_integration.py`                                  |
| RF-006    | P1         | TC-RF-006-01  | Unitário/Integração | `tests/unit/test_version_control.py`; `tests/integration/test_sap_integration.py` |
| RF-007    | P1         | TC-RF-007-01  | Integração          | `tests/integration/test_sap_integration.py`                                       |
| RF-008    | P1         | TC-RF-008-01  | Unitário/Integração | `tests/unit/test_sap_utils.py`; `tests/integration/test_sap_integration.py`       |
| RF-009    | P0         | TC-RF-009-01  | Unitário/Integração | `tests/unit/test_api_client.py`; `tests/integration/test_siscomex_integration.py` |
| RNF-001   | P1         | TC-RNF-001-01 | Integração          | `tests/integration/test_siscomex_integration.py`                                  |
| RNF-002   | P2         | TC-RNF-002-01 | Integração          | `tests/integration/test_sap_integration.py`                                       |
| RNF-003   | P0         | TC-RNF-003-01 | Unitário/Integração | `tests/unit/test_api_client.py`; `tests/integration/test_siscomex_integration.py` |
| RNF-004   | P0         | TC-RNF-004-01 | Unitário            | `tests/unit/test_logger.py`                                                       |
| RNF-005   | P0         | TC-RNF-005-01 | Unitário            | `tests/unit/test_logger.py`                                                       |
| RNF-006   | P2         | TC-RNF-006-01 | Integração          | `tests/integration/test_sap_integration.py`                                       |

---

## 5. Nota técnica obrigatória — RF-003 (tipos)

Nos testes de RF-003, cobrir explicitamente:
- BOOLEANO
- LISTA_ESTATICA
- NUMERO_INTEIRO / NUMERO_REAL
- TEXTO
- DATA
- **COMPOSTO**
- **MULTIVALORADO**

---

## 6. Execução

### 6.1 Local (Windows)
- `.\venv\Scripts\activate`
- `pytest tests/unit -v`
- `pytest tests/integration -v -m "not smoke_sandbox"`
- `pytest tests/ --cov=src --cov-report=term-missing`

### 6.2 CI/CD (GitHub Actions)
- Rodar unit + integration com mock/stub.
- Publicar cobertura no pipeline.
- Gate de cobertura conforme política oficial da fase.

### 6.3 Homologação
- Rodar smoke e contrato crítico com ambiente real SAP/SISCOMEX.
- Evidenciar resultado no relatório da release.

---

## 7. Critérios de aceite do plano

- 100% dos RF/RNF presentes no plano.
- Cada requisito com pelo menos 1 caso de teste.
- Cada caso com **Nível de Teste** e **Arquivo de Teste**.
- Prioridades coerentes com matriz e cenários.
- Cobertura-alvo documentada: 80% críticos / 60% auxiliares.

---

## 8. Status

**Status:** Em revisão integrada  
**Próximo:** Aprovação conjunta com `traceability_matrix.md` e `test_scenarios.md`