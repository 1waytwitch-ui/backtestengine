import streamlit as st
import requests
import numpy as np
import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

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
    "Coup de pouce": {"ratio": (0.2, 0.8), "objectif": "Range efficace", "contexte": "Faible volatilité (attention à inverser en fonction du marché)"},
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
.deFi-buttons a {
    color: white;
    font-size: 18px;
    font-weight: 600;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 12px;
    margin-left: 10px;
}
.guide-btn {
    background-color: #a17fff;
}
.telegram-btn {
    background-color: #6c5ce7; /* optionnel, juste pour différencier */
}
</style>

<div class="deFi-banner">
    <div class="deFi-title-text">LP STRATÉGIES BACKTEST ENGINE</div>
    <div class="deFi-buttons">
        <a href="#guide" class="guide-btn">Guide</a>
        <a href="https://t.me/Pigeonchanceux" target="_blank" class="telegram-btn">
            <img src="https://t.me/i/userpic/320/Pigeonchanceux.jpg" style="width:30px;height:30px;border-radius:50%; vertical-align: middle; margin-right:5px;">
            Mon Telegram
        </a>
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

    # ---- RECAP OVERLAY ----
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

    # === GAUGE A/B ===
    fig_bar = go.Figure()

    fig_bar.add_trace(go.Bar(
        x=[ratioA * 100],
        y=[f"{tokenA}"],
        orientation="h",
        marker=dict(color="#FF8C00"),
        name=tokenA
    ))

    fig_bar.add_trace(go.Bar(
        x=[ratioB * 100],
        y=[f"{tokenB}"],
        orientation="h",
        marker=dict(color="#6A5ACD"),
        name=tokenB
    ))

    fig_bar.update_layout(
        barmode="stack",
        height=120,
        title="Répartition A / B (%)",
        margin=dict(l=10, r=10, t=40, b=20),
        xaxis=dict(range=[0, 100], title="Pourcentage"),
        yaxis=dict(showticklabels=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---- HISTORIQUE ----
    key = f"{tokenA}_prices_{datetime.date.today()}"
    if key not in st.session_state:
        st.session_state[key] = get_market_chart(COINGECKO_IDS[tokenA])
    pricesA = st.session_state[key]

    vol_30d = compute_volatility(pricesA)
    rebalances = sum((p < range_low) or (p > range_high) for p in pricesA)

    # ---- ANALYSE STRATEGIE ----
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

    st.write(f"Volatilité (30j) : {vol_30d*100:.2f}% — Hors range : {rebalances}")

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

    st.write(f"Vol 7j : {vol_7d*100:.2f}% — Suggestion : {suggestion}")

    st.markdown("</div>", unsafe_allow_html=True)


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

# --- Fonctions de calcul ---
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

# --- Interface IL ---
st.markdown("""
<div style="background: linear-gradient(135deg,#8e2de2,#4fac66);padding:20px;border-radius:12px;margin-top:20px;">
    <span style="color:white;font-size:28px;font-weight:700;">IMPERMANENT LOSS</span>
</div>
""", unsafe_allow_html=True)

# --- Inputs compacts ---
st.write("")
row1_col1, row1_col2, row1_col3 = st.columns([1,1,1])
with row1_col1:
    P_deposit = st.number_input("P_deposit", value=3000.0, format="%.6f", step=0.001)
with row1_col2:
    P_now = st.number_input("P_now", value=3000.0, format="%.6f", step=0.001)
with row1_col3:
    v_deposit = st.number_input("Valeur deposit (USD)", value=500.0, format="%.2f", step=0.01)

row2_col1, row2_col2 = st.columns([1,1])
with row2_col1:
    P_lower = st.number_input("P_lower", value=2800.0, format="%.6f", step=0.001)
with row2_col2:
    P_upper = st.number_input("P_upper", value=3500.0, format="%.6f", step=0.001)

# --- Calcul de L et normalisation ---
L_raw = compute_L(P_deposit, P_lower, P_upper, v_deposit)
x0_raw, y0_raw = tokens_from_L(L_raw, P_deposit, P_lower, P_upper)
L, x0, y0 = normalize_L(L_raw, x0_raw, y0_raw, P_deposit, v_deposit)

# --- Grille prix ---
prices = np.linspace(P_lower*0.8, P_upper*1.3, 400)
LP_values = V_LP(prices, L, P_lower, P_upper)
HODL_values = V_HODL(prices, x0, y0)
IL_curve = (LP_values / HODL_values - 1) * 100

# --- Graphique IL(%) ---
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=prices,
    y=IL_curve,
    mode="lines",
    name="IL(%)",
    line=dict(color="red", width=3)
))


fig.add_vline(
    x=P_lower,
    line=dict(color="green", width=2, dash="dot"),
    name="Range Low"
)
fig.add_annotation(
    x=P_lower,
    y=max(IL_curve),
    text="Low",
    showarrow=False,
    font=dict(color="green", size=12),
    yshift=10
)

fig.add_vline(
    x=P_upper,
    line=dict(color="green", width=2, dash="dot"),
    name="Range High"
)
fig.add_annotation(
    x=P_upper,
    y=max(IL_curve),
    text="High",
    showarrow=False,
    font=dict(color="green", size=12),
    yshift=10
)

fig.add_vline(
    x=P_deposit,
    line=dict(color="blue", width=2, dash="dash"),
    name="Price Deposit"
)
fig.add_annotation(
    x=P_deposit,
    y=min(IL_curve),
    text="Deposit",
    showarrow=False,
    font=dict(color="blue", size=12),
    yshift=-10
)

fig.add_vline(
    x=P_now,
    line=dict(color="purple", width=2),
    name="Price Now"
)
fig.add_annotation(
    x=P_now,
    y=min(IL_curve),
    text="Now",
    showarrow=False,
    font=dict(color="purple", size=12),
    yshift=-10
)

fig.update_xaxes(range=[min(prices), max(prices)])
fig.update_yaxes(tickformat=".2f", automargin=True)

fig.update_layout(
    height=380,
    title="Impermanent Loss (%)",
    xaxis_title="Prix",
    yaxis_title="IL (%)",
    margin=dict(l=70, r=40, t=50, b=40),
    plot_bgcolor="rgba(245,245,245,0.6)",
    paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig, use_container_width=True)



# --- Valeurs actuelles et L au dépôt ---
IL_now = (V_LP(P_now, L, P_lower, P_upper) / V_HODL(P_now, x0, y0) - 1) * 100
LP_now = V_LP(P_now, L, P_lower, P_upper)
HODL_now = V_HODL(P_now, x0, y0)

html_block = f"""
<div style="background-color:#27F5A9;border-left:6px solid #00754A;padding:18px 25px;border-radius:12px;margin-top:20px;color:#000;text-align:center;">

<h3 style="margin:0 0 10px 0;">Simulation IL</h3>

<div style="font-size:18px;font-weight:600;display:flex;justify-content:center;gap:35px;flex-wrap:wrap;">
    <span>IL maintenant : {IL_now:.2f}%</span>
    <span>Valeur LP : ${LP_now:,.2f}</span>
    <span>Valeur HODL : ${HODL_now:,.2f}</span>
</div>

</div>
"""

st.markdown(html_block, unsafe_allow_html=True)

# --- GUIDE COMPLET ---
guide_html = """
<div id="guide" style="background:#f9f9f9; padding:25px 30px; border-radius:12px; margin-top:40px; font-family:sans-serif; color:#222; max-width:900px; line-height:1.6;">

<h2 style="border-bottom:3px solid #4caf50; padding-bottom:10px;">Guide - Fournir de la liquidité concentrée</h2>

<p>Bienvenue !<br>
Ce guide t’explique <b>pas à pas</b> comment comprendre et utiliser les stratégies de LP (Liquidity Providing) dans un AMM (automated Market Maker) concentré comme Uniswap, Aerodrome, Pancake...</p>

<p>Krystal, Vfat, aperture... <b>sont uniquement des agrégateurs de positions</b> !</p>

<h3>— C’est quoi fournir de la liquidité ?</h3>

<p>Quand tu fournis de la liquidité à une pool (ex : WETH/USDC), tu apportes <b>deux tokens en même temps</b>. En échange, tu deviens <b>market maker</b> et tu touches des <b>frais de trading (trading fees)</b>.</p>

<p>Dans un AMM concentré tu choisis <b>un range</b> où ton capital est actif, si le prix sort du range → tu deviens <b>full Token A</b> ou <b>full Token B</b> et pour rester efficace → parfois il faut <b>rebalance</b> ton range.</p>

<p>Ta position s’ajuste automatiquement : <b>quand le prix baisse, tu accumules le token le plus volatile</b> à l’inverse, <b>quand le prix monte, tu revends progressivement ce token volatile.</b></p>

<h3>— Les trois concepts fondamentaux</h3>

<p>→ Le ratio c’est la proportion entre Token A (volatile) et Token B (stable ou moins volatile).</p>

<p>Exemples :</p>
<ul>
<li>50/50 → neutre</li>
<li>20/80 → plutôt défensif</li>
<li>95/5 → très agressif vers Token A</li>
</ul>

<p>Ce ratio influence ton <b>risque</b>, ta <b>direction</b> (bullish ou bearish) et ton <b>range</b>.</p>

<p>→ Le range définit la zone de prix dans laquelle ton capital est utilisé dans la pool.</p>

<p>Exemple avec un range 1800 – 2200, si le prix du token reste dans la fourchette → tu génères des fees et si le prix sort → tu n’en génères plus.</p>

<p>Plus <b>le range est serré</b> :</p>
<ul>
<li>Plus tu gagnes de fees</li>
<li>Plus tu risques des rebalances fréquentes</li>
<li>Plus tu subis de l’Impermanent Loss (IL)</li>
</ul>

<p>→ L'impermanent loss (IL) c’est la perte que tu aurais évitée si tu avais juste conservé (hold) tes tokens sans les déposer.</p>

<p>Important :<br>
L’IL n’est pas un joker magique.<br>
Elle n’est pas toujours “petite”.<br>
Elle augmente si le prix s’éloigne fortement du point d’entrée.</p>

<p>Un range très large donnera une IL <b>extrêmement importante qu'il faudra savoir gérer soit par une sortie de la position soit pas un rebalance partiel.</b></p>

<h3>→ Voici les stratégies possibles</h3>
<ul>
<li>Neutre : 50/50 — Pour : marché incertain, latéral — Avantages : stable, simple — Risques : IL si gros mouvement</li>
<li>Coup de pouce : 20/80 — Pour : marché calme, faible volatilité — Avantages : protège du token volatil — Mode : plus défensif</li>
<li>Mini-doux : 10/90 — Pour : anticipation de tendance — Avantages : minimise l’IL — Mode : très défensif</li>
<li>Side-line up : 100/0 — Pour : bas de marché, dumps — Avantages : accumuler du token volatile — Mode : agressif / accumulation</li>
<li>Side-line down : 0/100 — Pour : marché haussier — Avantages : prendre profit naturellement — Mode : agressif vers la vente</li>
</ul>

<h3>— Comment choisir un range ?</h3>

<p>Le choix du range dépend de ton objectif, de la volatilité et du marché.</p>
<ul>
<li>marché haussier → privilégier des stratégies de profits A→B</li>
<li>marché baissier → privilégier des stratégies d’accumulation B→A</li>
<li>range latéral → neutre ou coup de pouce</li>
</ul>

<p>Objectifs :</p>
<ul>
<li><b>Saisir des fees</b> → petit range</li>
<li><b>Limiter IL</b> → grand range sans rebalance ou mini-doux</li>
<li><b>DCA</b> → ratio 100/0 ou 0/100</li>
</ul>

<h3>— Exemple simple avec un pool WETH/USDC</h3>
<ul>
<li>Capital = 1000 USD</li>
<li>Prix ETH = 3000</li>
<li>Stratégie = 50/50</li>
<li>Range = ±20% (car volatilité à 8%)</li>
</ul>

<h4>Étape 1 : Répartition</h4>
<p>→ 500 USD en ETH<br>→ 500 USD en USDC</p>

<h4>Étape 2 : Range calculé</h4>
<p>→ Bas ≈ 3000 × (1 - 0.5 × 0.20) = 2700<br>→ Haut ≈ 3000 × (1 + 0.5 × 0.20) = 3300</p>

<h4>Résultat 1 : Si le prix = 3300</h4>
<p>→ tu deviens plus riche en USDC<br>→ tu as généré des fees</p>

<h4>Résultat 2 : Si le prix = 2700</h4>
<p>→ tu possède maintenant plus de token ETH<br>→ tu as généré des fees<br>→ tu subis un IL très faible (~1 à 2%)</p>

<h3>— Les erreurs de débutant</h3>
<h4>Range trop serré</h4>
<p>Résultat trop de rebalances, coût d'opportunité importants, IL amplifiée et capital qui va rapidement partir.</p>

<h4>Oublier que l’IL existe</h4>
<p>Les fees <b>ne compensent pas toujours</b> l’IL.</p>

<h4>Choisir un range sans regarder la volatilité</h4>
<p>La volatilité 7j et 30j est un indicateur clé. Il n’existe pas de stratégie <i>set and forget</i> réellement viable sur le long terme...</p>

<h3>— Rebalancer la position</h3>
<p>Quand le prix sort du range tu deviens full A ou full B, tu ne gagnes plus de fees, ta LP = un simple “bag” de tokens et tu dois repositionner la liquidité si tu veux rester efficace.</p>

<p>L'app calcule automatiquement :</p>
<ul>
<li>combien de fois prix sort dans le passé</li>
<li>combien de fois dans une simulation future</li>
<li>comment ajuster automatiquement un range</li>
</ul>

<p>Ça aide énormément à <b>planifier l'automation ou les rebalances</b> d’une stratégie.</p>

<h3>— Comprendre la courbe d’Impermanent Loss</h3>
<p>Le graphe montre :</p>
<ul>
<li>IL(%) en fonction du prix actuel</li>
<li>une ligne pour le prix de dépôt</li>
<li>une ligne pour le prix actuel</li>
<li>le range bas/haut</li>
</ul>

<p>Interprétation :</p>
<ul>
<li><b>Le minimum de la courbe = prix de dépôt</b></li>
<li>Plus on s’éloigne → plus l’IL augmente</li>
<li>IL = 0 seulement si tu restes exactement au même prix</li>
</ul>

<h3>— Quand une stratégie LP est rentable ?</h3>
<p>Elle devient rentable si :</p>
<ul>
<li><b>Les frais gagnés sont > impermanent loss</b></li>
<li>Le prix <b>ne sort pas trop vite du range</b></li>
<li>Ta stratégie est cohérente avec ton objectif (DCA, prise de profit, accumulation…)</li>
</ul>

<h3>— Astuces et autonomie des choix</h3>
<ul>
<li>Commence toujours avec un faible capital et un <b>range large</b></li>
<li>Utilise des stratégies <b>asymétriques</b> si marché directionnel</li>
<li>Vérifie toujours la <b>volatilité 7j et 30j</b></li>
<li>Ne dépose pas tout ton capital d’un coup</li>
<li>Surveille la <b>courbe IL</b> après le dépôt</li>
<li>Utilise le dex pour déposer la liquidité (expert)</li>
</ul>

<h3>— Conclusion</h3>
<p>Ce guide t’a donné :</p>
<ul>
<li>les concepts fondamentaux</li>
<li>des explication simple des stratégies</li>
<li>comment interpréter ratios, range, volatilité</li>
<li>comment lire l’IL</li>
<li>comment éviter les erreurs classiques</li>
</ul>

<p>Avec l'application, tu as un <b>backtest complet des LP</b>, parfait pour apprendre et comprendre comment gérer des pools concentrés avec la mécanique globale.</p>

</div>
"""

st.markdown(guide_html, unsafe_allow_html=True)
