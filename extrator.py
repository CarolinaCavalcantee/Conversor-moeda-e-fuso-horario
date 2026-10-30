import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(page_title="Conversor de Moedas", page_icon="💱", layout="centered")

URL_API = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL"

MOEDAS = {
    "BRL": "🇧🇷 Real (BRL)",
    "USD": "🇺🇸 Dólar (USD)",
    "EUR": "🇪🇺 Euro (EUR)",
    "BTC": "₿ Bitcoin (BTC)",
}


@st.cache_data(ttl=30, show_spinner=False)
def buscar_cotacoes():
    resposta = requests.get(URL_API, timeout=10)
    resposta.raise_for_status()
    return resposta.json()


def processar_fuso_horario(timestamp_api):
    try:
        data_utc = datetime.fromtimestamp(int(timestamp_api), ZoneInfo("UTC"))
        data_local = data_utc.astimezone(ZoneInfo("America/Maceio"))
        return data_local.strftime("%d/%m/%Y às %H:%M:%S (%Z)")
    except Exception as erro:
        return f"Não foi possível converter o fuso horário: {erro}"


def montar_taxas_em_brl(dados_api):
    return {
        "BRL": 1.0,
        "USD": float(dados_api["USDBRL"]["bid"]),
        "EUR": float(dados_api["EURBRL"]["bid"]),
        "BTC": float(dados_api["BTCBRL"]["bid"]),
    }


def converter(valor, moeda_origem, moeda_destino, taxas):
    valor_em_brl = valor * taxas[moeda_origem]
    return valor_em_brl / taxas[moeda_destino]


def formatar(valor, moeda):
    casas = 8 if moeda == "BTC" else 2
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def inverter_moedas():
    origem = st.session_state["moeda_origem"]
    st.session_state["moeda_origem"] = st.session_state["moeda_destino"]
    st.session_state["moeda_destino"] = origem


if "moeda_origem" not in st.session_state:
    st.session_state["moeda_origem"] = "USD"
if "moeda_destino" not in st.session_state:
    st.session_state["moeda_destino"] = "BRL"


st.title("Conversor de Moedas")
st.caption("Cotações em tempo real. O resultado aparece sozinho, sem precisar clicar em nada.")

try:
    dados = buscar_cotacoes()
    taxas = montar_taxas_em_brl(dados)
except (requests.exceptions.RequestException, KeyError, ValueError):
    st.error("Não foi possível obter as cotações agora. Tente novamente em instantes.")
    st.stop()

valor_usuario = st.number_input(
    "Valor a converter", min_value=0.0, value=100.0, step=10.0, format="%.4f"
)

col_origem, col_botao, col_destino = st.columns([5, 2, 5])

with col_origem:
    moeda_origem = st.selectbox(
        "De", list(MOEDAS), format_func=lambda s: MOEDAS[s], key="moeda_origem"
    )

with col_botao:
    st.write("")
    st.write("")
    st.button("⇄ Inverter", on_click=inverter_moedas, use_container_width=True)

with col_destino:
    moeda_destino = st.selectbox(
        "Para", list(MOEDAS), format_func=lambda s: MOEDAS[s], key="moeda_destino"
    )

st.divider()

if moeda_origem == moeda_destino:
    st.info("Escolha moedas diferentes para a conversão.")
else:
    convertido = converter(valor_usuario, moeda_origem, moeda_destino, taxas)

    st.metric(
        label=f"{formatar(valor_usuario, moeda_origem)} {moeda_origem} equivalem a",
        value=f"{formatar(convertido, moeda_destino)} {moeda_destino}",
    )

    col_min, col_max = st.columns(2)
    col_min.metric("Margem inferior (-3%)", f"{formatar(convertido * 0.97, moeda_destino)} {moeda_destino}")
    col_max.metric("Margem superior (+3%)", f"{formatar(convertido * 1.03, moeda_destino)} {moeda_destino}")

st.subheader(f"{formatar(valor_usuario, moeda_origem)} {moeda_origem} em todas as moedas")
linhas = []
for sigla in MOEDAS:
    if sigla != moeda_origem:
        valor_na_moeda = converter(valor_usuario, moeda_origem, sigla, taxas)
        linhas.append({"Moeda": MOEDAS[sigla], "Valor": formatar(valor_na_moeda, sigla)})
st.table(linhas)

horario = processar_fuso_horario(dados["USDBRL"]["timestamp"])
st.caption(f"Horário da cotação: {horario}")

if st.button("Atualizar cotações agora"):
    buscar_cotacoes.clear()
    st.rerun()
