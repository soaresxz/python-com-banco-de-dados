# -*- coding: utf-8 -*-
import sqlite3
from datetime import date

# Nome do arquivo do banco de dados
DB_NAME = "empresa.db"

def setup_database():
    """
    Cria o banco de dados e as tabelas 'clientes' e 'pedidos' se não existirem.
    Habilita o suporte a chaves estrangeiras.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Habilita o suporte a chaves estrangeiras no SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # [cite_start]Cria a tabela de clientes [cite: 2]
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        telefone TEXT
    );
    """)

    # [cite_start]Cria a tabela de pedidos [cite: 2]
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto TEXT NOT NULL,
        valor REAL NOT NULL,
        data DATE NOT NULL,
        cliente_id INTEGER NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

# [cite_start]--- Funções CRUD para Clientes --- [cite: 2]

def adicionar_cliente(nome, email, telefone):
    """Adiciona um novo cliente ao banco de dados."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)", (nome, email, telefone))
        conn.commit()
        print(f"\n✅ Cliente '{nome}' adicionado com sucesso!")
    except sqlite3.IntegrityError:
        print(f"\n❌ Erro: O email '{email}' já está cadastrado.")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro: {e}")
    finally:
        conn.close()

def listar_clientes():
    """Exibe todos os clientes cadastrados."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, telefone FROM clientes")
    clientes = cursor.fetchall()
    conn.close()

    if not clientes:
        print("\nℹ️ Nenhum cliente cadastrado.")
    else:
        print("\n--- Lista de Clientes ---")
        for cliente in clientes:
            print(f"ID: {cliente[0]} | Nome: {cliente[1]} | Email: {cliente[2]} | Telefone: {cliente[3]}")
        print("------------------------")

def atualizar_cliente(cliente_id, nome, email, telefone):
    """Atualiza os dados de um cliente existente."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE clientes 
        SET nome = ?, email = ?, telefone = ? 
        WHERE id = ?
        """, (nome, email, telefone, cliente_id))
        
        if cursor.rowcount == 0:
            print(f"\n❌ Erro: Nenhum cliente encontrado com o ID {cliente_id}.")
        else:
            conn.commit()
            print(f"\n✅ Cliente ID {cliente_id} atualizado com sucesso!")
    except sqlite3.IntegrityError:
        print(f"\n❌ Erro: O email '{email}' já pertence a outro cliente.")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro: {e}")
    finally:
        conn.close()

def deletar_cliente(cliente_id):
    """Deleta um cliente e seus pedidos associados (devido ao ON DELETE CASCADE)."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        
        if cursor.rowcount == 0:
            print(f"\n❌ Erro: Nenhum cliente encontrado com o ID {cliente_id}.")
        else:
            conn.commit()
            print(f"\n✅ Cliente ID {cliente_id} e todos os seus pedidos foram deletados com sucesso.")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro: {e}")
    finally:
        conn.close()


# [cite_start]--- Funções CRUD para Pedidos --- [cite: 2]

def adicionar_pedido(cliente_id, produto, valor):
    """Adiciona um novo pedido para um cliente."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Verifica se o cliente existe
        cursor.execute("SELECT id FROM clientes WHERE id = ?", (cliente_id,))
        if not cursor.fetchone():
            print(f"\n❌ Erro: Cliente com ID {cliente_id} não encontrado.")
            return

        data_hoje = date.today().isoformat()
        cursor.execute("INSERT INTO pedidos (cliente_id, produto, valor, data) VALUES (?, ?, ?, ?)",
                       (cliente_id, produto, valor, data_hoje))
        conn.commit()
        print(f"\n✅ Pedido para o cliente ID {cliente_id} adicionado com sucesso!")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro: {e}")
    finally:
        conn.close()

def listar_pedidos_com_clientes():
    """Lista todos os pedidos, relacionando-os com os nomes dos clientes."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # [cite_start]Consulta que relaciona pedidos aos seus clientes [cite: 2]
    cursor.execute("""
    SELECT 
        p.id, p.produto, p.valor, p.data,
        c.nome, c.email
    FROM pedidos p
    JOIN clientes c ON p.cliente_id = c.id
    ORDER BY c.nome, p.data DESC
    """)
    pedidos = cursor.fetchall()
    conn.close()

    if not pedidos:
        print("\nℹ️ Nenhum pedido cadastrado.")
    else:
        print("\n--- Lista de Todos os Pedidos ---")
        for pedido in pedidos:
            print(f"Pedido ID: {pedido[0]} | Produto: {pedido[1]} | Valor: R${pedido[2]:.2f} | Data: {pedido[3]} | Cliente: {pedido[4]} ({pedido[5]})")
        print("---------------------------------")


# [cite_start]--- Interface do Menu Interativo --- [cite: 3]

def menu():
    """Exibe o menu principal e gerencia a entrada do usuário."""
    while True:
        print("\n--- Sistema de Cadastro ---")
        print("--- Gerenciar Clientes ----")
        print("1. Adicionar Cliente")
        print("2. Listar Clientes")
        print("3. Atualizar Cliente")
        print("4. Deletar Cliente")
        print("---- Gerenciar Pedidos ----")
        print("5. Adicionar Pedido")
        print("6. Listar Todos os Pedidos")
        print("---------------------------")
        print("0. Sair")
        
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            nome = input("Nome do cliente: ")
            email = input("Email do cliente: ")
            telefone = input("Telefone do cliente: ")
            adicionar_cliente(nome, email, telefone)
        
        elif escolha == '2':
            listar_clientes()
            
        elif escolha == '3':
            try:
                cliente_id = int(input("ID do cliente a ser atualizado: "))
                nome = input("Novo nome: ")
                email = input("Novo email: ")
                telefone = input("Novo telefone: ")
                atualizar_cliente(cliente_id, nome, email, telefone)
            except ValueError:
                print("\n❌ ID inválido. Por favor, digite um número.")

        elif escolha == '4':
            try:
                cliente_id = int(input("ID do cliente a ser deletado: "))
                deletar_cliente(cliente_id)
            except ValueError:
                print("\n❌ ID inválido. Por favor, digite um número.")

        elif escolha == '5':
            try:
                cliente_id = int(input("ID do cliente para o pedido: "))
                produto = input("Nome do produto: ")
                valor = float(input("Valor do pedido: "))
                adicionar_pedido(cliente_id, produto, valor)
            except ValueError:
                print("\n❌ ID ou valor inválido. Por favor, digite números.")

        elif escolha == '6':
            listar_pedidos_com_clientes()
            
        elif escolha == '0':
            print("\n👋 Saindo do sistema. Até logo!")
            break
        else:
            print("\n❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    setup_database() # Garante que o banco de dados e as tabelas existam
    menu()