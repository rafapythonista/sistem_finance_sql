import os
import pandas as pd
from sqlalchemy import create_engine

# =====================================================================
# 1. CONEXÃO E INFRAESTRUTURA
# =====================================================================
engine = create_engine('sqlite:///banco.db')

def inicializar_banco():
    """Cria dados iniciais apenas se o banco de dados não existir."""
    # Criando transações fictícias iniciais para teste
    dados_iniciais = {
        'data': ['2026-01-05', '2026-01-10', '2026-01-15', '2026-02-05', '2026-02-12', '2026-03-01'],
        'categoria': ['Salário', 'Moradia', 'Alimentação', 'Salário', 'Alimentação', 'Investimentos'],
        'tipo': ['Receita', 'Despesa', 'Despesa', 'Receita', 'Despesa', 'Receita'],
        'valor': [5000.00, 1500.00, 350.20, 5000.00, 410.50, 250.00],
        'descricao': ['Depósito Mensal', 'Aluguel apto', 'Supermercado', 'Depósito Mensal', 'Restaurantes', 'Dividendos']
    }
    
    # Criamos a tabela se ela não existir
    try:
        query = "SELECT count(*) FROM transacoes"
        pd.read_sql(query, con=engine)
    except:
        df = pd.DataFrame(dados_iniciais)
        df.to_sql('transacoes', con=engine, if_exists='replace', index=False)
        print("💡 Banco de dados criado do zero com dados de teste!")

# =====================================================================
# 2. OPERAÇÕES BANCO DE DADOS
# =====================================================================
def registrar_transacao(data, categoria, tipo, valor, descricao):
    """Insere um novo registro no banco SQL via Pandas."""
    nova_linha = pd.DataFrame([{
        'data': data,
        'categoria': categoria,
        'tipo': tipo,
        'valor': float(valor),
        'descricao': descricao
    }])
    nova_linha.to_sql('transacoes', con=engine, if_exists='append', index=False)

def obter_extrato():
    return pd.read_sql("SELECT data, categoria, tipo, valor, descricao FROM transacoes ORDER BY data DESC", con=engine)

def obter_resumo_financeiro():
    # Executa a query agrupando por tipo (Receita vs Despesa)
    df = pd.read_sql("SELECT tipo, SUM(valor) as total FROM transacoes GROUP BY tipo", con=engine)
    
    # Processa os dados para calcular o saldo final na tela
    receitas = df[df['tipo'] == 'Receita']['total'].sum()
    despesas = df[df['tipo'] == 'Despesa']['total'].sum()
    saldo = receitas - despesas
    return receitas, despesas, saldo

def obter_gastos_por_categoria():
    query = """
        SELECT categoria, SUM(valor) as total 
        FROM transacoes 
        WHERE tipo = 'Despesa' 
        GROUP BY categoria 
        ORDER BY total DESC
    """
    return pd.read_sql(query, con=engine)

# =====================================================================
# 3. INTERFACE DE TERMINAL INTERATIVA
# =====================================================================
def exibir_menu():
    print("\n" + "="*40)
    print("      💰 SISTEMA DE FINANÇAS PYTHON SQL 💰")
    print("="*40)
    print("[ 1 ] Ver Extrato Completo")
    print("[ 2 ] Cadastrar Nova Transação (Receita/Despesa)")
    print("[ 3 ] Ver Resumo Geral (Saldo)")
    print("[ 4 ] Ver Gastos por Categoria")
    print("[ 0 ] Sair do Sistema")
    print("="*40)

def loop_principal():
    inicializar_banco()
    
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n📋 EXTRATO COMPLETO:")
            df = obter_extrato()
            if df.empty:
                print("Nenhuma transação encontrada.")
            else:
                print(df.to_string(index=False))
                
        elif opcao == "2":
            print("\n✍️ NOVO CADASTRO:")
            data = input("Data (AAAA-MM-DD) [Ex: 2026-03-15]: ").strip()
            categoria = input("Categoria (Ex: Alimentação, Lazer, Salário): ").strip().capitalize()
            
            tipo = ""
            while tipo not in ["1", "2"]:
                tipo = input("Tipo: [ 1 ] Receita  |  [ 2 ] Despesa: ").strip()
            tipo = "Receita" if tipo == "1" else "Despesa"
            
            try:
                valor = float(input("Valor (R$): ").strip().replace(',', '.'))
            except ValueError:
                print("⚠️ Valor inválido! Operação cancelada.")
                continue
                
            descricao = input("Descrição curta: ").strip()
            
            registrar_transacao(data, categoria, tipo, valor, descricao)
            print(f"\n✅ Sucesso! '{descricao}' adicionado ao banco SQL.")
            
        elif opcao == "3":
            receitas, despesas, saldo = obter_resumo_financeiro()
            print("\n📊 BALANÇO GERAL:")
            print(f"🟢 Total Receitas: R$ {receitas:.2f}")
            print(f"🔴 Total Despesas: R$ {despesas:.2f}")
            print(f"🔹 Saldo Atual:    R$ {saldo:.2f}")
            if saldo < 0:
                print("⚠️ Atenção: Sua conta está no vermelho!")
                
        elif opcao == "4":
            print("\n🔍 GASTOS POR CATEGORIA:")
            df = obter_gastos_por_categoria()
            if df.empty:
                print("Nenhuma despesa registrada.")
            else:
                print(df.to_string(index=False))
                
        elif opcao == "0":
            print("\n👋 Saindo do sistema... Até logo!")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")

if __name__ == '__main__':
    loop_principal()
