import streamlit as st
import pandas as pd
import psycopg2

# URL de conexão com o Supabase (Porta 5432 / Pooler)
DB_URL = "postgresql://postgres.djhuawnkygdvlmzrvija:senhalanchonete@aws-0-sa-east-1.pooler.supabase.com:5432/postgres"

st.title("🍔 Lanchonete Universitária")
st.write("Painel e Cadastro - Integrado com Supabase.")

st.divider()

# Seção para inserir novo pedido
st.subheader("➕ Novo Pedido")
with st.form("form_novo_pedido"):
    item_pedido = st.text_input("Descrição do Pedido (Ex: X-Salada)")
    id_cliente = st.number_input("Número do Cliente (ID)", min_value=1, step=1, format="%d")
    
    enviar = st.form_submit_button("Cadastrar Pedido")

    if enviar:
        if item_pedido.strip() == "":
            st.warning("⚠️ Por favor, digite a descrição do pedido.")
        else:
            try:
                conn = psycopg2.connect(DB_URL)
                conn.autocommit = True
                cursor = conn.cursor()
                
                # Inserção no banco (o id_pedido pode ser autoincremento se a tabela estiver configurada)
                cursor.execute(
                    "INSERT INTO pedido (item, id_cliente) VALUES (%s, %s);",
                    (item_pedido, id_cliente)
                )
                
                cursor.close()
                conn.close()
                st.success(f"✅ Pedido '{item_pedido}' cadastrado com sucesso para o cliente ID {id_cliente}!")
            except Exception as e:
                st.error(f"Erro ao inserir pedido: {e}")

st.divider()
st.subheader("📋 Relatório de Pedidos em Tempo Real")

if st.button("🔄 Atualizar Lista"):
    st.rerun()

try:
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True

    # Consulta SQL com JOIN entre Pedido e Cliente
    query = 'SELECT cliente.nome AS "Cliente", pedido.item AS "Produto Pedido" FROM pedido JOIN cliente ON pedido.id_cliente = cliente.id_cliente'

    df = pd.read_sql(query, conn)
    conn.close()

    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
