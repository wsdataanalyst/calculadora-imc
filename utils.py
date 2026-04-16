def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso", "Aumente a ingestão calórica com orientação profissional."
    elif imc < 25:
        return "Peso normal", "Continue com bons hábitos!"
    elif imc < 30:
        return "Sobrepeso", "Ajuste alimentação e pratique exercícios."
    elif imc < 35:
        return "Obesidade grau 1", "Procure orientação profissional."
    elif imc < 40:
        return "Obesidade grau 2", "Acompanhamento médico recomendado."
    else:
        return "Obesidade grau 3", "Procure ajuda médica com urgência."

def peso_ideal(altura):
    return 22 * (altura ** 2)

def analisar_progresso(df):
    if len(df) < 2:
        return "Dados insuficientes para análise."

    peso_inicial = df["peso"].iloc[0]
    peso_atual = df["peso"].iloc[-1]

    perda_total = peso_inicial - peso_atual
    media = perda_total / len(df)

    if perda_total > 0:
        return f"📉 Você perdeu {perda_total:.2f} kg (média {media:.3f} por registro). Excelente!"
    elif perda_total < 0:
        return f"📈 Houve ganho de {abs(perda_total):.2f} kg. Atenção!"
    else:
        return "⚖️ Peso estável."