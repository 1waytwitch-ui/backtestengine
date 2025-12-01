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
# FONCTIONS
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
st.write("Analyse complète : ratio, range proportionnel, volatilité, rebalances historiques et simulation future.")

# ---------------------------------------------------------------------
# LAYOUT 2 COLONNES
# ---------------------------------------------------------------------
col1, col2 = st.columns([1.3, 1])

# --------- COLONNE 1 : CONFIGURATION ---------
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

    st.write(f"Ratio : {int(ratioA*100)}/{int(ratioB*100)}")
    st.write(f"Objectif : {info['objectif']}")
    st.write(f"Contexte idéal : {info['contexte']}")

    capital = st.number_input("Capital (USD)", value=1000, step=50)

    # LOGIQUE DES PRIX
    def get_price_usd(token):
        try:
            p = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={COINGECKO_IDS[token]}&vs_currencies=usd"
            ).json()
            return p[COINGECKO_IDS[token]]["usd"], True
        except:
            return 0.0, False

    if tokenB == "USDC":
        priceA_usd, okA = get_price_usd(tokenA)
        if not okA:
            priceA_usd = st.number_input(
                f"Prix manuel de {tokenA} (USD)", value=1.0, step=0.01
            )
        priceA = priceA_usd
    else:
        priceA_usd, okA = get_price_usd(tokenA)
        priceB_usd, okB = get_price_usd(tokenB)

        colA, colB = st.columns(2)
        with colA:
            if not okA:
                priceA_usd = st.number_input(
                    f"Prix manuel {tokenA} (USD)", value=1.0, step=0.01
                )
        with colB:
            if not okB:
                priceB_usd = st.number_input(
                    f"Prix manuel {tokenB} (USD)", value=1.0, step=0.01
                )

        priceB_usd = max(priceB_usd, 0.0000001)
        priceA = priceA_usd / priceB_usd

    # RANGE
    range_pct = st.number_input("Range (%)", min_value=1.0, max_value=100.0, value=20.0, step=1.0)
    range_low = priceA * (1 - ratioA * range_pct / 100)
    range_high = priceA * (1 + ratioB * range_pct / 100)

    capitalA = capital * ratioA
    capitalB = capital * ratioB

# --------- COLONNE 2 : AFFICHAGE ---------
with col2:
    st.subheader("Range et Prix")

    st.write(f"Prix actuel {tokenA}/{tokenB} : {priceA:.6f}")
    st.write(f"Limite basse : {range_low:.6f}")
    st.write(f"Limite haute : {range_high:.6f}")

    st.write("Répartition du capital :")
    st.write(f"{tokenA} : {capitalA:.2f} USD")
    st.write(f"{tokenB} : {capitalB:.2f} USD")

# ---------------------------------------------------------------------
# HISTORIQUE 30J
# ---------------------------------------------------------------------
today = str(datetime.date.today())
cache_key = f"{tokenA}_prices_{today}"

if cache_key in st.session_state:
    pricesA = st.session_state[cache_key]
else:
    prices = get_market_chart(COINGECKO_IDS[tokenA])
    if not prices:
        old_keys = [k for k in st.session_state.keys() if k.startswith(f"{tokenA}_prices_")]
        if old_keys:
            last_key = sorted(old_keys)[-1]
            prices = st.session_state[last_key]
        else:
            p, _ = get_current_price(COINGECKO_IDS[tokenA])
            prices = [p] * 30

    st.session_state[cache_key] = prices
    pricesA = prices

vol_30d = compute_volatility(pricesA)

# ---------------------------------------------------------------------
# ONGLET
# ---------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Backtest 30j",
    "Simulation future",
    "Analyse stratégie",
    "Graphique"
])

with tab1:
    st.subheader("Analyse sur 30 jours")
    st.write(f"Volatilité annualisée : {vol_30d:.2%}")
    rebalances = sum((p < range_low) or (p > range_high) for p in pricesA)
    st.write(f"Hors de range détectés : {rebalances}")

with tab2:
    st.subheader("Simulation des rebalances futurs")
    future_days = st.number_input("Jours à simuler :", min_value=1, max_value=120, value=30)
    vol_sim = vol_30d / np.sqrt(365)

    simulated = [pricesA[-1]]
    for _ in range(future_days):
        next_price = simulated[-1] * (1 + np.random.normal(0, vol_sim))
        simulated.append(next_price)

    future_reb = sum((p < range_low) or (p > range_high) for p in simulated)
    st.write(f"Hors de range : {future_reb}")

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

# ---------------------------------------------------------------------
# 🔥 4ᵉ ONGLETS : GRAPHIQUE AVEC RANGE (HISTORIQUES RATIO POUR PAIRES VOLATILES)
# ---------------------------------------------------------------------
with tab4:
    st.subheader("Graphique du prix sur 30 jours + Range")

    # Récupère les historiques USD des deux actifs
    pricesA_hist = get_market_chart(COINGECKO_IDS[tokenA])
    pricesB_hist = get_market_chart(COINGECKO_IDS[tokenB])

    # Si paire USDC, on affiche l'historique USD de tokenA
    if tokenB == "USDC":
        series = pricesA_hist
        ylabel = f"Prix {tokenA} (USD)"
    else:
        # paires volatiles : construire ratio historique A/B
        # s'assurer que les listes ont la même longueur
        n = min(len(pricesA_hist), len(pricesB_hist))
        if n == 0:
            series = []
        else:
            series = []
            for i in range(n):
                a = pricesA_hist[i]
                b = pricesB_hist[i] if pricesB_hist[i] is not None else 0.0
                series.append(a / max(b, 1e-12))
        ylabel = f"Prix {tokenA}/{tokenB}"

    if not series:
        st.error("Impossible de charger suffisamment de données historiques pour tracer le graphique.")
    else:
        fig, ax = plt.subplots(figsize=(10, 4))

        # Courbe du prix (historique)
        ax.plot(series, label="Prix 30j", linewidth=2)

        # Lignes range : utiliser range_low / range_high calculés précédemment (ils sont dans la même unité)
        # On trace seulement si range_low/high sont numériques
        try:
            low = float(range_low)
            high = float(range_high)

            # Range Low en rouge
            ax.axhline(low, linestyle="--", color="red", linewidth=1.5,
                       label=f"Range Low ({low:.4f})")

            # Range High en vert
            ax.axhline(high, linestyle="--", color="green", linewidth=1.5,
                       label=f"Range High ({high:.4f})")
        except Exception:
            # si conversion impossible on ignore les lignes
            pass

        ax.set_title(f"{ylabel} — 30 jours")
        ax.set_xlabel("Jours (ancien → récent)")
        ax.set_ylabel(ylabel)
        ax.legend()

        st.pyplot(fig)
