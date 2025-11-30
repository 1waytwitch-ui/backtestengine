import streamlit as st
import requests
import numpy as np

# ---------------------------------------------------------------------
# CONFIGURATION PAGE + MODE LARGE
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="LP Backtest Engine",
    layout="wide"
)

# ---------------------------------------------------------------------
# MODE SOMBRE / CLAIR (thème CSS custom)
# ---------------------------------------------------------------------
theme = st.sidebar.radio("Thème", ["Clair", "Sombre"])

if theme == "Sombre":
    st.markdown(
        """
        <style>
        body { background-color: #111 !important; color: #EEE !important; }
        .stApp { background-color: #111 !important; }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body { background-color: #FFFFFF !important; color: #000000 !important; }
        .stApp { background-color: #FFFFFF !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------------------------
# STRATÉGIES
# ---------------------------------------------------------------------
STRATEGIES = {
    "Neutre": {"ratio": (0.5, 0.5), "objectif": "Rester dans le range", "contexte": "Incertitude"},
    "Coup de pouce": {"ratio": (0.2, 0.8), "objectif": "Range efficace", "contexte": "Faible volatilité"},
    "Mini-doux": {"ratio": (0.1, 0.9), "objectif": "Nouveau régime prix", "contexte": "Changement de tendance"},
    "Side-line Up": {"ratio": (0.95, 0.05), "objectif": "Accumulation", "contexte": "Dump"},
    "Side-line Below": {"ratio": (0.05, 0.95), "objectif": "Attente avant pump", "contexte": "Marché haussier"},
    "DCA-in": {"ratio": (1.0, 0.0), "objectif": "Entrée progressive", "contexte": "Incertitude"},
    "DCA-out": {"ratio": (0.0, 1.0), "objectif": "Sortie progressive", "contexte": "Tendance haussière"},
}

# CoinGecko mapping
COINGECKO_IDS = {
    "WETH": "weth",
    "USDC": "usd-coin",
    "CBBTC": "coinbase-wrapped-btc",
    "VIRTUAL": "virtual-protocol",
    "AERO": "aerodrome-finance"
}

# ---------------------------------------------------------------------
# FONCTIONS
# ---------------------------------------------------------------------
def get_market_chart(asset_id):
    url = f"https://api.coingecko.com/api/v3/coins/{asset_id}/market_chart?vs_currency=usd&days=30&interval=daily"
    return requests.get(url).json()

def compute_volatility(prices):
    returns = np.diff(prices) / prices[:-1]
    return np.std(returns) * np.sqrt(365)

def impermanent_loss(old, new):
    ratio = new / old
    return 1 - (2 * np.sqrt(ratio) / (1 + ratio))


# ---------------------------------------------------------------------
# TITRE
# ---------------------------------------------------------------------
st.title("LP Backtest Engine")
st.write("Analyse complète d'une stratégie AMM : ratios, range, backtest, IL et projection future.")

# ---------------------------------------------------------------------
# LAYOUT EN 3 COLONNES (réduction scroll)
# ---------------------------------------------------------------------
col1, col2, col3 = st.columns([1.2, 1, 1])

# ---------------------------------------------------------------------
# COLONNE 1 : Pair + Stratégie + Capital
# ---------------------------------------------------------------------
with col1:
    st.subheader("Configuration du pool")

    pairs = [
        ("WETH", "USDC"),
        ("CBBTC", "USDC"),
        ("WETH", "CBBTC"),
        ("VIRTUAL", "WETH"),
        ("AERO", "WETH"),
    ]

    tokenA, tokenB = st.selectbox("Paire :", pairs)

    strategy_choice = st.selectbox("Stratégie :", list(STRATEGIES.keys()))
    info = STRATEGIES[strategy_choice]
    ratioA, ratioB = info["ratio"]

    st.write(f"Ratio : {int(ratioA*100)}/{int(ratioB*100)}")
    st.write(f"Objectif : {info['objectif']}")
    st.write(f"Contexte idéal : {info['contexte']}")

    capital = st.number_input("Capital (USD)", value=1000)


# ---------------------------------------------------------------------
# COLONNE 2 : Range + Prix
# ---------------------------------------------------------------------
with col2:
    st.subheader("Paramètres du range")

    range_pct = st.number_input("Range (%)", min_value=1.0, max_value=100.0, value=20.0)
    half_range = range_pct / 2 / 100

    priceA = requests.get(
        f"https://api.coingecko.com/api/v3/simple/price?ids={COINGECKO_IDS[tokenA]}&vs_currencies=usd"
    ).json()[COINGECKO_IDS[tokenA]]["usd"]

    st.write(f"Prix actuel {tokenA} : {priceA:.2f} USD")

    range_low = priceA * (1 - half_range)
    range_high = priceA * (1 + half_range)

    st.write(f"Limite basse : {range_low:.2f}")
    st.write(f"Limite haute : {range_high:.2f}")

    st.write("Répartition du capital :")
    st.write(f"{tokenA} : {capital * ratioA:.2f} USD")
    st.write(f"{tokenB} : {capital * ratioB:.2f} USD")


# ---------------------------------------------------------------------
# COLONNE 3 : Résumé
# ---------------------------------------------------------------------
with col3:
    st.subheader("Résumé des analyses")
    st.write("Les résultats détaillés sont disponibles dans les onglets ci-dessous.")
    st.write("- Volatilité 30j")
    st.write("- Rebalances")
    st.write("- IL")
    st.write("- Simulation future")
    st.write("- Recommandation")


# ---------------------------------------------------------------------
# TABS — Limitation du scroll
# ---------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["Backtest 30j", "Impermanent Loss", "Simulation future", "Analyse stratégie"])

# ======== TAB 1 : Backtest ========
with tab1:
    st.subheader("Analyse historique (30 jours)")

    data = get_market_chart(COINGECKO_IDS[tokenA])
    pricesA = [p[1] for p in data["prices"]]

    vol_30d = compute_volatility(pricesA)
    st.write(f"Volatilité annualisée : {vol_30d:.2%}")

    rebalances = sum((p < range_low) or (p > range_high) for p in pricesA)
    st.write(f"Rebalances détectés : {rebalances}")


# ======== TAB 2 : Impermanent Loss ========
with tab2:
    st.subheader("Impermanent Loss")

    price_old = pricesA[0]
    price_now = pricesA[-1]
    IL = impermanent_loss(price_old, price_now)

    st.write(f"Variation prix : {(price_now / price_old - 1):.2%}")
    st.write(f"IL estimé : {IL:.2%}")
    st.write(f"Impact sur capital : {capital * IL:.2f} USD")


# ======== TAB 3 : Simulation future ========
with tab3:
    st.subheader("Simulation des rebalances futurs")

    future_days = st.number_input("Jours à simuler :", min_value=1, max_value=120, value=30)

    vol_sim = vol_30d / np.sqrt(365)
    simulated = [price_now]

    for _ in range(future_days):
        next_price = simulated[-1] * (1 + np.random.normal(0, vol_sim))
        simulated.append(next_price)

    future_reb = sum((p < range_low) or (p > range_high) for p in simulated)

    st.write(f"Rebalances simulés : {future_reb}")


# ======== TAB 4 : Analyse ========
with tab4:
    st.subheader("Analyse de cohérence de la stratégie")

    vol_7d = compute_volatility(pricesA[-7:])
    st.write(f"Volatilité annualisée 7j : {vol_7d:.2%}")

    if vol_7d > 0.8:
        st.write("Suggestion : Neutre")
    elif vol_7d > 0.4:
        st.write("Suggestion : Coup de pouce")
    else:
        st.write("Suggestion : Mini-doux")
