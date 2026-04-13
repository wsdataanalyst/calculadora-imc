import streamlit as st

def dsa_calcula_imc(peso, altura):
    return peso / (altura ** 2)

def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso", "Seu peso está abaixo do ideal. Isso pode indicar desnutrição ou outros problemas de saúde.", "Procure um nutricionista e aumente a ingestão de alimentos nutritivos."
    
    elif 18.5 <= imc < 24.9:
        return "Peso normal", "Parabéns! Seu peso está dentro da faixa considerada saudável.", "Mantenha uma alimentação equilibrada e pratique atividades físicas regularmente."
    
    elif 25 <= imc < 29.9:
        return "Sobrepeso", "Você está acima do peso ideal, o que pode aumentar riscos de doenças.", "Tente melhorar sua alimentação e aumentar o nível de atividade física."
    
    elif 30 <= imc < 34.9:
        return "Obesidade grau I", "Nível inicial de obesidade, com riscos à saúde.", "Busque orientação médica e adote hábitos saudáveis."
    
    elif 35 <= imc < 39.9:
        return "Obesidade grau II", "Obesidade moderada com riscos elevados.", "Procure acompanhamento médico e nutricional."
    
    else:
        return "Obesidade grau III", "Obesidade grave, com alto risco à saúde.", "É essencial acompanhamento médico especializado."

st.title("Calculadora de IMC")

# Inputs sem valor padrão
peso = st.number_input("Peso (kg)", min_value=0.0, value=None, placeholder="Ex: 70")
altura = st.number_input("Altura (m)", min_value=0.0, value=None, placeholder="Ex: 1.75")

if st.button("Calcular"):
    if peso is not None and altura is not None and altura > 0:
        imc = dsa_calcula_imc(peso, altura)
        classificacao, descricao, dica = classificar_imc(imc)

        st.success(f"Seu IMC é: {imc:.2f}")
        st.info(f"Classificação: {classificacao}")
        st.write(descricao)
        st.warning(f"Dica: {dica}")
    else:
        st.error("Preencha peso e altura corretamente")
