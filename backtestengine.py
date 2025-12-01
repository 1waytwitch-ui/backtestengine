import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

TOKENS = ["WETH", "CBBTC", "AERO", "VIRTUAL", "USDC"]

COINGECKO_IDS = {
    "WETH": "weth",
    "CBBTC": "coinbase-wrapped-btc",
    "AERO": "aerodrome-finance",
    "VIRTUAL": "virtual-protocol",
    "USDC": "usd-coin"
}


# ------------------------------------------------------------
# HELPERS — PRIX
# ------------------------------------------------------------

def get_price_usd(token):
    """Récupère le prix USD d’un token via API."""
    try:
        r = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={COINGECKO_IDS[token]}&vs_currencies=usd"
        ).json()
        return float(r[COINGECKO_IDS[token]]["usd"]), True
    except:
        return 0.0, False


def get_price_history(token, days=30):
    """Historique de prix (list timestamp, price)."""
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{COINGECKO_IDS[token]}/market_chart?vs_currency=usd&days={days}"
        r = requests.get(url).json()

        prices = r.get("prices", [])
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    except:
        return None


# ------------------------------------------------------------
# CALCUL PRIX PAIRE
# ------------------------------------------------------------

def compute_pair_price(tokenA, tokenB):
    """
    Retourne :
    - price_ratio : prix du tokenA exprimé en tokenB
    - usdA, usdB : prix USD de chaque token (manuels si nécessaire)
    """

    # Cas : USDC → un seul prix
    if tokenB == "USDC":
        usdA, okA = get_price_usd(tokenA)

        if not okA:
            usdA = st.number_input(
                f"Prix manuel {tokenA} (USD)", value=1.0, step=0.01
            )

        return usdA, usdA, 1.0

    # Cas volatiles → deux prix
    usdA, okA = get_price_usd(tokenA)
    usdB, okB = get_price_usd(tokenB)

    col1, col2 = st.columns(2)
    with col1:
        if not okA:
            usdA = st.number_input(
                f"Prix manuel {tokenA} (USD)", value=1.0, step=0.01
            )

    with col2:
        if not okB:
            usdB = st.number_input(
                f"Prix manuel {tokenB} (USD)", value=1.0, step=0.01
            )

    usdB = max(usdB, 1e-12)

    # prix A en B
    price_ratio = usdA / usdB

    return price_ratio, usdA, usdB


# ------------------------------------------------------------
# PAGE ANALYSE AUTOMATIQUE
# ------------------------------------------------------------

def page_analyse_auto():

    st.header("Analyse Automatique de la Paire")

    tokenA = st.selectbox("Token A", TOKENS, index=0)
    tokenB = st.selectbox("Token B", TOKENS, index=1)

    st.subheader("📌 Prix actifs")

    price_ratio, usdA, usdB = compute_pair_price(tokenA, tokenB)

    st.write(f"**1 {tokenA} = {price_ratio:.6f} {tokenB}**")

    st.write("—")
    st.subheader("📉 Historique 30 jours (prix USD token A)")

    df = get_price_history(tokenA)
    if df is not None:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["timestamp"],
            y=df["price"],
            mode="lines"
        ))
        fig.update_layout(
            title=f"Historique {tokenA} (USD)",
            xaxis_title="Date",
            yaxis_title="Prix (USD)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Impossible de charger l’historique.")


# ------------------------------------------------------------
# PAGE GRAPHIQUE PRIX — AJOUT
# ------------------------------------------------------------

def page_graphique_prix():

    st.header("📊 Graphique des Prix — Comparaison Token A / Token B")

    tokenA = st.selectbox("Token A", TOKENS, index=0, key="gA")
    tokenB = st.selectbox("Token B", TOKENS, index=1, key="gB")

    st.subheader("Récupération des prix USD…")

    _, usdA, usdB = compute_pair_price(tokenA, tokenB)

    st.write(f"**Prix USD {tokenA} : {usdA}**")
    st.write(f"**Prix USD {tokenB} : {usdB}**")

    # Récup historique USD
    dfA = get_price_history(tokenA)
    dfB = get_price_history(tokenB)

    if dfA is None or dfB is None:
        st.warning("Impossible de charger les historiques.")
        return

    # Ratio tokenA/tokenB dans le temps
    df = pd.DataFrame({
        "timestamp": dfA["timestamp"],
        "ratio": dfA["price"] / dfB["price"].replace(0, 1e-12)
    })

    st.subheader(f"📈 Prix {tokenA}/{tokenB} sur 30 jours")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["ratio"],
        mode="lines"
    ))

    fig.update_layout(
        title=f"Historique du prix {tokenA}/{tokenB}",
        xaxis_title="Date",
        yaxis_title=f"Prix en {tokenB}",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------------------
# APP
# ------------------------------------------------------------

pages = {
    "Analyse Automatique": page_analyse_auto,
    "Graphique Prix": page_graphique_prix
}

st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à :", list(pages.keys()))

pages[page]()
