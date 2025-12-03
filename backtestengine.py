import streamlit as st
import requests
import numpy as np
import datetime

st.set_page_config(page_title="LP Stratégies Backtest Engine", layout="wide")

st.markdown("""
<style>
.stApp {background-color: #FFFFFF !important; color: #000000 !important;}
h1, h2, h3, h4 {color: #000000 !important;}
.stTextInput input,
.stNumberInput input {background-color: #F0F0F0 !important; color: #000000 !important; border: 1px solid #000000 !important;}
.stButton button {background-color: #000000 !important; color: #FFFFFF !important;}
.card {
    padding: 12px 16px;
    border: 1px solid #00000020;
    border-radius: 6px;
    background: #F7F7F7;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# STRATEGIES
# -------------------------------
STRATEGIES = {
    "Neutre": {"ratio": (0.5, 0.5)},
    "Coup de pouce": {"ratio": (0.2, 0.8)},
    "Mini-doux": {"ratio": (0.1, 0.9)},
    "Side-line Up": {"ratio": (0.95, 0.05)},
    "Side-line Below": {"ratio": (0.05, 0.95)},
    "DCA-in": {"ratio": (1.0, 0.0)},
    "DCA-out": {"ratio": (0.0, 1.0)},
}

COINGECKO_IDS = {
    "WETH": "weth",
    "USDC": "usd-coin",
    "CBBTC": "coinbase-wrapped-btc",
    "VIRTUAL": "virtual-protocol",
    "AERO": "aerodrome-finance"
}

PAIRS = [
    ("WETH", "USDC"), ("CBBTC", "USDC"), ("WETH", "CBBTC"),
    ("VIRTUAL", "WETH"), ("AERO", "WETH")
]

# ----------------------------------
# TOOLS
# ----------------------------------
@st.cache_data(ttl=3600)
def get_market_chart(asset_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{asset_id}/market_chart?vs_currency=usd&days=30&interval=daily"
        data = requests.get(url).json()
        return [p[1] for p in data.get("prices", [])]
    except:
        return [1.0] * 30

def compute_volatility(prices):
    if len(prices) < 2:
        return 0.0
    returns = np.diff(prices) / prices[:-1]
    return np.std(returns) * np.sqrt(365)

def get_price_usd(token):
    try:
        data = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={COINGECKO_IDS[token]}&vs_currencies=usd"
        ).json()
        return data[COINGECKO_IDS[token]]["usd"], True
    except:
        return 0.0, False


# -------------------------------
# HEADER
# -------------------------------
st.title("LP Stratégies Backtest Engine")

# -------------------------------
# LAYOUT
# -------------------------------
col1, col2 = st.columns([1.3, 1])

# -------------------------------
# CONFIG (COL 1)
# -------------------------------
with col1:
    st.subheader("Configuration Pool")

    left, right = st.columns(2)
    with left:
        pair_labels = [f"{a}/{b}" for a, b in PAIRS]
        selected_pair = st.radio("Paire :", pair_labels)
    with right:
        strategy_choice = st.radio("Stratégie :", list(STRATEGIES.keys()))

    tokenA, tokenB = selected_pair.split("/")
    ratioA, ratioB = STRATEGIES[strategy_choice]["ratio"]

    invert_market = st.checkbox("Inversion marché")
    if invert_market:
        ratioA, ratioB = ratioB, ratioA

    capital = st.number_input("Capital (USD)", value=1000)

    # Prix
    if tokenB == "USDC":
        pA, okA = get_price_usd(tokenA)
        if not okA:
            pA = st.number_input(f"Prix {tokenA}", value=1.0)
        priceA = pA
    else:
        pA, okA = get_price_usd(tokenA)
        pB, okB = get_price_usd(tokenB)

        if not okA:
            pA = st.number_input(f"Prix {tokenA}", value=1.0)
        if not okB:
            pB = st.number_input(f"Prix {tokenB}", value=1.0)

        pB = max(pB, 0.0000001)
        priceA = pA / pB

    range_pct = st.number_input("Range (%)", 1.0, 100.0, 20.0)

    range_low = priceA * (1 - ratioA * range_pct / 100)
    range_high = priceA * (1 + ratioB * range_pct / 100)

    if invert_market:
        range_low, range_high = range_high, range_low

    capitalA = capital * ratioA
    capitalB = capital * ratioB

# -------------------------------
# BLOC UNIQUE COMPACT (COL 2)
# -------------------------------
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Bloc Analyse Compact")

    # Prices
    st.write(f"Prix actuel : {priceA:.6f}")
    st.write(f"Range : {range_low:.6f} → {range_high:.6f}")
    st.write(f"Alloc. : {capitalA:.2f} USD {tokenA} / {capitalB:.2f} USD {tokenB}")

    # 30 jours de prix
    key = f"{tokenA}_prices"
    if key not in st.session_state:
        st.session_state[key] = get_market_chart(COINGECKO_IDS[tokenA])
    pricesA = st.session_state[key]

    vol_30d = compute_volatility(pricesA)
    out_30d = sum((p < range_low) or (p > range_high) for p in pricesA)

    st.write(f"30 jours : Vol {vol_30d:.2%} | Hors range {out_30d}")

    # Jours simulés — maintenant champ compact
    future_days = st.number_input("Jours de simulation", value=30, step=1)

    vol_sim = vol_30d / np.sqrt(365)
    simulated = [pricesA[-1]]
    for _ in range(future_days):
        simulated.append(simulated[-1] * (1 + np.random.normal(0, vol_sim)))
    future_out = sum((p < range_low) or (p > range_high) for p in simulated)

    st.write(f"Simulation {future_days}j : hors range {future_out}")

    # Analyse stratégie
    vol_7d = compute_volatility(pricesA[-7:])
    if vol_7d > 0.8:
        suggestion = "Neutre"
    elif vol_7d > 0.4:
        suggestion = "Coup de pouce"
    else:
        suggestion = "Mini-doux"

    st.write(f"Stratégie suggérée : {suggestion}")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# AUTOMATION EN BAS
# -------------------------------
st.write("---")
st.header("Automation")

st.subheader("Range automatique")
range_percent = st.slider("Range total (%)", 1.0, 90.0, 20.0)

ratio_low, ratio_high = 20, 80
low_off = -range_percent * ratio_low / 100
high_off = range_percent * ratio_high / 100

final_low = priceA * (1 + low_off/100)
final_high = priceA * (1 + high_off/100)

if invert_market:
    final_low, final_high = final_high, final_low

st.write(f"Range auto : {final_low:.6f} – {final_high:.6f}")

st.subheader("Triggers")
t1, t2 = st.columns(2)
with t1: trig_low = st.number_input("Trigger Low (%)", 0, 100, 10)
with t2: trig_high = st.number_input("Trigger High (%)", 0, 100, 90)

rw = final_high - final_low
trigger_low_price = final_low + (trig_low/100)*rw
trigger_high_price = final_low + (trig_high/100)*rw

st.write(f"Trigger Low : {trigger_low_price:.6f}")
st.write(f"Trigger High : {trigger_high_price:.6f}")

st.subheader("Time-buffer")
vola = vol_30d * 100
if vola < 1: recomand = "10-30 min"
elif vola < 3: recomand = "30-60 min"
else: recomand = "60+ min"

st.write(f"Recommandation : {recomand}")

st.subheader("Rebalance avancée")
c1, c2 = st.columns(2)
with c1:
    st.write("Marché baissier")
    st.write(f"Low : {priceA*0.96:.6f}")
    st.write(f"High : {priceA*1.16:.6f}")
with c2:
    st.write("Marché haussier")
    st.write(f"Low : {priceA*0.84:.6f}")
    st.write(f"High : {priceA*1.04:.6f}")
