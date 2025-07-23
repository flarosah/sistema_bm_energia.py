
import streamlit as st
import pandas as pd

st.set_page_config(page_title="BM Energia - Análise e Comparação", layout="wide")

st.title("🔌 Sistema BM Energia")
st.markdown("Sistema completo para análise de faturas, comparação de propostas e simulação no Mercado Livre de Energia.")

# Upload da fatura
fatura = st.file_uploader("📥 Faça upload da fatura em Excel (.xlsx)", type=["xlsx"])

if fatura:
    st.success("Fatura carregada com sucesso!")
    faturas = pd.read_excel(fatura, sheet_name=None)
    for sheet, df in faturas.items():
        st.subheader(f"📄 Unidade: {sheet}")
        st.dataframe(df)

st.markdown("---")

# Simulador PRC
st.header("🧮 Simulador de Preço de Referência Comparável (PRC)")
preco_base = st.number_input("Preço base estimado (R$/MWh)", value=320.00)
incluir_icms = st.checkbox("Incluir ICMS no cálculo")
sazonalizacao = st.checkbox("Aplicar sazonalização")
encargos = st.checkbox("Incluir encargos setoriais")
sustentavel = st.checkbox("Adicionar atributos sustentáveis (IREC, Carbono Neutro)")

ajuste = 0
ajuste += 20 if incluir_icms else 0
ajuste += 10 if sazonalizacao else 0
ajuste += 15 if encargos else 0
ajuste += 5 if sustentavel else 0

preco_final = preco_base + ajuste
st.success(f"💡 PRC Ajustado: R$ {preco_final:.2f}/MWh")

# Exportação
if st.button("📤 Exportar resultado (Excel)"):
    resultado = pd.DataFrame({
        "Base (R$/MWh)": [preco_base],
        "Ajustes (R$/MWh)": [ajuste],
        "PRC Final (R$/MWh)": [preco_final]
    })
    resultado.to_excel("resultado_prc.xlsx", index=False)
    with open("resultado_prc.xlsx", "rb") as f:
        st.download_button("📄 Baixar Excel", f, file_name="PRC_BM_Energia.xlsx")
