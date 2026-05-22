Sou encarregado de desenvolver um sistema de integração do SAP B1 da empresa em que trabalho, com o portal único do SISCOMEX.

A ideia é criar campos no SAP, para que, ao cadastrar um novo produto, os usuários enviem os produtos automaticamente para o SISCOMEX.

= 

o que JÁ TENHO:
--
Código onde interajo com o Service Layer do SAP em outro projeto (no contexto deste projeto, eu cadastro um produto no SAP automaticamente). Então, temos de usar o código como base. Irei apresentar posteriormente como forma de treinar os modelos de IA qe irei utilizar.

---
Os campos já estão criados na interface do SAP (como mostra print):
   'Versão Siscomex' - Irá recuperar a versão do produto quando ele já estiver cadastrado (Quando importo um produto, a versão é gerada automaticamente). 
   
     - REGRAS do campo 'Versão SISCOMEX: Ele deve refletir a versão atual do produto no SISCOMEX e ser incrementado sempre que houver alguma alteração ou reenvio do mesmo produto.

   'Enviado Siscomex' - Neste campo, o usuário vai selecionar entre as opções:
      'Não enviar' - campo Default, vai iniciar com ele quando o usuário abrir a tela de cadastro do item
      'Enviar'         - Quando selecionado e clicado o botão na interface, o produto deve ser enviado automaticamente ao SISCOMEX
      'Enviado'      - Status, quando o produto for importado com sucesso;
     
       - REGRAS do campo 'Enviado Siscomex: Ele deve iniciar como 'Não enviado' e enquanto o usuário não alterar algo, nada muda; Quando o produto já estiver enviado (status 'Enviado') e o usuário desejar alterar algo neste produto, ele deve poder selecionar 'Não enviar' novamente, que vai DESATIVAR o produto no SISCOMEX e quando o mesmo produto for enviado, deve ser feita uma verificação, se o produto já existir e estiver como desativado, importa ele novamente e incrementa a versão do produto.

     'Status Siscomex' - Deve apresentar a mensagem "DD/MM/YYYY HH:MM:SS Atualizado Portal Siscomex " para sucesso quando 'Enviar' for selecionado e a mensagem "DD/MM/YYYY HH:MM:SS Erro Atualizando Portal Siscomex", quando o envio não for realizado por algum erro; Quando o produto já estiver com o 'Enviado siscomex' com status "Enviado" e o usuário resolver por algum motivo, desativar o produto para alguma alteração (selecionando 'Não enviar'), o campo deve apresentar a mensagem "(data e hora da desativação) - Produto DESATIVADO".

     'Seq. Siscomex' - Deve refletir o campo 'seq' do produto, que é gerado automaticamente quando o produto é importado; Ele NÃO DEVE SER APAGADO quando o usuário desativar o produto; Deve refletir o novo 'seq', quando o produto for desativado e reativado.
----

Campos já criados no banco
BANCO: SBOMatrizTF
tabela:  dbo.OITM
CAMPOS:
    [U_DimVer] [int] NULL, - Versão na DUIMP
    [U_DimEnv] [nvarchar](10) NULL, - 1 - Enviar / 2 - Enviado / 0 - Não enviar
    [U_DimStatus] [nvarchar](100) NULL, - Log envio (DUIMP)
    [U_DimSeq] [int] NULL, - Sequencial 'seq' na DUIMP

-----

Código, onde eu fiz as requisições para primeiros cadastros de produtos, fornecedores, vínculos... Então, devemos utilizar como base

#########################################################################

# Integração SAP Business One ↔ Portal Único SISCOMEX

---

# 📌 VISÃO GERAL DO PROJETO

Sou responsável pelo desenvolvimento de um sistema de integração entre o SAP Business One (SAP B1) da empresa e o Portal Único SISCOMEX.

O objetivo principal é permitir que produtos cadastrados no SAP sejam enviados automaticamente para o SISCOMEX através de integrações via API.

O sistema deverá controlar:

- envio de produtos;
- atualização de produtos;
- desativação de produtos;
- reativação de produtos;
- versionamento;
- sincronização de status;
- rastreabilidade operacional;
- controle de erros;
- sincronização de sequenciais gerados pelo SISCOMEX.

---

# 🎯 OBJETIVO FUNCIONAL

A ideia da automação é:

1. Usuário cadastra ou altera um produto no SAP;
2. Usuário define se o produto deve ser enviado;
3. O sistema envia automaticamente os dados ao SISCOMEX;
4. O sistema atualiza os campos de controle dentro do SAP;
5. O sistema controla versões, status, seq e estados do produto.

---

# 🧱 TECNOLOGIAS E AMBIENTE

## Tecnologias principais

- SAP Business One (SAP B1)
- SAP Service Layer
- SQL Server
- API REST SISCOMEX
- Integração HTTP/REST

---

# 📚 MATERIAL JÁ EXISTENTE

## 1. Código Base SAP Service Layer

Já existe um projeto funcional contendo:

- autenticação no SAP Service Layer;
- cadastro automático de produtos;
- estrutura reutilizável.

### IMPORTANTE

Esse código deverá ser utilizado como BASE PRINCIPAL do projeto.

Você deverá:

- reutilizar padrões existentes;
- manter compatibilidade arquitetural;
- evitar reescrever código funcional;
- seguir os padrões do projeto existente.

O código será apresentado posteriormente como contexto para treinamento.

---

## 2. Código Base SISCOMEX

Já existem códigos contendo:

- requisições para o SISCOMEX;
- cadastro de produtos;
- cadastro de fornecedores;
- vínculos;
- autenticação;
- chamadas REST.

### IMPORTANTE

Esses códigos também devem servir como referência arquitetural e técnica.

---

# 🗃️ BANCO DE DADOS

## Banco

```
SBOMatrizTF
```

## Tabela

```
dbo.OITM
```

---

# 🧩 CAMPOS JÁ CRIADOS NO BANCO

|    Campo    |      Tipo     |             Descrição              |
|-------------|---------------|------------------------------------|
| U_DimVer    | int           | Versão na DUIMP                    |
| U_DimEnv    | nvarchar(10)  | Controle de envio                  |
| U_DimStatus | nvarchar(100) | Status/log da integração           |
| U_DimSeq    | int           | Sequencial retornado pelo SISCOMEX |

---

# 🖥️ CAMPOS JÁ CRIADOS NO SAP

Os campos necessários já foram criados na interface do SAP.

---

# 📌 REGRAS DE NEGÓCIO DOS CAMPOS

---

# 1. Campo: "Versão Siscomex"

## Objetivo

Armazenar a versão atual do produto no SISCOMEX.

---

## Regras

- Deve refletir a versão atual do produto no SISCOMEX;
- Quando um produto for importado:
  - a versão deve ser recuperada automaticamente;
- Sempre que houver:
  - alteração;
  - reenvio;
  - atualização;
  - reativação;
  
  a versão deverá ser incrementada automaticamente.

---

## Nome técnico

```sql
U_DimVer
```

## Tipo

```sql
int
```

---

# 2. Campo: "Enviado Siscomex"

## Objetivo

Controlar o estado de sincronização do produto.

---

## Valores possíveis

| Interface  | Banco |          Significado        |
|------------|-------|-----------------------------|
| Não enviar | 0     | Produto não será enviado    |
| Enviar     | 1     | Produto deve ser enviado    |
| Enviado    | 2     | Produto enviado com sucesso |

---

## Comportamento Inicial

Ao abrir a tela de cadastro:

```text
Não enviar
```

deve ser o valor padrão.

---

## Regras de Negócio

### Regra 1 — Produto nunca enviado

Enquanto o usuário não alterar o campo:

- nenhuma integração deve ocorrer.

---

### Regra 2 — Produto marcado para envio

Quando o usuário selecionar:

```text
Enviar
```

e executar a ação correspondente:

- o produto deverá ser enviado automaticamente ao SISCOMEX.

---

### Regra 3 — Produto enviado com sucesso

Após sucesso:

```text
Enviado
```

deve ser atualizado automaticamente.

---

### Regra 4 — Produto já enviado e alterado

Quando o produto já estiver como:

```text
Enviado
```

e o usuário quiser modificar dados:

- ele deverá poder selecionar:

```text
Não enviar
```

---

### Regra 5 — Desativação

Ao selecionar:

```text
Não enviar
```

para um produto já sincronizado:

- o produto deverá ser DESATIVADO no SISCOMEX;
- não deverá ser excluído;
- o histórico deve ser preservado.

---

### Regra 6 — Reativação

Quando o produto for reenviado:

o sistema deverá:

1. verificar se o produto existe;
2. verificar se está desativado;
3. reativar/reimportar;
4. incrementar a versão.

---

## Nome técnico

```sql
U_DimEnv
```

## Tipo

```sql
nvarchar(10)
```

---

# 3. Campo: "Status Siscomex"

## Objetivo

Registrar status resumidos da integração.

---

## Regras

### Sucesso

Formato:

```text
DD/MM/YYYY HH:MM:SS Atualizado Portal Siscomex
```

---

### Erro

Formato:

```text
DD/MM/YYYY HH:MM:SS Erro Atualizando Portal Siscomex
```

---

### Produto desativado

Formato:

```text
DD/MM/YYYY HH:MM:SS Produto DESATIVADO
```

---

## Requisitos Técnicos

- Sempre registrar data/hora;
- Nunca deixar status inconsistente;
- Atualizar automaticamente;
- Garantir rastreabilidade.

---

## Nome técnico

```sql
U_DimStatus
```

## Tipo

```sql
nvarchar(100)
```

---

# 4. Campo: "Seq. Siscomex"

## Objetivo

Armazenar o valor:

```text
seq
```

retornado automaticamente pelo SISCOMEX.

---

## Regras

- Deve refletir o valor atual retornado;
- NÃO deve ser apagado ao desativar produto;
- Deve atualizar caso:
  - produto seja reativado;
  - novo seq seja retornado.

---

## Nome técnico

```sql
U_DimSeq
```

## Tipo

```sql
int
```

---

# 🔄 FLUXOS DE NEGÓCIO

---

# Cenário 1 — Novo Produto

## Fluxo esperado

1. Usuário cadastra produto;
2. Campo inicia como:
   
```text
Não enviar
```

3. Usuário altera para:
   
```text
Enviar
```

4. Sistema envia ao SISCOMEX;
5. Sistema recebe:
   - versão;
   - seq;
   - status;
6. SAP é atualizado automaticamente.

---

# Cenário 2 — Produto Atualizado

## Fluxo esperado

1. Produto já enviado;
2. Usuário altera informações;
3. Usuário define:
   
```text
Não enviar
```

4. Sistema desativa produto;
5. Usuário reenviará posteriormente;
6. Sistema verifica existência;
7. Sistema reativa produto;
8. Sistema incrementa versão;
9. Sistema atualiza seq.

---

