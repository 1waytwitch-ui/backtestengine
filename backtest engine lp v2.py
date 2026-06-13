import streamlit as st
import requests
import numpy as np
import datetime
import plotly.graph_objects as go
import plotly.io as pio
import math
import time
import random
import streamlit.components.v1 as components


st.markdown("""
<style>

/* =========================
   MASQUER L'UI STREAMLIT
   ========================= */

#MainMenu {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    display: none;
}

[data-testid="stToolbar"] {
    display: none;
}

footer {
    display: none;
}

/* =========================
   DARK MODE FORCÉ
   ========================= */

:root {
    color-scheme: dark;
}

html, body {
    background: #0b0f19 !important;
}

.stApp {
    background: #0b0f19 !important;
}

/* Containers Streamlit */
[data-testid="stAppViewContainer"] {
    background: #0b0f19 !important;
}

[data-testid="stMain"] {
    background: transparent !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111827 !important;
}

/* Texte par défaut */
body,
p,
span,
label,
div {
    color: #f8fafc;
}

/* Espace pour ton header fixe */
.block-container {
    padding-top: 90px !important;
}

</style>
""", unsafe_allow_html=True)


# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="LP BACKTEST ENGINE v2",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== PLOTLY DARK =====================
pio.templates.default = "plotly_dark"

# ===================== GLOBAL THEME =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* ========== ROOT ========== */
:root {
    --bg-void:    #060a0e;
    --bg-main:    #080c10;
    --bg-panel:   #0d1318;
    --bg-card:    #111820;
    --bg-card-hover: #141d25;
    --accent:     #00d4aa;
    --accent-dim: rgba(0, 212, 170, 0.12);
    --accent-mid: rgba(0, 212, 170, 0.3);
    --accent-2:   #0ea5e9;
    --accent-3:   #f59e0b;
    --accent-red: #ef4444;
    --accent-green: #22c55e;
    --border:     rgba(0, 212, 170, 0.15);
    --border-soft: rgba(255,255,255,0.06);
    --text-hi:    #f0f4f8;
    --text-mid:   #8899aa;
    --text-lo:    #445566;
    --font-mono:  'JetBrains Mono', 'Courier New', monospace;
    --font-ui:    'Inter', sans-serif;
}

/* ========== APP BASE ========== */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-main) !important;
    color: var(--text-hi);
    font-family: var(--font-ui);
}

[data-testid="stAppViewContainer"] {
    background-color: var(--bg-main) !important;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ========== TOP NAV BAR ========== */
.nav-bar {
    position: fixed;
    top: 0; left: 0;
    width: 100%;
    height: 58px;
    z-index: 9999;
    background: rgba(6, 10, 14, 0.95);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 28px;
    box-sizing: border-box;
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.nav-glyph {
    width: 28px; height: 28px;
    border: 2px solid var(--accent);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-mono);
    font-size: 14px;
    color: var(--accent);
    font-weight: 700;
}

.nav-title {
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 600;
    color: var(--text-hi);
    letter-spacing: 2px;
    text-transform: uppercase;
}

.nav-subtitle {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-mid);
    letter-spacing: 1px;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 6px;
}

.nav-links a {
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 500;
    color: var(--text-mid);
    text-decoration: none;
    padding: 5px 12px;
    border: 1px solid transparent;
    border-radius: 5px;
    transition: all 0.2s ease;
    letter-spacing: 0.5px;
}

.nav-links a:hover {
    color: var(--accent);
    border-color: var(--border);
    background: var(--accent-dim);
}

.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--accent);
    animation: pulse-dot 2s infinite;
    display: inline-block;
    margin-right: 6px;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(0,212,170,0.4); }
    50% { opacity: 0.7; box-shadow: 0 0 0 4px rgba(0,212,170,0); }
}

/* ========== OFFSET FOR FIXED NAVBAR ========== */
[data-testid="stAppViewContainer"] > .main { padding-top: 72px !important; }

/* ========== SECTION HEADERS ========== */
.sec-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 28px 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}

.sec-head-icon {
    width: 24px; height: 24px;
    background: var(--accent-dim);
    border: 1px solid var(--border);
    border-radius: 5px;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px;
    color: var(--accent);
}

.sec-head-label {
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 600;
    color: var(--accent);
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ========== METRIC CARDS ========== */
.m-card {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 10px;
    padding: 16px 18px;
    margin: 8px 0;
    transition: border-color 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}

.m-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent);
    opacity: 0;
    transition: opacity 0.2s;
}

.m-card:hover { border-color: var(--border); box-shadow: 0 0 18px rgba(0,212,170,0.06); }
.m-card:hover::before { opacity: 1; }

.m-label {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-mid);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.m-value {
    font-family: var(--font-mono);
    font-size: 20px;
    font-weight: 600;
    color: var(--accent);
    line-height: 1.1;
}

.m-value-sm {
    font-family: var(--font-mono);
    font-size: 14px;
    font-weight: 500;
    color: var(--accent);
    line-height: 1.2;
}

.m-value-red { color: var(--accent-red); }
.m-value-green { color: var(--accent-green); }
.m-value-amber { color: var(--accent-3); }
.m-value-blue { color: var(--accent-2); }

/* ========== WIDE CARD ========== */
.m-card-wide {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 10px;
    padding: 18px 20px;
    margin: 8px 0;
}

/* ========== ALERT CARDS ========== */
.m-card-alert {
    background: rgba(239,68,68,0.06);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 10px;
    padding: 16px 18px;
    margin: 8px 0;
}

/* ========== TERMINAL BLOCK ========== */
.term-block {
    background: #050809;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px;
    font-family: var(--font-mono);
    font-size: 12px;
    line-height: 1.65;
    color: var(--accent);
    max-height: 420px;
    overflow-y: auto;
}

.term-block::-webkit-scrollbar { width: 4px; }
.term-block::-webkit-scrollbar-thumb { background: var(--accent-mid); border-radius: 2px; }
.term-block::-webkit-scrollbar-track { background: transparent; }

.term-cursor {
    display: inline-block;
    width: 7px; height: 13px;
    background: var(--accent);
    margin-left: 2px;
    vertical-align: middle;
    animation: blink-cur 1s step-end infinite;
}

@keyframes blink-cur { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

/* ========== METEO BOX ========== */
.meteo-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 20px;
    font-family: var(--font-mono);
    font-size: 12px;
    line-height: 1.7;
    color: var(--accent);
}

/* ========== INPUTS ========== */
div[data-baseweb="input"] input,
.stNumberInput input {
    background: var(--bg-panel) !important;
    color: var(--text-hi) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: 7px !important;
    font-family: var(--font-mono) !important;
    font-size: 13px !important;
}

div[data-baseweb="input"] input:focus,
.stNumberInput input:focus {
    border-color: var(--accent-mid) !important;
    box-shadow: 0 0 0 2px var(--accent-dim) !important;
    outline: none !important;
}

.stTextInput input {
    background: var(--bg-panel) !important;
    color: var(--text-hi) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: 7px !important;
    font-family: var(--font-mono) !important;
    font-size: 13px !important;
}

/* ========== SELECTBOX ========== */
.stSelectbox > div > div {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: 7px !important;
    color: var(--text-hi) !important;
    font-family: var(--font-mono) !important;
}

/* ========== LABELS ========== */
label, .stLabel {
    font-family: var(--font-ui) !important;
    font-size: 12px !important;
    color: var(--text-mid) !important;
    font-weight: 500 !important;
}

/* ========== BUTTONS ========== */
.stButton > button {
    background: var(--accent) !important;
    color: #030a07 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 10px 20px !important;
    transition: all 0.2s !important;
    text-transform: uppercase !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(0,212,170,0.3) !important;
    filter: brightness(1.08) !important;
}

/* ========== RADIO / CHECKBOX ========== */
.stRadio label, .stCheckbox label { color: var(--text-hi) !important; font-size: 13px !important; }

/* ========== SLIDER ========== */
.stSlider > div > div > div { background: var(--accent) !important; }

/* ========== EXPANDER ========== */
details { background: var(--bg-panel); border: 1px solid var(--border-soft); border-radius: 8px; padding: 4px 12px; }
summary { color: var(--accent); font-family: var(--font-mono); font-size: 12px; cursor: pointer; }

/* ========== ALERTS ========== */
.stAlert { background: var(--bg-panel); border-left: 3px solid var(--accent); color: var(--text-hi); border-radius: 8px; }

/* ========== SUBHEADER ========== */
h1, h2, h3, h4 { color: var(--text-hi) !important; font-family: var(--font-ui) !important; }
h3 { font-size: 14px !important; font-weight: 600 !important; letter-spacing: 0.3px !important; }

/* ========== DISCLAIMER BANNER ========== */
.disc-bar {
    background: rgba(0,212,170,0.05);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 16px;
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-mid);
    margin: 10px 0 18px 0;
}

.disc-bar span { color: var(--accent); }

/* ========== DIVIDER ========== */
.v2-divider {
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
    margin: 30px 0;
}

/* ========== GUIDE STYLES ========== */
.guide-wrap {
    font-family: var(--font-ui);
    color: var(--text-hi);
    margin-top: 10px;
}

.guide-section {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 10px;
    padding: 18px 22px;
    margin: 12px 0;
    transition: border-color 0.2s;
}

.guide-section:hover { border-color: var(--border); }

.guide-section h3 {
    color: var(--accent) !important;
    font-family: var(--font-mono) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    margin: 0 0 10px 0 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

.guide-section p, .guide-section li {
    font-size: 13px;
    color: #b0bec5;
    line-height: 1.7;
}

.guide-section b { color: var(--text-hi); }

.toc-box {
    background: var(--accent-dim);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 22px;
    margin-bottom: 20px;
}

.toc-box h4 { color: var(--accent); font-family: var(--font-mono); font-size: 12px; letter-spacing: 2px; margin: 0 0 12px 0; }
.toc-box a { color: var(--accent); font-family: var(--font-mono); font-size: 12px; text-decoration: none; opacity: 0.85; }
.toc-box a:hover { opacity: 1; text-decoration: underline; }
.toc-box li { margin-bottom: 5px; list-style: none; }
.toc-box li::before { content: '→ '; color: var(--text-lo); }

/* ========== SCROLLBAR ========== */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-track { background: transparent; }

/* ========== CHECKLIST TERMINAL ========== */
.checklist-term {
    background: #050809;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    font-family: var(--font-mono);
    font-size: 12px;
    line-height: 1.6;
    color: var(--accent);
    max-height: 400px;
    overflow-y: auto;
}

</style>
""", unsafe_allow_html=True)

# ========== TOP NAV BAR ==========
st.markdown("""
<div class="nav-bar">
    <div class="nav-brand">
        <div class="nav-glyph">◈</div>
        <div>
            <div class="nav-title">LP STRATÉGIES BACKTEST ENGINE</div>
            <div class="nav-subtitle"><span class="status-dot"></span>LIVE · LIQUIDITY PROVIDERS · TOOLS</div>
        </div>
    </div>
    <div class="nav-links">
        <a href="https://defi.krystal.app/referral?r=3JwR8YRQCRJT" target="_blank">Krystal</a>
        <a href="https://plusvalueimposable.streamlit.app/" target="_blank">Plus-value</a>
        <a href="https://defiwalletbacktest.streamlit.app/" target="_blank">Wallet</a>
        <a href="https://t.me/Pigeonchanceux" target="_blank">Telegram</a>
        <a href="https://shorturl.at/X3sYt" target="_blank">Formation</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== CONFIG DATA ==========
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
    "WETH": "weth", "USDC": "usd-coin", "CBBTC": "coinbase-wrapped-btc",
    "VIRTUAL": "virtual-protocol", "AERO": "aerodrome-finance"
}

PAIRS = [("WETH", "USDC"), ("CBBTC", "USDC"), ("WETH", "CBBTC"), ("VIRTUAL", "WETH"), ("AERO", "WETH")]


SECRET_CODE = st.secrets["Secret_Code"]

# ========== FUNCTIONS ==========
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
    if len(prices) < 2: return 0.0
    prices = np.array(prices)
    returns = np.diff(prices) / prices[:-1]
    returns = returns[~np.isnan(returns)]
    return float(np.std(returns))

def get_price_usd(token):
    try:
        res = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={COINGECKO_IDS[token]}&vs_currencies=usd").json()
        return res[COINGECKO_IDS[token]]["usd"], True
    except:
        return 0.0, False

def compute_L(P, P_l, P_u, V):
    sqrtP, sqrtPl, sqrtPu = np.sqrt(P), np.sqrt(P_l), np.sqrt(P_u)
    return V / (P * (1/sqrtP - 1/sqrtPu) + (sqrtP - sqrtPl))

def tokens_from_L(L, P, P_l, P_u):
    sqrtP, sqrtPl, sqrtPu = np.sqrt(P), np.sqrt(P_l), np.sqrt(P_u)
    return L * (1/sqrtP - 1/sqrtPu), L * (sqrtP - sqrtPl)

def normalize_L(L, x0, y0, P, V):
    factor = V / (x0*P + y0)
    return L*factor, x0*factor, y0*factor

def x_of_P(P, L, P_upper):
    P_arr = np.asarray(P, float)
    x = L * (1/np.sqrt(P_arr) - 1/np.sqrt(P_upper))
    return np.where(x < 0, 0, x) if isinstance(x, np.ndarray) else max(x, 0.0)

def y_of_P(P, L, P_lower):
    P_arr = np.asarray(P, float)
    y = L * (np.sqrt(P_arr) - np.sqrt(P_lower))
    return np.where(y < 0, 0, y) if isinstance(y, np.ndarray) else max(y, 0.0)

def V_LP(P, L, P_lower, P_upper):
    return x_of_P(P, L, P_upper)*np.asarray(P,float) + y_of_P(P, L, P_lower)

def V_HODL(P, x0, y0):
    return x0*P + y0

def calculate_clmm_apr(fees_usd_period, active_liquidity_usd_avg, period_days):
    if active_liquidity_usd_avg <= 0 or period_days <= 0: return 0.0
    return fees_usd_period / active_liquidity_usd_avg * (365/period_days) * 100

def calculate_pair_atr(price_x, atr_x, price_y, atr_y, multiplier=1):
    pair_price = price_x/price_y
    delta_x = atr_x/price_y
    delta_y = (price_x/(price_y**2))*atr_y
    atr_pair = math.sqrt(delta_x**2 + delta_y**2)*multiplier
    low = pair_price - atr_pair
    high = pair_price + atr_pair
    return {"pair_price": pair_price, "atr_pair": atr_pair, "low": low, "high": high, "range_pct": (atr_pair/pair_price)*100}

def sec(icon, label):
    st.markdown(f"""
    <div class="sec-head">
        <div class="sec-head-icon">{icon}</div>
        <div class="sec-head-label">{label}</div>
    </div>""", unsafe_allow_html=True)

def card(label, value, color="var(--accent)", wide=False):
    cls = "m-card-wide" if wide else "m-card"
    st.markdown(f"""
    <div class="{cls}">
        <div class="m-label">{label}</div>
        <div class="m-value" style="color:{color};">{value}</div>
    </div>""", unsafe_allow_html=True)

# ========== INIT SESSION STATE ==========
for k, v in [
    ("authenticated", False), ("show_disclaimer", True), ("content", []),
    ("finished", False), ("disclaimer_shown", False), ("secret_content", []),
    ("checklist_validee", False), ("checklist_content", []), ("meteo_cached", None)
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ========== TERMINAL BOOT ANIMATION ==========
terminal_placeholder = st.empty()

def render_term(placeholder, content, div_id="term-main", css_class="term-block"):
    placeholder.markdown(
        f"<div id='{div_id}' class='{css_class}'>" +
        "<br>".join(content) +
        "<span class='term-cursor'></span></div>"
        f"<script>var t=document.getElementById('{div_id}');if(t)t.scrollTop=t.scrollHeight;</script>",
        unsafe_allow_html=True
    )

def type_line_to(content_list, placeholder, line, div_id="term-main", css_class="term-block"):
    content_list.append("")
    cur = ""
    for char in line:
        cur += char
        content_list[-1] = cur
        render_term(placeholder, content_list, div_id, css_class)
        time.sleep(random.uniform(0.005, 0.015))

def add_term_line(content_list, placeholder, line, div_id="term-main", css_class="term-block"):
    type_line_to(content_list, placeholder, line, div_id, css_class)
    time.sleep(random.uniform(0.02, 0.08))

if not st.session_state.finished:
    lines_boot = [
        "◈ BACKTEST ENGINE LP v2.0 — INITIALIZING",
        "─────────────────────────────────────────",
        "▸ Chargement des modules...",
        "  [✓] Pool Setup | Price & Range | Automation avancée",
        "  [✓] IL Simulator | APR réel | ATR avancée",
        "  [✓] Break Even | Zeroswap Rebalance | Refill LP",
        "  [✓] Optimal range finder | Prix moyen CLM | Optimisation du range",
        "  [✓] Guide complet + Atelier vidéo IL & Calculatrice",
        "─────────────────────────────────────────",
        "▸ Nouveautés v2 :",
        "  [✓] LP Health Score activé",
        "  [✓] Auto Range disponible",
        "  [✓] Optimal Range Finder ajouté",
        "─────────────────────────────────────────",
        "▸ Optimisation des outils en cours...",
        "  Vous pouvez optimiser vos stratégies.",
        "  SYSTÈME PRÊT ◈"
    ]
    for line in lines_boot:
        add_term_line(st.session_state.content, terminal_placeholder, line)
    st.session_state.finished = True
else:
    render_term(terminal_placeholder, st.session_state.content)

if st.session_state.finished and not st.session_state.disclaimer_shown:
    disc_lines = [
        "",
        "$ cat disclaimer.txt",
        "──────────────────────────────────────────",
        "[!] SYSTEM WARNING — DISCLAIMER LOADED",
        "──────────────────────────────────────────",
        "⚠  DISCLAIMER IMPORTANT",
        "",
        "Un backtest en DeFi n'explique pas comment gagner,",
        "mais comment une stratégie peut perdre malgré des APY élevés.",
        "",
        "Accès réservé aux membres Team Élite (KBOUR Crypto)",
        "Code disponible dans le canal privé 'DEFI Académie'",
        "",
        "Cet outil peut contenir des approximations",
        "Ceci n'est PAS un conseil en investissement",
        "",
        "Faites vos propres recherches (DYOR)",
        "Comprenez les risques des pools de liquidités concentrés",
        "",
        "Si l'API est surchargée → saisie manuelle requise",
        "──────────────────────────────────────────"
    ]
    for line in disc_lines:
        add_term_line(st.session_state.content, terminal_placeholder, line)
    st.session_state.disclaimer_shown = True

st.markdown("""
<div class="disc-bar">
  <span>⚠</span> Un backtest en DeFi n'explique pas comment gagner, mais comment une stratégie peut perdre malgré des APY élevés.
</div>
""", unsafe_allow_html=True)

# ========== SECRET CODE ==========
if not st.session_state.authenticated:
    sec_placeholder = st.empty()
    if not st.session_state.secret_content:
        add_term_line(st.session_state.secret_content, sec_placeholder, "◈ ACCESS PROTOCOL — TEAM ÉLITE KBOUR CRYPTO", "sec-term", "term-block")
        add_term_line(st.session_state.secret_content, sec_placeholder, "▸ Vérification des droits en cours...", "sec-term", "term-block")
        add_term_line(st.session_state.secret_content, sec_placeholder, "▸ Saisissez le code d'accès ci-dessous.", "sec-term", "term-block")
    else:
        render_term(sec_placeholder, st.session_state.secret_content, "sec-term", "term-block")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    col_in, col_btn = st.columns([3, 1])
    with col_in:
        code_input = st.text_input("Code d'accès", key="secret_code", type="password", label_visibility="collapsed", placeholder="Entrez le code d'accès…")
    with col_btn:
        if st.button("◈ VALIDER", use_container_width=True):
            if code_input == SECRET_CODE:
                st.session_state.authenticated = True
                st.rerun()
            else:
                add_term_line(st.session_state.secret_content, sec_placeholder, "[!] CODE INCORRECT — Accès refusé.", "sec-term", "term-block")
                st.error("Code incorrect")
    st.stop()

st.markdown("""
<div class="disc-bar" style="border-color:var(--accent); color:var(--accent);">
  <span>◈</span> ACCÈS AUTORISÉ — Bonjour et bienvenue !
</div>
""", unsafe_allow_html=True)

# ========== CHECKLIST ==========
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

cl_placeholder = st.empty()

if not st.session_state.checklist_validee:
    if not st.session_state.checklist_content:
        add_term_line(st.session_state.checklist_content, cl_placeholder, "$ init checklist_protocol --lp_safety", "cl-term", "term-block")
        add_term_line(st.session_state.checklist_content, cl_placeholder, "▸ auto-checking all items...", "cl-term", "term-block")
        for item in checklist_items:
            add_term_line(st.session_state.checklist_content, cl_placeholder, f"  [✓] {item}", "cl-term", "term-block")
        score = len(checklist_items)
        bar = "█"*20 + "░"*0
        add_term_line(st.session_state.checklist_content, cl_placeholder, f"▸ progress: [{bar}] {score}/{score} — READY", "cl-term", "term-block")
    else:
        render_term(cl_placeholder, st.session_state.checklist_content, "cl-term", "term-block")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    if st.button("◈ J'AI COMPRIS — ACCÉDER AUX OUTILS", use_container_width=True):
        st.session_state.checklist_validee = True
        st.rerun()
    st.stop()

st.markdown("""
<div class="disc-bar">
  <span>◈</span> déverrouillage des outils...
</div>
""", unsafe_allow_html=True)

# ==========================================
# GENERATEUR METEO LP
# ==========================================

st.subheader("☀️ Générateur Météo LP")

col1, col2 = st.columns(2)

with col1:

    eth_price_v2 = st.number_input(
        "Prix ETH ($)",
        min_value=1.0,
        value=2992.0,
        step=10.0
    )

    eth_atr_v2 = st.number_input(
        "ATR ETH ($)",
        min_value=1.0,
        value=124.0,
        step=1.0
    )

with col2:

    btc_price_v2 = st.number_input(
        "Prix BTC ($)",
        min_value=1.0,
        value=124000.0,
        step=100.0
    )

    btc_atr_v2 = st.number_input(
        "ATR BTC ($)",
        min_value=1.0,
        value=2992.0,
        step=10.0
    )

if st.button("🚀 Générer la météo", use_container_width=True):

    # ==========================================
    # CALCUL DES RANGES EN $
    # ==========================================

    eth_range_low_v2 = eth_price_v2 - eth_atr_v2
    eth_range_high_v2 = eth_price_v2 + eth_atr_v2

    btc_range_low_v2 = btc_price_v2 - btc_atr_v2
    btc_range_high_v2 = btc_price_v2 + btc_atr_v2

    # ==========================================
    # ATR -> %
    # ==========================================

    eth_range_pct_v2 = (eth_atr_v2 / eth_price_v2) * 100
    btc_range_pct_v2 = (btc_atr_v2 / btc_price_v2) * 100

    # ==========================================
    # MULTIPLICATEURS LP
    # ==========================================

    weth_usdc_pct_v2 = eth_range_pct_v2 * 3
    usdc_cbbtc_pct_v2 = btc_range_pct_v2 * 3

    weth_cbbtc_pct_v2 = (
        (eth_range_pct_v2 + btc_range_pct_v2) / 2
    ) * 1.5

    # ==========================================
    # STOCKAGE STRUCTURÉ
    # ==========================================

    METEO = {
        "title": "☀️ METEO DeFi RANGE LP",
        "market": f"Volatilité moyenne : {weth_cbbtc_pct_v2:.1f}% → marché en range.",
        "strategies": [
            f"WETH/USDC → {weth_usdc_pct_v2:.1f}% RANGE | {eth_range_low_v2:,.0f}$ → {eth_range_high_v2:,.0f}$",
            f"USDC/cbBTC → {usdc_cbbtc_pct_v2:.1f}% RANGE | {btc_range_low_v2:,.0f}$ → {btc_range_high_v2:,.0f}$",
            f"WETH/cbBTC → {weth_cbbtc_pct_v2:.1f}% RANGE | ETH {eth_price_v2:,.0f}$ | BTC {btc_price_v2:,.0f}$"
        ],
        "conclusion": "On capte la volatilité, pas la direction. Les ranges sont calculés automatiquement à partir des ATR et des prix. Les volumes doivent être intégré dans la prise de décision du range final !"
    }

    st.session_state["meteo"] = METEO


# ==========================================
# SHOW METEO
# ==========================================

if "meteo" in st.session_state:

    METEO = st.session_state["meteo"]

    # bloc principal stylé via TON CSS .meteo-box
    st.markdown(
        f"""
        <div class="meteo-box">

        <b>{METEO["title"]}</b>
        <br><br>

        {METEO["market"]}
        <br><br>

        • {METEO["strategies"][0]}<br>
        • {METEO["strategies"][1]}<br>
        • {METEO["strategies"][2]}

        <br><br>

        {METEO["conclusion"]}

        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================================================
# ========== POOL SETUP ==========
# ==================================================================================
sec("⬡", "Pool Setup")

col1, col2 = st.columns([1.3, 1])

with col1:
    left, right = st.columns(2)
    with left:
        pair_labels = [f"{a}/{b}" for a, b in PAIRS]
        selected_pair = st.radio("Paire :", pair_labels, index=0)
    with right:
        strategy_choice = st.radio("Stratégie :", list(STRATEGIES.keys()))

    if "last_pair" not in st.session_state or st.session_state["last_pair"] != selected_pair:
        for k in list(st.session_state.keys()):
            if k.endswith("_prices_" + str(datetime.date.today())):
                del st.session_state[k]
        st.session_state["last_pair"] = selected_pair

    tokenA, tokenB = selected_pair.split("/")
    info = STRATEGIES[strategy_choice]
    ratioA, ratioB = info["ratio"]

    invert_market = st.checkbox("Inversion marché (bull → bear)")
    if invert_market:
        ratioA, ratioB = ratioB, ratioA

    capital = st.number_input("Capital (USD)", value=1000, step=50)

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

    keyA = f"{tokenA}_prices_{datetime.date.today()}"
    keyB = f"{tokenB}_prices_{datetime.date.today()}"
    if keyA not in st.session_state: st.session_state[keyA] = get_market_chart(COINGECKO_IDS[tokenA])
    if keyB not in st.session_state: st.session_state[keyB] = get_market_chart(COINGECKO_IDS[tokenB])

    pricesA = np.array(st.session_state[keyA])
    pricesB = np.array(st.session_state[keyB])

    def compute_pair_volatility(pA, pB):
        min_len = min(len(pA), len(pB))
        pA, pB = pA[:min_len], pB[:min_len]
        mask = (pA > 1e-8) & (pB > 1e-8)
        pA, pB = pA[mask], pB[mask]
        if len(pA) < 2: return 0.0
        pair_p = pA / pB
        rets = np.diff(pair_p) / pair_p[:-1]
        rets = rets[~np.isnan(rets)]
        return float(np.std(rets)) if len(rets) > 0 else 0.0

    if selected_pair in ["WETH/USDC", "CBBTC/USDC"]:
        vol_30d = compute_volatility(pricesA)
    else:
        vol_30d = compute_pair_volatility(pricesA, pricesB) / 2

    if vol_30d == 0:
        defaults = {"CBBTC/USDC": 0.12, "VIRTUAL/WETH": 0.45, "AERO/WETH": 0.45}
        vol_30d = defaults.get(selected_pair, 0.0)

    vol_sugg = vol_30d * 100
    if vol_sugg < 2: suggested_range = 3
    elif vol_sugg < 4: suggested_range = 7
    elif vol_sugg < 7: suggested_range = 10
    elif vol_sugg < 10: suggested_range = 16
    else: suggested_range = 20

    multipliers = {"CBBTC/USDC": (1.3, 1), "VIRTUAL/WETH": (6.2, 3.2), "AERO/WETH": (6.5, 2)}
    sm, vm = multipliers.get(selected_pair, (3, 3))
    suggested_range *= sm

    range_pct = st.number_input("Range (%)", min_value=1.0, max_value=200.0, value=20.0, key="range_pct")

    range_low = priceA * (1 - ratioA * range_pct / 100)
    range_high = priceA * (1 + ratioB * range_pct / 100)
    if invert_market: range_low, range_high = range_high, range_low

    capitalA, capitalB = capital * ratioA, capital * ratioB

with col2:
    sec("◎", "Price / Range")

    c1, c2 = st.columns(2)
    with c1: card("Prix actuel", f"{priceA:.6f} $")
    with c2: card("Range", f"{range_low:.4f} → {range_high:.4f}")

    card("Répartition capital", f"{capitalA:.2f} USD {tokenA}  ·  {capitalB:.2f} USD {tokenB}", wide=True)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=[ratioA*100], y=[tokenA], orientation="h",
        marker=dict(color="#00d4aa", opacity=0.85), showlegend=False))
    fig_bar.add_trace(go.Bar(x=[ratioB*100], y=[tokenB], orientation="h",
        marker=dict(color="#0ea5e9", opacity=0.85), showlegend=False))
    fig_bar.update_layout(
        height=110, margin=dict(l=5,r=5,t=5,b=5),
        xaxis=dict(range=[0,100], showgrid=False, tickfont=dict(color="#8899aa",size=10)),
        yaxis=dict(tickfont=dict(color="#f0f4f8",size=12)),
        plot_bgcolor="#0d1318", paper_bgcolor="#0d1318",
        barmode="stack"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown(f"""
    <div class="m-card-wide">
        <div class="m-label">Résumé stratégie</div>
        <div style="margin-top:8px; font-size:13px; color:#b0bec5; line-height:1.7;">
            <span style="color:#f0f4f8; font-weight:600;">Ratio :</span> {int(ratioA*100)} / {int(ratioB*100)}<br>
            <span style="color:#f0f4f8; font-weight:600;">Objectif :</span> {info['objectif']}<br>
            <span style="color:#f0f4f8; font-weight:600;">Contexte :</span> {info['contexte']}
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== AUTOMATION ==========
# ==================================================================================
sec("⚙", "Réglages Automation")

col_range, col_time = st.columns([2, 1])

ratioA_trigger, ratioB_trigger = ratioA, ratioB
if invert_market: ratioA_trigger, ratioB_trigger = ratioB_trigger, ratioA_trigger

with col_range:
    sec("◎", "Range future")
    range_percent = st.slider("Range total (%)", 1.0, 90.0, 20.0, step=0.1)
    low_offset_pct = -range_percent * 20 / 100
    high_offset_pct = range_percent * 80 / 100
    final_low = priceA * (1 + low_offset_pct/100)
    final_high = priceA * (1 + high_offset_pct/100)
    card("Range calculé", f"{final_low:.6f}  →  {final_high:.6f}", wide=True)

with col_time:
    sec("◷", "Time-buffer")
    vola = vol_30d * 100
    if vola < 2: recomand = "6 à 12 min"
    elif vola < 5: recomand = "18 à 48 min"
    else: recomand = "60 min +"
    card("Recommandation", recomand)

st.markdown("<br>", unsafe_allow_html=True)
col_trigger, col_rebalance = st.columns(2)

with col_trigger:
    sec("◈", "Trigger d'anticipation (RATIO)")
    t1, t2 = st.columns(2)
    with t1: trig_low = st.slider("Trigger Low (%)", 0.0, 100.0, 10.0, step=0.1)
    with t2: trig_high = st.slider("Trigger High (%)", 0.0, 100.0, 90.0, step=0.1)

    rw = final_high - final_low
    trigger_low_price = final_low + (trig_low/100)*rw
    trigger_high_price = final_low + (trig_high/100)*rw

    r1, r2 = st.columns(2)
    with r1: card("Trigger Low", f"{trigger_low_price:.6f}")
    with r2: card("Trigger High", f"{trigger_high_price:.6f}")

with col_rebalance:
    sec("⟳", "Rebalance avancée (futur range)")
    off_low_pct = -ratioA * range_percent
    off_high_pct = ratioB * range_percent
    bear_low = priceA * (1 + off_low_pct/100)
    bear_high = priceA * (1 + off_high_pct/100)
    bull_low = priceA * (1 - off_high_pct/100)
    bull_high = priceA * (1 - off_low_pct/100)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.markdown(f"""
        <div class="m-card">
            <div class="m-label">🔺 Marché Haussier (Pump)</div>
            <div class="m-value-sm" style="color:#22c55e;">{bull_low:.4f} → {bull_high:.4f}</div>
            <div style="font-size:11px; color:var(--text-mid); margin-top:4px;">{(-off_high_pct):.1f}% → {(-off_low_pct):.1f}%</div>
        </div>""", unsafe_allow_html=True)
    with col_b2:
        st.markdown(f"""
        <div class="m-card">
            <div class="m-label">🔻 Marché Baissier (Dump)</div>
            <div class="m-value-sm" style="color:#ef4444;">{bear_low:.4f} → {bear_high:.4f}</div>
            <div style="font-size:11px; color:var(--text-mid); margin-top:4px;">{off_low_pct:.1f}% → {off_high_pct:.1f}%</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== IMPERMANENT LOSS ==========
# ==================================================================================
sec("∿", "Impermanent Loss")

row1_col1, row1_col2, row1_col3 = st.columns(3)
with row1_col1:
    st.markdown('<p style="font-size:12px;color:var(--text-mid);margin-bottom:3px;">P_deposit</p>', unsafe_allow_html=True)
    P_deposit = st.number_input("P_deposit", value=3000.0, format="%.6f", step=0.001, label_visibility="collapsed")
with row1_col2:
    st.markdown('<p style="font-size:12px;color:var(--text-mid);margin-bottom:3px;">P_now</p>', unsafe_allow_html=True)
    P_now = st.number_input("P_now", value=3000.0, format="%.6f", step=0.001, label_visibility="collapsed")
with row1_col3:
    st.markdown('<p style="font-size:12px;color:var(--text-mid);margin-bottom:3px;">Valeur deposit (USD)</p>', unsafe_allow_html=True)
    v_deposit = st.number_input("Valeur deposit (USD)", value=500.0, format="%.6f", step=0.01, label_visibility="collapsed")

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    st.markdown('<p style="font-size:12px;color:var(--text-mid);margin-bottom:3px;">P_lower</p>', unsafe_allow_html=True)
    P_lower = st.number_input("P_lower", value=2800.0, format="%.6f", step=0.001, label_visibility="collapsed")
with row2_col2:
    st.markdown('<p style="font-size:12px;color:var(--text-mid);margin-bottom:3px;">P_upper</p>', unsafe_allow_html=True)
    P_upper = st.number_input("P_upper", value=3500.0, format="%.6f", step=0.001, label_visibility="collapsed")

L_raw = compute_L(P_deposit, P_lower, P_upper, v_deposit)
x0_raw, y0_raw = tokens_from_L(L_raw, P_deposit, P_lower, P_upper)
L, x0, y0 = normalize_L(L_raw, x0_raw, y0_raw, P_deposit, v_deposit)

prices_il = np.linspace(P_lower*0.8, P_upper*1.3, 400)
LP_values = V_LP(prices_il, L, P_lower, P_upper)
HODL_values = V_HODL(prices_il, x0, y0)
IL_curve = (LP_values / HODL_values - 1) * 100

fig_il = go.Figure()
fig_il.add_trace(go.Scatter(x=prices_il, y=IL_curve, mode="lines", name="IL(%)",
    line=dict(color="#ef4444", width=2.5), fill="tozeroy",
    fillcolor="rgba(239,68,68,0.05)"))

annot_cfg = [
    (P_lower, "Low", "#22c55e", max(IL_curve), 12),
    (P_upper, "High", "#22c55e", max(IL_curve), 12),
    (P_deposit, "Deposit", "#0ea5e9", min(IL_curve), -14),
    (P_now, "Now", "#f59e0b", min(IL_curve), -14),
]
for px, label, color, y_pos, yshift in annot_cfg:
    fig_il.add_vline(x=px, line=dict(color=color, width=1.5, dash="dot"))
    fig_il.add_annotation(x=px, y=y_pos, text=label, showarrow=False,
        font=dict(color=color, size=11), yshift=yshift)

fig_il.update_xaxes(title="Prix", title_font=dict(color="#8899aa", size=12),
    tickfont=dict(color="#8899aa", size=11), gridcolor="rgba(255,255,255,0.04)")
fig_il.update_yaxes(title="IL (%)", title_font=dict(color="#8899aa", size=12),
    tickfont=dict(color="#8899aa", size=11), gridcolor="rgba(255,255,255,0.04)")
fig_il.update_layout(height=350, plot_bgcolor="#0d1318", paper_bgcolor="#0d1318",
    title=dict(text="Impermanent Loss (%)", font=dict(color="#f0f4f8", size=14)),
    legend=dict(font=dict(color="#8899aa")), margin=dict(l=20,r=20,t=40,b=20))

st.plotly_chart(fig_il, use_container_width=True)

IL_now = (V_LP(P_now, L, P_lower, P_upper)/V_HODL(P_now, x0, y0)-1)*100
LP_now = V_LP(P_now, L, P_lower, P_upper)
HODL_now = V_HODL(P_now, x0, y0)

cols_il = st.columns(3)
with cols_il[0]: card("IL maintenant (%)", f"{IL_now:.2f}%", color="#ef4444" if IL_now < 0 else "#22c55e")
with cols_il[1]: card("Valeur LP ($)", f"${LP_now:,.2f}")
with cols_il[2]: card("Valeur HODL ($)", f"${HODL_now:,.2f}", color="#0ea5e9")

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== APR ==========
# ==================================================================================
sec("◉", "Calcul APR")

a1, a2, a3 = st.columns(3)
with a1: fees_usd_period = st.number_input("Total des fees (USD)", value=100.0, step=1000.0)
with a2: active_liquidity_usd_avg = st.number_input("Liquidité active moyenne (USD)", value=1000.0, step=10000.0)
with a3: period_days = st.number_input("Durée (jours)", value=30, min_value=1, step=1)

apr = calculate_clmm_apr(fees_usd_period, active_liquidity_usd_avg, period_days)
card("APR annualisé estimé", f"{apr:.2f} %", wide=True)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== ATR RANGE ==========
# ==================================================================================
sec("△", "ATR Range")

col_atr1, col_atr2, col_atr3 = st.columns(3)
with col_atr1: atr_usd = st.number_input("ATR 14 ($)", value=100.0, min_value=0.01, step=1.0)
with col_atr2: atr_mult = st.slider("Multiplicateur ATR", 0.5, 10.0, 3.0, step=0.25)
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

atr_low = asset_price*(1-range_total_pct*low_weight/100)
atr_high= asset_price*(1+range_total_pct*high_weight/100)

st.markdown(f"""
<div class="m-card-wide">
    <div class="m-label">Range basé sur ATR</div>
    <div class="m-value-sm" style="margin-top:8px;">
        ATR Low : <span style="color:#22c55e;">{atr_low:.2f}$</span>
        &nbsp;·&nbsp; ATR High : <span style="color:#ef4444;">{atr_high:.2f}$</span>
        &nbsp;·&nbsp; ±{range_total_pct:.2f}%
    </div>
</div>""", unsafe_allow_html=True)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== ATR PAIRE DOUBLE VOLATILE ==========
# ==================================================================================
sec("△△", "ATR Paire Double Volatile")

col1,col2,col3,col4=st.columns(4)
with col1: price_x = st.number_input("Prix actuel X", value=3111.0)
with col2: atr_x = st.number_input("ATR daily X", value=174.0)
with col3: price_y = st.number_input("Prix actuel Y", value=90113.0)
with col4: atr_y = st.number_input("ATR daily Y", value=3282.0)
atr_multiplier = st.slider("Multiplicateur ATR", 1.0, 6.0, 1.0, step=0.5)

if st.button("◈ Calculer ATR et RANGE"):
    result = calculate_pair_atr(price_x, atr_x, price_y, atr_y, atr_multiplier)
    st.markdown(f"""
    <div class="m-card-wide">
        <div class="m-label">ATR Paire Volatile</div>
        <div style="margin-top:8px; font-family:var(--font-mono); font-size:13px; color:#b0bec5; line-height:1.8;">
            Pair price : <span style="color:var(--accent);">{result['pair_price']:.6f}</span><br>
            ATR : <span style="color:var(--accent);">{result['atr_pair']:.6f}</span><br>
            Low / High : <span style="color:#22c55e;">{result['low']:.6f}</span> / <span style="color:#ef4444;">{result['high']:.6f}</span><br>
            ± <span style="color:var(--accent-3);">{result['range_pct']:.2f}%</span>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== BREAK-EVEN LP ==========
# ==================================================================================
sec("⊜", "Calculatrice Break-Even LP")

pair_type = st.selectbox("Type de paire", ["Volatile / Stable", "Double Volatile"])

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**METRICS**")
    capital_be = st.number_input("Capital engagé ($)", value=6400.0, step=0.01, format="%.2f")
    fees_be = st.number_input("Fees accumulés ($)", value=140.0, step=0.01, format="%.2f")
with col2:
    st.markdown("**Token A**")
    qty_a = st.number_input("Quantité", value=1.5, step=0.0001, format="%.6f")
    price_a = st.number_input("Prix actuel ($)", value=2950.0, step=0.01, format="%.2f")
with col3:
    if pair_type == "Volatile / Stable":
        st.markdown("**Token B (Stable)**")
        stable_amount = st.number_input("Montant ($)", value=1500.0, step=0.01, format="%.2f")
        value_be = qty_a * price_a + stable_amount
        effective_b = stable_amount + fees_be
    else:
        st.markdown("**Token B (Volatile)**")
        qty_b = st.number_input("Quantité", value=0.5, step=0.0001, format="%.6f")
        price_b = st.number_input("Prix actuel ($)", value=2000.0, step=0.01, format="%.2f")
        value_be = qty_a * price_a + qty_b * price_b
        effective_b = qty_b * price_b + fees_be

pnl_be = value_be - capital_be
pnl_to_be = capital_be - value_be
pnl_pct_be = (value_be / capital_be - 1) * 100
break_even_a = (capital_be - effective_b) / qty_a

sec("◎", "Résultats Break-Even LP")

be_cards = [
    ("Valeur actuelle", f"{value_be:.2f} $", "#22c55e" if pnl_be >= 0 else "#ef4444"),
    ("P&L", f"{pnl_be:.2f} $ ({pnl_pct_be:.2f}%)", "#22c55e" if pnl_be >= 0 else "#ef4444"),
    ("P&L restante pour BE", f"{pnl_to_be:.2f} $", "#22c55e" if pnl_be >= 0 else "#ef4444"),
    ("Break-even Token A", f"{break_even_a:.2f} $", "var(--accent)"),
]
if pair_type == "Double Volatile":
    break_even_b = (capital_be - (qty_a * price_a) - fees_be) / qty_b
    be_cards.append(("Break-even Token B", f"{break_even_b:.2f} $", "var(--accent)"))

be_cols = st.columns(len(be_cards))
for i, (lbl, val, col_color) in enumerate(be_cards):
    with be_cols[i]:
        card(lbl, val, color=col_color)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== ZERO SWAP REBALANCE ==========
# ==================================================================================
sec("⟳", "Zero Swap Rebalance")

t1, t2 = st.columns(2)
with t1: tokenA_zs = st.text_input("Token A", "Exemple WETH")
with t2: tokenB_zs = st.text_input("Token B", "Exemple USDC")

col1, col2, col3, col4 = st.columns(4)
with col1: price_tokenA = st.number_input(f"Prix {tokenA_zs} ($)", value=1850.0, step=1.0)
with col2: price_tokenB = st.number_input(f"Prix {tokenB_zs} ($)", value=1.0, step=0.01)
with col3: P_low_zs = st.number_input("Plow initial", value=1800.0, step=1.0)
with col4: P_high_zs = st.number_input("Phigh initial", value=2100.0, step=1.0)

if price_tokenB == 0:
    st.error("Le prix du token B ne peut pas être 0.")
    st.stop()

P_current_zs = price_tokenA / price_tokenB
if not (P_low_zs < P_current_zs < P_high_zs):
    st.error("Le prix actuel doit être strictement à l'intérieur du range initial.")
    st.stop()

sqrtP_zs = math.sqrt(P_current_zs)
sqrtPl_zs = math.sqrt(P_low_zs)
sqrtPh_zs = math.sqrt(P_high_zs)
ratio_zs = (sqrtPh_zs - sqrtP_zs) / (sqrtP_zs * sqrtPh_zs * (sqrtP_zs - sqrtPl_zs))

sec("⟳", "Zero Swap Bidirectionnel")
col_low, col_high, col_dir = st.columns(3)
with col_low: new_P_low = st.number_input("New Plow (dump)", value=P_low_zs * 0.9, step=1.0)
with col_high: new_P_high = st.number_input("New Phigh (pump)", value=P_high_zs * 1.1, step=1.0)
with col_dir: direction_select = st.selectbox("Mode de recalcul", options=["Auto", "Dump", "Pump"])

rebalance_pct_zs = st.selectbox("Rebalance partiel (%)", options=[25, 50, 75, 100], index=3) / 100

old_P_low_zs = P_low_zs
old_P_high_zs = P_high_zs

mode = None
if direction_select == "Dump": mode = "bear"
elif direction_select == "Pump": mode = "bull"
else:
    dist_low = abs(P_current_zs - new_P_low)
    dist_high = abs(new_P_high - P_current_zs)
    mode = "bear" if dist_low > dist_high else "bull" if dist_high > dist_low else None

if mode == "bear":
    if new_P_low >= P_current_zs:
        st.error("La nouvelle borne basse doit être inférieure au prix actuel.")
        st.stop()
    sqrtNewPl_zs = math.sqrt(new_P_low)
    denominator = 1 - ratio_zs * sqrtP_zs * (sqrtP_zs - sqrtNewPl_zs)
    if denominator <= 0:
        st.error("Configuration impossible : borne haute tend vers l'infini.")
        st.stop()
    new_P_high = (sqrtP_zs / denominator) ** 2
    direction_label = "🔻 Mode actif : Dump"
elif mode == "bull":
    if new_P_high <= P_current_zs:
        st.error("La nouvelle borne haute doit être supérieure au prix actuel.")
        st.stop()
    sqrtNewPh_zs = math.sqrt(new_P_high)
    numerator = (1 - (sqrtP_zs / sqrtNewPh_zs))
    sqrtNewPl_zs = sqrtP_zs - (numerator / (ratio_zs * sqrtP_zs))
    if sqrtNewPl_zs <= 0:
        st.error("Configuration impossible : borne basse négative.")
        st.stop()
    new_P_low = sqrtNewPl_zs ** 2
    direction_label = "🔺 Mode actif : Pump"
else:
    direction_label = "— Ajuste une borne pour activer le recalcul —"

adj_P_low = old_P_low_zs + (new_P_low - old_P_low_zs) * rebalance_pct_zs
adj_P_high = old_P_high_zs + (new_P_high - old_P_high_zs) * rebalance_pct_zs

sqrt_adj_low = math.sqrt(adj_P_low)
sqrt_adj_high = math.sqrt(adj_P_high)
ratio_adj_zs = (sqrt_adj_high - sqrtP_zs) / (sqrtP_zs * sqrt_adj_high * (sqrtP_zs - sqrt_adj_low))
implicit_cost = abs(ratio_adj_zs - ratio_zs) / ratio_zs

sec("◎", "Résultats - Rebalance / Élargissement")
card("Direction active", direction_label, wide=True)

r1, r2, r3, r4 = st.columns(4)
with r1: card("Ratio Zero Swap", f"{ratio_zs:.8f}")
with r2: card("Nouvelle borne basse", f"{adj_P_low:.2f}")
with r3: card("Nouvelle borne haute", f"{adj_P_high:.2f}")
with r4: card("Coût implicite", f"{implicit_cost*100:.2f}%", color="#f59e0b")

interp_map = {
    0.25: "🟢 Ajustement léger : conserve majoritairement la position initiale (faible impact).",
    0.50: "🟡 Ajustement équilibré : compromis entre conservation et adaptation.",
    0.75: "🟠 Ajustement agressif : forte adaptation, coût implicite plus élevé.",
    1.0:  "🔴 Rebalance complet (100%) : Zero Swap full, aucun coût implicite."
}
card("Interprétation", interp_map.get(rebalance_pct_zs, ""), wide=True)

sec("◎", "Resserrement du range")
tighten_percent = st.number_input("Tighten (%)", value=5.0, step=0.5)

if tighten_percent > 0:
    new_tight_plow = P_current_zs * (1 - tighten_percent/100)
    sqrtP_reb = math.sqrt(P_current_zs)
    sqrtPl_reb = math.sqrt(new_tight_plow)
    sqrtPh_reb = math.sqrt(adj_P_high)
    ratio_reb = (sqrtPh_reb - sqrtP_reb) / (sqrtP_reb * sqrtPh_reb * (sqrtP_reb - sqrtPl_reb))
    denom_tight = 1 - ratio_reb * sqrtP_reb * (sqrtP_reb - sqrtPl_reb)
    if denom_tight > 0:
        new_tight_phigh = (sqrtP_reb / denom_tight) ** 2
        rt1, rt2 = st.columns(2)
        with rt1: card("Tight Plow", f"{new_tight_plow:.2f}")
        with rt2: card("Tight Phigh", f"{new_tight_phigh:.2f}")

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== LP REFILL BACKTEST ==========
# ==================================================================================
sec("⊕", "LP Refill BACKTEST")

c1, c2, c3 = st.columns(3)
with c1: tokenA_price_rf = st.number_input("Prix Token A ($)", value=1900.0)
with c2: tokenB_price_rf = st.number_input("Prix Token B ($)", value=1.0)
with c3: refill_amount = st.number_input("Montant à ajouter ($)", value=1000.0)

q1, q2 = st.columns(2)
with q1: tokenA_lp_rf = st.number_input("Quantité Token A dans la LP", value=4.0)
with q2: tokenB_lp_rf = st.number_input("Quantité Token B dans la LP", value=3000.0)

r1, r2 = st.columns(2)
with r1: P_low_rf = st.number_input("Borne basse", value=1700.0)
with r2: P_high_rf = st.number_input("Borne haute", value=2100.0)

lp_value_rf = tokenA_lp_rf * tokenA_price_rf + tokenB_lp_rf * tokenB_price_rf
ratio_A_rf = (tokenA_lp_rf * tokenA_price_rf) / lp_value_rf
ratio_B_rf = (tokenB_lp_rf * tokenB_price_rf) / lp_value_rf

zone_bottom = P_low_rf + (P_high_rf - P_low_rf) * 0.15
if tokenA_price_rf < P_low_rf:
    message_rf = "🔴 Prix sous le range : risque directionnel élevé"
elif tokenA_price_rf <= zone_bottom:
    message_rf = "🟢 Bon moment : prix proche du bas de range"
elif tokenA_price_rf < P_high_rf:
    message_rf = "🟡 Prix encore dans le range mais pas optimal"
else:
    message_rf = "🔴 Prix au-dessus du range"

price_position_rf = max(0, min(1, (tokenA_price_rf - P_low_rf)/(P_high_rf - P_low_rf)))
target_ratio_A_rf = 1 - price_position_rf
target_ratio_B_rf = price_position_rf

tokenA_value_added = refill_amount * target_ratio_A_rf
tokenB_value_added = refill_amount * target_ratio_B_rf
tokenA_added = tokenA_value_added / tokenA_price_rf
tokenB_added = tokenB_value_added / tokenB_price_rf
new_tokenA = tokenA_lp_rf + tokenA_added
new_tokenB = tokenB_lp_rf + tokenB_added
new_value_rf = new_tokenA * tokenA_price_rf + new_tokenB * tokenB_price_rf
new_ratio_A_rf = (new_tokenA * tokenA_price_rf) / new_value_rf
new_ratio_B_rf = (new_tokenB * tokenB_price_rf) / new_value_rf

sec("◎", "Analyse")
card("État du marché", message_rf, wide=True)

sec("◎", "Position actuelle")
r1_rf, r2_rf, r3_rf = st.columns(3)
with r1_rf: card("Valeur LP", f"${lp_value_rf:,.2f}")
with r2_rf: card("Ratio Token A", f"{ratio_A_rf*100:.2f}%")
with r3_rf: card("Ratio Token B", f"{ratio_B_rf*100:.2f}%")

sec("◎", "Projection après Refill")
rr1, rr2, rr3 = st.columns(3)
with rr1: card("Token A ajouté", f"{tokenA_added:.4f}")
with rr2: card("Token B ajouté", f"{tokenB_added:.2f}")
with rr3: card("Valeur LP future", f"${new_value_rf:,.2f}", color="#22c55e")

st.markdown(f"""
<div class="m-card-wide">
    <div class="m-label">Nouveau ratio LP</div>
    <div class="m-value-sm" style="margin-top:6px;">
        Token A : {new_ratio_A_rf*100:.2f}%  ·  Token B : {new_ratio_B_rf*100:.2f}%
    </div>
</div>""", unsafe_allow_html=True)

with st.expander("Résumé stratégique : Gestion et timing de l'ajout de liquidité (LP Refill)"):
    st.markdown("""
    <div style="font-family:var(--font-mono);font-size:12px;color:#8899aa;line-height:1.7;">
    <p>Cet outil permet d'évaluer si un ajout de liquidité dans une position LP est stratégique ou risqué.
    Il analyse la position actuelle, la proximité avec le bas de range et simule l'impact d'un refill
    sur l'exposition et le ratio de la position.</p>

    <p><b style="color:#f0f4f8;">Objectif de l'outil</b><br>
    L'ajout de liquidité ne doit pas être une réaction émotionnelle à une baisse du prix.
    Cet outil aide à déterminer si le prix est dans une zone stratégique pour renforcer une LP
    sans augmenter excessivement le risque directionnel.</p>

    <p><b style="color:#f0f4f8;">Mauvais moment pour ajouter de la liquidité</b><br>
    Ajouter après une cassure nette du bas de range peut transformer une position LP neutre
    en position directionnelle fortement exposée à la baisse.<br>
    Situations à éviter :<br>
    · Prix sous la range active<br>
    · Forte accélération baissière<br>
    · Absence de plan de capital maximum<br>
    · Moyennage agressif sans paliers</p>

    <p><b style="color:#f0f4f8;">Meilleur moment pour un refill</b><br>
    Le moment idéal est lorsque le prix reste encore dans le range mais se rapproche de la borne basse.<br>
    Conditions favorables :<br>
    · Prix proche du bas de range<br>
    · Baisse en ralentissement<br>
    · LP toujours active dans la fourchette<br>
    · Impermanent loss encore non réalisée</p>

    <p><b style="color:#f0f4f8;">Stratégie d'ajout progressif</b><br>
    Les ajouts doivent être planifiés sous forme de paliers afin d'éviter un surdimensionnement.<br>
    Exemple : Position initiale → Palier 1 (bas de range) → Palier 2 → Palier 3 (dernier).</p>

    <p><b style="color:#f0f4f8;">Principe clé</b><br>
    La discipline de capital est plus importante que le timing parfait.<br>
    Ajouter trop tôt expose à la tendance. Ajouter trop tard augmente le risque directionnel.<br>
    Un refill doit toujours être planifié, limité et intégré dans une stratégie globale de gestion du risque.</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== LP HEALTH SCORE ==========
# ==================================================================================
sec("◉", "LP Health Score")

c1, c2 = st.columns(2)
with c1: tokenA_price_h = st.number_input("Prix Token A ($) ", value=1900.0, key="h_a_price")
with c2: tokenB_price_h = st.number_input("Prix Token B ($) ", value=1.0, key="h_b_price")

q1, q2 = st.columns(2)
with q1: tokenA_lp_h = st.number_input("Quantité Token A LP ", value=4.0, key="h_a_lp")
with q2: tokenB_lp_h = st.number_input("Quantité Token B LP ", value=3000.0, key="h_b_lp")

r1, r2 = st.columns(2)
with r1: P_low_h = st.number_input("Borne basse ", value=1700.0, key="h_low")
with r2: P_high_h = st.number_input("Borne haute ", value=2100.0, key="h_high")

atr_h = st.number_input("ATR ($)", value=80.0)

lp_value_h = tokenA_lp_h * tokenA_price_h + tokenB_lp_h * tokenB_price_h
ratio_A_h = (tokenA_lp_h * tokenA_price_h) / lp_value_h
ratio_B_h = (tokenB_lp_h * tokenB_price_h) / lp_value_h
range_width_h = P_high_h - P_low_h
price_position_h = max(0, min(1, (tokenA_price_h - P_low_h) / range_width_h))

position_score = (1 - price_position_h) * 100
target_ratio_A_h = 1 - price_position_h
imbalance = abs(ratio_A_h - target_ratio_A_h)
balance_score = max(0, 100 - imbalance * 200)

if price_position_h < 0.3: exposure_penalty = ratio_B_h
elif price_position_h > 0.7: exposure_penalty = ratio_A_h
else: exposure_penalty = abs(ratio_A_h - 0.5)
exposure_score = max(0, 100 - exposure_penalty * 100)

atr_ratio_h = atr_h / range_width_h
volatility_score = max(0, 100 - atr_ratio_h * 150)
health_score = position_score*0.3 + balance_score*0.25 + exposure_score*0.2 + volatility_score*0.25

rebalance_needed = imbalance > 0.2 or price_position_h < 0.1 or price_position_h > 0.9 or atr_ratio_h > 0.25
rebalance_reason = "Déséquilibre des tokens" if imbalance > 0.2 else "Prix proche des bornes" if (price_position_h < 0.1 or price_position_h > 0.9) else "Volatilité élevée (ATR)"

if health_score > 75: status_h = "🟢 Position optimale"
elif health_score > 60: status_h = "🟡 Position correcte"
elif health_score > 40: status_h = "🟠 Position à surveiller"
else: status_h = "🔴 Position risquée"

score_color = "#22c55e" if health_score > 75 else "#f59e0b" if health_score > 60 else "#ef4444"

s1, s2, s3, s4 = st.columns(4)
with s1: card("Health Score", f"{health_score:.1f} / 100", color=score_color)
with s2: card("Position", f"{position_score:.0f}")
with s3: card("Balance", f"{balance_score:.0f}")
with s4: card("Volatilité", f"{volatility_score:.0f}", color="#0ea5e9")

card("Statut", status_h, wide=True, color=score_color)

if rebalance_needed:
    st.markdown(f"""
    <div class="m-card-alert">
        <div class="m-label">⚠ Rebalance recommandé</div>
        <div class="m-value-sm" style="color:#ef4444;">{rebalance_reason}</div>
    </div>""", unsafe_allow_html=True)
else:
    card("Rebalance", "Aucune action nécessaire", wide=True, color="#22c55e")

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== AUTO RANGE ==========
# ==================================================================================
sec("⊡", "Auto Range")

col1_ar, col2_ar = st.columns(2)
with col1_ar: atr_auto = st.number_input("ATR pour optimisation ($)", value=80.0, key="auto_atr")
with col2_ar: multiplier_ar = st.slider("Facteur de range", 1.0, 4.0, 2.0, 0.5)

old_range_width_ar = P_high_h - P_low_h
old_position_ar = max(0, min(1, (tokenA_price_h - P_low_h) / old_range_width_ar))
new_range_width_ar = atr_auto * multiplier_ar * 2
optimal_low = max(0, tokenA_price_h - (old_position_ar * new_range_width_ar))
optimal_high = optimal_low + new_range_width_ar

r1, r2, r3 = st.columns(3)
with r1: card("Range bas", f"{optimal_low:.0f}")
with r2: card("Range haut", f"{optimal_high:.0f}")
with r3: card("Largeur %", f"{(new_range_width_ar/tokenA_price_h)*100:.1f}%", color="#0ea5e9")

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== PRIX MOYEN CLM ==========
# ==================================================================================
sec("◈", "Prix moyen CLM")

c1, c2, c3 = st.columns(3)
with c1: P0_clm = st.number_input("Prix actuel", value=1900.0, key="clm_P0")
with c2: P_entry_clm = st.number_input("Prix d'entrée", value=1900.0, key="clm_entry")
with c3: capital_clm = st.number_input("Capital ($)", value=1000.0, key="clm_capital")

r1, r2 = st.columns(2)
with r1: P_low_clm = st.number_input("Borne basse", value=1700.0, key="clm_low")
with r2: P_high_clm = st.number_input("Borne haute", value=2500.0, key="clm_high")

valid_clm = P_low_clm < P0_clm < P_high_clm
if not valid_clm:
    st.error("⚠ Il faut : P_low < Prix actuel < P_high")
else:
    sqrtP_clm = math.sqrt(P0_clm)
    sqrtPlow_clm = math.sqrt(P_low_clm)
    sqrtPhigh_clm = math.sqrt(P_high_clm)
    denom_clm = P0_clm*(1/sqrtP_clm - 1/sqrtPhigh_clm) + (sqrtP_clm - sqrtPlow_clm)
    L_clm = capital_clm / denom_clm if denom_clm != 0 else 0
    x0_clm = L_clm * (1/sqrtP_clm - 1/sqrtPhigh_clm)
    y0_clm = L_clm * (sqrtP_clm - sqrtPlow_clm)
    token_final_clm = L_clm * (1/sqrtPlow_clm - 1/sqrtPhigh_clm)
    P_avg_clm = capital_clm / token_final_clm if token_final_clm > 0 else 0

    sec("◎", "Résultats")
    r1, r2, r3 = st.columns(3)
    with r1: card("Token initial", f"{x0_clm:.4f}")
    with r2: card("Token final", f"{token_final_clm:.4f}")
    with r3: card("Prix moyen", f"${P_avg_clm:,.2f}", color="#0ea5e9")

    sec("◎", "Accumulation dynamique")
    sim_price_clm = st.slider("Simulation du prix", min_value=int(P_low_clm), max_value=int(P0_clm), value=int(P0_clm), key="clm_slider")
    sqrtSim_clm = math.sqrt(sim_price_clm)
    token_sim_clm = L_clm * (1/sqrtSim_clm - 1/sqrtPhigh_clm)
    accumulation_clm = token_sim_clm - x0_clm

    card("Accumulation", f"+{accumulation_clm:.4f} token  ·  Total : {token_sim_clm:.4f}", wide=True)

    sec("◎", "Optimiseur de range")
    target_price_clm = st.number_input("Prix moyen cible", value=1500.0, key="clm_target")

    best_low_clm = None
    best_diff_clm = 1e9
    for test_low in range(int(P0_clm*0.3), int(P0_clm), max(1, int(P0_clm*0.02))):
        sqrtPl_t = math.sqrt(test_low)
        denom_t = P0_clm*(1/sqrtP_clm - 1/sqrtPhigh_clm) + (sqrtP_clm - sqrtPl_t)
        if denom_t <= 0: continue
        L_t = capital_clm / denom_t
        token_t = L_t * (1/sqrtPl_t - 1/sqrtPhigh_clm)
        if token_t <= 0: continue
        P_t = capital_clm / token_t
        diff_t = abs(P_t - target_price_clm)
        if diff_t < best_diff_clm:
            best_diff_clm = diff_t
            best_low_clm = test_low

    card("Range optimisée", f"P_low optimal : {best_low_clm}  ·  P_high : {P_high_clm}", wide=True)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== FEES / TVL / VOLUME ==========
# ==================================================================================
sec("◉", "Analyse LP : Fees / TVL / Volume 24h")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**POOL METRICS**")
    tvl = st.number_input("TVL ($)", value=2_000_000.0, step=1000.0, format="%.2f")
    fees_24h = st.number_input("Fees 24h ($)", value=10_000.0, step=10.0, format="%.2f")
    volume_24h = st.number_input("Volume 24h ($)", value=5_000_000.0, step=10000.0, format="%.2f")
with col2:
    st.markdown("**POSITION**")
    capital_lp = st.number_input("Capital LP ($)", value=10_000.0, step=10.0, format="%.2f")
    range_width_fees = st.number_input("Largeur de range (%)", value=5.0, step=0.1, format="%.2f")

fee_yield = (fees_24h/tvl)*100 if tvl > 0 else 0
volume_tvl_ratio = (volume_24h/tvl)*100 if tvl > 0 else 0
fee_capture = (fees_24h/volume_24h)*100 if volume_24h > 0 else 0
share_fees = capital_lp / tvl if tvl > 0 else 0
concentration_score = 1/range_width_fees if range_width_fees > 0 else 0
lef = volume_tvl_ratio * concentration_score
adjusted_fee_yield = fee_yield * concentration_score
lp_fees_calc = share_fees * fees_24h * concentration_score
score_fees = (fee_yield*0.5) + (fee_capture*0.3) + (volume_tvl_ratio*0.2)

sec("◎", "Analyse de performance de la POOL")

fees_data = [
    ("Fee Yield (24h)", f"{fee_yield:.4f} %", "var(--accent)"),
    ("Volume / TVL", f"{volume_tvl_ratio:.2f} %", "#22c55e"),
    ("Fee Capture Rate", f"{fee_capture:.4f} %", "#f59e0b"),
    ("Ta part LP", f"{share_fees*100:.4f} %", "var(--accent)"),
    ("Fees estimés (24h)", f"{lp_fees_calc:.2f} $", "#22c55e"),
    ("LP Score", f"{score_fees:.2f}", "var(--accent)"),
    ("Concentration Score", f"{concentration_score:.4f}", "#f59e0b"),
    ("Liquidity Efficiency Factor", f"{lef:.4f}", "var(--accent)"),
    ("Fee Yield Ajusté (range)", f"{adjusted_fee_yield:.4f} %", "#22c55e"),
]

fees_cols = st.columns(len(fees_data))
for i, (lbl, val, col_color) in enumerate(fees_data):
    with fees_cols[i]:
        card(lbl, val, color=col_color)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== GRID BUILDER ==========
# ==================================================================================
sec("⊞", "Grid Builder : Accumulation / Distribution Engine")

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1: asset_price_g = st.number_input("Prix actuel ($)", value=2300.0, step=1.0)
with col2: capital_g = st.number_input("Capital total ($)", value=1000.0, step=100.0)
with col3: alloc_L0 = st.number_input("L0 - 0% (%)", value=20, min_value=0, max_value=100, step=1)
with col4: alloc_L1 = st.number_input("L1 - (-3%) (%)", value=30, min_value=0, max_value=100, step=1)
with col5: alloc_L2 = st.number_input("L2 - (-6%) (%)", value=30, min_value=0, max_value=100, step=1)
with col6: alloc_L3 = st.number_input("L3 - (-9%) (%)", value=20, min_value=0, max_value=100, step=1)

total_alloc_g = alloc_L0 + alloc_L1 + alloc_L2 + alloc_L3
if total_alloc_g != 100:
    st.warning(f"⚠ La somme des allocations d'achat est de {total_alloc_g}% — elle doit être égale à 100%")

sec("◎", "Répartition de la vente par palier")
col1, col2, col3 = st.columns(3)
with col1: sell_alloc_S1 = st.number_input("S1 - (+3%) (%)", value=20, min_value=0, max_value=100, step=1)
with col2: sell_alloc_S2 = st.number_input("S2 - (+6%) (%)", value=30, min_value=0, max_value=100, step=1)
with col3: sell_alloc_S3 = st.number_input("S3 - (+9%) (%)", value=50, min_value=0, max_value=100, step=1)

total_sell_alloc_g = sell_alloc_S1 + sell_alloc_S2 + sell_alloc_S3
if total_sell_alloc_g != 100:
    st.warning(f"⚠ La somme des allocations de vente est de {total_sell_alloc_g}% — elle doit être égale à 100%")

buy_levels_def = [
    {"pct": 0.00, "alloc": alloc_L0/100}, {"pct": -0.03, "alloc": alloc_L1/100},
    {"pct": -0.06, "alloc": alloc_L2/100}, {"pct": -0.09, "alloc": alloc_L3/100},
]
sell_levels_def = [
    {"pct": 0.03, "alloc": sell_alloc_S1/100}, {"pct": 0.06, "alloc": sell_alloc_S2/100},
    {"pct": 0.09, "alloc": sell_alloc_S3/100},
]

grid_buy = []
for b in buy_levels_def:
    pl = asset_price_g * (1 + b["pct"])
    ac = capital_g * b["alloc"]
    grid_buy.append({"pct": b["pct"], "price": pl, "capital": ac, "qty": ac/pl if pl > 0 else 0})

total_buy_capital_g = sum(g["capital"] for g in grid_buy)
total_qty_g = sum(g["qty"] for g in grid_buy)
avg_entry_price_g = sum(g["price"]*g["qty"] for g in grid_buy)/total_qty_g if total_qty_g > 0 else 0

pnl_table_g = []
for s in sell_levels_def:
    sp = asset_price_g * (1 + s["pct"])
    qty_sold = total_qty_g * s["alloc"]
    cost = qty_sold * avg_entry_price_g
    sv = qty_sold * sp
    pnl_g = sv - cost
    pnl_table_g.append({"pct": s["pct"], "price": sp, "alloc": s["alloc"],
        "qty_sold": qty_sold, "sell_value": sv, "pnl": pnl_g,
        "pnl_pct": (pnl_g/cost)*100 if cost > 0 else 0})

final_cycle_value_g = sum(p["sell_value"] for p in pnl_table_g)
cycle_profit_g = final_cycle_value_g - total_buy_capital_g
cycle_return_pct_g = (cycle_profit_g/total_buy_capital_g)*100 if total_buy_capital_g > 0 else 0

sec("◎", "Paliers d'achat")
buy_cols = st.columns(len(grid_buy))
for i, g in enumerate(grid_buy):
    pct_label = f"{g['pct']*100:+.0f}%" if g["pct"] != 0 else "L0"
    alloc_pct_g = g["capital"]/capital_g*100 if capital_g > 0 else 0
    with buy_cols[i]:
        st.markdown(f"""
        <div class="m-card">
            <div class="m-label">BUY {pct_label}</div>
            <div class="m-value-sm">{g['price']:.2f} $</div>
            <div style="margin-top:8px; font-size:11px; color:var(--text-mid);">
                Capital : <span style="color:var(--accent);">{g['capital']:.2f}$</span>
                <span style="color:var(--text-lo);"> ({alloc_pct_g:.0f}%)</span><br>
                Qté : <span style="color:var(--accent);">{g['qty']:.6f}</span>
            </div>
        </div>""", unsafe_allow_html=True)

sec("◎", "Paliers de vente")
sell_cols = st.columns(len(pnl_table_g))
for i, p in enumerate(pnl_table_g):
    with sell_cols[i]:
        st.markdown(f"""
        <div class="m-card">
            <div class="m-label">SELL +{p['pct']*100:.0f}%</div>
            <div class="m-value-sm" style="color:#f59e0b;">{p['price']:.2f} $</div>
            <div style="margin-top:8px; font-size:11px; color:var(--text-mid);">
                Vendu : <span style="color:#f59e0b;">{p['alloc']*100:.0f}%</span>
                · Qté : <span style="color:#f59e0b;">{p['qty_sold']:.6f}</span><br>
                Valeur : <span style="color:#f59e0b;">{p['sell_value']:.2f}$</span>
                · PnL : <span style="color:#22c55e;">{p['pnl']:.2f}$ ({p['pnl_pct']:.2f}%)</span>
            </div>
        </div>""", unsafe_allow_html=True)

sec("◎", "Capital & Performance")
cp1, cp2, cp3, cp4, cp5 = st.columns(5)
with cp1: card("Capital engagé", f"{total_buy_capital_g:.2f} $")
with cp2: card("Quantité totale", f"{total_qty_g:.6f}", color="#0ea5e9")
with cp3: card("Prix moyen d'entrée", f"{avg_entry_price_g:.2f} $", color="#0ea5e9")
with cp4: card("Valeur cycle complet", f"{final_cycle_value_g:.2f} $")
with cp5: card("ROI cycle", f"{cycle_return_pct_g:.2f} %", color="#f59e0b")

efficiency_g = cycle_return_pct_g / 9 if cycle_return_pct_g > 0 else 0
card("Efficiency Score", f"{efficiency_g:.2f}", color="var(--accent)")

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== GUIDE ==========
# ==================================================================================
sec("◎", "Guide")

guide_html = """
<div class="guide-wrap">

<div class="toc-box">
    <h4>SOMMAIRE</h4>
    <ul>
        <li><a href="#cest-quoi-fournir-de-la-liquidite">C'est quoi fournir de la liquidité ?</a></li>
        <li><a href="#concepts-fondamentaux">Concepts fondamentaux</a></li>
        <li><a href="#strategies-possibles">Stratégies possibles</a></li>
        <li><a href="#choisir-un-range">Choisir un range</a></li>
        <li><a href="#exemple-simple-weth-usdc">Exemple simple WETH/USDC</a></li>
        <li><a href="#erreurs-de-debutant">Erreurs de débutant</a></li>
        <li><a href="#rebalancer-la-position">Rebalancer la position</a></li>
        <li><a href="#courbe-impermanent-loss">Comprendre la courbe d'Impermanent Loss</a></li>
        <li><a href="#strategie-lp-rentable">Quand une stratégie LP est rentable ?</a></li>
        <li><a href="#astuces-et-autonomie">Astuces et autonomie des choix</a></li>
        <li><a href="#conclusion">Conclusion</a></li>
    </ul>
</div>

<div class="guide-section" id="cest-quoi-fournir-de-la-liquidite">
    <h3>C'est quoi fournir de la liquidité ?</h3>
    <p>Quand tu fournis de la liquidité à une pool (ex : WETH/USDC), tu apportes <b>deux tokens en même temps</b>. En échange, tu deviens <b>market maker</b> et touches des <b>frais de trading</b>.<br><br>
    Dans un AMM concentré, tu choisis <b>un range</b>. Si le prix sort du range → tu deviens <b>full Token A</b> ou <b>full Token B</b>. Ta position s'ajuste automatiquement : <b>quand le prix baisse, tu accumules le token le plus volatile</b> ; à l'inverse, <b>quand le prix monte, tu revends progressivement ce token volatile.</b></p>
</div>

<div class="guide-section" id="concepts-fondamentaux">
    <h3>Concepts fondamentaux</h3>
    <p>· <b>Ratio</b> : proportion entre Token A (volatile) et Token B (stable ou moins volatile). Exemple : 50/50 = neutre, 20/80 = défensif, 95/5 = agressif.<br>
    · <b>Range</b> : zone de prix où ton capital est actif. Range serré = plus de fees mais plus de rebalances et IL possible.<br>
    · <b>Impermanent Loss (IL)</b> : perte que tu aurais évitée si tu avais conservé tes tokens. Plus le prix s'éloigne, plus l'IL augmente.</p>
</div>

<div class="guide-section" id="strategies-possibles">
    <h3>Stratégies possibles</h3>
    <p>· <b>Neutre (50/50)</b> : marché incertain, stable et simple, risque IL si gros mouvement<br>
    · <b>Coup de pouce (20/80)</b> : marché calme, protège du token volatil, défensif<br>
    · <b>Mini-doux (10/90)</b> : anticipation de tendance, minimise IL, très défensif<br>
    · <b>Side-line up (100/0)</b> : bas de marché, accumulation token volatile, agressif<br>
    · <b>Side-line down (0/100)</b> : marché haussier, prise de profit naturel, agressif vers la vente</p>
</div>

<div class="guide-section" id="choisir-un-range">
    <h3>Choisir un range</h3>
    <p>Le choix dépend de ton objectif, de la volatilité et du marché : haussier → profits A→B, baissier → accumulation B→A, latéral → neutre ou coup de pouce.<br><br>
    Pour affiner ton range, utilise l'indicateur <b>ATR (Average True Range)</b> disponible sur TradingView dans la catégorie <em>Technical</em>.<br>
    L'ATR représente de manière simplifiée <b>l'écart-type du prix d'un actif exprimé en dollars</b> : il mesure l'amplitude moyenne des mouvements de prix sur une période donnée.<br><br>
    Sur l'outil, règle l'ATR en <b>daily</b> avec une période <b>ATR 14</b>, puis applique un <b>multiplicateur</b> afin de définir la largeur de ton range autour du prix actuel.<br>
    Par exemple : <b>ATR × 3</b> correspond généralement à une tenue de range d'environ <b>1 semaine à 10 jours</b>, selon la volatilité du marché.<br>
    Une fois le range défini, vérifie l'ATR affiché en <b>weekly</b> et compare-le à ton choix initial en calculant : <b>borne haute − borne basse</b>.<br>
    Ajuste ensuite ton range en confrontant ces valeurs avec les données de l'ATR14 en <b>WEEKLY</b> ainsi que <b>volatilité sur 7 jours et 30 jours</b>.</p>
</div>

<div class="guide-section" id="exemple-simple-weth-usdc">
    <h3>Exemple simple WETH/USDC</h3>
    <p>· Capital = 1000 USD, Prix ETH = 3000, Stratégie = 50/50, Range ±20%<br>
    · Répartition : 500 USD ETH, 500 USD USDC<br>
    · Range bas ≈ 2700, Range haut ≈ 3300<br>
    · Si prix = 3300 → plus riche en USDC, fees générés<br>
    · Si prix = 2700 → plus d'ETH, fees générés</p>
</div>

<div class="guide-section" id="erreurs-de-debutant">
    <h3>Erreurs de débutant</h3>
    <p>· Range trop serré : rebalances fréquents, coûts d'opportunité, IL amplifiée<br>
    · Oublier que l'IL existe : fees ne compensent pas toujours IL<br>
    · Choisir un range sans regarder la volatilité : volatilité 7j et 30j clé, pas de stratégie "set and forget"</p>
</div>

<div class="guide-section" id="rebalancer-la-position">
    <h3>Rebalancer la position</h3>
    <p>Quand le prix sort du range, tu deviens full A ou full B, tu ne gagnes plus de fees. Ta LP = simple "bag" de tokens, il faut repositionner la liquidité.<br>
    L'app calcule combien de fois le prix est sorti dans le passé et en simulation future, et ajuste automatiquement le range.</p>
    <p><b>Rappel sur l'automation et les rebalances :</b><br>
    · Les triggers doivent toujours se baser sur le <b>RATIO</b>, jamais sur % ou $.<br>
    · Lors de l'utilisation des <b>futures ranges</b> (option avancée), réglez-les correctement en %.<br>
    · Si votre range actuel est très large ou trop court comparé aux futures ranges, vous aurez un décalage de stratégie.<br>
    · <b>Conseil pratique :</b> Partagez uniquement des captures claires de l'édition de l'automation et de la stratégie.<br>
    · <b>Attention sur vos décisions :</b> Achetez le token volatile seulement si prêt à vendre pour limiter la perte.</p>
</div>

<div class="guide-section" id="courbe-impermanent-loss">
    <h3>Comprendre la courbe d'Impermanent Loss</h3>
    <p>Le graphe montre : IL(%) en fonction du prix actuel, ligne pour prix de dépôt, ligne pour prix actuel, range bas/haut.<br>
    Interprétation : minimum de la courbe = prix de dépôt ; plus on s'éloigne, plus IL augmente ; IL=0 seulement si prix reste identique.</p>
</div>

<div class="guide-section" id="strategie-lp-rentable">
    <h3>Quand une stratégie LP est rentable ?</h3>
    <p>· Frais gagnés > impermanent loss<br>
    · Prix ne sort pas trop vite du range<br>
    · Stratégie cohérente avec l'objectif (DCA, prise de profit, accumulation…)</p>
</div>

<div class="guide-section" id="astuces-et-autonomie">
    <h3>Astuces et autonomie des choix</h3>
    <p>· Commencer avec un faible capital et un range large<br>
    · Utiliser des stratégies asymétriques si marché directionnel<br>
    · Vérifier la volatilité 7j et 30j<br>
    · Ne pas déposer tout le capital d'un coup<br>
    · Surveiller la courbe IL après dépôt<br>
    · Utiliser le dex pour déposer la liquidité (expert)</p>
</div>

<div class="guide-section" id="conclusion">
    <h3>Conclusion</h3>
    <p>Ce guide t'a donné les concepts fondamentaux, des explications simples des stratégies, comment interpréter ratios, range, volatilité, lire l'IL et éviter les erreurs classiques.<br>
    Avec l'application, tu as un backtest complet des LP, parfait pour apprendre et gérer des pools concentrés avec une vision globale de la mécanique.</p>
</div>

</div>
"""
st.markdown(guide_html, unsafe_allow_html=True)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== VIDEO IL ==========
# ==================================================================================
sec("▶", "Calculatrice Impermanent Loss")
col_v, = st.columns(1)
with col_v:
    st.video("https://www.youtube.com/watch?v=uQPeyXsQNrs")

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ==================================================================================
# ========== ATELIER IL ==========
# ==================================================================================
sec("◈", "Atelier Impermanent Loss")
components.iframe(src="https://www.desmos.com/calculator/i7mnoyyqdb?lang=fr", width=None, height=700, scrolling=True)

st.markdown("""
<div style="height:40px;"></div>
<div style="text-align:center; font-family:var(--font-mono); font-size:11px; color:var(--text-lo); letter-spacing:1px;">
    ◈ LP BACKTEST ENGINE v2.0 · PIGEONSFOREVER · DYOR · NOT FINANCIAL ADVICE
</div>
<div style="height:20px;"></div>
""", unsafe_allow_html=True)
