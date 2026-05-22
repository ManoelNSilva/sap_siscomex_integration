# SAP SISCOMEX Integration

Integração entre **SAP Business One (SAP B1)** e **Portal Único SISCOMEX** para automação de envio, validação de atributos, sincronização de status e observabilidade operacional.

---

## Funcionalidades Principais

- Integração com SAP Service Layer
- Integração com API SISCOMEX
- Validação de atributos obrigatórios e regras condicionais
- Controle de versão e status de integração
- Logs estruturados e suporte a rastreabilidade por correlação

---

## Documentação Oficial do Projeto

- **SRS (requisitos e critérios de aceite):** `docs/project/software_requirements.md`
- **Estrutura do projeto:** `docs/project/structure.md`
- **Instruções do projeto:** `docs/project/instructions.md`
- **Padrões de nomenclatura:** `docs/project/naming_conventions.md`
- **Implementação técnica SISCOMEX:** `docs/technical/siscomex_api_implementation.md`

> Em caso de conflito, o **SRS** é a fonte oficial para requisitos.

---

## Diretrizes Técnicas (Resumo)

### Autenticação
- Modo atual: `autenticar/chave-acesso`
- Credenciais por variáveis de ambiente
- Em produção: uso obrigatório de cofre de segredos

### Confiabilidade
- Timeout padrão: `connect=5s`, `read=30s`
- Retry com backoff exponencial + jitter para `429`, `5xx` e timeout
- `401`: reautenticar 1x e repetir 1x (fluxo controlado)

### Idempotência
- Operações `POST` devem usar chave de idempotência (`X-Idempotency-Key`) para evitar duplicidade

### Observabilidade
- Logs estruturados com `correlation_id`
- Propagação de `X-Correlation-ID`

---

## Estrutura Atual do Projeto

```text
sap_siscomex_integration/
├── docs/
│   ├── project/
│   │   ├── instructions.md
│   │   ├── naming_conventions.md
│   │   ├── software_requirements.md
│   │   ├── structure.md
│   │   └── timeline.md
│   ├── prompts/
│   │   ├── prompt_development.md
│   │   ├── prompt_documentation.md
│   │   └── prompt_tests.md
│   ├── technical/
│   │   └── siscomex_api_implementation.md
│   └── sap_fields.png
├── src/
│   ├── core/
│   │   ├── product_manager.py
│   │   └── version_control.py
│   ├── sap/
│   │   ├── service_layer.py
│   │   └── utils.py
│   ├── siscomex/
│   │   ├── api_client.py
│   │   └── utils.py
│   ├── utils/
│   │   └── logger.py
│   └── main.py
├── tests/
│   ├── integration/
│   ├── unit/
│   └── conftest.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Configuração do Ambiente (Windows)

1. Criar ambiente virtual:
   - `python -m venv venv`
   - `.\venv\Scripts\activate`

2. Instalar dependências:
   - `pip install -r requirements.txt`

3. Criar `.env` na raiz do projeto (não commitar):
   - Definir variáveis de SAP/SISCOMEX
   - Referência: `docs/technical/siscomex_api_implementation.md`

4. Executar testes:
   - `pytest tests/`

---

## Comandos de qualidade e testes

### Lint 
`ruff check .`

### Verificar formatação
`black --check .` 

### Formatar código
`black .`

## Testes 
`pytest -q`

## Segurança

- Nunca commitar `.env`, tokens, chaves ou segredos
- Nunca registrar credenciais em texto claro
- Validar `.env` no `.gitignore`

---

## Fluxo Geral

1. Ler dados no SAP (`src/sap`)
2. Gerenciar versão e estado (`src/core`)
3. Validar e integrar com SISCOMEX (`src/siscomex`)
4. Registrar logs e status (`src/utils`)
5. Validar com testes (`tests/unit` e `tests/integration`)