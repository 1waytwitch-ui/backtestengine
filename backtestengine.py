import streamlit as st
import requests
import numpy as np
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="LP STRATÉGIES BACKTEST ENGINE ", layout="wide")

# ---- STYLES GÉNÉRAUX ----
st.markdown("""
<style>
.stApp {background-color: #FFFFFF !important; color: #000000 !important;}
h1, h2, h3, h4 {color: #000000 !important;}
.stTextInput input, .stNumberInput input {
    background-color: #F0F0F0 !important; 
    color: #000000 !important;
    border: 1px solid #000000 !important;
}
.stButton button {
    background-color: #000000 !important;
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

# ---- FORCE DARK MODE ----
st.markdown("""
<style>
.stRadio label, .stRadio div, 
.stSelectbox label, .stSelectbox div,
.stCheckbox label, .stCheckbox div {
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

# ---- INIT ----
if "show_disclaimer" not in st.session_state:
    st.session_state.show_disclaimer = True

# ---- DATA ----
STRATEGIES = {
    "Neutre": {"ratio": (0.5, 0.5), "objectif": "Rester dans le range", "contexte": "Incertitude (attention à l'impermanent loss vente à perte ou rachat trop cher)"},
    "Coup de pouce": {"ratio": (0.2, 0.8), "objectif": "Range efficace", "contexte": "Faible volatilité(attention à inverser en fonction du marché)"},
    "Mini-doux": {"ratio": (0.1, 0.9), "objectif": "Nouveau régime prix", "contexte": "Changement de tendance (attention à inverser en fonction du marché)"},
    "Side-line Up": {"ratio": (0.95, 0.05), "objectif": "Accumulation", "contexte": "Dump"},
    "Side-line Below": {"ratio": (0.05, 0.95), "objectif": "Attente avant pump", "contexte": "Marché haussier"},
    "DCA-in": {"ratio": (1.0, 0.0), "objectif": "Entrée progressive", "contexte": "Accumulation de l'actif le plus volatile (Token A)"},
    "DCA-out": {"ratio": (0.0, 1.0), "objectif": "Sortie progressive", "contexte": "Tendance haussière revente de l'actif le plus volatile (token A contre le token B)"},
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

# ---- FONCTIONS ----
@st.cache_data(ttl=3600, show_spinner=False)
def get_market_chart(asset_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{asset_id}/market_chart?vs_currency=usd&days=30&interval=daily"
        data = requests.get(url).json()
        prices = [p[1] for p in data.get("prices", [])]
        prices = np.array(prices)
        prices = prices[~np.isnan(prices)]
        prices = prices[prices > 0]
        return prices.tolist() if len(prices) > 0 else [1.0] * 30
    except:
        return [1.0] * 30

def compute_volatility(prices):
    if len(prices) < 2:
        return 0.0
    prices = np.array(prices)
    returns = np.diff(prices) / prices[:-1]
    returns = returns[~np.isnan(returns)]
    return float(np.std(returns))

def get_price_usd(token):
    try:
        res = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={COINGECKO_IDS[token]}&vs_currencies=usd"
        ).json()
        return res[COINGECKO_IDS[token]]["usd"], True
    except:
        return 0.0, False

# ---- HEADER ----
st.markdown("""
<style>
.deFi-banner {
    background: linear-gradient(135deg, #0a0f1f 0%, #1e2761 40%, #4b1c7d 100%);
    padding: 25px 30px;
    border-radius: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0px 4px 18px rgba(0,0,0,0.45);
    margin-bottom: 25px;
}
.deFi-title-text {
    font-size: 36px;
    font-weight: 700;
    color: white !important;
}
</style>

<div class="deFi-banner">
    <div class="deFi-title-text">LP STRATÉGIES BACKTEST ENGINE</div>
    <div>
        <img src="https://t.me/i/userpic/320/Pigeonchanceux.jpg" style="width:60px;height:60px;border-radius:50%;">
        <a href="https://t.me/Pigeonchanceux" target="_blank" style="color:white;font-size:18px;font-weight:600;text-decoration:none;">Mon Telegram</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- DISCLAIMER ----
if st.session_state.show_disclaimer:
    st.markdown("""
    <div style="
        background-color: #fff3cd;
        border-left: 6px solid #ffca2c;
        padding: 15px 20px;
        border-radius: 8px;
        color: #000;
        margin-bottom: 25px;
        font-size: 15px;
    ">
    <b>⚠️ DISCLAIMER IMPORTANT</b><br><br>
    Cet outil peut comporter des approximations ou des inexactitudes. Il ne s’agit en aucun cas d’un conseil en investissement. Veuillez effectuer vos propres recherches et comprendre le mécanisme des pools de liquidités concentrés et du capital déposé. Si l’API est surchargée, certains prix devront être saisis manuellement et les suggestions de rebalances seront désactivées.
    </div>
    """, unsafe_allow_html=True)

# ----------------------------- LAYOUT -----------------------------
col1, col2 = st.columns([1.3, 1])

# ============================== GAUCHE ==============================
with col1:

    st.subheader("POOL SETUP")

    left, right = st.columns(2)
    with left:
        pair_labels = [f"{a}/{b}" for a, b in PAIRS]
        selected_pair = st.radio("Paire :", pair_labels, index=0)
    with right:
        strategy_choice = st.radio("Stratégie :", list(STRATEGIES.keys()))

    tokenA, tokenB = selected_pair.split("/")
    info = STRATEGIES[strategy_choice]
    ratioA, ratioB = info["ratio"]

    invert_market = st.checkbox("Inversion marché (bull → bear)")
    if invert_market:
        ratioA, ratioB = ratioB, ratioA

    # ---- RECAP DANS CADRE ----
    st.markdown(f"""
    <div style="
        background-color: #27F5A9;
        border-left: 6px solid #00754A;
        padding: 15px 20px;
        border-radius: 8px;
        margin: 12px 0 25px 0;
    ">
    <b>Ratio :</b> {int(ratioA*100)} / {int(ratioB*100)}<br>
    <b>Objectif :</b> {info['objectif']}<br>
    <b>Contexte :</b> {info['contexte']}
    </div>
    """, unsafe_allow_html=True)

    capital = st.number_input("Capital (USD)", value=1000, step=50)

    # ---- PRIX ----
    if tokenB == "USDC":
        priceA_usd, okA = get_price_usd(tokenA)
        if not okA:
            priceA_usd = st.number_input(f"Prix manuel {tokenA}", value=1.0)
        priceA = priceA_usd
        okB = True
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

        priceB_usd = max(priceB_usd, 1e-7)
        priceA = priceA_usd / priceB_usd

    # ---- RANGE ----
    range_pct = st.number_input("Range (%)", 1.0, 100.0, 20.0)
    range_low = priceA * (1 - ratioA * range_pct / 100)
    range_high = priceA * (1 + ratioB * range_pct / 100)
    if invert_market:
        range_low, range_high = range_high, range_low

    capitalA, capitalB = capital * ratioA, capital * ratioB


# ============================== DROITE ==============================
with col2:

    # ---- Price/range ----
    st.markdown("""
    <div style="
        background-color:#FFA700;
        border-left:6px solid #754C00;
        padding:15px 20px;
        border-radius:8px;
        margin-bottom:25px;
    ">
        <h3>PRICE / RANGE</h3>
    """, unsafe_allow_html=True)

    st.write(f"Prix actuel : {priceA:.6f} $")
    st.write(f"Range : {range_low:.6f} ↔ {range_high:.6f}")
    st.write(f"Répartition : {capitalA:.2f} USD {tokenA} ◄► {capitalB:.2f} USD {tokenB}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---- HISTORIQUE ----
    key = f"{tokenA}_prices_{datetime.date.today()}"
    if key not in st.session_state:
        st.session_state[key] = get_market_chart(COINGECKO_IDS[tokenA])
    pricesA = st.session_state[key]

    vol_30d = compute_volatility(pricesA)
    rebalances = sum((p < range_low) or (p > range_high) for p in pricesA)

    # ---- SECTION ANALYSE 30 JOURS ----
    st.markdown("""
    <div style="
        background-color:#FFA700;
        border-left:6px solid #754C00;
        padding:15px 20px;
        border-radius:8px;
        margin-bottom:25px;
    ">
        <h3>Analyse 30 jours</h3>
    """, unsafe_allow_html=True)

    st.write(f"Volatilité : {vol_30d*100:.2f}% — Hors range : {rebalances}")

    # Simulation fixée à 30 jours
    future_days = 30
    vol_sim = vol_30d
    simulated = [pricesA[-1]]

    for _ in range(future_days):
        simulated.append(simulated[-1] * (1 + np.random.normal(0, vol_sim)))

    future_reb = sum((p < range_low) or (p > range_high) for p in simulated)
    st.write(f"Simulation future (30j) → Hors range : {future_reb}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---- ANALYSE STRATEGIE ----
    vol_7d = compute_volatility(pricesA[-7:])
    suggestion = "Mini-doux"

    if okA and okB:
        if vol_7d > 0.04:
            suggestion = "Coup de pouce"
        elif vol_7d > 0.02:
            suggestion = "Mini-Doux"
    else:
        suggestion = "Coup de pouce"

    st.markdown("""
    <div style="
        background-color:#FFA700;
        border-left:6px solid #754C00;
        padding:15px 20px;
        border-radius:8px;
        margin-bottom:25px;
    ">
        <h3>Analyse stratégie</h3>
    """, unsafe_allow_html=True)

    st.write(f"Vol 7j : {vol_7d*100:.2f}% — Suggestion : {suggestion}")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================== AUTOMATION ===========================
st.markdown("""
<div style="background: linear-gradient(135deg,#8e2de2,#4fac66);padding:20px;border-radius:12px;margin-top:20px;">
    <span style="color:white;font-size:28px;font-weight:700;">REGLAGES AUTOMATION</span>
</div>
""", unsafe_allow_html=True)

# ---- Range future + Time-buffer (2 colonnes) ----
col_range, col_time = st.columns([2,1])

with col_range:
    st.markdown("""
    <div style="
        background-color:#FFA700;
        border-left:6px solid #754C00;
        padding:15px 20px;
        border-radius:8px;
        margin-top:25px;
        margin-bottom:15px;
    ">
        <h3>Range future</h3>
    </div>
    """, unsafe_allow_html=True)

    range_percent = st.slider("Range total (%)", 1.0, 90.0, 20.0, step=0.5)
    ratio_low, ratio_high = 20, 80
    low_offset_pct = -range_percent * ratio_low / 100
    high_offset_pct = range_percent * ratio_high / 100
    final_low = priceA * (1 + low_offset_pct/100)
    final_high = priceA * (1 + high_offset_pct/100)
    if invert_market:
        final_low, final_high = final_high, final_low
    st.write(f"Range : {final_low:.6f} – {final_high:.6f}")

with col_time:
    st.markdown("""
    <div style="
        background-color:#FFA700;
        border-left:6px solid #754C00;
        padding:15px 20px;
        border-radius:8px;
        margin-top:25px;
        margin-bottom:15px;
    ">
        <h3>Time-buffer</h3>
    </div>
    """, unsafe_allow_html=True)

    vola = vol_30d * 100
    if vola < 1:
        recomand = "6 à 12 minutes"
    elif vola < 3:
        recomand = "18 à 48 minutes"
    else:
        recomand = "60 minutes et plus"
    st.write(f"Recommandation avec la volatilité actuelle : {recomand}")

# ---- Trigger d’anticipation ----
st.markdown("""
<div style="
    background-color:#FFA700;
    border-left:6px solid #754C00;
    padding:15px 20px;
    border-radius:8px;
    margin-top:25px;
    margin-bottom:15px;
">
    <h3>Trigger d’anticipation</h3>
</div>
""", unsafe_allow_html=True)

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

# ---- Rebalance avancée (futur range) ----
st.markdown("""
<div style="
    background-color:#FFA700;
    border-left:6px solid #754C00;
    padding:15px 20px;
    border-radius:8px;
    margin-top:25px;
    margin-bottom:15px;
">
    <h3>Rebalance avancée (futur range)</h3>
</div>
""", unsafe_allow_html=True)

global_range = range_percent
off_low_pct  = -ratioA * global_range
off_high_pct =  ratioB * global_range
bear_low  = priceA * (1 + off_low_pct / 100)
bear_high = priceA * (1 + off_high_pct / 100)
bull_low  = priceA * (1 - off_high_pct / 100)
bull_high = priceA * (1 - off_low_pct / 100)

col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown("**Marché Baissier (Dump)**")
    st.write(f"Range Low : {bear_low:.6f} ({off_low_pct:.0f}%)")
    st.write(f"Range High : {bear_high:.6f} (+{off_high_pct:.0f}%)")

with col_b2:
    st.markdown("**Marché Haussier (Pump)**")
    st.write(f"Range Low : {bull_low:.6f} ({-off_high_pct:.0f}%)")
    st.write(f"Range High : {bull_high:.6f} (+{off_low_pct:.0f}%)")
