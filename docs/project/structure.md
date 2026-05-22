# Estrutura do Projeto

Este documento descreve a estrutura de diretórios do projeto **SAP SISCOMEX Integration** e a finalidade de cada pasta/arquivo.

---

## Estrutura de Diretórios

```plaintext
sap_siscomex_integration/
├── docs/                                 # Documentação do projeto
│   ├── project/                          # Documentos de planejamento e requisitos
│   │   ├── instructions.md               # Instruções gerais do projeto
│   │   ├── naming_conventions.md         # Convenções de nomenclatura
│   │   ├── software_requirements.md      # SRS (requisitos funcionais e não funcionais)
│   │   ├── structure.md                  # Estrutura do projeto (este arquivo)
│   │   └── timeline.md                   # Cronograma do projeto
│   ├── prompts/                          # Prompts para modelos de IA
│   │   ├── prompt_development.md         # Diretrizes para desenvolvimento
│   │   ├── prompt_documentation.md       # Diretrizes para documentação
│   │   └── prompt_tests.md               # Diretrizes para testes
│   ├── technical/                        # Documentação técnica de implementação
│   │   └── siscomex_api_implementation.md
│   └── sap_fields.png                    # Imagem de referência dos campos SAP
├── src/                                  # Código-fonte principal
│   ├── core/                             # Regras centrais de negócio
│   │   ├── product_manager.py            # Orquestração de produto
│   │   └── version_control.py            # Controle de versão e estado
│   ├── sap/                              # Integração com SAP Service Layer
│   │   ├── service_layer.py              # Cliente SAP Service Layer
│   │   └── utils.py                      # Utilitários SAP
│   ├── siscomex/                         # Integração com API SISCOMEX
│   │   ├── api_client.py                 # Cliente HTTP SISCOMEX
│   │   └── utils.py                      # Utilitários SISCOMEX
│   ├── utils/                            # Utilitários compartilhados
│   │   └── logger.py                     # Logging estruturado
│   └── main.py                           # Ponto de entrada da aplicação
├── tests/                                # Testes automatizados
│   ├── integration/                      # Testes de integração
│   ├── unit/                             # Testes unitários
│   └── conftest.py                       # Configuração global do pytest
├── venv/                                 # Ambiente virtual local (não versionar)
├── .gitignore                            # Regras de arquivos ignorados no Git
├── README.md                             # Visão geral do projeto
└── requirements.txt                      # Dependências Python
```

---

## Descrição por Área

### 1) `docs/`
Centraliza toda a documentação:
- **`project/`**: requisitos, estrutura, instruções e cronograma.
- **`prompts/`**: guias para uso dos modelos de IA.
- **`technical/`**: documentação técnica de integração (endpoints, políticas e contratos).

> Observação: arquivos `docs/*.py` são referências legadas e não devem ser tratados como código principal de produção.

### 2) `src/`
Contém o código principal da aplicação:
- **`core/`**: lógica de negócio e orquestração.
- **`sap/`**: comunicação com SAP Service Layer.
- **`siscomex/`**: comunicação com API SISCOMEX.
- **`utils/`**: logging e utilitários comuns.
- **`main.py`**: inicialização do fluxo da aplicação.

### 3) `tests/`
Cobertura automatizada:
- **`unit/`**: validação isolada de funções/módulos.
- **`integration/`**: validação ponta a ponta entre módulos e integrações.
- **`conftest.py`**: fixtures e configuração do `pytest`.

### 4) Arquivos de configuração
- **`.gitignore`**: ignora `venv/`, `.env`, cache Python etc.
- **`requirements.txt`**: dependências necessárias.
- **`README.md`**: onboarding e visão geral.

---

## Regras de Organização

1. Código executável principal deve ficar em `src/`.
2. Documentação deve ficar em `docs/`.
3. Testes devem espelhar a estrutura de `src/` sempre que possível.
4. Segredos nunca devem ser commitados (`.env`, tokens, chaves).
5. Novos módulos devem seguir padrão `snake_case` (PEP 8).

---

## Referências

- `docs/project/software_requirements.md`
- `docs/project/naming_conventions.md`
- `docs/technical/siscomex_api_implementation.md`