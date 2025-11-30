import streamlit as st
import requests
import numpy as np

# ------------------------
#       CSS COMPACT
# ------------------------
st.markdown("""
<style>

.stNumberInput input {
    max-width: 120px !important;
}

.stNumberInput {
    padding: 0 !important;
    margin: 0 !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------------
#   PAIRS + IDs
# ------------------------
PAIRS = [
    ("WETH", "USDC"),
    ("CBTC", "USDC"),
    ("WETH", "CBTC"),
    ("VIRTUAL", "WETH"),
    ("AERO", "WETH")
]

COINGECKO_IDS = {
    "WETH": "weth",
    "USDC": "usd-coin",
    "CBTC": "cbtc",
    "VIRTUAL": "virtual-protocol",
    "AERO": "aerodrome-finance"
}

STRATEGIES = {
    "Neutre": 0,
    "Coup de pouce": 1,
    "Mini-doux": 2,
    "Side-line Up": 3,
    "Side-line Below": 4,
    "DCA-in": 5,
    "DCA-out": 6,
}

# ------------------------
#  API SAFE + CACHE
# ------------------------
@st.cache_data(show_spinner=False, ttl=3600)
def fetch_prices_cached(coingecko_id):
    """Requête API sécurisée + cache interne Streamlit pour 1h."""
    try:
        url = (
            f"https://api.coingecko.com/api/v3/coins/{coingecko_id}/market_chart"
            f"?vs_currency=usd&days=30&interval=daily"
        )
        data = requests.get(url).json()
        prices = [p[1] for p in data.get("prices", [])]

        if not prices:
            return [1.0] * 30  # fallback si vide

        return prices

    except:
        return [1.0] * 30   # fallback total


def get_market_chart(asset_id):
    return fetch_prices_cached(asset_id)


def compute_volatility(prices):
    if len(prices) < 2:
        return 0.0
    returns = np.diff(prices) / prices[:-1]
    return float(np.std(returns) * np.sqrt(365))


# ------------------------
#   TITRE
# ------------------------
st.title("Configuration du Pool")


# ------------------------
#   PAIRE + STRATEGIE (horizontal)
# ------------------------
pair_col, strat_col = st.columns(2)

with pair_col:
    pair_labels = [f"{a}/{b}" for a, b in PAIRS]
    selected_pair = st.radio("Paire :", pair_labels)

with strat_col:
    strategy_choice = st.radio("Stratégie :", list(STRATEGIES.keys()))


# ------------------------
#   EXTRACTION TOKENS
# ------------------------
tokenA, tokenB = selected_pair.split("/")


# ------------------------
#   CAPITAL + RANGE (horizontal)
# ------------------------
cap_col, range_col = st.columns(2)

with cap_col:
    capital = st.number_input("Capital (USD)", value=1000, step=50)

with range_col:
    range_pct = st.number_input(
        "Range (%)", min_value=1.0, max_value=100.0, value=20.0, step=1.0
    )


# ------------------------
#   PRIX + VOLATILITE AVEC SESSION_STATE
# ------------------------
if "pricesA" not in st.session_state or st.session_state.get("tokenA") != tokenA:
    prices = get_market_chart(COINGECKO_IDS[tokenA])

    if not prices:
        prices = [1.0] * 30

    st.session_state.pricesA = prices
    st.session_state.tokenA = tokenA
    st.session_state.vol_30d = compute_volatility(prices)

pricesA = st.session_state.pricesA
volA = st.session_state.vol_30d


# ------------------------
# CALCULS RANGE & PRIX
# ------------------------
price_now = pricesA[-1] if pricesA else 1.0

# Range haut/bas
range_low = price_now * (1 - range_pct / 100)
range_high = price_now * (1 + range_pct / 100)

# ------------------------
# AFFICHAGE (réintégré entièrement)
# ------------------------
st.write(f"### Détails du pool")

st.write(f"**Prix actuel ({tokenA}) :** {price_now:,.4f} USD")
st.write(f"**Ratio :** 50/50")
st.write(f"**Objectif :** Rester dans le range")
st.write(f"**Volatilité 30 jours :** {volA:.2%}")

st.write("### Fourchette de prix")
col_low, col_mid, col_high = st.columns(3)

with col_low:
    st.metric("Range bas", f"{range_low:,.4f} USD")

with col_mid:
    st.metric("Prix actuel", f"{price_now:,.4f} USD")

with col_high:
    st.metric("Range haut", f"{range_high:,.4f} USD")

st.write("Contexte idéal : Incertitude")
