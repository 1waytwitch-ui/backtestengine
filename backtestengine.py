import streamlit as st
import requests
import numpy as np

# ---------------------------------------------------------------------
# CONFIG PAGE (wide mode)
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="LP Backtest Engine",
    layout="wide"
)

# ---------------------------------------------------------------------
# THEME NOIR ET BLANC LISIBLE + INPUTS COMPACT
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }
    h1, h2, h3, h4 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    p, span, div, label {
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }
    /* INPUTS PLUS COMPACT */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #111111 !important;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        height: 28px !important;
        padding: 0 8px !important;
        font-size: 14px !important;
    }
    .stButton > button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border: 1px solid #FFFFFF !important;
        padding: 0.4rem 1rem !important;
        border-radius: 6px !important;
    }
    .stTabs [role="tab"] {
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
        background-color: #111111 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-bottom: 2px solid #FFFFFF !important;
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

PAIRS = [("WETH", "USDC"), ("CBBTC", "USDC"), ("WETH", "CBBTC"), ("VIRTUAL", "WETH"), ("AERO", "WETH")]

# ---------------------------------------------------------------------
# FONCTIONS
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
# TITRE
# ---------------------------------------------------------------------
st.title("LP Backtest Engine — Noir & Blanc")
st.write("Analyse AMM complète : ratio, range proportionnel, volatilité, rebalances historiques et simulation future.")

# ---------------------------------------------------------------------
# LAYOUT 2 COLONNES
# ---------------------------------------------------------------------
col1, col2 = st.columns([1.3, 1])

# --------- COLONNE 1 : CONFIGURATION ---------
with col1:
    st.subheader("Configuration du Pool")
    
    # Sélection de la paire
    pair_labels = [f"{a}/{b}" for a,b in PAIRS]
    selected_pair = st.radio("Paire :", pair_labels)
    tokenA, tokenB = selected_pair.split("/")
    
    # Sélection stratégie
    strategy_choice = st.radio("Stratégie :", list(STRATEGIES.keys()))
    info = STRATEGIES[strategy_choice]
    ratioA, ratioB = info["ratio"]
    st.write(f"Ratio : {int(ratioA*100)}/{int(ratioB*100)}")
    st.write(f"Objectif : {info['objectif']}")
    st.write(f"Contexte idéal : {info['contexte']}")
    
    # Capital
    capital = st.number_input("Capital (USD)", value=1000, step=50)
    
    # Prix actif
    priceA, success = get_current_price(COINGECKO_IDS[tokenA])
    if not success:
        priceA = st.number_input(f"Prix manuel pour {tokenA} (USD)", value=1.0, step=0.01)
    
    # Range proportionnel au ratio
    range_pct = st.number_input("Range (%)", min_value=1.0, max_value=100.0, value=20.0, step=1.0)
    range_low = priceA * (1 - ratioA * range_pct / 100)
    range_high = priceA * (1 + ratioB * range_pct / 100)
    
    # Répartition capital
    capitalA = capital * ratioA
    capitalB = capital * ratioB

# --------- COLONNE 2 : AFFICHAGE ---------
with col2:
    st.subheader("Range et Prix")
    st.write(f"Prix actuel {tokenA} : {priceA:.2f} USD")
    st.write(f"Limite basse : {range_low:.2f} USD")
    st.write(f"Limite haute : {range_high:.2f} USD")
    
    st.write("Répartition du capital selon la stratégie :")
    st.write(f"{tokenA} : {capitalA:.2f} USD")
    st.write(f"{tokenB} : {capitalB:.2f} USD")

# ---------------------------------------------------------------------
# HISTORIQUES 30 JOURS EN MÉMOIRE
# ---------------------------------------------------------------------
if 'pricesA' not in st.session_state or st.session_state.get('tokenA') != tokenA:
    st.session_state.pricesA = get_market_chart(COINGECKO_IDS[tokenA])
    st.session_state.tokenA = tokenA
    st.session_state.vol_30d = compute_volatility(st.session_state.pricesA)

pricesA = st.session_state.pricesA
vol_30d = st.session_state.vol_30d

# ---------------------------------------------------------------------
# ONGLETS
# ---------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Backtest 30j", "Simulation future", "Analyse stratégie"])

# ===== TAB 1 : BACKTEST 30J =====
with tab1:
    st.subheader("Analyse sur 30 jours")
    st.write(f"Volatilité annualisée : {vol_30d:.2%}")
    rebalances = sum((p < range_low) or (p > range_high) for p in pricesA)
    st.write(f"Rebalances détectés : {rebalances}")

# ===== TAB 2 : SIMULATION FUTURE =====
with tab2:
    st.subheader("Simulation des rebalances futurs")
    future_days = st.number_input("Jours à simuler :", min_value=1, max_value=120, value=30)
    vol_sim = vol_30d / np.sqrt(365)
    simulated = [pricesA[-1]]
    for _ in range(future_days):
        next_price = simulated[-1] * (1 + np.random.normal(0, vol_sim))
        simulated.append(next_price)
    future_reb = sum((p < range_low) or (p > range_high) for p in simulated)
    st.write(f"Rebalances simulés : {future_reb}")

# ===== TAB 3 : SUGGESTION STRATEGIE =====
with tab3:
    st.subheader("Analyse automatique")
    vol_7d = compute_volatility(pricesA[-7:])
    st.write(f"Volatilité annualisée 7j : {vol_7d:.2%}")
    if vol_7d > 0.8:
        suggestion = "Neutre"
    elif vol_7d > 0.4:
        suggestion = "Coup de pouce"
    else:
        suggestion = "Mini-doux"
    st.write(f"Stratégie suggérée : {suggestion}")
