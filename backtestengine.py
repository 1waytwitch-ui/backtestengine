import streamlit as st
import requests
import numpy as np
import datetime

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
st.markdown("""
<style>
.stApp {background-color:#FFFFFF !important; color:#000000 !important; font-weight:500 !important;}
h1,h2,h3,h4 {color:#000000 !important; font-weight:700 !important;}
.stTextInput > div > div > input, .stNumberInput > div > div > input {
    background-color:#F0F0F0 !important; color:#000000 !important; border:1px solid #000000 !important; border-radius:6px !important; font-weight:600 !important; height:28px !important; padding:0 8px !important; font-size:14px !important;
}
.stButton > button {background-color:#000000 !important; color:#FFFFFF !important; font-weight:700 !important; border:1px solid #000000 !important; padding:0.4rem 1rem !important; border-radius:6px !important;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# STRATEGIES ET TOKENS
# ---------------------------------------------------------------------
STRATEGIES = {
    "Neutre": {"ratio": (0.5, 0.5), "objectif": "Rester dans le range", "contexte": "Incertitude"},
    "Coup de pouce": {"ratio": (0.2, 0.8), "objectif": "Range efficace", "contexte": "Faible volatilité"},
    "Mini-doux": {"ratio": (0.1, 0.9), "objectif": "Nouveau régime prix", "contexte": "Changement de tendance"},
}

COINGECKO_IDS = {
    "WETH": "weth",
    "USDC": "usd-coin",
    "CBBTC": "coinbase-wrapped-btc",
}

PAIRS = [("WETH","USDC"), ("CBBTC","USDC"), ("WETH","CBBTC")]

# ---------------------------------------------------------------------
# FONCTIONS
# ---------------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def get_market_chart(asset_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{asset_id}/market_chart?vs_currency=usd&days=30&interval=daily"
        data = requests.get(url).json()
        prices = [p[1] for p in data.get("prices", [])]
        return prices if prices else [1.0]*30
    except:
        return [1.0]*30

def get_current_price(asset_id):
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={asset_id}&vs_currencies=usd").json()
        return response[asset_id]["usd"], True
    except:
        return 0.0, False

def compute_volatility(prices):
    if len(prices)<2: return 0.0
    returns = np.diff(prices)/prices[:-1]
    return np.std(returns)*np.sqrt(365)

# ---------------------------------------------------------------------
# TITRE + TELEGRAM
# ---------------------------------------------------------------------
col_title, col_telegram = st.columns([3,1])
with col_title:
    st.title("LP Stratégies Backtest Engine")
with col_telegram:
    st.image("https://t.me/i/userpic/320/Pigeonchanceux.jpg", width=80)
    st.markdown("[Mon Telegram](https://t.me/Pigeonchanceux)")

# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------
col1, col2 = st.columns([1.3,1])
with col1:
    st.subheader("Configuration de la Pool")
    pair_labels = [f"{a}/{b}" for a,b in PAIRS]
    selected_pair = st.radio("Paire :", pair_labels)
    strategy_choice = st.radio("Stratégie :", list(STRATEGIES.keys()))
    tokenA, tokenB = selected_pair.split("/")
    ratioA, ratioB = STRATEGIES[strategy_choice]["ratio"]

    # Checkbox inversion marché Bull/Bear
    invert_market = st.checkbox("Inversion marché (Bull → Bear)")
    if invert_market:
        ratioA, ratioB = ratioB, ratioA

    st.write(f"Ratio : {int(ratioA*100)}/{int(ratioB*100)}")
    capital = st.number_input("Capital (USD)", value=1000, step=50)

    # Prix
    def get_price_usd(token):
        try:
            p = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={COINGECKO_IDS[token]}&vs_currencies=usd").json()
            return p[COINGECKO_IDS[token]]["usd"], True
        except:
            return 0.0, False

    priceA_usd,_ = get_price_usd(tokenA)
    if tokenB=="USDC":
        priceA = priceA_usd
    else:
        priceB_usd,_ = get_price_usd(tokenB)
        priceB_usd = max(priceB_usd,0.0000001)
        priceA = priceA_usd/priceB_usd

    range_pct = st.number_input("Range (%)", 1.0,100.0,20.0,1.0)
    range_low = priceA*(1-ratioA*range_pct/100)
    range_high = priceA*(1+ratioB*range_pct/100)
    if invert_market:
        range_low, range_high = range_high, range_low

    capitalA = capital*ratioA
    capitalB = capital*ratioB

with col2:
    st.subheader("Range et Prix")
    st.write(f"Prix actuel {tokenA}/{tokenB} : {priceA:.6f}")
    st.write(f"Limite basse : {range_low:.6f}")
    st.write(f"Limite haute : {range_high:.6f}")
    st.write(f"{tokenA} : {capitalA:.2f} USD")
    st.write(f"{tokenB} : {capitalB:.2f} USD")

# ---------------------------------------------------------------------
# HISTORIQUE 30J
# ---------------------------------------------------------------------
pricesA = get_market_chart(COINGECKO_IDS[tokenA])
vol_30d = compute_volatility(pricesA)

# ---------------------------------------------------------------------
# ONGLET AUTOMATION
# ---------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["Backtest 30j","Simulation future","Analyse stratégie","Automation"])
with tab4:
    st.subheader("Automation intelligente des ranges et triggers")

    # --- Slider Range ---
    range_percent = st.slider("Range total (%)",1.0,50.0,20.0,0.5)
    ratio_low = 20
    ratio_high = 80
    low_offset_pct = -range_percent*ratio_low/100.0
    high_offset_pct = range_percent*ratio_high/100.0
    final_low = priceA*(1+low_offset_pct/100.0)
    final_high = priceA*(1+high_offset_pct/100.0)

    # --- Radio Baissier/Haussier ---
    market_trend_auto = st.radio("Tendance du marché :", ["Baissier","Haussier"])

    # Calcul Range selon stratégie
    if strategy_choice in ["Mini-doux","Coup de pouce"]:
        if market_trend_auto=="Baissier":
            range_low_pct_actual = -4.0
            range_high_pct_actual = 16.0
        else:
            range_low_pct_actual = -16.0
            range_high_pct_actual = 4.0
    else:
        range_low_pct_actual = (final_low-priceA)/priceA*100
        range_high_pct_actual = (final_high-priceA)/priceA*100

    # Appliquer inversion Bull/Bear
    if invert_market:
        range_low_pct_actual, range_high_pct_actual = range_high_pct_actual, range_low_pct_actual

    st.write(f"Range Low : **{range_low_pct_actual:.2f}%**")
    st.write(f"Range High : **{range_high_pct_actual:.2f}%**")

    # --- Triggers ---
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        trigger_low_pct = st.slider("Trigger Low (%)",0,100,15)
    with col_t2:
        trigger_high_pct = st.slider("Trigger High (%)",0,100,85)

    range_width = final_high-final_low
    trigger_low_price = final_low + (trigger_low_pct/100.0)*range_width
    trigger_high_price = final_low + (trigger_high_pct/100.0)*range_width
    st.write(f"Trigger Low : **{trigger_low_price:.6f}**")
    st.write(f"Trigger High : **{trigger_high_price:.6f}**")

    # --- Récap JSON ---
    st.header("Récapitulatif Automation")
    st.json({
        "Range total (%)": range_percent,
        "Range Low (%)": f"{range_low_pct_actual:.2f}%",
        "Range High (%)": f"{range_high_pct_actual:.2f}%",
        "Trigger Low (%)": trigger_low_pct,
        "Trigger Low (price)": trigger_low_price,
        "Trigger High (%)": trigger_high_pct,
        "Trigger High (price)": trigger_high_price
    })
