import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# ============================================
# CONFIGURAÇÕES INICIAIS
# ============================================
st.set_page_config(
    page_title="Calculadora de IMC - Saúde+",
    page_icon="⚕️",
    layout="wide"
)

# ============================================
# FUNÇÕES DE CÁLCULO
# ============================================
def dsa_calcula_imc(peso, altura):
    return peso / (altura ** 2)

def calcular_peso_ideal(altura, sexo="feminino"):
    peso_min = 18.5 * (altura ** 2)
    peso_max = 24.9 * (altura ** 2)
    
    if sexo == "feminino":
        peso_ideal_devine = 45.5 + 2.3 * ((altura * 100) - 152.4) / 2.54
    else:
        peso_ideal_devine = 50 + 2.3 * ((altura * 100) - 152.4) / 2.54
    
    return peso_min, peso_max, peso_ideal_devine

def classificar_imc(imc, peso, altura, sexo="feminino"):
    peso_min, peso_max, peso_ideal = calcular_peso_ideal(altura, sexo)
    diferenca_peso = peso - peso_ideal
    
    if imc < 18.5:
        peso_a_ganhar = peso_min - peso
        return (
            "Abaixo do peso",
            f"Seu IMC é {imc:.1f}. Você está abaixo do peso ideal.",
            f"Peso ideal: entre **{peso_min:.1f} kg e {peso_max:.1f} kg**\n\nPrecisa ganhar **{peso_a_ganhar:.1f} kg**",
            "🔴 Riscos: Deficiências nutricionais, osteoporose, anemia, imunidade baixa.",
            "💡 Aumente ingestão calórica com alimentos nutritivos. Consulte nutricionista.",
            "⚠️",
            peso_min, peso_max, peso_ideal
        )
    
    elif 18.5 <= imc < 24.9:
        return (
            "Peso normal",
            f"Seu IMC é {imc:.1f}. Parabéns! Peso saudável.",
            f"Peso ideal: entre **{peso_min:.1f} kg e {peso_max:.1f} kg**\n\nContinue assim!",
            "🟢 Benefícios: Menor risco de doenças cardiovasculares e diabetes.",
            "💡 Mantenha alimentação balanceada e 150min de exercício/semana.",
            "✅",
            peso_min, peso_max, peso_ideal
        )
    
    elif 25 <= imc < 29.9:
        peso_a_perder = peso - peso_max
        return (
            "Sobrepeso",
            f"Seu IMC é {imc:.1f}. Você está com sobrepeso.",
            f"Peso ideal: entre **{peso_min:.1f} kg e {peso_max:.1f} kg**\n\nRecomenda-se perder **{peso_a_perder:.1f} kg**",
            "🟡 Riscos: Hipertensão, colesterol alto, diabetes tipo 2.",
            "💡 Reduza 300-500 calorias/dia. Aumente fibras. Exercício 30min 5x/semana.",
            "⚠️",
            peso_min, peso_max, peso_ideal
        )
    
    elif 30 <= imc < 34.9:
        peso_a_perder = peso - peso_max
        return (
            "Obesidade grau I",
            f"Seu IMC é {imc:.1f}. Obesidade grau I.",
            f"Peso ideal: entre **{peso_min:.1f} kg e {peso_max:.1f} kg**\n\nRecomenda-se perder **{peso_a_perder:.1f} kg**",
            "🟠 Riscos: Diabetes, hipertensão, doenças cardíacas, apneia.",
            "💡 Procure orientação médica. Metas realistas de 5-10% do peso.",
            "🔴",
            peso_min, peso_max, peso_ideal
        )
    
    elif 35 <= imc < 39.9:
        peso_a_perder = peso - peso_max
        return (
            "Obesidade grau II",
            f"Seu IMC é {imc:.1f}. Obesidade grau II (severa).",
            f"Peso ideal: entre **{peso_min:.1f} kg e {peso_max:.1f} kg**\n\nÉ necessário perder **{peso_a_perder:.1f} kg**",
            "🔴 Riscos: Elevado para todas as complicações da obesidade.",
            "💡 Acompanhamento médico multidisciplinar ESSENCIAL.",
            "🔴🔴",
            peso_min, peso_max, peso_ideal
        )
    
    else:
        peso_a_perder = peso - peso_max
        return (
            "Obesidade grau III",
            f"Seu IMC é {imc:.1f}. Obesidade grau III (mórbida).",
            f"Peso ideal: entre **{peso_min:.1f} kg e {peso_max:.1f} kg**\n\nÉ necessário perder **{peso_a_perder:.1f} kg**",
            "🔴🔴 Riscos: Extremamente elevado de mortalidade prematura.",
            "💡 URGENTE: Procure equipe médica especializada.",
            "🚨",
            peso_min, peso_max, peso_ideal
        )

# ============================================
# FUNÇÕES DE GERENCIAMENTO DE USUÁRIOS
# ============================================
def salvar_consulta(usuario, dados_consulta):
    """Salva uma consulta no histórico do usuário"""
    arquivo = f"historico_{usuario}.json"
    
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            historico = json.load(f)
    else:
        historico = []
    
    historico.append(dados_consulta)
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

def carregar_historico(usuario):
    """Carrega o histórico de consultas do usuário"""
    arquivo = f"historico_{usuario}.json"
    
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def listar_usuarios():
    """Lista todos os usuários cadastrados"""
    usuarios = []
    for arquivo in os.listdir('.'):
        if arquivo.startswith('historico_') and arquivo.endswith('.json'):
            usuario = arquivo.replace('historico_', '').replace('.json', '')
            usuarios.append(usuario)
    return sorted(usuarios)

def comparar_consultas(consulta_atual, consulta_anterior):
    """Compara duas consultas e retorna análise"""
    if not consulta_anterior:
        return None
    
    diferenca_peso = consulta_atual['peso'] - consulta_anterior['peso']
    diferenca_imc = consulta_atual['imc'] - consulta_anterior['imc']
    dias = (datetime.strptime(consulta_atual['data'], '%Y-%m-%d %H:%M:%S') - 
            datetime.strptime(consulta_anterior['data'], '%Y-%m-%d %H:%M:%S')).days
    
    if diferenca_peso < 0:
        tendencia = "✅ Perdeu peso"
        cor = "green"
    elif diferenca_peso > 0:
        tendencia = "⚠️ Ganhou peso"
        cor = "orange"
    else:
        tendencia = "➖ Peso mantido"
        cor = "blue"
    
    return {
        'diferenca_peso': diferenca_peso,
        'diferenca_imc': diferenca_imc,
        'dias': dias,
        'tendencia': tendencia,
        'cor': cor
    }

# ============================================
# INTERFACE PRINCIPAL
# ============================================
st.title("⚕️ Calculadora de IMC - Saúde+")
st.markdown("### Acompanhe sua evolução de forma inteligente")

# Sidebar para login/usuário
with st.sidebar:
    st.header("👤 Área do Usuário")
    
    # Opções de usuário
    modo = st.radio(
        "Escolha uma opção:",
        ["🔑 Login", "📝 Criar nova conta", "👀 Continuar sem salvar"],
        key="modo_usuario"
    )
    
    if modo == "🔑 Login":
        usuarios = listar_usuarios()
        if usuarios:
            usuario_selecionado = st.selectbox("Selecione seu perfil:", usuarios)
            if st.button("Entrar", use_container_width=True):
                st.session_state['usuario_logado'] = usuario_selecionado
                st.session_state['historico'] = carregar_historico(usuario_selecionado)
                st.success(f"✅ Bem-vindo(a) de volta, {usuario_selecionado}!")
                st.rerun()
        else:
            st.info("Nenhum usuário cadastrado ainda. Crie uma conta!")
    
    elif modo == "📝 Criar nova conta":
        novo_usuario = st.text_input("Nome de usuário:", placeholder="Ex: maria_silva")
        if st.button("Criar conta", use_container_width=True):
            if novo_usuario:
                if novo_usuario not in listar_usuarios():
                    st.session_state['usuario_logado'] = novo_usuario
                    st.session_state['historico'] = []
                    st.success(f"✅ Conta criada! Bem-vindo(a), {novo_usuario}!")
                    st.rerun()
                else:
                    st.error("❌ Nome de usuário já existe!")
            else:
                st.error("❌ Digite um nome de usuário!")
    
    else:
        if 'usuario_logado' in st.session_state:
            del st.session_state['usuario_logado']
        st.info("👋 Você não está logado. Os dados não serão salvos.")
    
    # Mostrar usuário logado
    if 'usuario_logado' in st.session_state:
        st.markdown("---")
        st.success(f"👤 Logado como: **{st.session_state['usuario_logado']}**")
        if st.button("🚪 Sair", use_container_width=True):
            del st.session_state['usuario_logado']
            st.rerun()
        
        # Mostrar número de consultas
        historico = carregar_historico(st.session_state['usuario_logado'])
        st.metric("📊 Total de consultas", len(historico))

# ============================================
# TABS PRINCIPAIS
# ============================================
if 'usuario_logado' in st.session_state:
    tab1, tab2, tab3 = st.tabs(["📊 Nova Consulta", "📈 Histórico", "🔄 Comparativo"])
else:
    tab1, tab2 = st.tabs(["📊 Calculadora", "ℹ️ Informações"])
    st.info("💡 **Dica:** Crie uma conta ou faça login para salvar seu histórico e acompanhar sua evolução!")

# ============================================
# TAB 1: CALCULADORA
# ============================================
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Seus Dados")
        
        # Dados básicos
        if 'usuario_logado' in st.session_state:
            nome = st.text_input("Nome completo (opcional)", placeholder="Ex: Maria Silva")
            idade = st.number_input("Idade", min_value=1, max_value=120, value=30)
        
        peso = st.number_input(
            "Peso atual (kg)", 
            min_value=20.0, 
            max_value=300.0,
            value=None, 
            placeholder="Ex: 70"
        )
        
        altura = st.number_input(
            "Altura (m)", 
            min_value=1.0, 
            max_value=2.5,
            value=None, 
            placeholder="Ex: 1.75"
        )
        
        sexo = st.radio("Sexo biológico", ["Feminino", "Masculino"], horizontal=True)
        
        # Dados adicionais para usuários logados
        if 'usuario_logado' in st.session_state:
            with st.expander("📋 Dados complementares (opcional)"):
                cintura = st.number_input("Circunferência da cintura (cm)", min_value=0.0, value=None)
                pratica_exercicio = st.selectbox("Pratica exercícios?", ["Selecione...", "Sim, regularmente", "Sim, ocasionalmente", "Não"])
                objetivo = st.selectbox("Objetivo principal", ["Manter peso", "Perder peso", "Ganhar peso", "Melhorar saúde"])
    
    with col2:
        st.subheader("ℹ️ Informações")
        st.info(
            """
            **O que é IMC?**
            
            O Índice de Massa Corporal (IMC) é uma medida internacional 
            usada para avaliar se uma pessoa está no peso ideal.
            
            **Classificação (OMS):**
            - Abaixo de 18.5: Abaixo do peso
            - 18.5 a 24.9: Peso normal
            - 25 a 29.9: Sobrepeso
            - 30 a 34.9: Obesidade grau I
            - 35 a 39.9: Obesidade grau II
            - Acima de 40: Obesidade grau III
            
            **Limitações:**
            - Não considera composição corporal
            - Não diferencia músculo de gordura
            """
        )
    
    st.markdown("---")
    
    if st.button("🔍 Calcular IMC", type="primary", use_container_width=True):
        if peso is not None and altura is not None and altura > 0 and peso > 0:
            imc = dsa_calcula_imc(peso, altura)
            (classificacao, resumo, peso_ideal_str, riscos, recomendacoes, 
             alerta, peso_min, peso_max, peso_ideal) = classificar_imc(imc, peso, altura, sexo.lower())
            
            # Salvar consulta se usuário estiver logado
            if 'usuario_logado' in st.session_state:
                consulta = {
                    'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'nome': nome if 'nome' in locals() else '',
                    'idade': idade if 'idade' in locals() else None,
                    'peso': peso,
                    'altura': altura,
                    'imc': round(imc, 2),
                    'classificacao': classificacao,
                    'sexo': sexo,
                    'cintura': cintura if 'cintura' in locals() and cintura > 0 else None,
                    'exercicio': pratica_exercicio if 'pratica_exercicio' in locals() else None,
                    'objetivo': objetivo if 'objetivo' in locals() else None,
                    'peso_ideal': round(peso_ideal, 2)
                }
                salvar_consulta(st.session_state['usuario_logado'], consulta)
                st.success("✅ Consulta salva no seu histórico!")
            
            # Resultados
            st.markdown("---")
            st.header("📋 Resultado da Análise")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Seu IMC", f"{imc:.1f}")
            with col2:
                st.metric("Classificação", classificacao)
            with col3:
                st.metric("Peso Ideal", f"{peso_ideal:.1f} kg")
            with col4:
                st.metric("Faixa Saudável", f"{peso_min:.1f} - {peso_max:.1f} kg")
            
            st.markdown("---")
            
            # Detalhes
            st.subheader(f"{alerta} {classificacao}")
            st.write(resumo)
            st.info(peso_ideal_str)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🏥 Riscos à Saúde")
                st.write(riscos)
            with col2:
                st.subheader("💡 Recomendações")
                st.success(recomendacoes)
            
            # Comparação com última consulta
            if 'usuario_logado' in st.session_state:
                historico = carregar_historico(st.session_state['usuario_logado'])
                if len(historico) >= 2:
                    st.markdown("---")
                    st.subheader("📊 Comparação com consulta anterior")
                    comparacao = comparar_consultas(consulta, historico[-2])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        delta = f"{comparacao['diferenca_peso']:+.1f} kg"
                        st.metric("Variação de Peso", f"{peso:.1f} kg", delta)
                    with col2:
                        delta = f"{comparacao['diferenca_imc']:+.1f}"
                        st.metric("Variação de IMC", f"{imc:.1f}", delta)
                    with col3:
                        st.metric("Dias entre consultas", f"{comparacao['dias']} dias")
                    
                    if comparacao['diferenca_peso'] < 0:
                        st.success(f"🎉 Parabéns! Você perdeu {abs(comparacao['diferenca_peso']):.1f} kg desde a última consulta!")
                    elif comparacao['diferenca_peso'] > 0:
                        st.warning(f"⚠️ Você ganhou {comparacao['diferenca_peso']:.1f} kg desde a última consulta.")
                    else:
                        st.info("➖ Seu peso se manteve estável desde a última consulta.")
        
        else:
            st.error("❌ Por favor, preencha peso e altura com valores válidos!")

# ============================================
# TAB 2: HISTÓRICO (apenas para logados)
# ============================================
if 'usuario_logado' in st.session_state:
    with tab2:
        st.header("📈 Seu Histórico de Consultas")
        
        historico = carregar_historico(st.session_state['usuario_logado'])
        
        if historico:
            # Criar DataFrame
            df = pd.DataFrame(historico)
            df['data'] = pd.to_datetime(df['data']).dt.strftime('%d/%m/%Y %H:%M')
            df = df.sort_values('data', ascending=False)
            
            # Métricas gerais
            col1, col2, col3 = st.columns(3)
            with col1:
                primeiro_peso = historico[0]['peso']
                ultimo_peso = historico[-1]['peso']
                variacao_total = ultimo_peso - primeiro_peso
                st.metric(
                    "Evolução Total", 
                    f"{ultimo_peso:.1f} kg",
                    f"{variacao_total:+.1f} kg"
                )
            
            with col2:
                st.metric("Total de Consultas", len(historico))
            
            with col3:
                if len(historico) >= 2:
                    dias_total = (datetime.strptime(historico[-1]['data'], '%Y-%m-%d %H:%M:%S') - 
                                 datetime.strptime(historico[0]['data'], '%Y-%m-%d %H:%M:%S')).days
                    st.metric("Período acompanhado", f"{dias_total} dias")
            
            st.markdown("---")
            
            # Gráfico de evolução
            st.subheader("📊 Evolução do Peso e IMC")
            
            df_grafico = pd.DataFrame(historico)
            df_grafico['data'] = pd.to_datetime(df_grafico['data'])
            df_grafico = df_grafico.sort_values('data')
            
            # Criar duas colunas para os gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                st.line_chart(df_grafico.set_index('data')['peso'], height=300)
                st.caption("Evolução do Peso (kg)")
            
            with col2:
                st.line_chart(df_grafico.set_index('data')['imc'], height=300)
                st.caption("Evolução do IMC")
            
            st.markdown("---")
            
            # Tabela de histórico
            st.subheader("📋 Histórico Detalhado")
            
            # Selecionar colunas para mostrar
            colunas_mostrar = ['data', 'peso', 'imc', 'classificacao', 'peso_ideal']
            df_display = df[colunas_mostrar].copy()
            df_display.columns = ['Data', 'Peso (kg)', 'IMC', 'Classificação', 'Peso Ideal']
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True
            )
            
            # Opção para exportar
            csv = df_display.to_csv(index=False)
            st.download_button(
                label="📥 Baixar histórico (CSV)",
                data=csv,
                file_name=f"historico_imc_{st.session_state['usuario_logado']}.csv",
                mime="text/csv"
            )
            
            # Estatísticas detalhadas
            with st.expander("📊 Estatísticas Detalhadas"):
                st.subheader("Análise Estatística")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Peso:**")
                    st.write(f"• Mínimo: {df_grafico['peso'].min():.1f} kg")
                    st.write(f"• Máximo: {df_grafico['peso'].max():.1f} kg")
                    st.write(f"• Média: {df_grafico['peso'].mean():.1f} kg")
                
                with col2:
                    st.write("**IMC:**")
                    st.write(f"• Mínimo: {df_grafico['imc'].min():.1f}")
                    st.write(f"• Máximo: {df_grafico['imc'].max():.1f}")
                    st.write(f"• Média: {df_grafico['imc'].mean():.1f}")
        
        else:
            st.info("📝 Nenhuma consulta registrada ainda. Faça sua primeira consulta na aba 'Nova Consulta'!")

# ============================================
# TAB 3: COMPARATIVO (apenas para logados)
# ============================================
if 'usuario_logado' in st.session_state:
    with tab3:
        st.header("🔄 Comparativo de Consultas")
        
        historico = carregar_historico(st.session_state['usuario_logado'])
        
        if len(historico) >= 2:
            st.write("Selecione duas consultas para comparar:")
            
            # Criar lista de datas para seleção
            datas = [f"{i+1}. {datetime.strptime(h['data'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')} - IMC: {h['imc']:.1f}" 
                    for i, h in enumerate(historico)]
            
            col1, col2 = st.columns(2)
            with col1:
                idx1 = st.selectbox("Consulta 1 (mais antiga)", range(len(datas)), format_func=lambda x: datas[x])
            with col2:
                idx2 = st.selectbox("Consulta 2 (mais recente)", range(len(datas)), 
                                   format_func=lambda x: datas[x], index=len(datas)-1 if datas else 0)
            
            if idx1 != idx2:
                consulta1 = historico[idx1]
                consulta2 = historico[idx2]
                
                # Garantir ordem cronológica
                if idx1 > idx2:
                    consulta1, consulta2 = consulta2, consulta1
                    idx1, idx2 = idx2, idx1
                
                comparacao = comparar_consultas(consulta2, consulta1)
                
                st.markdown("---")
                st.subheader("📊 Resultado da Comparação")
                
                # Métricas comparativas
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Peso",
                        f"{consulta2['peso']:.1f} kg",
                        f"{comparacao['diferenca_peso']:+.1f} kg"
                    )
                
                with col2:
                    st.metric(
                        "IMC",
                        f"{consulta2['imc']:.1f}",
                        f"{comparacao['diferenca_imc']:+.1f}"
                    )
                
                with col3:
                    st.metric(
                        "Classificação",
                        consulta2['classificacao'],
                        f"Era: {consulta1['classificacao']}"
                    )
                
                with col4:
                    st.metric(
                        "Dias entre consultas",
                        f"{comparacao['dias']}"
                    )
                
                # Análise de tendência
                st.markdown("---")
                
                if comparacao['diferenca_peso'] < 0:
                    if consulta2['imc'] < consulta1['imc']:
                        if consulta2['imc'] < 25 and consulta1['imc'] >= 25:
                            st.success("🎉 **PARABÉNS!** Você saiu da faixa de sobrepeso/obesidade!")
                        else:
                            st.success(f"✅ Ótimo progresso! Você perdeu {abs(comparacao['diferenca_peso']):.1f} kg.")
                    else:
                        st.success(f"👍 Você perdeu {abs(comparacao['diferenca_peso']):.1f} kg. Continue assim!")
                
                elif comparacao['diferenca_peso'] > 0:
                    st.warning(f"⚠️ Você ganhou {comparacao['diferenca_peso']:.1f} kg neste período.")
                    
                    # Análise do ganho
                    ganho_mensal = (comparacao['diferenca_peso'] / comparacao['dias']) * 30
                    if ganho_mensal > 2:
                        st.error(f"⚠️ Atenção: Ganho médio de {ganho_mensal:.1f} kg/mês. Recomenda-se avaliação profissional.")
                
                else:
                    st.info("➖ Seu peso permaneceu estável neste período.")
                
                # Recomendações baseadas na comparação
                st.markdown("---")
                st.subheader("💡 Análise e Recomendações")
                
                if comparacao['diferenca_peso'] < -5:
                    st.success(
                        "Excelente progresso! Perda de peso significativa. "
                        "Certifique-se de que está perdendo peso de forma saudável e sustentável."
                    )
                elif comparacao['diferenca_peso'] > 5:
                    st.warning(
                        "Ganho de peso significativo detectado. "
                        "Recomenda-se consultar um profissional de saúde para avaliação."
                    )
                
                if consulta2['imc'] < consulta1['imc'] and consulta2['imc'] >= 25:
                    st.info(
                        "Você está progredindo na direção certa! "
                        f"Mantenha o foco para atingir a faixa de peso normal (IMC < 25)."
                    )
                
            else:
                st.warning("Selecione duas consultas diferentes para comparar.")
        
        else:
            st.info("📝 Você precisa de pelo menos 2 consultas registradas para fazer comparações.")

# ============================================
# TAB 2 ALTERNATIVA: INFORMAÇÕES (não logado)
# ============================================
if 'usuario_logado' not in st.session_state:
    with tab2:
        st.header("ℹ️ Informações sobre Saúde")
        
        st.markdown("""
        ### Por que criar uma conta?
        
        Ao criar uma conta gratuita, você pode:
        
        - ✅ **Salvar** todas as suas consultas
        - 📈 **Acompanhar** sua evolução com gráficos
        - 🔄 **Comparar** resultados entre consultas
        - 📊 **Exportar** seu histórico completo
        - 🎯 **Definir e acompanhar** suas metas
        
        ### Como funciona?
        
        1. Clique em "Criar nova conta" na barra lateral
        2. Escolha um nome de usuário
        3. Pronto! Seus dados ficarão salvos automaticamente
        
        ### Seus dados estão seguros
        
        Todas as informações são armazenadas localmente no seu computador.
        Nenhum dado é enviado para servidores externos.
        """)
        
        st.image("https://via.placeholder.com/800x400/667eea/ffffff?text=Sua+Saúde+em+Primeiro+Lugar", 
                 use_container_width=True)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "⚕️ Calculadora de IMC - Saúde+ | Informações baseadas em diretrizes da OMS | "
    "Consulte sempre um profissional de saúde"
    "</p>", 
    unsafe_allow_html=True
)
