import streamlit as st
import sqlite3
conn = sqlite3.connect("daa.db")
import pandas as pd

st.set_page_config(page_title="dashbord vendas",layout="wide")


c = conn.cursor()
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS tabelavend(numnota NUMBER, cliente TEXT, data TEXT, valor number)') 

def add_user_data(cliente,valors,numnota,datas):
    c.execute('INSERT INTO tabelavend(numnota,cliente,data,valor) VALUES (?,?,?,?)', (cliente, valors,numnota,datas))
    conn.commit()
def login_user(cliente, valors, numnota, datas):
    c.execute('SELECT * FROM tabelavend WHERE cliente =? AND valor =? AND numnota =? AND data =?', (cliente, valors,numnota,datas))
    data = c.fetchall()
    return data
def view_all_users():
    c.execute('SELECT * FROM tabelavend')
    data = c.fetchall()
    return data
def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS userstabless(username TEXT, password TEXT)')

def add_user_datas(username, password):
    c.execute('INSERT INTO userstabless(username,password) VALUES (?,?)', (username, password))
    conn.commit()
def login_users(username, password):
    c.execute('SELECT * FROM userstabless WHERE username =? AND password =?', (username, password))
    data = c.fetchall()
    return data
def main():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Usuário")
    password = st.sidebar.text_input("Senha", type="password")
    boton = st.sidebar.radio(label="opções", options=["entrar"], horizontal=True,label_visibility="hidden")
    if boton == "entrar":
        create_table()
        create_tables()
        result = login_users(username, password)
        if result:
            tab1, tab2, tab3= st.tabs(["Dashbord", "Análise geral", "Incluir cliente"])
            with tab3:
                col1, col2 = st.columns(2)
                with col1.form(key ="clientes"):
                    nome = st.text_input(label="nome do cliente")
                    valor = st.number_input(label="valor da venda",format="%f")
                    nota = st.number_input(label="número da nota", format="%i", step=1)
                    data = st.date_input(label="data de entrega")
                    botao = st.form_submit_button("Enviar")
                if botao:
                    if nome and valor and nota and data:
                        st.success("venda cadastrada com sucesso!")
                        create_table()
                        add_user_data(nota, nome, data, valor)
                    else:
                        st.error("Error!")
            dados = pd.DataFrame(view_all_users(), columns=["numnota", "cliente", "data","valor"])
            dados["mês"] = dados["data"].str.split("-").str[1]
            dados["ano"] = dados["data"].str.split("-").str[0]
            ano = dados["ano"].value_counts().index.sort_values()
            mes = dados["mês"].value_counts().index.sort_values()
            
            with tab1:
                col3, col4 = st.columns(2)
                anos = col3.radio("ANO", ano, horizontal=True)
                mess = col4.selectbox("MÊS", mes)
                dados_ano = dados[dados["ano"] == anos]
                dados_mes = dados[dados["mês"] == mess]
                col3.bar_chart(dados_ano[["mês", "valor"]].groupby("mês").sum())
                col4.bar_chart(dados_mes[["ano", "valor"]].groupby("ano").sum())
            with tab2:
                dados = dados.drop("ano", axis=1)
                dados = dados.drop("mês", axis=1)
                dados_clientes = dados["cliente"].value_counts().index
                col5, col6 = st.columns(2)
                check = st.checkbox("todos os itens")
                if check:
                    cliente = col5.selectbox("Cliente",dados_clientes )
                    dados_stats = dados[dados["cliente"] == cliente]
                    st.dataframe(dados, column_config={
                    "numnota": st.column_config.NumberColumn(format="%i"),
                    "data": st.column_config.DateColumn(format="DD/MM/YYYY")
                })
                else:
                    cliente = col5.selectbox("Cliente",dados_clientes )
                    dados_stats = dados[dados["cliente"] == cliente]
                    st.dataframe(dados_stats, column_config={
                    "numnota": st.column_config.NumberColumn(format="%i"),
                    "data": st.column_config.DateColumn(format="DD/MM/YYYY"),
                    "cliente": st.column_config.TextColumn(width="large"),
                })

        else:
            st.title("ANÁLISE DE VENDAS")
            st.text("faça o login para acessar o dashbord!")
            st.sidebar.warning("senha/usuário incorreto")
if __name__ == "__main__":
    main()
    
