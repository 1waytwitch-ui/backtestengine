import streamlit as st
import requests
import pandas as pd
import numpy as np

# -----------------------------
# Config stratégies
# -----------------------------
STRATEGIES = {
    "Neutre": (0.5, 0.5),
    "Coup de pouce": (0.2, 0.8),
    "Mini-doux": (0.1, 0.9),
    "Side-line Up": (0.95, 0.05),
    "Side-line Down": (0.05, 0.95),
    "DCA-in": (1.0, 0.0),
    "DCA-out": (0.0, 1.0),
}

# Mapping CoinGecko IDs
COINGECKO_IDS = {
    "WETH": "weth",
    "USDC": "usd-coin",
    "CBBTC": "coinbase-wrapped-btc",
    "VIRTUAL": "virtual-protocol",
    "AERO": "aerodrome-finance"
}

# -----------------------------
# Helper API CoinGecko
# -----------------------------
def get_market_chart(asset_id):
    url = f"https://api.coingecko.com/api/v3/coins/{asset_id}/market_chart?vs_currency=usd&days=30&interval=daily"
    return requests.get(url).json()

def compute_volatility(prices):
    returns = np.diff(prices) / prices[:-1]
    return np.std(returns) * np.sqrt(365)  # annualized vol

# Impermanent Loss formula
def impermanent_loss(p_old, p_new):
    ratio = p_new / p_old
    IL = 1 - (2 * np.sqrt(ratio) / (1 + ratio))
    return IL

# -----------------------------
# App Streamlit
# -----------------------------
st.title("📊 LP Backtest Engine – Stratégies AMM")

# Choix des paires
pairs = [
    ("WETH", "USDC"),
    ("CBBTC", "USDC"),
    ("WETH", "CBBTC"),
    ("VIRTUAL", "WETH"),
    ("AERO", "WETH"),
]

pair_choice = st.selectbox("Choisir une paire :", pairs)
tokenA, tokenB = pair_choice

# Choix stratégie
strategy_choice = st.selectbox("Stratégie :", list(STRATEGIES.keys()))
ratioA, ratioB = STRATEGIES[strategy_choice]

# Capital
capital = st.number_input("Capital total ($)", value=1000)

# Range
range_pct = st.slider("Range (%)", 1, 50, 20)
half_range = range_pct / 2 / 100

# Prix market
st.subheader("📈 Données marché en temps réel")
priceA = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={COINGECKO_IDS[tokenA]}&vs_currencies=usd").json()[COINGECKO_IDS[tokenA]]["usd"]

st.write(f"**Prix actuel de {tokenA} : ${priceA:.2f}**")

# Compute range
range_low = priceA * (1 - half_range)
range_high = priceA * (1 + half_range)

st.write(f"📌 **Range Low : ${range_low:.2f}**")
st.write(f"📌 **Range High : ${range_high:.2f}**")

# Ratio capital
amountA = capital * ratioA
amountB = capital * ratioB
st.subheader("💰 Répartition du capital")
st.write(f"- {tokenA}: **${amountA:.2f}** ({ratioA*100:.0f}%)")
st.write(f"- {tokenB}: **${amountB:.2f}** ({ratioB*100:.0f}%)")

# -----------------------------
# Récupération des prix 30 jours pour backtest
# -----------------------------
st.subheader("📊 Analyse 30 jours & Rebalance")

dataA = get_market_chart(COINGECKO_IDS[tokenA])
pricesA = [p[1] for p in dataA["prices"]]

vol_30d = compute_volatility(pricesA)
st.write(f"📌 **Volatilité 30j : {vol_30d:.2%}**")

# estimation très simple rebalance : nombre de touches hors range
rebalances = sum((p < range_low) or (p > range_high) for p in pricesA)
st.write(f"🔄 **Rebalances estimés sur 30j : {rebalances}**")

# -----------------------------
# Suggestion stratégie (volatilité 7 jours)
# -----------------------------
st.subheader("🤖 Suggestion automatique de stratégie")

prices7 = pricesA[-7:]
vol_7d = compute_volatility(prices7)

if vol_7d > 0.8:
    suggestion = "Neutre"
elif 0.4 < vol_7d <= 0.8:
    suggestion = "Coup de pouce"
elif vol_7d <= 0.4:
    suggestion = "Mini-doux"
else:
    suggestion = "Neutre"

st.write(f"📌 **Volatilité 7j : {vol_7d:.2%}**")
st.write(f"👉 Stratégie recommandée : **{suggestion}**")

# -----------------------------
# Impermanent Loss estimation
# -----------------------------
st.subheader("⚠️ Impermanent Loss (IL)")

price_old = pricesA[0]
price_now = pricesA[-1]
IL = impermanent_loss(price_old, price_now)

st.write(f"📉 Variation prix 30j : {price_now/price_old - 1:.2%}")
st.write(f"⚠️ Impermanent Loss estimé : **{IL:.2%}**")

# Impact sur ton capital
loss_value = capital * IL
st.write(f"💸 Perte potentielle : **${loss_value:.2f}**")

st.info("L’IL augmente fortement lors des stratégies 50/50 si le prix sort du range → une stratégie Side-line Up/Down peut limiter l’impact.")

