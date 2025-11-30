import streamlit as st
import requests
import numpy as np

# -----------------------------------------
# Configuration des stratégies
# -----------------------------------------
STRATEGIES = {
    "Neutre": {
        "ratio": (0.5, 0.5),
        "objectif": "Rester dans le range",
        "contexte": "Incertitude"
    },
    "Coup de pouce": {
        "ratio": (0.2, 0.8),
        "objectif": "Range efficace",
        "contexte": "Faible volatilité"
    },
    "Mini-doux": {
        "ratio": (0.1, 0.9),
        "objectif": "Nouveau régime prix",
        "contexte": "Changement de tendance"
    },
    "Side-line Up": {
        "ratio": (0.95, 0.05),
        "objectif": "Accumulation",
        "contexte": "Dump"
    },
    "Side-line Below": {
        "ratio": (0.05, 0.95),
        "objectif": "Attente avant pump",
        "contexte": "Marché haussier"
    },
    "DCA-in": {
        "ratio": (1.0, 0.0),
        "objectif": "Entrée progressive",
        "contexte": "Incertitude"
    },
    "DCA-out": {
        "ratio": (0.0, 1.0),
        "objectif": "Sortie progressive",
        "contexte": "Tendance haussière"
    }
}

# Correspondance avec CoinGecko
COINGECKO_IDS = {
    "WETH": "weth",
    "USDC": "usd-coin",
    "CBBTC": "coinbase-wrapped-btc",
    "VIRTUAL": "virtual-protocol",
    "AERO": "aerodrome-finance"
}


# -----------------------------------------
# Fonctions utilitaires
# -----------------------------------------
def get_market_chart(asset_id):
    url = f"https://api.coingecko.com/api/v3/coins/{asset_id}/market_chart?vs_currency=usd&days=30&interval=daily"
    return requests.get(url).json()


def compute_volatility(prices):
    returns = np.diff(prices) / prices[:-1]
    return np.std(returns) * np.sqrt(365)


def impermanent_loss(p_old, p_new):
    ratio = p_new / p_old
    return 1 - (2 * np.sqrt(ratio) / (1 + ratio))


# -----------------------------------------
# Interface Streamlit
# -----------------------------------------
st.title("LP Backtest Engine")
st.write("Cet outil vous permet d'analyser une stratégie AMM, d'estimer les rebalances passés et futurs, et d'évaluer l’impact potentiel sur votre capital.")

# -----------------------------------------
# Choix des paires (affichage sans guillemets)
# -----------------------------------------
pairs = [
    ("WETH", "USDC"),
    ("CBBTC", "USDC"),
    ("WETH", "CBBTC"),
    ("VIRTUAL", "WETH"),
    ("AERO", "WETH"),
]

pair_choice = st.selectbox("Sélectionnez une paire :", pairs)
tokenA, tokenB = pair_choice

# -----------------------------------------
# Choix de la stratégie
# -----------------------------------------
strategy_choice = st.selectbox("Sélectionnez une stratégie :", list(STRATEGIES.keys()))
info = STRATEGIES[strategy_choice]

ratioA, ratioB = info["ratio"]

st.subheader("Informations sur la stratégie sélectionnée")
st.write(f"Ratio Token A / Token B : {int(ratioA*100)}/{int(ratioB*100)}")
st.write(f"Objectif : {info['objectif']}")
st.write(f"Contexte idéal : {info['contexte']}")

# -----------------------------------------
# Saisie du capital
# -----------------------------------------
capital = st.number_input("Capital total en USD :", value=1000)

# -----------------------------------------
# Range manuel (%)
# -----------------------------------------
range_pct = st.number_input("Range (%)", min_value=1.0, max_value=100.0, value=20.0)
half_range = range_pct / 2 / 100

# -----------------------------------------
# Prix du Token A
# -----------------------------------------
priceA = requests.get(
    f"https://api.coingecko.com/api/v3/simple/price?ids={COINGECKO_IDS[tokenA]}&vs_currencies=usd"
).json()[COINGECKO_IDS[tokenA]]["usd"]

st.subheader("Prix du marché")
st.write(f"Prix actuel de {tokenA} : {priceA:.2f} USD")

range_low = priceA * (1 - half_range)
range_high = priceA * (1 + half_range)

st.write(f"Limite basse du range : {range_low:.2f} USD")
st.write(f"Limite haute du range : {range_high:.2f} USD")

# -----------------------------------------
# Répartition du capital selon la stratégie
# -----------------------------------------
amountA = capital * ratioA
amountB = capital * ratioB

st.subheader("Répartition du capital selon la stratégie")
st.write(f"{tokenA} : {amountA:.2f} USD")
st.write(f"{tokenB} : {amountB:.2f} USD")

# -----------------------------------------
# Analyse sur 30 jours
# -----------------------------------------
st.subheader("Analyse historique sur 30 jours")

dataA = get_market_chart(COINGECKO_IDS[tokenA])
pricesA = [p[1] for p in dataA["prices"]]

vol_30d = compute_volatility(pricesA)
st.write(f"Volatilité annualisée sur 30 jours : {vol_30d:.2%}")

rebalances = sum((p < range_low) or (p > range_high) for p in pricesA)
st.write(f"Nombre de rebalances détectés sur 30 jours : {rebalances}")

# -----------------------------------------
# Suggestion automatique de stratégie
# -----------------------------------------
prices7 = pricesA[-7:]
vol_7d = compute_volatility(prices7)

if vol_7d > 0.8:
    suggestion = "Neutre"
elif vol_7d > 0.4:
    suggestion = "Coup de pouce"
else:
    suggestion = "Mini-doux"

st.subheader("Suggestion automatique")
st.write(f"Volatilité annualisée sur 7 jours : {vol_7d:.2%}")
st.write(f"Stratégie recommandée : {suggestion}")

# -----------------------------------------
# Impermanent Loss
# -----------------------------------------
st.subheader("Impermanent Loss théorique")

price_old = pricesA[0]
price_now = pricesA[-1]
IL = impermanent_loss(price_old, price_now)

st.write(f"Variation du prix sur 30 jours : {(price_now/price_old - 1):.2%}")
st.write(f"Impermanent Loss estimé : {IL:.2%}")
st.write(f"Perte potentielle sur capital : {capital * IL:.2f} USD")

# -----------------------------------------
# Simulation des futurs rebalances
# -----------------------------------------
st.subheader("Simulation des rebalances futurs")

future_days = st.number_input("Nombre de jours à simuler :", value=30, min_value=1, max_value=90)

vol_sim = vol_7d / np.sqrt(365)   # volatilité journalière

current_price = price_now
simulated_prices = [current_price]

for _ in range(future_days):
    shock = np.random.normal(0, vol_sim)
    next_price = simulated_prices[-1] * (1 + shock)
    simulated_prices.append(next_price)

future_rebalances = sum((p < range_low) or (p > range_high) for p in simulated_prices)

st.write(f"Rebalances simulés sur {future_days} jours : {future_rebalances}")

# -----------------------------------------
# Analyse qualitative selon stratégie
# -----------------------------------------
st.subheader("Analyse de cohérence de la stratégie")

if strategy_choice in ["Neutre", "Coup de pouce", "Mini-doux"]:
    if future_rebalances > future_days * 0.30:
        st.write("La simulation indique un nombre élevé de rebalances. Une stratégie asymétrique pourrait être plus adaptée.")
    else:
        st.write("La stratégie semble compatible avec les conditions simulées.")
elif strategy_choice in ["Side-line Up", "Side-line Below"]:
    if future_rebalances < future_days * 0.10:
        st.write("La simulation montre peu de rebalances. Une stratégie plus neutre pourrait permettre de capter davantage de frais.")
    else:
        st.write("La stratégie asymétrique semble cohérente avec la volatilité projetée.")
elif strategy_choice == "DCA-in":
    if simulated_prices[-1] < simulated_prices[0]:
        st.write("La tendance simulée est baissière. DCA-in reste cohérent.")
    else:
        st.write("Le prix simulé augmente. Une stratégie Neutre ou DCA-out pourrait être plus pertinente.")
elif strategy_choice == "DCA-out":
    if simulated_prices[-1] > simulated_prices[0]:
        st.write("La tendance simulée est haussière. DCA-out est approprié.")
    else:
        st.write("Une tendance baissière simulée suggère de revenir vers une stratégie plus neutre.")
