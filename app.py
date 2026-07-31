import streamlit as st
import pandas as pd
import psycopg2

# URL de conexão direta com o Supabase (Porta 5432)
DB_URL = "postgresql://postgres:senhalachonete@db.seu-id-do-projeto.supabase.co:5432/postgres"

st.title("🍔 Lanchonete Universitária")
st.write("Painel de Visualização - Integrado com Supabase.")

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
