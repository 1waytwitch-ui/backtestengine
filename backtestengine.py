import streamlit as st
import requests
import numpy as np

# ---------------------------------------------------------------------
# CONFIG PAGE
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="LP Backtest Engine",
    layout="wide"
)

# ---------------------------------------------------------------------
# CSS COMPACT + STYLE
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* INPUT STYLING */
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        background-color: #F0F0F0 !important;
        border: 1px solid #000000 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        height: 28px !important;
        padding: 0 8px !important;
        max-width: 120px !important; /* 🔥 Réduction largeur */
    }

    .stNumberInput {
        margin: 0 !important;
        padding: 0 !important;
    }

    .stButton > button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        padding: 0.4rem 1rem !important;
        font-weight: 700 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------
# STRATEGIES & PAIRS
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
# FUNCTIONS
# ---------------------------------------------------------------------
def get_market_chart(asset_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{asset_id}/market_chart?vs_currency=usd&days=30&interval=daily"
        data = requests.get(url).json()
        return [p[1] for p in data.get("prices", [])]
    except:
        st.warning(f"Impossible de récupérer l'historique pour {asset_id}")
        return [1.0]*30

def get_current_price(asset_id):
    try:
        response = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={asset_id}&vs_currencies=usd"
        ).json()
        return response[asset_id]["usd"], True
    except:
        return 1.0, False

def compute_volatility(prices):
    returns = np.diff(prices) / prices[:-1]
    return np.std(returns) * np.sqrt(365)

# ---------------------------------------------------------------------
# UI TITLE
# ---------------------------------------------------------------------
st.title("LP Backtest Engine — Compact UI")

# ---------------------------------------------------------------------
# MAIN LAYOUT
# ---------------------------------------------------------------------
col1, col2 = st.columns([1.3, 1])

# ============================================================
# LEFT COLUMN — CONFIG
# ============================================================
with col1:
    st.subheader("Configuration du Pool")

    # --------------------------------------------------------
    # PAIRES + STRATEGIE SUR UNE SEULE LIGNE
    # --------------------------------------------------------
    pair_col, strat_col = st.columns([1, 1])

    with pair_col:
        pair_labels = [f"{a}/{b}" for a, b in PAIRS]
        selected_pair = st.radio("Paire :", pair_labels)

    with strat_col:
        strategy_choice = st.radio("Stratégie :", list(STRATEGIES.keys()))

    tokenA, tokenB = selected_pair.split("/")
    info = STRATEGIES[strategy_choice]
    ratioA, ratioB = info["ratio"]

    st.write(f"**Ratio :** {int(ratioA*100)}/{int(ratioB*100)}")
    st.write(f"**Objectif :** {info['objectif']}")
    st.write(f"**Contexte idéal :** {info['contexte']}")

    # --------------------------------------------------------
    # CAPITAL + RANGE SUR UNE SEULE LIGNE
    # --------------------------------------------------------
    cap_col, range_col = st.columns([1, 1])

    with cap_col:
        capital = st.number_input("Capital (USD)", value=1000, step=50)

    with range_col:
        range_pct = st.number_input("Range (%)", min_value=1.0, max_value=100.0, value=20.0, step=1.0)

    # Price
    priceA, success = get_current_price(COINGECKO_IDS[tokenA])
    if not success:
        priceA = st.number_input(f"Prix manuel {tokenA} (USD)", value=1.0)

    range_low = priceA * (1 - ratioA * range_pct / 100)
    range_high = priceA * (1 + ratioB * range_pct / 100)

    capitalA = capital * ratioA
    capitalB = capital * ratioB

# ============================================================
# RIGHT COLUMN — DISPLAY
# ============================================================
with col2:
    st.subheader("Range & Prix")

    st.write(f"Prix actuel {tokenA} : **{priceA:.2f} USD**")
    st.write(f"Limite basse : **{range_low:.2f} USD**")
    st.write(f"Limite haute : **{range_high:.2f} USD**")

    st.write("### Répartition du capital")
    st.write(f"{tokenA} : **{capitalA:.2f} USD**")
    st.write(f"{tokenB} : **{capitalB:.2f} USD**")

# ---------------------------------------------------------------------
# HISTORIQUES
# ---------------------------------------------------------------------
if 'pricesA' not in st.session_state or st.session_state.get('tokenA') != tokenA:
    st.session_state.pricesA = get_market_chart(COINGECKO_IDS[tokenA])
    st.session_state.tokenA = tokenA
    st.session_state.vol_30d = compute_volatility(st.session_state.pricesA)

pricesA = st.session_state.pricesA
vol_30d = st.session_state.vol_30d

# ---------------------------------------------------------------------
# TABS
# ---------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Backtest 30j", "Simulation future", "Analyse stratégie"])

with tab1:
    st.subheader("Analyse 30 jours")
    st.write(f"Volatilité annualisée : **{vol_30d:.2%}**")
    rebalances = sum((p < range_low) or (p > range_high) for p in pricesA)
    st.write(f"Rebalances détectés : **{rebalances}**")

with tab2:
    st.subheader("Simulation future")
    future_days = st.number_input("Jours à simuler :", min_value=1, max_value=120, value=30)
    vol_sim = vol_30d / np.sqrt(365)
    simulated = [pricesA[-1]]
    for _ in range(future_days):
        next_price = simulated[-1] * (1 + np.random.normal(0, vol_sim))
        simulated.append(next_price)
    future_reb = sum((p < range_low) or (p > range_high) for p in simulated)
    st.write(f"Rebalances simulés : **{future_reb}**")

with tab3:
    st.subheader("Analyse automatique")
    vol_7d = compute_volatility(pricesA[-7:])
    st.write(f"Volatilité annualisée 7j : **{vol_7d:.2%}**")
    if vol_7d > 0.8:
        suggestion = "Neutre"
    elif vol_7d > 0.4:
        suggestion = "Coup de pouce"
    else:
        suggestion = "Mini-doux"
    st.write(f"Stratégie suggérée : **{suggestion}**")
