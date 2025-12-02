import streamlit as st
import requests
import numpy as np
import datetime
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# CONFIG PAGE (wide mode)
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="LP Stratégies Backtest Engine",
    layout="wide"
)

# ---------------------------------------------------------------------
# THEME BLANC ET NOIR
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 500 !important;
    }
    h1, h2, h3, h4 {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    p, span, div, label {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #F0F0F0 !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        height: 28px !important;
        padding: 0 8px !important;
        font-size: 14px !important;
    }
    .stButton > button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: 1px solid #000000 !important;
        padding: 0.4rem 1rem !important;
        border-radius: 6px !important;
    }
    .stTabs [role="tab"] {
        color: #000000 !important;
        border: 1px solid #000000 !important;
        background-color: #E0E0E0 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-bottom: 2px solid #000000 !important;
        font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------
# STRATEGIES ET COINS
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

COINGECKO_IDS = {
    "WETH": "weth",
    "USDC": "usd-coin",
    "CBBTC": "coinbase-wrapped-btc",
    "VIRTUAL": "virtual-protocol",
    "AERO": "aerodrome-finance"
}

PAIRS = [
    ("WETH", "USDC"),
    ("CBBTC", "USDC"),
    ("WETH", "CBBTC"),
    ("VIRTUAL", "WETH"),
    ("AERO", "WETH")
]

# ---------------------------------------------------------------------
# FONCTIONS PRIX
# ---------------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def get_market_chart(asset_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{asset_id}/market_chart?vs_currency=usd&days=30&interval=daily"
        data = requests.get(url).json()
        prices = [p[1] for p in data.get("prices", [])]
        return prices if prices else [1.0] * 30
    except:
        return [1.0] * 30


def get_current_price(asset_id):
    try:
        response = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={asset_id}&vs_currencies=usd"
        ).json()
        return response[asset_id]["usd"], True
    except:
        return 0.0, False


def compute_volatility(prices):
    if len(prices) < 2:
        return 0.0
    returns = np.diff(prices) / prices[:-1]
    return np.std(returns) * np.sqrt(365)

# ---------------------------------------------------------------------
# TITRE
# ---------------------------------------------------------------------
st.title("LP Stratégies Backtest Engine")

# ---------------------------------------------------------------------
# COLONNE SETUP
# ---------------------------------------------------------------------
col1, col2 = st.columns([1.3, 1])

with col1:
    st.subheader("Configuration de la Pool")

    pcol, scol = st.columns([1, 1])

    with pcol:
        pair_labels = [f"{a}/{b}" for a, b in PAIRS]
        selected_pair = st.radio("Paire :", pair_labels)

    with scol:
        strategy_choice = st.radio("Stratégie :", list(STRATEGIES.keys()))

    tokenA, tokenB = selected_pair.split("/")
    info = STRATEGIES[strategy_choice]
    ratioA, ratioB = info["ratio"]

    # ------------------------------------------------------
    # 🔥 OPTION D’INVERSION (marché haussier → baissier)
    # ------------------------------------------------------
    invert = False
    if strategy_choice in ["Coup de pouce", "Mini-doux"]:
        invert = st.checkbox("Inverser la stratégie (marché baissier ↔ haussier)", value=False)

        if invert:
            ratioA, ratioB = ratioB, ratioA      # inversion des ratios
            tokenA, tokenB = tokenB, tokenA      # inversion des tokens
            st.info("⚠️ Stratégie inversée : ratio, range et capital inversés.")

    st.write(f"Ratio effectif : **{int(ratioA*100)}/{int(ratioB*100)}**")
    st.write(f"Objectif : {info['objectif']}")
    st.write(f"Contexte idéal : {info['contexte']}")

    capital = st.number_input("Capital (USD)", value=1000, step=50)

    # ------------------------------------------------------
    # PRIX & RANGE
    # ------------------------------------------------------
    def get_price_usd(token):
        try:
            p = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={COINGECKO_IDS[token]}&vs_currencies=usd"
            ).json()
            return p[COINGECKO_IDS[token]]["usd"], True
        except:
            return 0.0, False

    # prix du tokenA dans le tokenB
    if tokenB == "USDC":
        priceA_usd, okA = get_price_usd(tokenA)
        if not okA:
            priceA_usd = st.number_input(f"Prix manuel {tokenA} (USD)", value=1.0)
        priceA = priceA_usd
    else:
        priceA_usd, okA = get_price_usd(tokenA)
        priceB_usd, okB = get_price_usd(tokenB)

        colA, colB = st.columns(2)
        with colA:
            if not okA:
                priceA_usd = st.number_input(f"Prix manuel {tokenA} (USD)", value=1.0)
        with colB:
            if not okB:
                priceB_usd = st.number_input(f"Prix manuel {tokenB} (USD)", value=1.0)

        priceB_usd = max(priceB_usd, 0.0001)
        priceA = priceA_usd / priceB_usd

    range_pct = st.number_input("Range (%)", min_value=1.0, max_value=100.0, value=20.0)

    # fourchette
    range_low = priceA * (1 - ratioA * range_pct / 100)
    range_high = priceA * (1 + ratioB * range_pct / 100)

    # capital
    capitalA = capital * ratioA
    capitalB = capital * ratioB

with col2:
    st.subheader("Range et Prix")

    st.write(f"Prix {tokenA}/{tokenB} : {priceA:.6f}")
    st.write(f"Limite basse : {range_low:.6f}")
    st.write(f"Limite haute : {range_high:.6f}")

    st.write("Répartition du capital :")
    st.write(f"{tokenA} : {capitalA:.2f} USD")
    st.write(f"{tokenB} : {capitalB:.2f} USD")

# ---------------------------------------------------------------------
# HISTORIQUE (reste identique)
# ---------------------------------------------------------------------

# [tout le code d’origine continue ici, inchangé…]
# ✔️ y compris ton nouvel onglet "Automation"
# ✔️ aucune autre partie n’est modifiée


