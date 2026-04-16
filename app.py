import streamlit as st
import pandas as pd
import plotly.express as px
from database import criar_tabelas, conectar
from auth import login, registrar
from utils import calcular_imc, classificar_imc, peso_ideal, analisar_progresso

st.set_page_config(page_title="App IMC PRO", layout="wide")
criar_tabelas()

st.title("📊 App de IMC Inteligente")

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# LOGIN
if not st.session_state.user_id:

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Registrar"])

    with tab1:
        user = st.text_input("Usuário", key="login_user")
        senha = st.text_input("Senha", type="password", key="login_pass")

        if st.button("Entrar", key="btn_login"):
            user_id = login(user, senha)
            if user_id:
                st.session_state.user_id = user_id
                st.success("Login realizado!")
                st.rerun()
            else:
                st.error("Credenciais inválidas")

    with tab2:
        new_user = st.text_input("Novo usuário", key="register_user")
        new_pass = st.text_input("Senha", type="password", key="register_pass")

        if st.button("Registrar", key="btn_register"):
            if registrar(new_user, new_pass):
                st.success("Usuário criado!")
            else:
                st.error("Erro ao registrar")

# APP
else:

    if st.sidebar.button("Sair", key="logout"):
        st.session_state.user_id = None
        st.rerun()

    conn = conectar()

    df = pd.read_sql_query(
        f"SELECT * FROM historico WHERE user_id = {st.session_state.user_id}",
        conn
    )

    cursor = conn.cursor()
    cursor.execute("SELECT peso_meta FROM usuarios WHERE id = ?", (st.session_state.user_id,))
    meta_usuario = cursor.fetchone()[0]

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📏 Calcular IMC", "🎯 Meta"])

    # DASHBOARD
    with tab1:

        if not df.empty:
            df["data"] = pd.to_datetime(df["data"])

            peso_atual = df["peso"].iloc[-1]
            altura = df["altura"].iloc[-1]
            imc = df["imc"].iloc[-1]
            ideal = peso_ideal(altura)

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Peso Atual", f"{peso_atual:.2f} kg")
            col2.metric("IMC", f"{imc:.2f}")
            col3.metric("Peso Ideal", f"{ideal:.2f} kg")

            if meta_usuario:
                col4.metric("Meta Usuário", f"{meta_usuario:.2f} kg")

            st.subheader("📈 Evolução do Peso")

            fig = px.line(
                df,
                x="data",
                y="peso",
                markers=True,
                title="Histórico de Peso"
            )

            fig.update_layout(height=400, hovermode="x unified")

            st.plotly_chart(fig, use_container_width=True)

            st.subheader("🧠 Insights")

            st.info(analisar_progresso(df))

            if len(df) > 1:
                diff = df["peso"].iloc[-2] - df["peso"].iloc[-1]

                if diff > 0:
                    st.success(f"👏 Você perdeu {diff:.2f} kg no último registro!")
                else:
                    st.warning("⚠️ Atenção ao progresso")

        else:
            st.info("Sem dados ainda")

    # CALCULAR
    with tab2:

        peso = st.number_input("Peso (kg)", min_value=1.0, key="peso_input")
        altura = st.number_input("Altura (m)", min_value=0.5, key="altura_input")

        if st.button("Calcular IMC", key="btn_calcular"):
            imc = calcular_imc(peso, altura)
            classificacao, dica = classificar_imc(imc)
            ideal = peso_ideal(altura)

            st.success(f"IMC: {imc:.2f}")
            st.write(classificacao)
            st.info(dica)
            st.write(f"🎯 Peso ideal: {ideal:.2f} kg")

            cursor.execute(
                "INSERT INTO historico (user_id, peso, altura, imc) VALUES (?, ?, ?, ?)",
                (st.session_state.user_id, peso, altura, imc)
            )
            conn.commit()

    # META
    with tab3:

        nova_meta = st.number_input("Defina sua meta (kg)", min_value=1.0, key="meta_input")

        if st.button("Salvar meta", key="btn_meta"):
            cursor.execute(
                "UPDATE usuarios SET peso_meta = ? WHERE id = ?",
                (nova_meta, st.session_state.user_id)
            )
            conn.commit()
            st.success("Meta salva!")

        if meta_usuario:
            st.write(f"Meta atual: {meta_usuario} kg")