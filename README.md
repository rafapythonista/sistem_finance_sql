# 💰 Sistema de Finanças (Python + SQL)

Este é um sistema de controle financeiro que roda direto no terminal. Criei esse projeto para aplicar na prática a integração de código Python com bancos de dados relacionais (SQL). 

O sistema funciona como um aplicativo de finanças real: ele permite cadastrar movimentações, calcula o saldo automaticamente e gera relatórios de gastos direto de um banco de dados local.

---

## 🛠️ Tecnologias Utilizadas

*   **Linguagem principal:** Python 3
*   **Organização de dados:** Pandas (`DataFrames`)
*   **Conexão com o Banco:** SQLAlchemy
*   **Banco de Dados:** SQL (SQLite pela praticidade de rodar direto no computador)

---

## 🚀 O que o Sistema Faz

O menu do terminal foi construído para ser simples e interativo:

*   **[ 1 ] Ver Extrato Completo:** Busca no banco de dados todas as transações e mostra na tela, organizadas da mais recente para a mais antiga (`ORDER BY data DESC`).
*   **[ 2 ] Cadastrar Nova Transação:** Salva novas receitas ou despesas direto no banco SQL. O código tem uma proteção (`try/except`) para o sistema não quebrar caso o usuário digite um valor inválido (como letras).
*   **[ 3 ] Ver Resumo Geral (Saldo):** O banco soma todas as receitas e despesas (`SUM` e `GROUP BY`) e calcula o saldo atual em tempo real. Se a conta estiver negativa, o sistema solta um alerta vermelho.
*   **[ 4 ] Ver Gastos por Categoria:** Mostra para onde o dinheiro está indo, agrupando as despesas e ordenando do maior gasto para o menor.

---

## 🖥️ Como Executar o Projeto

### 1. Instale as bibliotecas necessárias
Abra o terminal do seu computador e rode o comando abaixo para instalar o Pandas e o conector do banco:

```bash
pip install pandas sqlalchemy
```

### 2. Rode o código
Com as bibliotecas instaladas, execute o arquivo principal:

```bash
python seu_arquivo_financas.py
```

*Nota: Não precisa se preocupar em criar o banco de dados antes. Na primeira vez que você rodar, o próprio script percebe que o arquivo não existe, cria o `banco.db` do zero e já coloca alguns dados de teste para você ver o sistema funcionando de cara!*
