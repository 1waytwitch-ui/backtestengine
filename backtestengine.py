import streamlit as st
import requests
import numpy as np
import datetime
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# CONFIG PAGE
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="LP Stratégies Backtest Engine",
    layout="wide"
)

# ---------------------------------------------------------------------
# THEME
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {background-color: #FFFFFF !important; color: #000000 !important;}
    h1, h2, h3, h4 {color: #000000 !important;}
    .stTextInput input,
    .stNumberInput input {background-color: #F0F0F0 !important; color: #000000 !important; border: 1px solid #000000 !important;}
    .stButton button {background-color: #000000 !important; color: #FFFFFF !important;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------
# STRATEGIES
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
        res = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={asset_id}&vs_currencies=usd"
        ).json()
        return res[asset_id]["usd"], True
    except:
        return 0.0, False

def compute_volatility(prices):
    if len(prices) < 2:
        return 0.0
    returns = np.diff(prices) / prices[:-1]
    return np.std(returns) * np.sqrt(365)

# ---------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------
col_title, col_telegram = st.columns([3, 1])
with col_title:
    st.title("LP Stratégies Backtest Engine")
with col_telegram:
    st.image("https://t.me/i/userpic/320/Pigeonchanceux.jpg", width=80)
    st.markdown("[Mon Telegram](https://t.me/Pigeonchanceux)")

# ---------------------------------------------------------------------
# LAYOUT
# ---------------------------------------------------------------------
col1, col2 = st.columns([1.3, 1])

with col1:
    st.subheader("Configuration de la Pool")

    left, right = st.columns(2)
    with left:
        pair_labels = [f"{a}/{b}" for a, b in PAIRS]
        selected_pair = st.radio("Paire :", pair_labels)
    with right:
        strategy_choice = st.radio("Stratégie :", list(STRATEGIES.keys()))

    tokenA, tokenB = selected_pair.split("/")
    info = STRATEGIES[strategy_choice]
    ratioA, ratioB = info["ratio"]

    invert_market = st.checkbox("Inversion marché (bull → bear)")
    if invert_market:
        ratioA, ratioB = ratioB, ratioA

    st.write(f"Ratio : {int(ratioA*100)} / {int(ratioB*100)}")
    st.write(f"Objectif : {info['objectif']}")
    st.write(f"Contexte : {info['contexte']}")

    capital = st.number_input("Capital (USD)", value=1000, step=50)

    def get_price_usd(token):
        try:
            res = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={COINGECKO_IDS[token]}&vs_currencies=usd"
            ).json()
            return res[COINGECKO_IDS[token]]["usd"], True
        except:
            return 0.0, False

    if tokenB == "USDC":
        priceA_usd, okA = get_price_usd(tokenA)
        if not okA:
            priceA_usd = st.number_input(f"Prix manuel {tokenA}", value=1.0)
        priceA = priceA_usd
    else:
        priceA_usd, okA = get_price_usd(tokenA)
        priceB_usd, okB = get_price_usd(tokenB)

        la, lb = st.columns(2)
        with la:
            if not okA:
                priceA_usd = st.number_input(f"Prix manuel {tokenA}", value=1.0)
        with lb:
            if not okB:
                priceB_usd = st.number_input(f"Prix manuel {tokenB}", value=1.0)

        priceB_usd = max(priceB_usd, 0.0000001)
        priceA = priceA_usd / priceB_usd

    range_pct = st.number_input("Range (%)", 1.0, 100.0, 20.0)

    range_low = priceA * (1 - ratioA * range_pct / 100)
    range_high = priceA * (1 + ratioB * range_pct / 100)

    if invert_market:
        range_low, range_high = range_high, range_low

    capitalA = capital * ratioA
    capitalB = capital * ratioB

# ---------------------------------------------------------------------
# COLONNE 2 : RANGE + ANALYSES INTÉGRÉES
# ---------------------------------------------------------------------
with col2:
    st.subheader("Range et Prix")
    st.write(f"Prix actuel : {priceA:.6f}")
    st.write(f"Limite basse : {range_low:.6f}")
    st.write(f"Limite haute : {range_high:.6f}")
    st.write(f"{tokenA} : {capitalA:.2f} USD")
    st.write(f"{tokenB} : {capitalB:.2f} USD")

    # 30 jours
    today = str(datetime.date.today())
    key = f"{tokenA}_prices_{today}"
    if key in st.session_state:
        pricesA = st.session_state[key]
    else:
        prices = get_market_chart(COINGECKO_IDS[tokenA])
        st.session_state[key] = prices
        pricesA = prices

    vol_30d = compute_volatility(pricesA)
    rebalances = sum((p < range_low) or (p > range_high) for p in pricesA)

    st.write("---")
    st.subheader("Analyse 30 jours")
    st.write(f"Volatilité annualisée : {vol_30d:.2%}")
    st.write(f"Hors de range détectés : {rebalances}")

    st.write("---")
    st.subheader("Simulation future")
    future_days = st.number_input("Jours à simuler", 1, 120, 30)
    vol_sim = vol_30d / np.sqrt(365)
    simulated = [pricesA[-1]]
    for _ in range(future_days):
        simulated.append(simulated[-1] * (1 + np.random.normal(0, vol_sim)))

    future_reb = sum((p < range_low) or (p > range_high) for p in simulated)
    st.write(f"Hors de range simulés : {future_reb}")

    st.write("---")
    st.subheader("Analyse stratégie")
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
# AUTOMATION TOUT EN BAS
# ---------------------------------------------------------------------
st.write("---")
st.header("Automation")

st.subheader("Range automatique")
range_percent = st.slider("Range total (%)", 1.0, 90.0, 20.0)

ratio_low = 20
ratio_high = 80
low_offset_pct = -range_percent * ratio_low / 100
high_offset_pct = range_percent * ratio_high / 100

final_low = priceA * (1 + low_offset_pct/100)
final_high = priceA * (1 + high_offset_pct/100)

if invert_market:
    final_low, final_high = final_high, final_low

st.write(f"Range : {final_low:.6f} – {final_high:.6f}")
st.write("---")

st.subheader("Trigger d’anticipation")
t1, t2 = st.columns(2)
with t1:
    trig_low = st.slider("Trigger Low (%)", 0, 100, 10)
with t2:
    trig_high = st.slider("Trigger High (%)", 0, 100, 90)

rw = final_high - final_low
trigger_low_price = final_low + (trig_low/100)*rw
trigger_high_price = final_low + (trig_high/100)*rw

st.write(f"Trigger Low : {trigger_low_price:.6f}")
st.write(f"Trigger High : {trigger_high_price:.6f}")

st.write("---")
st.subheader("Time-buffer")
vola = vol_30d * 100
if vola < 1:
    recomand = "10-30 minutes"
elif vola < 3:
    recomand = "30-60 minutes"
else:
    recomand = "60+ minutes"

st.write(f"Recommandation : {recomand}")

st.write("---")
st.subheader("Rebalance avancée")
b1, b2 = st.columns(2)
with b1:
    st.write("Marché baissier")
    st.write(f"Low : {priceA*0.96:.6f}")
    st.write(f"High : {priceA*1.16:.6f}")
with b2:
    st.write("Marché haussier")
    st.write(f"Low : {priceA*0.84:.6f}")
    st.write(f"High : {priceA*1.04:.6f}")
