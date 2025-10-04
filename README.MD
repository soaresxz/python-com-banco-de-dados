# Sistema de Cadastro de Clientes e Pedidos

Este projeto é uma implementação em Python de um sistema de cadastro para gerenciar clientes e seus respectivos pedidos, como parte de uma atividade acadêmica.

## [cite_start]📋 Funcionalidades [cite: 2]

O sistema oferece as seguintes operações:

* **Gerenciamento de Clientes:**
    * Adicionar um novo cliente.
    * Listar todos os clientes cadastrados.
    * Atualizar as informações de um cliente existente.
    * Deletar um cliente (o que também remove todos os pedidos associados a ele).

* **Gerenciamento de Pedidos:**
    * Adicionar um novo pedido para um cliente existente.
    * Listar todos os pedidos, exibindo os detalhes do cliente associado.

## [cite_start]🛠️ Estrutura do Banco de Dados [cite: 2]

O sistema utiliza um banco de dados SQLite (`empresa.db`) com duas tabelas:

1.  **`clientes`**: Armazena os dados dos clientes.
    * `id` (Chave Primária, Autoincremento)
    * `nome` (Texto)
    * `email` (Texto, Único)
    * `telefone` (Texto)
2.  **`pedidos`**: Armazena os pedidos, com uma chave estrangeira para a tabela de clientes.
    * `id` (Chave Primária, Autoincremento)
    * `cliente_id` (Chave Estrangeira para `clientes.id`)
    * `produto` (Texto)
    * `valor` (Decimal)
    * `data` (Data)

## 🚀 Como Usar

### Pré-requisitos

* Python 3 instalado em seu sistema.

### Execução

1.  Salve o código principal em um arquivo chamado `sistema_cadastro.py`.
2.  Abra um terminal ou prompt de comando na pasta onde você salvou o arquivo.
3.  Execute o script com o seguinte comando:
    ```bash
    python sistema_cadastro.py
    ```
4.  O banco de dados `empresa.db` será criado automaticamente na primeira execução.
5.  [cite_start]Siga as instruções do menu interativo para usar o sistema. [cite: 3]