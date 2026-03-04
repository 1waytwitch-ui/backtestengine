import streamlit as st
import requests
import numpy as np
import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import yfinance as yf
import math


# Forcer l'application en mode écran large
st.set_page_config(layout="wide")

# ---- HEADER FIXE COMPACT & THEME TERMINAL ----
st.markdown("""
<style>
.deFi-banner {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 70px;  /* plus compact */
    z-index: 9999;
    background: linear-gradient(135deg, #0b0f14 0%, #141a2a 40%, #1c2338 100%);
    padding: 15px 20px;  /* réduit */
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0px 4px 18px rgba(0,0,0,0.45);
}

/* Titre */
.deFi-title-text {
    font-size: 24px;  /* plus petit */
    font-weight: 700;
    color: #00ff88 !important;  /* style terminal vert */
    font-family: "Courier New", monospace;
}

/* Boutons compact terminal style */
.deFi-buttons a {
    color: #00ff88;
    font-size: 12px;  /* plus petit */
    font-weight: 600;
    text-decoration: none;
    padding: 4px 10px;  /* moins de padding */
    border-radius: 6px;
    margin-left: 6px;
    background-color: #11161d;  /* fond sombre style terminal */
    border: 1px solid #00ff88;
    font-family: "Courier New", monospace;
    transition: 0.2s all;
}

.deFi-buttons a:hover {
    background-color: #0b0f14;
    box-shadow: 0 0 8px #00ff88;
}

/* Décaler le reste du contenu */
[data-testid="stAppViewContainer"] {
    margin-top: 70px;  /* correspond à la hauteur du header */
}
</style>

<div class="deFi-banner">
    <div class="deFi-title-text">LP STRATÉGIES BACKTEST ENGINE</div>
    <div class="deFi-buttons">
        <a href="https://defi.krystal.app/referral?r=3JwR8YRQCRJT" target="_blank">Krystal</a>
        <a href="https://plusvalueimposable.streamlit.app/" target="_blank">Plus-value</a>
        <a href="https://defiwalletbacktest.streamlit.app/" target="_blank">Wallet</a>
        <a href="https://t.me/Pigeonchanceux" target="_blank">
            <img src="https://t.me/i/userpic/320/Pigeonchanceux.jpg" style="width:20px;height:20px;border-radius:50%; vertical-align: middle; margin-right:4px;">Telegram
        </a>
        <a href="https://shorturl.at/X3sYt" target="_blank">Formation</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ===================== PLOTLY DARK =====================
pio.templates.default = "plotly_dark"

# ===================== DARK THEME GLOBAL =====================
st.markdown("""
<style>

/* ================= ROOT ================= */
:root {
    --bg-main: #0b0f14;
    --bg-card: #121716;
    --bg-soft: #181f1e;
    --accent: #1de9b6;
    --accent-soft: rgba(29,233,182,0.15);
    --text-main: #e5e7eb;
    --text-muted: #9ca3af;
    --border-soft: rgba(255,255,255,0.08);
}

/* ================= APP ================= */
.stApp {
    background-color: var(--bg-main);
    color: var(--text-main);
}

/* ================= TITRES ================= */
h1, h2, h3, h4, h5 {
    color: var(--text-main) !important;
}

/* ================= TEXTE ================= */
p, span, label {
    color: var(--text-main);
}

/* ================= INPUTS ================= */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"],
.stMultiSelect div,
.stDateInput input {
    background-color: var(--bg-soft) !important;
    color: var(--text-main) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: 10px;
}

/* Placeholder */
.stTextInput input::placeholder {
    color: var(--text-muted);
}

/* ================= CHECKBOX / RADIO ================= */
.stCheckbox label,
.stRadio label {
    color: var(--text-main) !important;
}

/* ================= BUTTONS ================= */
.stButton button {
    background: linear-gradient(135deg, #1de9b6, #14b8a6);
    color: #062b23 !important;
    border-radius: 14px;
    font-weight: 700;
    border: none;
    padding: 0.6em 1.4em;
}

.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(29,233,182,0.35);
}

/* ================= ALERTS ================= */
.stAlert {
    background-color: var(--bg-soft);
    color: var(--text-main);
    border-left: 5px solid var(--accent);
}

/* ================= PROGRESS ================= */
.stProgress > div > div {
    background-color: var(--accent);
}

/* ================= SCROLLBAR ================= */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #1de9b6;
    border-radius: 10px;
}
::-webkit-scrollbar-track {
    background: #0b0f0e;
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



# ---- DISCLAIMER ----
if st.session_state.show_disclaimer:
    st.markdown("""
    <style>
    .disclaimer-card {
        background-color: #0b0f14;
        border-left: 6px solid #00ff88;
        padding: 15px 20px;
        border-radius: 8px;
        color: #e6edf3;
        margin-bottom: 25px;
        font-size: 15px;
        line-height: 1.5;
        box-shadow: 0 0 12px rgba(0,255,136,0.05);
        transition: 0.3s ease;
    }
    .disclaimer-card:hover {
        box-shadow: 0 0 25px rgba(0,255,136,0.15);
    }
    .disclaimer-card .title {
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 10px;
    }
    .disclaimer-card .text {
        font-weight: 400;
        font-size: 16px;
        margin-bottom: 10px;
    }
    </style>

    <div class="disclaimer-card">
        <div class="title">⚠️ DISCLAIMER IMPORTANT</div>
        <div class="text">
        Un backtest en DeFi n’explique pas comment gagner, mais comment une stratégie de farming automatisée peut perdre malgré des APY élevés.
        </div>
        <div class="text">
        L’accès au backtest est exclusivement réservé aux membres de la Team Élite de la chaîne KBOUR Crypto. 
        Le code d’accès est disponible dans le canal privé “DEFI Académie”. 
        Cet outil peut comporter des approximations ou des inexactitudes. 
        Il ne s’agit en aucun cas d’un conseil en investissement. 
        Veuillez effectuer vos propres recherches et comprendre le mécanisme des pools de liquidités concentrés et du capital déposé. 
        Si l’API est surchargée, certains prix devront être saisis manuellement !
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------
# CODE SECRET
# -----------------------
SECRET_CODE = st.secrets["Secret_Code"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    # HTML + CSS overlay + bouton
    st.markdown("""
    <style>
    .login-card {
        background: linear-gradient(135deg, #0a0f1f 0%, #1e2761 40%, #4b1c7d 100%);
        padding: 28px 30px;
        border-radius: 18px;
        max-width: 420px;
        margin: 3rem auto;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0px 4px 18px rgba(0,0,0,0.45);
        text-align: center;
    }
    .login-title { font-size: 28px; font-weight: 700; color: white !important; margin-bottom: 6px; }
    .login-subtitle { font-size: 14px; color: #d1d5db; margin-bottom: 18px; }
    .elite-btn {
        display: inline-block;
        background-color: #facc15;
        color: #111827 !important;
        font-size: 16px;
        font-weight: 700;
        text-decoration: none !important;
        padding: 10px 18px;
        border-radius: 14px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        margin-bottom: 18px;
    }
    .elite-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(250,204,21,0.4);
    }
    </style>

    <div class="login-card">
        <div class="login-title">Accès sécurisé</div>
        <div class="login-subtitle">
            Réservé aux membres de la <b>Team Élite KBOUR Crypto</b><br>
            Code disponible dans <b>DEFI Académie</b>
        </div>
        <!-- BOUTON EXTERNE -->
        <a href="https://www.youtube.com/channel/UCZL_vS9bsLI4maA4Oja9zyg/join" 
           target="_blank" class="elite-btn">
           Rejoindre la Team Élite
        </a>
    </div>
    """, unsafe_allow_html=True)

    # INPUT STREAMLIT séparé pour que ce soit cliquable
    st.text_input("Code d'accès", key="secret_code", type="password")
    if st.button("Valider", use_container_width=True):
        if st.session_state.secret_code == SECRET_CODE:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Code incorrect")

    st.stop()


# ======= STYLE CHECKLIST TERMINAL ======
st.markdown("""
<style>
/* Label des checkboxes */
div[data-baseweb="checkbox"] label {
    font-family: "Courier New", monospace;
    color: #00ff88;
    font-size: 13px;
}

/* Card de la checklist */
.checklist-card {
    background-color: #0b0f14;
    border: 1px solid #00ff88;
    border-radius: 8px;
    padding: 12px 16px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ======= HEADER DE LA CHECKLIST ======
st.markdown("""
<div class="checklist-card">
    <span style="font-weight:700; font-size:20px; color:#00ff88;">
        Checklist avant utilisation de l'outil
    </span>
</div>
""", unsafe_allow_html=True)

# ======= ITEMS =======
checklist_items = [
    "Je comprends que mon capital n'est productif que lorsqu'il est dans le range",
    "J'ai défini un range cohérent avec la volatilité actuelle et de la tendence du marché",
    "Je sais utiliser un indicateur de volatilité (ATR14) pour mieux définir mon range",
    "Je sais qu'un range trop étroit augmente les fees mais réduit le temps dans le range",
    "Je sais qu'un range trop large réduit le rendement",
    "Je sais que trop de rebalance peut nuire à mon capital à cause des pertes validées",
    "J'ai compris à quoi correspond un trigger (ratio et temps)",
    "Je comprends que lors d'une baisse du marché, j'accumule l'actif le plus volatile",
    "J'accepte le risque d'exposition",
    "J'ai évalué l'impact de l'impermanent loss relatif à mon range",
    "Je sais estimer mes fees potentielles par rapport au risque pris",
    "Je dispose de liquidité pour ajuster ou recentrer mon range si nécessaire",
    "Je ne fournis de la liquidité que sur des paires que je suis prêt à détenir",
    "Je surveille régulièrement le prix et la position dans le range / hors du range",
    "Je comprends que l'APR affiché sur l'aggragateur est indicatif et non garanti"
]

# ======= CHECKBOXES =======
user_check = [st.checkbox(item, key=item) for item in checklist_items]

# ======= BOUTON VALIDATION =======
if st.button("Valider le questionnaire"):
    st.session_state.checklist_validee = True

# Blocage si non validé
if not st.session_state.get("checklist_validee", False):
    st.info("Veuillez compléter et valider le questionnaire pour accéder à l'application.")
    st.stop()


# ----------------------------- LAYOUT -----------------------------
col1, col2 = st.columns([1.3, 1])

# ============================== GAUCHE ==============================
with col1:

    st.markdown('<div class="section-title">Pool Setup</div>', unsafe_allow_html=True)

    # --- PAIRE & STRATEGIE ---
    left, right = st.columns(2)
    with left:
        pair_labels = [f"{a}/{b}" for a, b in PAIRS]
        selected_pair = st.radio("Paire :", pair_labels, index=0)
    with right:
        strategy_choice = st.radio("Stratégie :", list(STRATEGIES.keys()))

    # --- RESET DU CACHE SI ON CHANGE DE PAIRE ---
    if (
        "last_pair" not in st.session_state
        or st.session_state["last_pair"] != selected_pair
    ):
        for k in list(st.session_state.keys()):
            if k.endswith("_prices_" + str(datetime.date.today())):
                del st.session_state[k]
        st.session_state["last_pair"] = selected_pair

    # --- EXTRACTION STRAT ---
    tokenA, tokenB = selected_pair.split("/")
    info = STRATEGIES[strategy_choice]
    ratioA, ratioB = info["ratio"]

    invert_market = st.checkbox("Inversion marché (bull → bear)")
    if invert_market:
        ratioA, ratioB = ratioB, ratioA

    # --- CAPITAL ---
    capital = st.number_input("Capital (USD)", value=1000, step=50)

    # ================== PRIX TOKEN ==================
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

    # ================== VOLATILITÉ PAIRE ==================
    keyA = f"{tokenA}_prices_{datetime.date.today()}"
    keyB = f"{tokenB}_prices_{datetime.date.today()}"

    if keyA not in st.session_state:
        st.session_state[keyA] = get_market_chart(COINGECKO_IDS[tokenA])
    if keyB not in st.session_state:
        st.session_state[keyB] = get_market_chart(COINGECKO_IDS[tokenB])

    pricesA = np.array(st.session_state[keyA])
    pricesB = np.array(st.session_state[keyB])

    def compute_pair_volatility(pricesA, pricesB):
        min_len = min(len(pricesA), len(pricesB))
        pricesA, pricesB = pricesA[:min_len], pricesB[:min_len]
        mask = (pricesA > 1e-8) & (pricesB > 1e-8)
        pricesA, pricesB = pricesA[mask], pricesB[mask]
        if len(pricesA) < 2:
            return 0.0
        pair_prices = pricesA / pricesB
        returns = np.diff(pair_prices) / pair_prices[:-1]
        returns = returns[~np.isnan(returns)]
        return float(np.std(returns)) if len(returns) > 0 else 0.0

    if selected_pair == "WETH/USDC":
        vol_30d = compute_volatility(pricesA)
    elif selected_pair == "CBBTC/USDC":
        vol_30d = compute_volatility(pricesA)
    elif selected_pair == "WETH/CBBTC":
        vol_30d = compute_pair_volatility(pricesA, pricesB) / 2
    elif selected_pair == "VIRTUAL/WETH":
        vol_30d = compute_pair_volatility(pricesA, pricesB) / 2
    elif selected_pair == "AERO/WETH":
        vol_30d = compute_pair_volatility(pricesA, pricesB) / 2
    else:
        vol_30d = compute_pair_volatility(pricesA, pricesB)

    if vol_30d == 0:
        if selected_pair == "CBBTC/USDC":
            vol_30d = 0.12
        elif selected_pair == "VIRTUAL/WETH":
            vol_30d = 0.45
        elif selected_pair == "AERO/WETH":
            vol_30d = 0.45

    # ================== SUGGESTION ==================
    vol_sugg = vol_30d * 100

    if vol_sugg < 2:
        suggested_range = 3
    elif vol_sugg < 4:
        suggested_range = 7
    elif vol_sugg < 7:
        suggested_range = 10
    elif vol_sugg < 10:
        suggested_range = 16
    else:
        suggested_range = 20

    if selected_pair == "CBBTC/USDC":
        suggested_range *= 1.3
        vol_sugg_display = vol_sugg
    elif selected_pair == "VIRTUAL/WETH":
        suggested_range *= 6.2
        vol_sugg_display = vol_sugg * 3.2
    elif selected_pair == "AERO/WETH":
        suggested_range *= 6.5
        vol_sugg_display = vol_sugg * 2
    elif selected_pair == "WETH/USDC":
        suggested_range *= 3
        vol_sugg_display = vol_sugg * 3
    else:
        suggested_range *= 3
        vol_sugg_display = vol_sugg * 3

    range_pct = st.number_input(
        "Range (%)",
        min_value=1.0,
        max_value=200.0,
        value=20.0,
        key="range_pct"
    )

    range_low = priceA * (1 - ratioA * range_pct / 100)
    range_high = priceA * (1 + ratioB * range_pct / 100)

    if invert_market:
        range_low, range_high = range_high, range_low

    capitalA, capitalB = capital * ratioA, capital * ratioB


# ============================== DROITE ==============================
with col2:

    st.markdown('<div class="section-title">Price / Range</div>', unsafe_allow_html=True)

    r1, r2 = st.columns(2)

    with r1:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-title">Prix actuel</div>
            <div class="result-value">{priceA:.6f} $</div>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-title">Range</div>
            <div class="result-value">{range_low:.6f} → {range_high:.6f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card-wide">
        <div class="result-title">Répartition capital</div>
        <div class="result-value">
            {capitalA:.2f} USD {tokenA}  |  {capitalB:.2f} USD {tokenB}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # === GAUGE A/B ===
    fig_bar = go.Figure()

    fig_bar.add_trace(go.Bar(
        x=[ratioA * 100],
        y=[tokenA],
        orientation="h",
        marker=dict(color="#FF8C00"),
        showlegend=False
    ))

    fig_bar.add_trace(go.Bar(
        x=[ratioB * 100],
        y=[tokenB],
        orientation="h",
        marker=dict(color="#6A5ACD"),
        showlegend=False
    ))

    fig_bar.update_layout(
        height=120,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(range=[0, 100]),
        plot_bgcolor="#0f141b",
        paper_bgcolor="#0f141b",
        font=dict(color="#e6edf3", size=11)
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown(f"""
    <div class="result-card-wide">
        <div class="result-title">Résumé stratégie</div>
        <div style="font-size:13px;opacity:0.8;margin-top:6px;">
            <b>Ratio :</b> {int(ratioA*100)} / {int(ratioB*100)}<br>
            <b>Objectif :</b> {info['objectif']}<br>
            <b>Contexte :</b> {info['contexte']}
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================== AUTOMATION ===========================

st.markdown('<div class="section-title">Réglages Automation</div>', unsafe_allow_html=True)

# ---- Range future / Time-buffer ----
col_range, col_time = st.columns([2,1])

# ---- Ratios pour trigger/future range ----
ratioA_trigger, ratioB_trigger = ratioA, ratioB
if invert_market:
    ratioA_trigger, ratioB_trigger = ratioB_trigger, ratioA_trigger

# ================= RANGE FUTURE =================

with col_range:

    st.markdown('<div class="section-title">Range future</div>', unsafe_allow_html=True)

    range_percent = st.slider("Range total (%)", 1.0, 90.0, 20.0, step=0.1)

    low_offset_pct = -range_percent * 20 / 100
    high_offset_pct = range_percent * 80 / 100

    final_low = priceA * (1 + low_offset_pct/100)
    final_high = priceA * (1 + high_offset_pct/100)

    st.markdown(f"""
    <div class="result-card-wide">
        <div class="result-title">Range calculé</div>
        <div class="result-value">
            {final_low:.6f} → {final_high:.6f}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ================= TIME BUFFER =================

with col_time:

    st.markdown('<div class="section-title">Time-buffer</div>', unsafe_allow_html=True)

    vola = vol_30d * 100

    if vola < 2:
        recomand = "6 à 12 minutes"
    elif vola < 5:
        recomand = "18 à 48 minutes"
    else:
        recomand = "60 minutes et plus"

    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Recommandation</div>
        <div class="result-value">{recomand}</div>
    </div>
    """, unsafe_allow_html=True)


# ================= TRIGGER =================

col_trigger, col_rebalance = st.columns(2)

with col_trigger:

    st.markdown('<div class="section-title">Trigger d’anticipation (RATIO)</div>', unsafe_allow_html=True)

    t1, t2 = st.columns(2)
    with t1:
        trig_low = st.slider("Trigger Low (%)", 0.0, 100.0, 10.0, step=0.1)
    with t2:
        trig_high = st.slider("Trigger High (%)", 0.0, 100.0, 90.0, step=0.1)

    rw = final_high - final_low
    trigger_low_price = final_low + (trig_low/100)*rw
    trigger_high_price = final_low + (trig_high/100)*rw

    r1, r2 = st.columns(2)

    with r1:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-title">Trigger Low</div>
            <div class="result-value">{trigger_low_price:.6f}</div>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-title">Trigger High</div>
            <div class="result-value">{trigger_high_price:.6f}</div>
        </div>
        """, unsafe_allow_html=True)


# ================= REBALANCE AVANCÉE =================

with col_rebalance:

    st.markdown('<div class="section-title">Rebalance avancée (futur range)</div>', unsafe_allow_html=True)

    off_low_pct  = -ratioA * range_percent
    off_high_pct =  ratioB * range_percent

    bear_low  = priceA * (1 + off_low_pct / 100)
    bear_high = priceA * (1 + off_high_pct / 100)

    bull_low  = priceA * (1 - off_high_pct / 100)
    bull_high = priceA * (1 - off_low_pct / 100)

    col_b1, col_b2 = st.columns(2)

    with col_b1:
        st.markdown("""
        <div class="result-card">
            <div class="result-title">Marché Haussier (Pump)</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-card-wide">
            <div class="result-title">Range</div>
            <div class="result-value">
                {bull_low:.6f} → {bull_high:.6f}
            </div>
            <div class="result-subvalue">
                {(-off_high_pct):.1f}% → {(-off_low_pct):.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b2:
        st.markdown("""
        <div class="result-card">
            <div class="result-title">Marché Baissier (Dump)</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-card-wide">
            <div class="result-title">Range</div>
            <div class="result-value">
                {bear_low:.6f} → {bear_high:.6f}
            </div>
            <div class="result-subvalue">
                {off_low_pct:.1f}% → {off_high_pct:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)


# =================== FONCTIONS (INCHANGÉES) ===================

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
    
# ======================= IMPERMANENT LOSS & ATR (Terminal Style) =======================

# --- Style Terminal DeFi ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0b0f14;
    color: #e6edf3;
    font-family: "Courier New", monospace;
}

.section-title {
    border-left: 4px solid #00ff88;
    padding: 8px 14px;
    margin-top: 24px;
    margin-bottom: 14px;
    font-weight: 600;
    font-size: 16px;
    background: rgba(0,255,136,0.05);
    letter-spacing: 1px;
}

div[data-baseweb="input"] input {
    background-color: #11161d !important;
    color: #00ff88 !important;
    border: 1px solid #1f2a36 !important;
    padding-top: 6px !important;
    padding-bottom: 6px !important;
    font-size: 13px;
}

label { font-size: 12px !important; opacity: 0.7; }

.result-card, .result-card-wide {
    background: #0f141b;
    border: 1px solid #1f2a36;
    border-radius: 10px;
    padding: 14px;
    text-align: left;
    box-shadow: 0 0 12px rgba(0,255,136,0.05);
    margin-top: 14px;
}

.result-card-wide { padding: 16px; }

.result-title { font-size: 11px; opacity: 0.6; text-transform: uppercase; letter-spacing: 1px; }
.result-value { font-size: 18px; font-weight: 600; color: #00ff88; margin-top: 6px; }

</style>
""", unsafe_allow_html=True)


# =================== INPUTS ===================
st.markdown('<div class="section-title">Impermanent Loss</div>', unsafe_allow_html=True)

row1_col1, row1_col2, row1_col3 = st.columns([1,1,1])
with row1_col1:
    P_deposit = st.number_input("P_deposit", value=3000.0, format="%.6f", step=0.001, label_visibility="collapsed")
with row1_col2:
    P_now = st.number_input("P_now", value=3000.0, format="%.6f", step=0.001, label_visibility="collapsed")
with row1_col3:
    v_deposit = st.number_input("Valeur deposit (USD)", value=500.0, format="%.6f", step=0.01, label_visibility="collapsed")

row2_col1, row2_col2 = st.columns([1,1])
with row2_col1:
    P_lower = st.number_input("P_lower", value=2800.0, format="%.6f", step=0.001, label_visibility="collapsed")
with row2_col2:
    P_upper = st.number_input("P_upper", value=3500.0, format="%.6f", step=0.001, label_visibility="collapsed")

# --- Calcul IL ---
L_raw = compute_L(P_deposit, P_lower, P_upper, v_deposit)
x0_raw, y0_raw = tokens_from_L(L_raw, P_deposit, P_lower, P_upper)
L, x0, y0 = normalize_L(L_raw, x0_raw, y0_raw, P_deposit, v_deposit)

prices = np.linspace(P_lower*0.8, P_upper*1.3, 400)
LP_values = V_LP(prices, L, P_lower, P_upper)
HODL_values = V_HODL(prices, x0, y0)
IL_curve = (LP_values / HODL_values - 1) * 100

# --- Graph IL ---
fig = go.Figure()

# Courbe IL
fig.add_trace(go.Scatter(
    x=prices, y=IL_curve, mode="lines", name="IL(%)",
    line=dict(color="red", width=3)
))

# Lignes verticales et annotations
for px, label, color in [
    (P_lower, "Low", "green"),
    (P_upper, "High", "green"),
    (P_deposit, "Deposit", "blue"),
    (P_now, "Now", "purple")
]:
    fig.add_vline(
        x=px,
        line=dict(color=color, width=2, dash="dot" if label in ["Low","High"] else "dash")
    )
    fig.add_annotation(
        x=px,
        y=max(IL_curve) if label in ["Low","High"] else min(IL_curve),
        text=label,
        showarrow=False,
        font=dict(color=color, size=12),
        yshift=10 if label in ["Low","High"] else -10
    )

# Axes et grilles
fig.update_xaxes(
    title="Prix",
    title_font=dict(color="white", size=14),
    tickfont=dict(color="white", size=12),
    gridcolor="rgba(255,255,255,0.1)",
    zerolinecolor="rgba(255,255,255,0.2)"
)
fig.update_yaxes(
    title="IL (%)",
    title_font=dict(color="white", size=14),
    tickfont=dict(color="white", size=12),
    gridcolor="rgba(255,255,255,0.1)",
    zerolinecolor="rgba(255,255,255,0.2)"
)

# Fond couleur #0b0f14
fig.update_layout(
    height=380,
    plot_bgcolor="#0b0f14",   # fond du graphique
    paper_bgcolor="#0b0f14",  # fond autour du graphique
    title=dict(text="Impermanent Loss (%)", font=dict(color="white", size=16)),
    legend=dict(font=dict(color="white"))
)

st.plotly_chart(fig, use_container_width=True)

# --- Valeurs actuelles IL ---
IL_now = (V_LP(P_now, L, P_lower, P_upper)/V_HODL(P_now, x0, y0)-1)*100
LP_now = V_LP(P_now, L, P_lower, P_upper)
HODL_now = V_HODL(P_now, x0, y0)

cols = st.columns(3)
results = [
    ("IL maintenant (%)", f"{IL_now:.2f}%"),
    ("Valeur LP ($)", f"${LP_now:,.2f}"),
    ("Valeur HODL ($)", f"${HODL_now:,.2f}")
]
for i, (title,val) in enumerate(results):
    with cols[i]:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-title">{title}</div>
            <div class="result-value">{val}</div>
        </div>
        """, unsafe_allow_html=True)

# --- APR ---
def calculate_clmm_apr(fees_usd_period: float, active_liquidity_usd_avg: float, period_days: int) -> float:
    if active_liquidity_usd_avg <= 0 or period_days <= 0:
        return 0.0
    return fees_usd_period / active_liquidity_usd_avg * (365 / period_days) * 100

st.markdown('<div class="section-title">Calcul APR</div>', unsafe_allow_html=True)
fees_usd_period = st.number_input("Total des fees (USD)", value=100.0, step=1000.0)
active_liquidity_usd_avg = st.number_input("Liquidité active moyenne (USD)", value=1000.0, step=10000.0)
period_days = st.number_input("Durée (jours)", value=30, min_value=1, step=1)

apr = calculate_clmm_apr(fees_usd_period, active_liquidity_usd_avg, period_days)
st.markdown(f"""
<div class="result-card-wide" style="text-align:center;">
    <div class="result-title">APR annualisé estimé</div>
    <div class="result-value">{apr:.2f} %</div>
</div>
""", unsafe_allow_html=True)

# --- ATR Range ---
st.markdown('<div class="section-title">ATR Range</div>', unsafe_allow_html=True)
col_atr1, col_atr2, col_atr3 = st.columns(3)
with col_atr1: atr_usd = st.number_input("ATR 14 ($)", value=100.0, min_value=0.01, step=1.0)
with col_atr2: atr_mult = st.slider("Multiplicateur ATR", 0.5,10.0,3.0, step=0.25)
with col_atr3: asym_mode = st.selectbox("Stratégie de range", ["Neutre","Bull","Bear","Custom"])
asset_price = st.number_input("Prix actif pour ATR ($)", value=float(P_deposit), min_value=0.0001, step=1.0)

atr_pct = (atr_usd/asset_price)*100
range_total_pct = atr_pct*atr_mult
if asym_mode=="Neutre": low_weight,high_weight=0.5,0.5
elif asym_mode=="Bull": low_weight,high_weight=0.2,0.8
elif asym_mode=="Bear": low_weight,high_weight=0.8,0.2
else:
    cw1,cw2=st.columns(2)
    with cw1: low_weight = st.slider("Poids bas (%)",0,100,40)/100
    with cw2: high_weight = 1-low_weight

atr_low = P_deposit*(1-range_total_pct*low_weight/100)
atr_high= P_deposit*(1+range_total_pct*high_weight/100)
low_pct_display = (atr_low/P_deposit-1)*100
high_pct_display = (atr_high/P_deposit-1)*100

st.markdown(f"""
<div class="result-card-wide" style="text-align:center;">
    <div class="result-title">Range basé sur ATR</div>
    <div class="result-value">
    ATR Low: {atr_low:.2f}$ | ATR High: {atr_high:.2f}$ | ±{range_total_pct:.2f}%</div>
</div>
""", unsafe_allow_html=True)

# --- ATR Expert (Double Volatile) ---
st.markdown('<div class="section-title">ATR Paire Double Volatile</div>', unsafe_allow_html=True)
col1,col2,col3,col4=st.columns(4)
with col1: price_x = st.number_input("Prix actuel X", value=3111.0)
with col2: atr_x = st.number_input("ATR daily X", value=174.0)
with col3: price_y = st.number_input("Prix actuel Y", value=90113.0)
with col4: atr_y = st.number_input("ATR daily Y", value=3282.0)
atr_multiplier = st.slider("Multiplicateur ATR",1.0,6.0,1.0,step=0.5)

def calculate_pair_atr(price_x, atr_x, price_y, atr_y, multiplier=1):
    pair_price = price_x/price_y
    delta_x=atr_x/price_y
    delta_y=(price_x/(price_y**2))*atr_y
    atr_pair=math.sqrt(delta_x**2+delta_y**2)*multiplier
    low=pair_price-atr_pair
    high=pair_price+atr_pair
    range_pct=(atr_pair/pair_price)*100
    return {"pair_price":pair_price,"atr_pair":atr_pair,"low":low,"high":high,"range_pct":range_pct}

if st.button("Calculer ATR et RANGE"):
    result = calculate_pair_atr(price_x, atr_x, price_y, atr_y, atr_multiplier)
    st.markdown(f"""
    <div class="result-card-wide" style="text-align:center;">
        <div class="result-title">ATR Paire Volatile</div>
        <div class="result-value">
        Pair price: {result['pair_price']:.6f} | ATR: {result['atr_pair']:.6f} | Low/High: {result['low']:.6f}/{result['high']:.6f} | ±{result['range_pct']:.2f}%
        </div>
    </div>
    """, unsafe_allow_html=True)


# ======================= BE LP (Terminal Style) =======================


st.set_page_config(layout="wide")

# --- Header ---
st.markdown("""
<div style="
    background: linear-gradient(135deg, #0b0f14 0%, #141a2a 40%, #1c2338 100%);
    padding:20px;
    border-radius:12px;
    margin-top:20px;
    margin-bottom:20px;
">
    <span style="color:white;font-size:28px;font-weight:700;">
        CALCULATRICE BREAK-EVEN LP
    </span>
</div>
""", unsafe_allow_html=True)

# ================= TERMINAL STYLE =================

st.markdown("""
<style>

/* ===== GLOBAL TERMINAL THEME ===== */
[data-testid="stAppViewContainer"] {
    background-color: #0b0f14;
    color: #e6edf3;
    font-family: "Courier New", monospace;
}

/* ===== SECTION TITLES ===== */
.section-title {
    border-left: 4px solid #00ff88;
    padding: 8px 14px;
    margin-top: 24px;
    margin-bottom: 14px;
    font-weight: 600;
    font-size: 16px;
    background: rgba(0,255,136,0.05);
    letter-spacing: 1px;
}

/* ===== INPUTS ===== */
div[data-baseweb="input"] input {
    background-color: #11161d !important;
    color: #00ff88 !important;
    border: 1px solid #1f2a36 !important;
    padding-top: 6px !important;
    padding-bottom: 6px !important;
    font-size: 13px;
}

label {
    font-size: 12px !important;
    opacity: 0.7;
}

/* ===== RESULT CARDS ===== */
.result-card {
    background: #0f141b;
    border: 1px solid #1f2a36;
    border-radius: 10px;
    padding: 14px;
    text-align: left;
    box-shadow: 0 0 12px rgba(0,255,136,0.05);
    margin-top: 14px;
}

.result-title {
    font-size: 11px;
    opacity: 0.6;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.result-value {
    font-size: 18px;
    font-weight: 600;
    color: #00ff88;
    margin-top: 6px;
}

</style>
""", unsafe_allow_html=True)

# =================== CONFIGURATION ===================

st.markdown('<div class="section-title">Configuration de la paire</div>', unsafe_allow_html=True)

pair_type = st.selectbox(
    "Type de paire",
    ["Volatile / Stable", "Double Volatile"]
)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("METRICS")
    capital = st.number_input("Capital engagé ($)", value=6400.0, step=0.01, format="%.2f")
    fees = st.number_input("Fees accumulés ($)", value=140.0, step=0.01, format="%.2f")

with col2:
    st.subheader("Token A")
    qty_a = st.number_input("Quantité", value=1.5, step=0.0001, format="%.6f")
    price_a = st.number_input("Prix actuel ($)", value=2950.0, step=0.01, format="%.2f")

with col3:
    if pair_type == "Volatile / Stable":
        st.subheader("Token B (Stable)")
        stable_amount = st.number_input("Montant ($)", value=1500.0, step=0.01, format="%.2f")
        value = qty_a * price_a + stable_amount
        effective_b = stable_amount + fees
    else:
        st.subheader("Token B (Volatile)")
        qty_b = st.number_input("Quantité", value=0.5, step=0.0001, format="%.6f")
        price_b = st.number_input("Prix actuel ($)", value=2000.0, step=0.01, format="%.2f")
        value = qty_a * price_a + qty_b * price_b
        effective_b = qty_b * price_b + fees

# =================== CALCULS ===================

pnl = value - capital
pnl_to_be = capital - value
pnl_pct = (value / capital - 1) * 100
break_even_a = (capital - effective_b) / qty_a

break_even_b = None
if pair_type == "Double Volatile":
    break_even_b = (capital - (qty_a * price_a) - fees) / qty_b

# =================== RESULTATS ===================

st.markdown('<div class="section-title">Résultats Break-Even LP</div>', unsafe_allow_html=True)

# Création des cartes de résultats
cards = []

cards.append({
    "title": "Valeur actuelle",
    "value": f"{value:.2f} $",
    "color": "#FF6B6B" if pnl < 0 else "#2EF2A2"
})
cards.append({
    "title": "P&L",
    "value": f"{pnl:.2f} $ ({pnl_pct:.2f}%)",
    "color": "#FF6B6B" if pnl < 0 else "#2EF2A2"
})
cards.append({
    "title": "P&L restante pour BE",
    "value": f"{pnl_to_be:.2f} $",
    "color": "#FF6B6B" if pnl < 0 else "#2EF2A2"
})
cards.append({
    "title": "Break-even Token A",
    "value": f"{break_even_a:.2f} $",
    "color": "#00ff88"
})
if pair_type == "Double Volatile":
    cards.append({
        "title": "Break-even Token B",
        "value": f"{break_even_b:.2f} $",
        "color": "#00ff88"
    })

# Affichage en colonnes
cols = st.columns(len(cards))
for i, card in enumerate(cards):
    with cols[i]:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-title">{card['title']}</div>
            <div class="result-value" style="color:{card['color']};">{card['value']}</div>
        </div>
        """, unsafe_allow_html=True)


# ======================= Less IL =======================


st.set_page_config(layout="wide")

# --- Header ---
st.markdown("""
<div style="
    background: linear-gradient(135deg, #0b0f14 0%, #141a2a 40%, #1c2338 100%);
    padding:20px;
    border-radius:12px;
    margin-top:20px;
    margin-bottom:20px;
">
    <span style="color:white;font-size:28px;font-weight:700;">
        Zero Swap Rebalance
    </span>
</div>
""", unsafe_allow_html=True)

# =================== CONFIGURATION ===================
st.markdown('<div class="section-title">Configuration de la paire</div>', unsafe_allow_html=True)

t1, t2 = st.columns(2)

with t1:
    tokenA = st.text_input("Token A", "Exemple WETH")

with t2:
    tokenB = st.text_input("Token B", "Exemple USDC")

col1, col2, col3, col4 = st.columns(4)

with col1:
    price_tokenA = st.number_input(f"Prix {tokenA} ($)", value=1850.0, step=1.0)

with col2:
    price_tokenB = st.number_input(f"Prix {tokenB} ($)", value=1.0, step=0.01)

with col3:
    P_low = st.number_input("Plow initial", value=1800.0, step=1.0)

with col4:
    P_high = st.number_input("Phigh initial", value=2100.0, step=1.0)

if price_tokenB == 0:
    st.error("Le prix du token B ne peut pas être 0.")
    st.stop()

P_current = price_tokenA / price_tokenB

if not (P_low < P_current < P_high):
    st.error("Le prix actuel doit être strictement à l'intérieur du range initial.")
    st.stop()

# =================== CALCUL RATIO ===================
sqrtP = math.sqrt(P_current)
sqrtPl = math.sqrt(P_low)
sqrtPh = math.sqrt(P_high)

ratio = (sqrtPh - sqrtP) / (sqrtP * sqrtPh * (sqrtP - sqrtPl))

# =================== ZERO SWAP BIDIRECTIONNEL ===================
st.markdown('<div class="section-title">Zero Swap Bidirectionnel</div>', unsafe_allow_html=True)

# Trois colonnes : New Plow | New Phigh | Direction
col_low, col_high, col_dir = st.columns(3)

with col_low:
    new_P_low = st.number_input("New Plow (dump)", value=P_low * 0.9, step=1.0)

with col_high:
    new_P_high = st.number_input("New Phigh (pump)", value=P_high * 1.1, step=1.0)

with col_dir:
    direction_select = st.selectbox(
        "Mode de recalcul",
        options=["Auto", "Dump", "Pump"],
        help="Auto: calcule selon la borne la plus éloignée. Dump: priorise New Plow. Pump: priorise New Phigh."
    )

# Détermination du mode
mode = None
if direction_select == "Dump":
    mode = "bear"
elif direction_select == "Pump":
    mode = "bull"
elif direction_select == "Auto":
    dist_low = abs(P_current - new_P_low)
    dist_high = abs(new_P_high - P_current)
    if dist_low > dist_high:
        mode = "bear"
    elif dist_high > dist_low:
        mode = "bull"
# =================== CALCUL ===================
if mode == "bear":

    if new_P_low >= P_current:
        st.error("La nouvelle borne basse doit être inférieure au prix actuel.")
        st.stop()

    sqrtNewPl = math.sqrt(new_P_low)
    denominator = 1 - ratio * sqrtP * (sqrtP - sqrtNewPl)

    if denominator <= 0:
        st.error("Configuration impossible : borne haute tend vers l'infini.")
        st.stop()

    sqrtNewPh = sqrtP / denominator
    new_P_high = sqrtNewPh ** 2

    direction_label = "🔻 Mode actif : Dump"

elif mode == "bull":

    if new_P_high <= P_current:
        st.error("La nouvelle borne haute doit être supérieure au prix actuel.")
        st.stop()

    sqrtNewPh = math.sqrt(new_P_high)
    numerator = (1 - (sqrtP / sqrtNewPh))
    sqrtNewPl = sqrtP - (numerator / (ratio * sqrtP))

    if sqrtNewPl <= 0:
        st.error("Configuration impossible : borne basse négative.")
        st.stop()

    new_P_low = sqrtNewPl ** 2
    direction_label = "🔺 Mode actif : Pump"

else:
    direction_label = "— Ajuste une borne pour activer le recalcul —"

# =================== RESULTATS ===================
st.markdown('<div class="section-title">Résultats</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="result-card">
    <div class="result-title">Direction active</div>
    <div class="result-value">{direction_label}</div>
</div>
""", unsafe_allow_html=True)

r1, r2, r3 = st.columns(3)

with r1:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Ratio Zero Swap</div>
        <div class="result-value">{ratio:.10f}</div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Nouvelle borne basse</div>
        <div class="result-value">{new_P_low:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Nouvelle borne haute</div>
        <div class="result-value">{new_P_high:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="result-card-wide">
    <div class="result-title">Range recalibré</div>
    <div class="result-value">
        {new_P_low:.2f} → {new_P_high:.2f}
    </div>
</div>
""", unsafe_allow_html=True)

# =================== FORMULES ===================
with st.expander("Résumé complet des formules utilisées (Zero Swap Rebalance)"):

    # Texte d’intro réduit (optionnel)
    st.markdown(
        '<div style="font-size:12px; color:#aaa; margin-bottom:10px; font-family: Courier, monospace;">'
        'Ces formules permettent de calculer le range, le ratio et le rebalance automatiquement.'
        '</div>',
        unsafe_allow_html=True
    )

    # Titres de section en monospace, petite taille, et en blanc cassé
    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Prix courant</div>', unsafe_allow_html=True)
    st.latex(r"P = \frac{Price_{TokenA}}{Price_{TokenB}}")

    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Racines utilisées</div>', unsafe_allow_html=True)
    st.latex(r"\sqrt{P}, \quad \sqrt{P_\mathrm{low}}, \quad \sqrt{P_\mathrm{high}}, \quad \sqrt{P_\mathrm{rebalance}}")

    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Ratio initial A/B</div>', unsafe_allow_html=True)
    st.latex(r"""
    \mathrm{ratio} = \frac{\sqrt{P_\mathrm{high}} - \sqrt{P}}
    {\sqrt{P} \cdot \sqrt{P_\mathrm{high}} \cdot \left(\sqrt{P} - \sqrt{P_\mathrm{low}}\right)}
    """)

    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">New Plow (déplacement borne basse)</div>', unsafe_allow_html=True)
    st.latex(r"\mathrm{New\ Plow} = P_\mathrm{low}^{new}")

    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Nouvelle borne haute Zero-Swap</div>', unsafe_allow_html=True)
    st.latex(r"""
    \sqrt{\mathrm{New\ P\ High}} = \frac{\sqrt{P}}
    {1 - \mathrm{ratio} \cdot \sqrt{P} \cdot \left(\sqrt{P} - \sqrt{P_\mathrm{low}^{new}}\right)}
    """)

    st.latex(r"""
    \mathrm{New\ P\ High} = \left(\sqrt{\mathrm{New\ P\ High}}\right)^2
    """)

    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Resserrement (tighten)</div>', unsafe_allow_html=True)
    st.latex(r"""
    \mathrm{New\ Tight\ Plow} = P_\mathrm{rebalance} \cdot \left(1 - \frac{\mathrm{tighten\_percent}}{100}\right)
    """)

    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Ratio recalculé au rebalance</div>', unsafe_allow_html=True)
    st.latex(r"""
    \mathrm{ratio}_\mathrm{reb} = \frac{\sqrt{P_\mathrm{high}} - \sqrt{P_\mathrm{rebalance}}}
    {\sqrt{P_\mathrm{rebalance}} \cdot \sqrt{P_\mathrm{high}} \cdot \left(\sqrt{P_\mathrm{rebalance}} - \sqrt{P_\mathrm{low}}\right)}
    """)

    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Nouvelle borne haute Tight (Zero-Swap)</div>', unsafe_allow_html=True)
    st.latex(r"""
    \sqrt{\mathrm{New\ Tight\ P\ High}} = \frac{\sqrt{P_\mathrm{rebalance}}}
    {1 - \mathrm{ratio}_\mathrm{reb} \cdot \sqrt{P_\mathrm{rebalance}} \cdot \left(\sqrt{P_\mathrm{rebalance}} - \sqrt{\mathrm{New\ Tight\ Plow}}\right)}
    """)

    st.latex(r"""
    \mathrm{New\ Tight\ P\ High} = \left(\sqrt{\mathrm{New\ Tight\ P\ High}}\right)^2
    """)

# --- GUIDE COMPLET TERMINAL STYLE ---
st.markdown("""
<div style="
    background: linear-gradient(135deg, #0b0f14 0%, #141a2a 40%, #1c2338 100%);
    padding:20px;
    border-radius:12px;
    margin-top:20px;
    margin-bottom:18px;
">
    <span style="color:white;font-size:28px;font-weight:700;">
        GUIDE COMPLET - ENGAGER DU CAPITAL SUR LP
    </span>
</div>
""", unsafe_allow_html=True)

guide_html = """
<style>
/* ===== GUIDE TERMINAL THEME ===== */
#guide {
    font-family: "Courier New", monospace;
    color: #e6edf3;
    margin-top: 20px;
    padding: 24px;
    background-color: #0f141b;
    border: 1px solid #1f2a36;
    border-radius: 12px;
    box-shadow: 0 0 18px rgba(0,255,136,0.05);
}

#guide h2, #guide h3, #guide h4 {
    color: #00ff88;
    margin-top: 28px;
    margin-bottom: 10px;
    letter-spacing: 0.5px;
}

#guide p, #guide li {
    line-height: 1.6em;
    font-size: 14px;
    color: #c9d1d9;
}

#guide ul {
    margin-left: 20px;
}

#guide ul li {
    margin-bottom: 6px;
}

/* ===== SOMMAIRE ===== */
#sommaire {
    background-color: rgba(0,255,136,0.05);
    border: 1px solid #1f2a36;
    padding: 18px;
    border-radius: 10px;
    margin-bottom: 30px;
}

#sommaire h4 {
    margin-top: 0;
    font-weight: 700;
    color: #00ff88;
}

#sommaire ul {
    list-style-type: none;
    padding-left: 10px;
}

#sommaire ul li {
    margin-bottom: 6px;
}

#sommaire ul li a {
    text-decoration: none;
    color: #00ff88;
    font-size: 13px;
    opacity: 0.9;
}

#sommaire ul li a:hover {
    text-decoration: underline;
    opacity: 1;
}

/* ===== EMPHASE ===== */
#guide b, #guide strong {
    color: #ffffff;
}

#guide em {
    color: #9cdcfe;
}

/* ===== ENCARTS SECTIONS ===== */
.encadre {
    background-color: #0f141b;
    border: 1px solid #1f2a36;
    border-radius: 10px;
    padding: 14px;
    margin-top: 14px;
    margin-bottom: 14px;
    box-shadow: 0 0 15px rgba(0,255,136,0.1);
}

.encadre:hover {
    box-shadow: 0 0 25px rgba(0,255,136,0.2);
}

.encadre .title {
    font-weight: 700;
    color: #00ff88;
    margin-bottom: 6px;
    font-size: 15px;
}
</style>

<div id="guide">

<!-- Introduction -->
<div class="encadre">
    <div class="title">Introduction</div>
    <p>Bienvenue !<br>
    Ce guide t’explique <b>pas à pas</b> comment comprendre et utiliser les stratégies de LP (Liquidity Providing) dans un AMM concentré comme Uniswap, Aerodrome, Pancake...<br><br>
    Krystal, Vfat, aperture... <b>sont uniquement des agrégateurs de positions</b> !</p>
</div>

<!-- Sommaire -->
<div id="sommaire">
<h4>Sommaire</h4>
<ul>
    <li><a href="#cest-quoi-fournir-de-la-liquidite">C’est quoi fournir de la liquidité ?</a></li>
    <li><a href="#concepts-fondamentaux">Concepts fondamentaux</a></li>
    <li><a href="#strategies-possibles">Stratégies possibles</a></li>
    <li><a href="#choisir-un-range">Choisir un range</a></li>
    <li><a href="#exemple-simple-weth-usdc">Exemple simple WETH/USDC</a></li>
    <li><a href="#erreurs-de-debutant">Erreurs de débutant</a></li>
    <li><a href="#rebalancer-la-position">Rebalancer la position</a></li>
    <li><a href="#courbe-impermanent-loss">Comprendre la courbe d’Impermanent Loss</a></li>
    <li><a href="#strategie-lp-rentable">Quand une stratégie LP est rentable ?</a></li>
    <li><a href="#astuces-et-autonomie">Astuces et autonomie des choix</a></li>
    <li><a href="#conclusion">Conclusion</a></li>
</ul>
</div>

<!-- Sections principales -->
<h3 id="cest-quoi-fournir-de-la-liquidite">C’est quoi fournir de la liquidité ?</h3>
<div class="encadre">
<p>Quand tu fournis de la liquidité à une pool (ex : WETH/USDC), tu apportes <b>deux tokens en même temps</b>. En échange, tu deviens <b>market maker</b> et touches des <b>frais de trading</b>.<br>
Dans un AMM concentré, tu choisis <b>un range</b>. Si le prix sort du range → tu deviens <b>full Token A</b> ou <b>full Token B</b>. Ta position s’ajuste automatiquement : <b>quand le prix baisse, tu accumules le token le plus volatile</b> ; à l’inverse, <b>quand le prix monte, tu revends progressivement ce token volatile.</b></p>
</div>

<h3 id="concepts-fondamentaux">Concepts fondamentaux</h3>
<div class="encadre">
<ul>
    <li><b>Ratio</b> : proportion entre Token A (volatile) et Token B (stable ou moins volatile). Exemple : 50/50 = neutre, 20/80 = défensif, 95/5 = agressif.</li>
    <li><b>Range</b> : zone de prix où ton capital est actif. Range serré = plus de fees mais plus de rebalances et IL possible.</li>
    <li><b>Impermanent Loss (IL)</b> : perte que tu aurais évitée si tu avais conservé tes tokens. Plus le prix s’éloigne, plus l’IL augmente.</li>
</ul>
</div>

<h3 id="strategies-possibles">Stratégies possibles</h3>
<div class="encadre">
<ul>
    <li><b>Neutre (50/50)</b> : marché incertain, stable et simple, risque IL si gros mouvement</li>
    <li><b>Coup de pouce (20/80)</b> : marché calme, protège du token volatil, défensif</li>
    <li><b>Mini-doux (10/90)</b> : anticipation de tendance, minimise IL, très défensif</li>
    <li><b>Side-line up (100/0)</b> : bas de marché, accumulation token volatile, agressif</li>
    <li><b>Side-line down (0/100)</b> : marché haussier, prise de profit naturel, agressif vers la vente</li>
</ul>
</div>

<h3 id="choisir-un-range">Choisir un range</h3>
<div class="encadre">
<p>Le choix dépend de ton objectif, de la volatilité et du marché : haussier → profits A→B, baissier → accumulation B→A, latéral → neutre ou coup de pouce.<br>
Objectifs : saisir des fees → petit range ; limiter l’IL → grand range sans rebalance ou mini-doux ; DCA → ratio 100/0 ou 0/100.<br><br>
Pour affiner ton range, utilise l’indicateur <strong>ATR (Average True Range)</strong> disponible sur TradingView dans la catégorie <em>Technical</em>.<br>
L’ATR représente de manière simplifiée <strong>l’écart-type du prix d’un actif exprimé en dollars</strong> : il mesure l’amplitude moyenne des mouvements de prix sur une période donnée.<br><br>
Sur l’outil, règle l’ATR en <strong>daily</strong> avec une période <strong>ATR 14</strong>, puis applique un <strong>multiplicateur</strong> afin de définir la largeur de ton range autour du prix actuel.<br>
Par exemple : <strong>ATR × 3</strong> correspond généralement à une tenue de range d’environ <strong>1 semaine à 10 jours</strong>, selon la volatilité du marché.<br>
Une fois le range défini, vérifie l’ATR affiché en <strong>weekly</strong> et compare-le à ton choix initial en calculant :
<strong>borne haute − borne basse</strong>.<br>
Ajuste ensuite ton range en confrontant ces valeurs avec les données de l'ATR14 en <strong>WEEKLY</strong> ainsi que <strong>volatilité sur 7 jours et 30 jours</strong>, afin de sélectionner le compromis le plus adapté à la tendence entre fréquence de rebalance, capture de fees et exposition au risque.</p>
</div>

<!-- Continue with remaining sections in the same encadré style -->
<h3 id="exemple-simple-weth-usdc">Exemple simple WETH/USDC</h3>
<div class="encadre">
<ul>
    <li>Capital = 1000 USD, Prix ETH = 3000, Stratégie = 50/50, Range ±20%</li>
    <li>Répartition : 500 USD ETH, 500 USD USDC</li>
    <li>Range bas ≈ 2700, Range haut ≈ 3300</li>
    <li>Si prix = 3300 → plus riche en USDC, fees générés</li>
    <li>Si prix = 2700 → plus d’ETH, fees générés</li>
</ul>
</div>

<h3 id="erreurs-de-debutant">Erreurs de débutant</h3>
<div class="encadre">
<ul>
    <li>Range trop serré : rebalances fréquents, coûts d’opportunité, IL amplifiée</li>
    <li>Oublier que l’IL existe : fees ne compensent pas toujours IL</li>
    <li>Choisir un range sans regarder la volatilité : volatilité 7j et 30j clé, pas de stratégie “set and forget”</li>
</ul>
</div>

<h3 id="rebalancer-la-position">Rebalancer la position</h3>
<div class="encadre">
<p>Quand le prix sort du range, tu deviens full A ou full B, tu ne gagnes plus de fees. Ta LP = simple “bag” de tokens, il faut repositionner la liquidité.<br>
L'app calcule combien de fois le prix est sorti dans le passé et en simulation future, et ajuste automatiquement le range.</p>

<h4>Rappel sur l’automation et les rebalances</h4>
<ul>
  <li>Les triggers doivent toujours se baser sur le <strong>RATIO</strong>, jamais sur % ou $.</li>
  <li>Lors de l’utilisation des <strong>futures ranges</strong> (option avancée), réglez-les correctement en %.</li>
  <li>Si votre range actuel est très large ou trop court comparé aux futures ranges, vous aurez un décalage de stratégie.</li>
  <li><strong>Conseil pratique :</strong> Partagez uniquement des captures claires de l’édition de l’automation et de la stratégie.</li>
  <li><strong>Attention sur vos décisions :</strong> Achetez le token volatile seulement si prêt à vendre pour limiter la perte.</li>
</ul>
</div>

<h3 id="courbe-impermanent-loss">Comprendre la courbe d’Impermanent Loss</h3>
<div class="encadre">
<p>Le graphe montre : IL(%) en fonction du prix actuel, ligne pour prix de dépôt, ligne pour prix actuel, range bas/haut.<br>
Interprétation : minimum de la courbe = prix de dépôt ; plus on s’éloigne, plus IL augmente ; IL=0 seulement si prix reste identique.</p>
</div>

<h3 id="strategie-lp-rentable">Quand une stratégie LP est rentable ?</h3>
<div class="encadre">
<ul>
    <li>Frais gagnés > impermanent loss</li>
    <li>Prix ne sort pas trop vite du range</li>
    <li>Stratégie cohérente avec l’objectif (DCA, prise de profit, accumulation…)</li>
</ul>
</div>

<h3 id="astuces-et-autonomie">Astuces et autonomie des choix</h3>
<div class="encadre">
<ul>
    <li>Commencer avec un faible capital et un range large</li>
    <li>Utiliser des stratégies asymétriques si marché directionnel</li>
    <li>Vérifier la volatilité 7j et 30j</li>
    <li>Ne pas déposer tout le capital d’un coup</li>
    <li>Surveiller la courbe IL après dépôt</li>
    <li>Utiliser le dex pour déposer la liquidité (expert)</li>
</ul>
</div>

<h3 id="conclusion">Conclusion</h3>
<div class="encadre">
<p>Ce guide t’a donné les concepts fondamentaux, des explications simples des stratégies, comment interpréter ratios, range, volatilité, lire l’IL et éviter les erreurs classiques.<br>
Avec l'application, tu as un backtest complet des LP, parfait pour apprendre et gérer des pools concentrés avec une vision globale de la mécanique.</p>
</div>

</div>
"""

st.markdown(guide_html, unsafe_allow_html=True)

# ======================= video IL =======================
st.markdown("""
<div style="
    background: linear-gradient(135deg, #0b0f14 0%, #141a2a 40%, #1c2338 100%);
    padding:20px;
    border-radius:12px;
    margin-top:20px;
    margin-bottom:20px;
">
    <span style="color:white;font-size:28px;font-weight:700;">
        ATELIER IMPERMANENT LOSS
    </span>
</div>
""", unsafe_allow_html=True)
st.set_page_config(layout="wide")

# colonne unique large
col, = st.columns(1)

with col:
    st.video("https://www.youtube.com/watch?v=uQPeyXsQNrs")

# ======================= outil atelier IL =======================
import streamlit.components.v1 as components

st.markdown("""
<div style="
    background: linear-gradient(135deg, #0b0f14 0%, #141a2a 40%, #1c2338 100%);
    padding:20px;
    border-radius:12px;
    margin-top:20px;
    margin-bottom:20px;
">
    <span style="color:white;font-size:28px;font-weight:700;">
        CALCULATRICE IMPERMANENT LOSS
    </span>
</div>
""", unsafe_allow_html=True)

st.set_page_config(layout="wide")

desmos_url = "https://www.desmos.com/calculator/i7mnoyyqdb?lang=fr"

components.iframe(
    src=desmos_url,
    width="100%",
    height=700,
    scrolling=True
)
