import sqlite3
import streamlit as st
st.set_page_config(page_title="Players",
                    layout="wide")

conn = sqlite3.connect("daa.db")
c = conn.cursor()
def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS userstabless(username TEXT, password TEXT)')

def add_user_datas(username, password):
    c.execute('INSERT INTO userstabless(username,password) VALUES (?,?)', (username, password))
    conn.commit()
def login_users(username, password):
    c.execute('SELECT * FROM userstabless WHERE username =? AND password =?', (username, password))
    data = c.fetchall()
    return data
st.sidebar.title("Cadastre-se")
novo_user = st.sidebar.text_input("usuário")
new_password = st.sidebar.text_input("senha", type="password")
st.title("ANÁLISE DE VENDAS")
st.text("faça o login para acessar o dashbord!")
if st.sidebar.button("inscrever-se"):
    create_tables()
    add_user_datas(novo_user, new_password)
    st.success("você criou uma conta!")
    st.info("vá para o a aba de login para logar!")