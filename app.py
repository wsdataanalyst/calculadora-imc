import streamlit as st

def dsa_calcula_imc(peso, altura):
    return peso / (altura ** 2)

st.title("Calculadora de IMC")

peso = st.number_input("Peso (kg)", min_value=0.0)
altura = st.number_input("Altura (m)", min_value=0.0)

if st.button("Calcular"):
    if altura > 0:
        imc = dsa_calcula_imc(peso, altura)
        st.success(f"Seu IMC é: {imc:.2f}")
    else:
        st.error("Altura deve ser maior que zero")