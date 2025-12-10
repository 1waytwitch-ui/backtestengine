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
# ======================
#   BANNIÈRE + BOUTON
# ======================

if "show_guide" not in st.session_state:
    st.session_state.show_guide = False

clicked = st.button("Guide", key="guide_button_top")

if clicked:
    st.session_state.show_guide = not st.session_state.show_guide

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
        <img src="https://t.me/i/userpic/320/Pigeonchanceux.jpg" 
             style="width:60px;height:60px;border-radius:50%;border:2px solid white;">
        <a href="https://t.me/Pigeonchanceux" target="_blank" 
           style="color:white;font-size:18px;font-weight:600;text-decoration:none;margin-left:10px;">
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

# ======================
#   CONTENU DU GUIDE
# ======================

st.session_state["guide_text"] = """
Bienvenue !  
Ce guide t’explique **pas à pas** comment comprendre et utiliser les stratégies de LP (Liquidity Providing) dans un AMM (Automated Market Maker) concentré comme Uniswap, Aerodrome, Pancake...

Krystal, Vfat, Aperture... **ne sont que des agrégateurs de positions** !

# — C’est quoi fournir de la liquidité ?

Quand tu fournis de la liquidité à une pool (ex : WETH/USDC), tu apportes **deux tokens en même temps**. En échange, tu deviens **market maker** et tu touches des **frais de trading (trading fees)**.

Dans un AMM concentré, tu choisis **un range** où ton capital est actif. Si le prix sort du range → tu deviens **full Token A** ou **full Token B**. Pour rester efficace, il faut parfois **rebalance** ta position.

Ta position s’ajuste automatiquement : **quand le prix baisse, tu accumules le token le plus volatile** ; à l’inverse, **quand le prix monte, tu revends progressivement ce token volatil.**

# — Les trois concepts fondamentaux

→ Le **ratio**, c’est la proportion entre Token A (volatile) et Token B (stable ou moins volatile).

Exemples :
- 50/50 → neutre  
- 20/80 → plutôt défensif  
- 95/5 → très agressif vers Token A  

Ce ratio influence ton **risque**, ta **direction** (bullish ou bearish) et ton **range**.

→ Le **range** définit la zone de prix dans laquelle ton capital est utilisé dans la pool.  
Exemple : Range 1800 – 2200.  
Si le prix reste dans cette fourchette → tu génères des fees.  
S’il en sort → tu n’en génères plus.

Plus **le range est serré** :  
- *plus tu gagnes de fees*  
- *plus les rebalances seront fréquents*  
- *plus l’Impermanent Loss (IL) augmente*

→ L’**impermanent loss (IL)** est la perte que tu aurais évitée si tu avais simplement conservé (HOLD) tes tokens.

Important :  
- L’IL n’est pas un joker magique.  
- Elle n’est pas toujours “petite”.  
- Elle augmente fortement si le prix s’éloigne du point d’entrée.

Un range très large donne une IL **extrêmement importante**, qu’il faudra gérer soit par une sortie de position, soit par un rebalance partiel.

# — Les stratégies possibles

**Neutre : 50/50**  
Pour : marché incertain, latéral  
Avantages : stable, simple  
Risques : IL si gros mouvement

**Coup de pouce : 20/80**  
Pour : marché calme, faible volatilité  
Avantages : protège du token volatil  
Mode : défensif

**Mini-doux : 10/90**  
Pour : anticipation de tendance  
Avantages : minimise l’IL  
Mode : très défensif

**Side-line up : 100/0**  
Pour : bas de marché, dumps  
Avantages : accumuler le token volatil  
Mode : agressif / accumulation

**Side-line down : 0/100**  
Pour : marché haussier  
Avantages : prise de profit naturelle  
Mode : agressif vers la vente

# — Comment choisir un range ?

Le choix du range dépend de ton objectif, de la volatilité et du marché :

- marché haussier → stratégies de profits A→B  
- marché baissier → stratégies d’accumulation B→A  
- marché latéral → neutre ou coup de pouce

Objectifs :
- **Saisir des fees** → petit range  
- **Limiter l’IL** → range large ou mini-doux  
- **DCA** → ratio extrême (100/0 ou 0/100)

# — Exemple simple : pool WETH/USDC

- Capital : 1000 USD  
- Prix ETH : 3000  
- Stratégie : 50/50  
- Range : ±20% (volatilité = 8%)

### Étape 1 : Répartition  
→ 500 USD en ETH  
→ 500 USD en USDC  

### Étape 2 : Range  
→ Bas ≈ 2700  
→ Haut ≈ 3300  

### Résultat 1 : Si prix = 3300  
→ tu deviens plus riche en USDC  
→ tu as généré des fees  

### Résultat 2 : Si prix = 2700  
→ tu possèdes plus de token ETH  
→ tu as généré des fees  
→ IL très faible (~1 à 2%)

# — Les erreurs de débutant

### Range trop serré  
Trop de rebalances, IL amplifiée, capital qui s’épuise.

### Oublier l’IL  
Les fees **ne compensent pas toujours** l’impermanent loss.

### Oublier la volatilité  
La volatilité 7j et 30j est un indicateur clé.  
Il n’existe aucune stratégie *set and forget* viable à long terme. Même avec de l’automation, il faudra ajuster régulièrement.  
Sinon, autant acheter l’actif bas et simplement le HOLD jusqu’à une prise de profit.

# — Rebalancer une position

Quand le prix sort du range :  
→ tu deviens full A ou full B  
→ tu ne génères plus de fees  
→ ta LP devient un simple “bag”  
→ il faut repositionner la liquidité

L’application calcule automatiquement :
- combien de fois le prix est sorti dans le passé  
- combien de fois dans une simulation future  
- comment ajuster un range  

Cela aide à **planifier l’automation ou les rebalances**.

# — Comprendre la courbe d’Impermanent Loss

Le graphe montre :
- IL(%) selon le prix  
- le prix d’entrée  
- le prix actuel  
- le range bas/haut  

Interprétation :
- **Le minimum de la courbe = prix de dépôt**  
- Plus le prix s’éloigne → plus l’IL augmente  
- IL = 0 uniquement si le prix reste exactement au point d’entrée

# — Quand une stratégie LP devient rentable ?

Elle est rentable si :
1. **les frais gagnés > l’impermanent loss**  
2. le prix **ne sort pas trop vite** du range  
3. ta stratégie correspond à ton objectif (DCA, prise de profit, accumulation)

# — Astuces pour devenir autonome

- Commence avec un faible capital et un **range large**  
- Utilise des stratégies **asymétriques** si marché directionnel  
- Vérifie toujours la **volatilité 7j / 30j**  
- Ne dépose pas tout ton capital d’un coup  
- Surveille la **courbe IL** après le dépôt  
- Dépose via le DEX directement quand tu maîtrises mieux

# — Conclusion

Ce guide t’a apporté :  
- les concepts fondamentaux  
- une explication simple des stratégies  
- comment lire ratio, range, volatilité  
- comment interpréter l’IL  
- comment éviter les erreurs classiques  

Avec l’application, tu disposes d’un **véritable backtest LP**, parfait pour apprendre à gérer des pools concentrés et comprendre leur mécanique globale.
"""

# ======================
#   AFFICHAGE DU GUIDE
# ======================

st.markdown("---")  # séparation visuelle

if st.session_state.show_guide:
    st.subheader("Guide - Fournir de la liquidité concentrée")
    st.markdown(st.session_state["guide_text"], unsafe_allow_html=True)


