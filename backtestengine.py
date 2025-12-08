import streamlit as st
import requests
import numpy as np
import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="LP STRATÉGIES BACKTEST ENGINE", layout="wide")

# ----------------- STYLES -----------------
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

# ----------------- HEADER -----------------
st.markdown("""
<div style="background-color:#FFA700;padding:20px;border-radius:12px; display:flex; justify-content:space-between; align-items:center;">
    <h1 style="color:white;margin:0;">LP STRATÉGIES BACKTEST ENGINE</h1>
    <div>
        <img src="https://t.me/i/userpic/320/Pigeonchanceux.jpg" style="width:60px;height:60px;border-radius:50%;vertical-align:middle;">
        <a href="https://t.me/Pigeonchanceux" target="_blank" style="color:white;font-size:18px;font-weight:600;text-decoration:none;margin-left:10px;">Mon Telegram</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- STRATEGIES / PAIRS -----------------
STRATEGIES = {
    "Neutre": {"ratio": (0.5, 0.5), "objectif": "Rester dans le range", "contexte": "Incertitude"},
    "Coup de pouce": {"ratio": (0.2, 0.8), "objectif": "Range efficace", "contexte": "Faible volatilité"},
    "Mini-doux": {"ratio": (0.1, 0.9), "objectif": "Nouveau régime prix", "contexte": "Changement de tendance"},
    "Side-line Up": {"ratio": (0.95, 0.05), "objectif": "Accumulation", "contexte": "Dump"},
    "Side-line Below": {"ratio": (0.05, 0.95), "objectif": "Attente avant pump", "contexte": "Marché haussier"},
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

# ----------------- FONCTIONS UTILITAIRES -----------------
@st.cache_data(ttl=3600)
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

# ----------------- LAYOUT PRINCIPAL -----------------
col1, col2 = st.columns([1.3,1])

with col1:
    st.subheader("POOL SETUP")
    left, right = st.columns(2)
    with left:
        pair_labels = [f"{a}/{b}" for a,b in PAIRS]
        selected_pair = st.radio("Paire :", pair_labels, index=0)
    with right:
        strategy_choice = st.radio("Stratégie :", list(STRATEGIES.keys()))

    tokenA, tokenB = selected_pair.split("/")
    ratioA, ratioB = STRATEGIES[strategy_choice]["ratio"]

    invert_market = st.checkbox("Inversion marché (bull → bear)")
    if invert_market:
        ratioA, ratioB = ratioB, ratioA

    st.markdown(f"""
    <div style="background-color:#27F5A9;padding:12px;border-radius:8px;margin:12px 0 25px 0;">
    <b>Ratio :</b> {int(ratioA*100)} / {int(ratioB*100)}<br>
    <b>Objectif :</b> {STRATEGIES[strategy_choice]['objectif']}<br>
    <b>Contexte :</b> {STRATEGIES[strategy_choice]['contexte']}
    </div>
    """, unsafe_allow_html=True)

    capital = st.number_input("Capital (USD)", value=1000.0, step=50.0, format="%.2f")

    # PRIX ACTUELS
    priceA_usd, okA = get_price_usd(tokenA)
    priceB_usd, okB = get_price_usd(tokenB)
    if not okA:
        priceA_usd = st.number_input(f"Prix manuel {tokenA}", value=1.0, format="%.6f")
    if not okB:
        priceB_usd = st.number_input(f"Prix manuel {tokenB}", value=1.0, format="%.6f")

    priceB_usd = max(priceB_usd, 1e-7)
    priceA = priceA_usd / priceB_usd

    range_pct = st.number_input("Range (%)", 1.0, 100.0, 20.0)
    range_low = priceA * (1 - ratioA * range_pct / 100)
    range_high = priceA * (1 + ratioB * range_pct / 100)
    if invert_market:
        range_low, range_high = range_high, range_low

    capitalA, capitalB = capital * ratioA, capital * ratioB

with col2:
    st.markdown(f"""
    <div style="background-color:#FFA700;padding:15px;border-radius:8px;margin-bottom:25px;">
        <h3>PRICE / RANGE</h3>
        Prix actuel : {priceA:.6f} $<br>
        Range : {range_low:.6f} ↔ {range_high:.6f}<br>
        Répartition : {capitalA:.2f} USD {tokenA} ◄► {capitalB:.2f} USD {tokenB}
    </div>
    """, unsafe_allow_html=True)

    # HISTORIQUE 30 JOURS
    key = f"{tokenA}_prices_{datetime.date.today()}"
    if key not in st.session_state:
        st.session_state[key] = get_market_chart(COINGECKO_IDS[tokenA])
    pricesA = st.session_state[key]

    vol_30d = compute_volatility(pricesA)
    rebalances = sum((p < range_low) or (p > range_high) for p in pricesA)

    st.markdown(f"""
    <div style="background-color:#FFA700;padding:15px;border-radius:8px;margin-bottom:25px;">
        <h3>Analyse 30 jours</h3>
        Volatilité : {vol_30d*100:.2f}% — Hors range : {rebalances}
    </div>
    """, unsafe_allow_html=True)

    # SIMULATION 30 JOURS FUTURE
    simulated = [pricesA[-1]]
    for _ in range(30):
        simulated.append(simulated[-1] * (1 + np.random.normal(0, vol_30d)))
    future_reb = sum((p < range_low) or (p > range_high) for p in simulated)
    st.write(f"Simulation future (30j) → Hors range : {future_reb}")

    # SUGGESTION STRATEGIE
    vol_7d = compute_volatility(pricesA[-7:])
    suggestion = "Mini-doux"
    if vol_7d > 0.04:
        suggestion = "Coup de pouce"
    elif vol_7d > 0.02:
        suggestion = "Mini-doux"
    st.markdown(f"""
    <div style="background-color:#FFA700;padding:15px;border-radius:8px;margin-bottom:25px;">
        <h3>Analyse stratégie</h3>
        Vol 7j : {vol_7d*100:.2f}% — Suggestion : {suggestion}
    </div>
    """, unsafe_allow_html=True)


# =========================== AUTOMATION ===========================
st.markdown("""
<div style="background: linear-gradient(135deg,#8e2de2,#4fac66);padding:20px;border-radius:12px;margin-top:20px;">
    <span style="color:white;font-size:28px;font-weight:700;">REGLAGES AUTOMATION</span>
</div>
""", unsafe_allow_html=True)

# ---- Range future / Time-buffer ----
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
    if vola < 2:
        recomand = "6 à 12 minutes"
    elif vola < 5:
        recomand = "18 à 48 minutes"
    else:
        recomand = "60 minutes et plus"
    st.write(f"Recommandation avec la volatilité actuelle : {recomand}")

# ---- Trigger d’anticipation / Rebalance avancée ----
col_trigger, col_rebalance = st.columns(2)

with col_trigger:
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

with col_rebalance:
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

# ----------------- SECTION IL / LP -----------------
st.markdown("<h2 style='background-color:#FFA500;color:white;padding:10px;border-radius:8px;'>Interactive Impermanent Loss (IL)</h2>", unsafe_allow_html=True)

row1_col1, row1_col2, row1_col3 = st.columns([1,1,1])
with row1_col1:
    P_deposit = st.number_input("Prix dépôt (P_deposit)", value=3000.0, format="%.6f")
with row1_col2:
    P_now = st.number_input("Prix actuel (P_now)", value=3000.0, format="%.6f")
with row1_col3:
    v_deposit = st.number_input("Valeur dépôt (USD)", value=500.0, format="%.2f")

row2_col1, row2_col2 = st.columns([1,1])
with row2_col1:
    P_lower = st.number_input("Prix lower (P_lower)", value=2800.0, format="%.6f")
with row2_col2:
    P_upper = st.number_input("Prix upper (P_upper)", value=3500.0, format="%.6f")

# FONCTIONS LP / HODL
def compute_L(P, P_l, P_u, V):
    sqrtP = np.sqrt(P)
    sqrtPl = np.sqrt(P_l)
    sqrtPu = np.sqrt(P_u)
    A = (1 / sqrtP - 1 / sqrtPu)
    B = (sqrtP - sqrtPl)
    return V / (P * A + B)

def tokens_from_L(L, P, P_l, P_u):
    sqrtP = np.sqrt(P)
    sqrtPl = np.sqrt(P_l)
    sqrtPu = np.sqrt(P_u)
    x = L * (1 / sqrtP - 1 / sqrtPu)
    y = L * (sqrtP - sqrtPl)
    return x, y

def normalize_L(L, x0, y0, P, V):
    factor = V / (x0 * P + y0)
    return L * factor, x0 * factor, y0 * factor

def x_of_P(P, L, P_upper):
    P_arr = np.asarray(P, float)
    sqrtP = np.sqrt(P_arr)
    x = L * (1 / sqrtP - 1 / np.sqrt(P_upper))
    if isinstance(x, np.ndarray):
        return np.where(x < 0, 0, x)
    return max(x, 0.0)

def y_of_P(P, L, P_lower):
    P_arr = np.asarray(P, float)
    sqrtP = np.sqrt(P_arr)
    y = L * (sqrtP - np.sqrt(P_lower))
    if isinstance(y, np.ndarray):
        return np.where(y < 0, 0, y)
    return max(y, 0.0)

def V_LP(P, L, P_lower, P_upper):
    P_arr = np.asarray(P, float)
    return x_of_P(P_arr, L, P_upper) * P_arr + y_of_P(P_arr, L, P_lower)

def V_HODL(P, x0, y0):
    return x0 * P + y0

# CALCUL
L_raw = compute_L(P_deposit, P_lower, P_upper, v_deposit)
x0_raw, y0_raw = tokens_from_L(L_raw, P_deposit, P_lower, P_upper)
L, x0, y0 = normalize_L(L_raw, x0_raw, y0_raw, P_deposit, v_deposit)

prices = np.linspace(P_lower*0.8, P_upper*1.3, 400)
LP_values = V_LP(prices, L, P_lower, P_upper)
HODL_values = V_HODL(prices, x0, y0)
IL_curve = (LP_values / HODL_values - 1) * 100

fig = go.Figure()
fig.add_trace(go.Scatter(x=prices, y=IL_curve, mode="lines", name="IL (%)", line=dict(color="red", width=3)))
fig.update_layout(height=350, title="Impermanent Loss (%) — Courbe exacte", xaxis_title="Prix", yaxis_title="IL (%)")
st.plotly_chart(fig, use_container_width=True)

IL_now = (V_LP(P_now, L, P_lower, P_upper) / V_HODL(P_now, x0, y0) - 1) * 100
LP_now = V_LP(P_now, L, P_lower, P_upper)
HODL_now = V_HODL(P_now, x0, y0)

row_metrics = st.columns(4)
row_metrics[0].metric("IL now", f"{IL_now:.2f} %")
row_metrics[1].metric("LP now", f"${LP_now:,.2f}")
row_metrics[2].metric("HODL now", f"${HODL_now:,.2f}")
