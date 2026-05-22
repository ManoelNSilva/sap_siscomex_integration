# Padrões de Nomenclatura para Arquivos e Pastas

Este documento descreve os padrões de nomenclatura que devem ser seguidos para arquivos, pastas e código-fonte no projeto **SAP SISCOMEX Integration**.

---

## **1. Introdução**

Seguir padrões de nomenclatura consistentes é essencial para garantir a organização, legibilidade e manutenção do código. Este documento define as regras que devem ser seguidas para nomear arquivos, pastas e elementos do código-fonte.

---

## **2. Padrões para Diretórios**

- Os nomes dos diretórios devem ser escritos em **letras minúsculas**.
- Utilize **snake_case** para separar palavras em nomes compostos.
- Os nomes devem ser **descritivos** e indicar claramente o propósito do diretório.
- Use diretórios compostos (ex.: `sap_service_layer/`) apenas quando for necessário diferenciar subcomponentes ou funcionalidades específicas dentro de um módulo maior.
- **Diretórios gerados automaticamente**, como `venv\` (ambiente virtual), não devem ser incluídos no controle de versão. Certifique-se de adicioná-los ao arquivo `.gitignore`.
 
### Exemplos:
- `docs/`
- `src/`
- `tests/`
- `core/`
- `sap/`
- `sap_service_layer/` (quando o módulo SAP for subdividido em componentes específicos, como camadas de serviço)
- `siscomex_api/` (quando o módulo SISCOMEX for subdividido em componentes específicos, como APIs)

---

## **3. Padrões para Arquivos**

- Os nomes dos arquivos devem ser escritos em **letras minúsculas**.
- Utilize **snake_case** para separar palavras em nomes compostos.
- Os nomes devem refletir o conteúdo ou funcionalidade do arquivo.

### Exemplos:
- `product_manager.py`
- `version_control.py`
- `service_layer.py`
- `api_client.py`
- `logger.py`

---

## **4. Padrões para Código-Fonte**

### **4.1. Funções e Métodos**
- Devem ser nomeados em **snake_case**.
- Os nomes devem ser descritivos e indicar claramente a funcionalidade.
- Devem começar com um verbo que descreva a ação realizada.

#### Exemplos:
```python
def get_product_data():
    """Obtém os dados do produto."""
    pass

def send_to_siscomex(data):
    """Envia os dados para o SISCOMEX."""
    pass

class TProductManager:
    def add_product(self, product_data):
        """Adiciona um novo produto."""
        pass

    def remove_product(self, product_id):
        """Remove um produto existente."""
        pass

### **4.2. Classes**
- Devem ser nomeadas em **PascalCase**.
- Os nomes devem ser substantivos que descrevam o propósito da classe.
- Devem iniciar com um ** T **, para identificação de classes Python.

#### Exemplos:
```python
class TProductManager:
    """Gerencia as operações relacionadas aos produtos."""
    pass

class TSAPServiceLayer:
    """Gerencia a comunicação com o SAP Service Layer."""
    pass

class TSISCOMEXClient:
    """Gerencia a comunicação com o Portal Único SISCOMEX."""
    pass

### **4.3. Variáveis**
- Devem ser nomeadas em snake_case.
- Os nomes devem ser curtos, mas descritivos.
- Evite abreviações desnecessárias.

#### Exemplos:
```python
    product_data = {}
    response_status = "success"
    current_version = "1.0.0"

### **4.4. Constantes**
- Devem ser nomeadas em UPPER_SNAKE_CASE.
- Devem ser usadas para valores que não mudam durante a execução do programa.

#### Exemplos:
```python
    MAX_RETRIES = 5
    DEFAULT_TIMEOUT = 30
    API_BASE_URL = "https://api.siscomex.gov.br"

## **5. Exemplos Práticos**
Estrutura de Diretórios

src/
├── core/
│   ├── product_manager.py          # Gerenciamento de produtos
│   └── version_control.py          # Controle de versões
├── sap/
│   ├── service_layer.py            # Comunicação com o SAP Service Layer
│   └── utils.py                    # Funções utilitárias para o SAP
├── siscomex/
│   ├── api_client.py               # Cliente para chamadas à API do SISCOMEX
│   └── utils.py                    # Funções utilitárias para o SISCOMEX
├── utils/
│   └── logger.py                   # Configuração e gerenciamento de logs
└── main.py                         # Ponto de entrada principal do sistema

tests/
├── unit/                           # Testes unitários
│   ├── test_product_manager.py     # Testes para o módulo product_manager
│   ├── test_version_control.py     # Testes para o módulo version_control
│   └── test_logger.py              # Testes para o módulo logger
├── integration/                    # Testes de integração
│   ├── test_sap_integration.py     # Testes de integração com o SAP
│   └── test_siscomex_integration.py # Testes de integração com o SISCOMEX
└── conftest.py                     # Configuração do pytest

## **6. Considerações Finais**
Seguir os padrões de nomenclatura descritos neste documento é essencial para garantir a consistência e a qualidade do projeto. 
