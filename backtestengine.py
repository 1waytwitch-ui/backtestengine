import streamlit as st
import requests
import numpy as np
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="LP STRATÉGIES BACKTEST ENGINE ", layout="wide")

# ==============================
#   LANG SELECTOR
# ==============================
if "lang" not in st.session_state:
    st.session_state.lang = "FR"

st.session_state.lang = st.radio("🌐 Langue / Language", ["FR", "EN"], horizontal=True)

# ==============================
#   LANGUAGE DICTIONARY
# ==============================
TXT = {
    "FR": {
        "disclaimer_title": "⚠️ DISCLAIMER IMPORTANT",
        "disclaimer_text": """
Cet outil peut comporter des approximations ou des inexactitudes. 
Il ne s’agit en aucun cas d’un conseil en investissement. 
Veuillez effectuer vos propres recherches et comprendre le mécanisme des pools de liquidités concentrés et du capital déposé.

Si l’API est surchargée, certains prix devront être saisis manuellement et les suggestions de rebalances seront désactivées.
        """,

        "config_pool": "Configuration de la Pool",
        "pair": "Paire :",
        "strategy": "Stratégie :",
        "invert": "Inversion marché (bull → bear)",

        "ratio": "Ratio",
        "objective": "Objectif",
        "context": "Contexte",

        "capital": "Capital (USD)",
        "manual_price": "Prix manuel",

        "range": "Range (%)",
        "range_price": "Range ($)",
        "current_price": "Prix actuel",
        "distribution": "Répartitions",

        "analysis_30d": "Analyse 30 jours",
        "volatility": "Volatilité",
        "out_of_range": "Hors range",

        "future_days": "Jours simulés future",
        "future_sim_out": "Simulation future → Hors range",

        "strategy_analysis": "Analyse stratégie",
        "vol7": "Vol 7j",

        "automation_settings": "REGLAGES AUTOMATION",
        "future_range": "Range future",
        "range_total": "Range total (%)",

        "trigger": "Trigger d’anticipation",
        "trigger_low": "Trigger Low (%)",
        "trigger_high": "Trigger High (%)",

        "buffer": "Time-buffer",
        "recommendation": "Recommandation avec la volatilité actuelle",

        "rebalance_adv": "Rebalance avancée (futur range)",
        "bear": "Marché Baissier (Dump)",
        "bull": "Marché Haussier (Pump)",

        "range_low": "Range Low",
        "range_high": "Range High"
    },

    "EN": {
        "disclaimer_title": "⚠️ IMPORTANT DISCLAIMER",
        "disclaimer_text": """
This tool may contain approximations or inaccuracies.  
It does NOT constitute investment advice.  
Please do your own research and make sure you fully understand 
how concentrated liquidity pools and deposited capital work.

If the API becomes overloaded, some prices may need to be entered manually 
and rebalance suggestions will be temporarily disabled.
        """,

        "config_pool": "Pool Configuration",
        "pair": "Pair:",
        "strategy": "Strategy:",
        "invert": "Market inversion (bull → bear)",

        "ratio": "Ratio",
        "objective": "Goal",
        "context": "Context",

        "capital": "Capital (USD)",
        "manual_price": "Manual price",

        "range": "Range (%)",
        "range_price": "Range ($)",
        "current_price": "Current price",
        "distribution": "Distribution",

        "analysis_30d": "30-day Analysis",
        "volatility": "Volatility",
        "out_of_range": "Out of range",

        "future_days": "Simulated future days",
        "future_sim_out": "Future simulation → Out of range",

        "strategy_analysis": "Strategy Analysis",
        "vol7": "7-day Vol",

        "automation_settings": "AUTOMATION SETTINGS",
        "future_range": "Future range",
        "range_total": "Total range (%)",

        "trigger": "Anticipation triggers",
        "trigger_low": "Trigger Low (%)",
        "trigger_high": "Trigger High (%)",

        "buffer": "Time-buffer",
        "recommendation": "Recommendation based on current volatility",

        "rebalance_adv": "Advanced Rebalance (future range)",
        "bear": "Bear Market (Dump)",
        "bull": "Bull Market (Pump)",

        "range_low": "Range Low",
        "range_high": "Range High"
    }
}

T = TXT[st.session_state.lang]

# ==============================
#   STYLES
# ==============================
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


# ==============================
#   DISCLAIMER
# ==============================
st.markdown(f"""
<div style="
    background-color: #fff3cd;
    border-left: 6px solid #ffca2c;
    padding: 15px 20px;
    border-radius: 8px;
    color: #000;
    margin-bottom: 25px;
    font-size: 15px;
">
<b>{T['disclaimer_title']}</b><br><br>
{T['disclaimer_text']}
</div>
""", unsafe_allow_html=True)


# ==============================
#   DATA
# ==============================
STRATEGIES = {
    "Neutre": {"ratio": (0.5, 0.5), "objectif": "Rester dans le range", "contexte": "Incertitude"},
    "Coup de pouce": {"ratio": (0.2, 0.8), "objectif": "Range efficace", "contexte": "Faible volatilité"},
    "Mini-doux": {"ratio": (0.1, 0.9), "objectif": "Nouveau régime prix", "contexte": "Tendance"},
    "Side-line Up": {"ratio": (0.95, 0.05), "objectif": "Accumulation", "contexte": "Dump"},
    "Side-line Below": {"ratio": (0.05, 0.95), "objectif": "Attente pump", "contexte": "Haussier"},
    "DCA-in": {"ratio": (1.0, 0.0), "objectif": "Entrée progressive", "contexte": "Accumulation"},
    "DCA-out": {"ratio": (0.0, 1.0), "objectif": "Sortie progressive", "contexte": "Tendance haussière"}
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

# ==============================
#   FUNCTIONS
# ==============================
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


# ==============================
#   LAYOUT
# ==============================
col1, col2 = st.columns([1.3, 1])

# ==============================
#   LEFT COLUMN
# ==============================
with col1:
    st.subheader(T["config_pool"])

    left, right = st.columns(2)
    with left:
        pair_labels = [f"{a}/{b}" for a, b in PAIRS]
        selected_pair = st.radio(T["pair"], pair_labels, index=0)

    with right:
        strategy_choice = st.radio(T["strategy"], list(STRATEGIES.keys()))

    tokenA, tokenB = selected_pair.split("/")
    info = STRATEGIES[strategy_choice]
    ratioA, ratioB = info["ratio"]

    invert_market = st.checkbox(T["invert"])
    if invert_market:
        ratioA, ratioB = ratioB, ratioA

    st.write(f"{T['ratio']} : {int(ratioA*100)} / {int(ratioB*100)}")
    st.write(f"{T['objective']} : {info['objectif']}")
    st.write(f"{T['context']} : {info['contexte']}")

    capital = st.number_input(T["capital"], value=1000, step=50)

    # PRICES
    if tokenB == "USDC":
        priceA_usd, okA = get_price_usd(tokenA)
        if not okA:
            priceA_usd = st.number_input(f"{T['manual_price']} {tokenA}", value=1.0)
        priceA = priceA_usd
        okB = True
    else:
        priceA_usd, okA = get_price_usd(tokenA)
        priceB_usd, okB = get_price_usd(tokenB)

        la, lb = st.columns(2)
        with la:
            if not okA:
                priceA_usd = st.number_input(f"{T['manual_price']} {tokenA}", value=1.0)
        with lb:
            if not okB:
                priceB_usd = st.number_input(f"{T['manual_price']} {tokenB}", value=1.0)

        priceB_usd = max(priceB_usd, 1e-7)
        priceA = priceA_usd / priceB_usd

    # RANGE
    range_pct = st.number_input(T["range"], 1.0, 100.0, 20.0)
    range_low = priceA * (1 - ratioA * range_pct / 100)
    range_high = priceA * (1 + ratioB * range_pct / 100)
    if invert_market:
        range_low, range_high = range_high, range_low

    capitalA, capitalB = capital * ratioA, capital * ratioB

# ==============================
#   RIGHT COLUMN
# ==============================
with col2:
    st.subheader("Range et Prix")
    st.write(f"{T['current_price']} : {priceA:.6f} $")
    st.write(f"{T['range_price']} : {range_low:.6f} ↔ {range_high:.6f}")
    st.write(f"{T['distribution']} : {capitalA:.2f} USD {tokenA} ◄► {capitalB:.2f} USD {tokenB}")

    # HISTO PRICES
    key = f"{tokenA}_prices_{datetime.date.today()}"
    if key not in st.session_state:
        st.session_state[key] = get_market_chart(COINGECKO_IDS[tokenA])
    pricesA = st.session_state[key]

    # VOL 30D
    vol_30d = compute_volatility(pricesA)
    rebalances = sum((p < range_low) or (p > range_high) for p in pricesA)

    st.subheader(T["analysis_30d"])
    st.write(f"{T['volatility']} : {vol_30d*100:.2f}% — {T['out_of_range']} : {rebalances}")

    # SIMULATION
    future_days = st.number_input(T["future_days"], 1, 120, 30)
    vol_sim = vol_30d
    simulated = [pricesA[-1]]
    for _ in range(future_days):
        simulated.append(simulated[-1] * (1 + np.random.normal(0, vol_sim)))

    future_reb = sum((p < range_low) or (p > range_high) for p in simulated)
    st.write(f"{T['future_sim_out']} : {future_reb}")

    # VOL 7D
    vol_7d = compute_volatility(pricesA[-7:])
    suggestion = "Mini-doux"

    if True:
        if vol_7d > 0.04:
            suggestion = "Coup de pouce"
        elif vol_7d > 0.02:
            suggestion = "Mini-Doux"
        else:
            suggestion = "Mini-doux"
    else:
        suggestion = "Coup de pouce"

    st.subheader(T["strategy_analysis"])
    st.write(f"{T['vol7']} : {vol_7d*100:.2f}% — Suggestion : {suggestion}")

# ==============================
#   AUTOMATION
# ==============================
st.markdown(f"""
<div style="background: linear-gradient(135deg,#8e2de2,#4fac66);
            padding:20px;border-radius:12px;margin-top:20px;">
    <span style="color:white;font-size:28px;font-weight:700;">
        {T['automation_settings']}
    </span>
</div>
""", unsafe_allow_html=True)

st.subheader(T["future_range"])
range_percent = st.slider(T["range_total"], 1.0, 90.0, 20.0, step=0.5)
ratio_low, ratio_high = 20, 80

low_offset_pct = -range_percent * ratio_low / 100
high_offset_pct = range_percent * ratio_high / 100

final_low = priceA * (1 + low_offset_pct/100)
final_high = priceA * (1 + high_offset_pct/100)
if invert_market:
    final_low, final_high = final_high, final_low

st.write(f"Range : {final_low:.6f} – {final_high:.6f}")

st.subheader(T["trigger"])
t1, t2 = st.columns(2)
with t1:
    trig_low = st.slider(T["trigger_low"], 0, 100, 10)
with t2:
    trig_high = st.slider(T["trigger_high"], 0, 100, 90)

rw = final_high - final_low
trigger_low_price = final_low + (trig_low/100)*rw
trigger_high_price = final_low + (trig_high/100)*rw

st.write(f"Trigger Low : {trigger_low_price:.6f}")
st.write(f"Trigger High : {trigger_high_price:.6f}")

st.subheader(T["buffer"])
vola = vol_30d * 100
if vola < 1:
    recomand = "6 à 12 minutes" if st.session_state.lang == "FR" else "6 to 12 minutes"
elif vola < 3:
    recomand = "18 à 48 minutes" if st.session_state.lang == "FR" else "18 to 48 minutes"
else:
    recomand = "60 minutes et plus" if st.session_state.lang == "FR" else "60 minutes or more"

st.write(f"{T['recommendation']} : {recomand}")

# ==============================
#   ADVANCED REBALANCE
# ==============================
st.subheader(T["rebalance_adv"])

global_range = range_percent
off_low_pct  = -ratioA * global_range
off_high_pct =  ratioB * global_range

bear_low  = priceA * (1 + off_low_pct / 100)
bear_high = priceA * (1 + off_high_pct / 100)
bull_low  = priceA * (1 - off_high_pct / 100)
bull_high = priceA * (1 - off_low_pct / 100)

col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown(f"**{T['bear']}**")
    st.write(f"{T['range_low']} : {bear_low:.6f} ({off_low_pct:.0f}%)")
    st.write(f"{T['range_high']} : {bear_high:.6f} (+{off_high_pct:.0f}%)")

with col_b2:
    st.markdown(f"**{T['bull']}**")
    st.write(f"{T['range_low']} : {bull_low:.6f} ({-off_high_pct:.0f}%)")
    st.write(f"{T['range_high']} : {bull_high:.6f} (+{off_low_pct:.0f}%)")
