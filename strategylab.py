import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="LP Strategy Lab V2",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

pio.templates.default = "plotly_dark"

# ===================== GLOBAL THEME =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-main:    #080c10;
    --bg-panel:   #0d1318;
    --bg-card:    #111820;
    --accent:     #00d4aa;
    --accent-dim: rgba(0,212,170,0.10);
    --accent-mid: rgba(0,212,170,0.30);
    --accent-2:   #0ea5e9;
    --accent-3:   #f59e0b;
    --accent-red: #ef4444;
    --accent-green:#22c55e;
    --border:     rgba(0,212,170,0.18);
    --border-soft:rgba(255,255,255,0.06);
    --text-hi:    #f0f4f8;
    --text-mid:   #8899aa;
    --text-lo:    #445566;
    --font-mono:  'JetBrains Mono','Courier New',monospace;
    --font-ui:    'Inter',sans-serif;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
.block-container { padding-top: 72px !important; padding-bottom: 40px !important; }

/* ── BASE ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-main) !important;
    color: var(--text-hi);
    font-family: var(--font-ui);
}
[data-testid="stHeader"] { background: transparent !important; display:none !important; }

/* ── NAV BAR ── */
.nav-bar {
    position: fixed;
    top: 0; left: 0;
    width: 100%;
    height: 58px;
    z-index: 99999;
    background: rgba(6,10,14,0.97);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 28px;
    box-sizing: border-box;
    pointer-events: all;
}
.nav-brand { display:flex; align-items:center; gap:10px; }
.nav-glyph {
    width:28px; height:28px;
    border:2px solid var(--accent);
    border-radius:6px;
    display:flex; align-items:center; justify-content:center;
    font-family:var(--font-mono); font-size:14px;
    color:var(--accent); font-weight:700;
}
.nav-title {
    font-family:var(--font-mono); font-size:13px; font-weight:600;
    color:var(--text-hi); letter-spacing:2px; text-transform:uppercase;
}
.nav-subtitle { font-family:var(--font-mono); font-size:10px; color:var(--text-mid); letter-spacing:1px; }
.status-dot {
    width:7px; height:7px; border-radius:50%;
    background:var(--accent); display:inline-block; margin-right:5px;
    animation:pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%,100%{opacity:1;box-shadow:0 0 0 0 rgba(0,212,170,0.4);}
    50%{opacity:.7;box-shadow:0 0 0 4px rgba(0,212,170,0);}
}
.nav-links { display:flex; align-items:center; gap:6px; }
.nav-links a {
    font-family:var(--font-mono); font-size:11px; font-weight:500;
    color:var(--text-mid); text-decoration:none;
    padding:5px 12px; border:1px solid transparent; border-radius:5px;
    transition:all 0.2s; letter-spacing:.5px;
    position:relative; z-index:99999;
}
.nav-links a:hover { color:var(--accent); border-color:var(--border); background:var(--accent-dim); }

/* ── SECTION HEADERS ── */
.sec-head {
    display:flex; align-items:center; gap:10px;
    margin:28px 0 14px 0; padding-bottom:8px;
    border-bottom:1px solid var(--border);
}
.sec-head-icon {
    width:24px; height:24px; background:var(--accent-dim);
    border:1px solid var(--border); border-radius:5px;
    display:flex; align-items:center; justify-content:center;
    font-size:11px; color:var(--accent);
}
.sec-head-label {
    font-family:var(--font-mono); font-size:11px; font-weight:600;
    color:var(--accent); letter-spacing:2px; text-transform:uppercase;
}

/* ── METRIC CARDS ── */
.m-card {
    background:var(--bg-card); border:1px solid var(--border-soft);
    border-radius:10px; padding:16px 18px; margin:8px 0;
    transition:border-color .2s,box-shadow .2s;
    position:relative; overflow:hidden;
}
.m-card::before {
    content:''; position:absolute; top:0;left:0;right:0; height:2px;
    background:linear-gradient(90deg,var(--accent),transparent);
    opacity:0; transition:opacity .2s;
}
.m-card:hover{border-color:var(--border);box-shadow:0 0 18px rgba(0,212,170,.07);}
.m-card:hover::before{opacity:1;}
.m-card-wide {
    background:var(--bg-card); border:1px solid var(--border-soft);
    border-radius:10px; padding:18px 20px; margin:8px 0;
}
.m-card-highlight {
    background:var(--accent-dim); border:1px solid var(--border);
    border-radius:10px; padding:18px 20px; margin:8px 0;
}
.m-label {
    font-family:var(--font-mono); font-size:10px; color:var(--text-mid);
    letter-spacing:1.5px; text-transform:uppercase; margin-bottom:8px;
}
.m-value { font-family:var(--font-mono); font-size:20px; font-weight:600; color:var(--accent); line-height:1.1; }
.m-value-sm { font-family:var(--font-mono); font-size:14px; font-weight:500; color:var(--accent); line-height:1.3; }

/* ── KPI CARD (wide with badge) ── */
.kpi-row { display:flex; gap:10px; flex-wrap:wrap; margin:10px 0; }
.kpi-card {
    flex:1; min-width:120px;
    background:var(--bg-card); border:1px solid var(--border-soft);
    border-radius:10px; padding:14px 16px;
    position:relative; overflow:hidden;
}
.kpi-card::after {
    content:''; position:absolute;
    bottom:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,var(--accent),transparent);
}
.kpi-label { font-family:var(--font-mono); font-size:10px; color:var(--text-mid); letter-spacing:1.5px; text-transform:uppercase; }
.kpi-val { font-family:var(--font-mono); font-size:22px; font-weight:700; color:var(--accent); margin-top:6px; }
.kpi-val-red { color:var(--accent-red); }
.kpi-val-green { color:var(--accent-green); }
.kpi-val-amber { color:var(--accent-3); }
.kpi-val-blue { color:var(--accent-2); }

/* ── TOOLTIP INPUT LABELS ── */
.label-tip {
    display:flex; align-items:center; gap:6px;
    font-size:12px; color:var(--text-mid);
    font-family:var(--font-ui); margin-bottom:3px;
}
.tip-icon {
    width:15px; height:15px;
    background:var(--accent-dim); border:1px solid var(--border);
    border-radius:50%; display:inline-flex; align-items:center; justify-content:center;
    font-size:9px; color:var(--accent); cursor:help; flex-shrink:0;
    position:relative;
}
.tip-icon:hover::after {
    content:attr(data-tip);
    position:absolute; left:20px; top:-4px;
    background:#0d1318; border:1px solid var(--border);
    border-radius:7px; padding:8px 12px;
    font-size:11px; color:var(--text-hi);
    width:220px; z-index:9999; line-height:1.5;
    font-family:var(--font-ui); font-weight:400;
    box-shadow:0 4px 20px rgba(0,0,0,.5);
    white-space:normal;
}

/* ── INPUTS ── */
div[data-baseweb="input"] input,
.stNumberInput input,
.stTextInput input {
    background:var(--bg-panel) !important;
    color:var(--text-hi) !important;
    border:1px solid var(--border-soft) !important;
    border-radius:7px !important;
    font-family:var(--font-mono) !important;
    font-size:13px !important;
}
div[data-baseweb="input"] input:focus,
.stNumberInput input:focus {
    border-color:var(--accent-mid) !important;
    box-shadow:0 0 0 2px var(--accent-dim) !important;
}
.stSelectbox > div > div {
    background:var(--bg-panel) !important;
    border:1px solid var(--border-soft) !important;
    border-radius:7px !important;
    color:var(--text-hi) !important;
    font-family:var(--font-mono) !important;
}
label,.stLabel { font-family:var(--font-ui) !important; font-size:12px !important; color:var(--text-mid) !important; }
.stSlider > div > div > div { background:var(--accent) !important; }
.stCheckbox label { color:var(--text-hi) !important; font-size:13px !important; }

/* ── BUTTONS ── */
.stButton > button {
    background:var(--accent) !important;
    color:#030a07 !important;
    border:none !important;
    border-radius:8px !important;
    font-family:var(--font-mono) !important;
    font-size:12px !important;
    font-weight:700 !important;
    letter-spacing:1px !important;
    padding:10px 20px !important;
    text-transform:uppercase !important;
    transition:all .2s !important;
}
.stButton > button:hover {
    transform:translateY(-1px) !important;
    box-shadow:0 6px 20px rgba(0,212,170,.3) !important;
}

/* ── METRIC NATIVE OVERRIDE ── */
[data-testid="stMetric"] {
    background:var(--bg-card);
    border:1px solid var(--border-soft);
    border-radius:10px;
    padding:14px 16px !important;
}
[data-testid="stMetricLabel"] { font-family:var(--font-mono); font-size:10px !important; color:var(--text-mid) !important; letter-spacing:1.5px; }
[data-testid="stMetricValue"] { font-family:var(--font-mono); font-size:20px !important; color:var(--accent) !important; font-weight:700 !important; }
[data-testid="stMetricDelta"] { font-family:var(--font-mono); font-size:11px !important; }

/* ── DATAFRAME ── */
.stDataFrame { background:var(--bg-card) !important; border-radius:10px; }

/* ── ALERTS ── */
.stAlert { background:var(--bg-panel); border-left:3px solid var(--accent); border-radius:8px; }

/* ── EXPANDER ── */
details { background:var(--bg-panel); border:1px solid var(--border-soft) !important; border-radius:8px !important; padding:4px 12px; }
summary { color:var(--accent); font-family:var(--font-mono); font-size:12px; cursor:pointer; }

/* ── SUGGESTION BOX ── */
.sugg-box {
    background:rgba(14,165,233,.07);
    border:1px solid rgba(14,165,233,.25);
    border-radius:10px;
    padding:18px 22px;
    margin:14px 0;
}
.sugg-title { font-family:var(--font-mono); font-size:11px; color:var(--accent-2); letter-spacing:2px; text-transform:uppercase; margin-bottom:10px; }
.sugg-row { display:flex; gap:8px; margin-bottom:6px; font-size:13px; color:var(--text-hi); }
.sugg-badge {
    display:inline-block; padding:2px 8px;
    border-radius:4px; font-family:var(--font-mono); font-size:10px; font-weight:600;
    letter-spacing:.5px; white-space:nowrap;
}
.badge-bull { background:rgba(34,197,94,.15); color:var(--accent-green); border:1px solid rgba(34,197,94,.3); }
.badge-bear { background:rgba(239,68,68,.15); color:var(--accent-red); border:1px solid rgba(239,68,68,.3); }
.badge-side { background:rgba(14,165,233,.15); color:var(--accent-2); border:1px solid rgba(14,165,233,.3); }
.badge-vol  { background:rgba(245,158,11,.15); color:var(--accent-3); border:1px solid rgba(245,158,11,.3); }

/* ── GUIDE ── */
.guide-section {
    background:var(--bg-card); border:1px solid var(--border-soft);
    border-radius:10px; padding:18px 22px; margin:10px 0;
    transition:border-color .2s;
}
.guide-section:hover { border-color:var(--border); }
.guide-section h3 {
    color:var(--accent) !important; font-family:var(--font-mono) !important;
    font-size:12px !important; font-weight:600 !important;
    margin:0 0 10px 0 !important; letter-spacing:1.5px !important; text-transform:uppercase !important;
}
.guide-section p,.guide-section li { font-size:13px; color:#b0bec5; line-height:1.75; }
.guide-section b { color:var(--text-hi); }

/* ── DIVIDER ── */
.v2-divider { height:1px; background:linear-gradient(90deg,var(--border),transparent); margin:28px 0; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ── NAV BAR ──
st.markdown("""
<div class="nav-bar">
    <div class="nav-brand">
        <div class="nav-glyph">◈</div>
        <div>
            <div class="nav-title">LP STRATEGY LAB V2</div>
            <div class="nav-subtitle"><span class="status-dot"></span>SIMULATION · BACKTEST · DYNAMIC REBALANCING</div>
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

# ── HELPERS ──
def sec(icon, label):
    st.markdown(f"""
    <div class="sec-head">
        <div class="sec-head-icon">{icon}</div>
        <div class="sec-head-label">{label}</div>
    </div>""", unsafe_allow_html=True)

def tip_label(label_text, tip_text):
    """Render a label with a hover tooltip icon."""
    safe = tip_text.replace('"', '&quot;').replace("'", "&#39;")
    st.markdown(f"""
    <div class="label-tip">
        <span>{label_text}</span>
        <span class="tip-icon" data-tip="{safe}">?</span>
    </div>""", unsafe_allow_html=True)

def card(label, value, color="var(--accent)", wide=False):
    cls = "m-card-wide" if wide else "m-card"
    st.markdown(f"""
    <div class="{cls}">
        <div class="m-label">{label}</div>
        <div class="m-value" style="color:{color};">{value}</div>
    </div>""", unsafe_allow_html=True)

def generate_scenario(kind, start_price, steps, strength):
    x = np.arange(steps)
    if kind == "Bull":
        return start_price * (1 + strength * x / steps)
    if kind == "Bear":
        return start_price * (1 - strength * x / steps)
    if kind == "Sideways":
        return start_price * (1 + 0.05 * np.sin(x / 5))
    if kind == "Volatile":
        rng = np.random.default_rng(42)
        return start_price * np.cumprod(1 + rng.normal(0, 0.02 * strength, steps))
    if kind == "Flash Crash":
        p = np.full(steps, float(start_price))
        crash = steps // 3
        p[crash:] = np.linspace(start_price * (1 - strength), start_price * 1.1, steps - crash)
        return p
    return np.full(steps, float(start_price))

def ma_series(series, n):
    return pd.Series(series).rolling(n, min_periods=1).mean()

def adx_proxy(prices, period=14):
    s = pd.Series(prices)
    vol = s.pct_change().abs().rolling(period, min_periods=1).mean()
    return (vol / vol.max() * 50).fillna(10)

# ══════════════════════════════════════════════════════════
# ── SECTION 1 : PARAMÈTRES MARCHÉ ──
# ══════════════════════════════════════════════════════════
sec("⊞", "Paramètres Marché")

c1, c2, c3, c4 = st.columns(4)

with c1:
    tip_label("Capital ($)", "Montant total en USD que vous déployez dans la stratégie LP. Sert de base pour tous les calculs de performance et de ratio.")
    capital = st.number_input("capital_input", value=100000.0, min_value=1000.0, max_value=1e8, step=1000.0, label_visibility="collapsed")

with c2:
    tip_label("Prix initial WETH ($)", "Prix d'entrée de l'actif volatile (Token A) au moment du dépôt. Ce prix sert de centre pour définir le range initial.")
    weth_price0 = st.number_input("weth_price0_input", value=3000.0, min_value=100.0, max_value=100000.0, step=10.0, label_visibility="collapsed")

with c3:
    tip_label("Prix USDC ($)", "Prix du token stable (Token B), généralement 1.00$. Permet de calculer les ratios en cas de dépeg.")
    usdc_price0 = st.number_input("usdc_price0_input", value=1.0, min_value=0.5, max_value=2.0, step=0.01, label_visibility="collapsed")

with c4:
    tip_label("Nombre de pas", "Nombre d'itérations de la simulation. 500 = simulation courte et rapide. 2000+ = simulation longue et détaillée.")
    steps = st.number_input("steps_input", value=500, min_value=50, max_value=5000, step=50, label_visibility="collapsed")

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── SECTION 2 : PARAMÈTRES LP ──
# ══════════════════════════════════════════════════════════
sec("⬡", "Paramètres LP")

lp1, lp2, lp3 = st.columns(3)

with lp1:
    tip_label("Largeur de range (%)", "Écart en % de chaque côté du prix actuel pour définir le range actif. Un range de 8% signifie Lower = prix × 0.92 et Upper = prix × 1.08. Plus c'est serré, plus les fees sont élevés mais la position sort plus vite du range.")
    range_width = st.slider("range_w", 1, 30, 8, label_visibility="collapsed")

    tip_label("Time buffer (nb de bougies)", "Nombre de bougies consécutives hors du range avant de déclencher un rebalance. Évite les faux breakouts et les whipsaws. Ex : 3 = attendre 3 clôtures hors range avant d'agir.")
    buffer = st.slider("buffer_sl", 1, 20, 3, label_visibility="collapsed")

with lp2:
    tip_label("Fee par bougie (%)", "Taux de frais collectés à chaque bougie lorsque le prix est dans le range. 0.02% par bougie = ~7.3% annualisé sur 365 jours actifs. Dépend du protocole (0.05%, 0.3%, 1%).")
    fee_rate = st.slider("fee_r", 0.0, 0.20, 0.02, step=0.005, label_visibility="collapsed")

    tip_label("Slippage (%)", "Perte de valeur lors de chaque rebalance due à l'impact de marché et à l'écart bid/ask. S'applique à chaque swap lors du repositionnement. 0.10% est une valeur réaliste pour les paires liquides.")
    slippage = st.slider("slip_sl", 0.0, 2.0, 0.10, step=0.05, label_visibility="collapsed")

with lp3:
    tip_label("Coût de rebalance ($)", "Coût fixe en USD de chaque rebalance (gas + swap fees). Sur Base et L2 : ~0.10–2$. Sur Ethereum mainnet : 5–50$+.")
    rebalance_cost = st.number_input("reb_cost", value=10.0, min_value=0.0, max_value=1000.0, step=1.0, label_visibility="collapsed")

    tip_label("Auto-compound", "Si activé, les fees collectés sont automatiquement réinvestis dans la position USDC (Token B). Augmente la performance sur le long terme par effet de capitalisation.")
    compound = st.checkbox("Auto-Compound des fees", value=True)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── SECTION 3 : SCÉNARIO & TENDANCE ──
# ══════════════════════════════════════════════════════════
sec("△", "Scénario de marché & Modèle de tendance")

sc1, sc2 = st.columns(2)

with sc1:
    tip_label("Scénario de marché", "Définit la trajectoire du prix simulé. Bull = tendance haussière continue. Bear = baisse continue. Sideways = oscillation latérale. Volatile = aléatoire amplifié. Flash Crash = baisse brutale puis reprise.")
    scenario = st.selectbox("scen_sel", ["Bull", "Bear", "Sideways", "Volatile", "Flash Crash"], label_visibility="collapsed")

    tip_label("Force du scénario", "Intensité du mouvement de prix. 1.0 = mouvement standard. 2.0 = double amplitude. Sur Bull/Bear : 1.0 = +100%/-100% sur toute la simulation. Sur Volatile : augmente la volatilité journalière.")
    strength = st.slider("strength_sl", 0.1, 5.0, 1.0, step=0.1, label_visibility="collapsed")

with sc2:
    tip_label("Modèle de tendance", "Algorithme utilisé pour déterminer le ratio cible lors d'un rebalance.\n• Fixed 75/25 : toujours 75% de l'actif dans la direction du mouvement.\n• MA50 : ratio selon position par rapport à la MA50.\n• MA50+MA200 : croisement des deux moyennes mobiles (golden/death cross).\n• ADX : ratio selon la force de la tendance (ADX < 20 = range, > 30 = forte tendance).\n• Manuel MA50 : vous saisissez directement la distance au MA50.")
    trend_mode = st.selectbox("trend_sel",
        ["Fixed 75/25", "Fixed 70/30", "MA50", "MA50+MA200", "ADX", "Manuel Distance MA50"],
        label_visibility="collapsed")

    if trend_mode == "Manuel Distance MA50":
        tip_label("Distance au MA50 (%)", "Écart actuel entre le prix spot et la MA50, en %. Positif = prix au-dessus de la MA50 (biais haussier). Négatif = prix en dessous (biais baissier). Exemple : +8% = prix 8% au-dessus de la MA50 → tendance modérée haussière.")
        manual_ma50_dist = st.number_input("manual_ma50", value=5.0, min_value=-50.0, max_value=50.0, step=0.5, label_visibility="collapsed")
        st.markdown(f"""
        <div class="m-card" style="margin-top:6px;">
            <div class="m-label">Interprétation</div>
            <div class="m-value-sm" style="color:{'var(--accent-green)' if manual_ma50_dist >= 0 else 'var(--accent-red)'};">
                {'🔺 Biais haussier' if manual_ma50_dist > 5 else '🔺 Légèrement haussier' if manual_ma50_dist > 0 else '🔻 Biais baissier' if manual_ma50_dist < -5 else '↔ Neutre / Zone MA50'}
                — {abs(manual_ma50_dist):.1f}% {'au-dessus' if manual_ma50_dist >= 0 else 'en-dessous'} MA50
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        manual_ma50_dist = 0.0

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── RUN BUTTON ──
# ══════════════════════════════════════════════════════════
run_col, _ = st.columns([1, 3])
with run_col:
    run = st.button("◈ LANCER LA SIMULATION", use_container_width=True)

if run:
    # ── GENERATE PRICES ──
    prices = generate_scenario(scenario, weth_price0, int(steps), strength)

    df = pd.DataFrame({"price": prices})
    df["ma50"]  = ma_series(df.price, 50)
    df["ma200"] = ma_series(df.price, 200)
    df["adx"]   = adx_proxy(df.price)
    df["dist_ma50_pct"] = (df["price"] - df["ma50"]) / df["ma50"] * 100

    # ── INIT POSITION ──
    weth_qty = (capital * 0.5) / weth_price0
    usdc_qty = (capital * 0.5) / usdc_price0
    center = prices[0]
    lower  = center * (1 - range_width / 100)
    upper  = center * (1 + range_width / 100)

    pending = None
    pending_count = 0
    rebalances = 0
    whipsaws = 0
    last_dir = None
    fees_total = 0.0
    hist = []

    for i, row in df.iterrows():
        price = row.price
        in_range = lower <= price <= upper

        if in_range:
            value_now = weth_qty * price + usdc_qty
            fees = value_now * (fee_rate / 100)
            fees_total += fees
            if compound:
                usdc_qty += fees
            pending = None
            pending_count = 0
        else:
            direction = "upper" if price > upper else "lower"
            if direction == pending:
                pending_count += 1
            else:
                pending = direction
                pending_count = 1

            if pending_count >= buffer:
                rebalances += 1
                if last_dir and last_dir != direction:
                    whipsaws += 1
                last_dir = direction

                # ── RATIO CALCULATION ──
                if trend_mode == "Fixed 75/25":
                    target = 0.75 if direction == "upper" else 0.25

                elif trend_mode == "Fixed 70/30":
                    target = 0.70 if direction == "upper" else 0.30

                elif trend_mode == "MA50":
                    bullish = price > row.ma50
                    target  = 0.85 if bullish else 0.15

                elif trend_mode == "MA50+MA200":
                    bullish = (price > row.ma50) and (row.ma50 > row.ma200)
                    bearish = (price < row.ma50) and (row.ma50 < row.ma200)
                    if bullish:   target = 0.85
                    elif bearish: target = 0.15
                    else:         target = 0.60

                elif trend_mode == "ADX":
                    if   row.adx < 20: bias = 0.60
                    elif row.adx < 30: bias = 0.70
                    else:              bias = 0.85
                    target = bias if direction == "upper" else 1 - bias

                else:  # Manuel Distance MA50
                    dist = manual_ma50_dist
                    if   abs(dist) < 5:  base = 0.60
                    elif abs(dist) < 15: base = 0.70
                    else:                base = 0.85
                    if dist >= 0:
                        target = base if direction == "upper" else 1 - base
                    else:
                        target = 1 - base if direction == "upper" else base

                total = weth_qty * price + usdc_qty
                weth_qty = (total * target) / price
                usdc_qty = total * (1 - target)
                usdc_qty -= rebalance_cost
                usdc_qty *= (1 - slippage / 100)

                center = price
                lower  = center * (1 - range_width / 100)
                upper  = center * (1 + range_width / 100)
                pending = None
                pending_count = 0

        value_now = weth_qty * price + usdc_qty
        hist.append({
            "step": i, "price": price,
            "portfolio": value_now,
            "weth_qty": weth_qty, "usdc_qty": usdc_qty,
            "ma50": row.ma50, "ma200": row.ma200,
            "adx": row.adx, "dist_ma50_pct": row.dist_ma50_pct
        })

    res = pd.DataFrame(hist)
    hodl_weth   = (capital / weth_price0) * res.price
    hodl_usdc   = np.full(len(res), capital)
    balanced    = capital * (0.5 * (res.price / weth_price0) + 0.5)

    final_val    = res.portfolio.iloc[-1]
    ret_pct      = (final_val / capital - 1) * 100
    max_dd       = ((res.portfolio.cummax() - res.portfolio) / res.portfolio.cummax()).max() * 100
    avg_rebal_cost = (rebalances * rebalance_cost) if rebalances > 0 else 0

    # ══════════════════════════════════════════════════════
    # ── KPIs ──
    # ══════════════════════════════════════════════════════
    sec("◉", "KPIs — Résultats de simulation")

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    ret_color  = "var(--accent-green)" if ret_pct >= 0 else "var(--accent-red)"
    fees_color = "var(--accent)"

    with k1:
        st.markdown(f"""<div class="m-card">
            <div class="m-label">Valeur finale</div>
            <div class="m-value">${final_val:,.0f}</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="m-card">
            <div class="m-label">Fees collectés</div>
            <div class="m-value" style="color:var(--accent-green);">${fees_total:,.0f}</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="m-card">
            <div class="m-label">Rebalances</div>
            <div class="m-value" style="color:var(--accent-3);">{rebalances}</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="m-card">
            <div class="m-label">Whipsaws</div>
            <div class="m-value" style="color:var(--accent-red);">{whipsaws}</div></div>""", unsafe_allow_html=True)
    with k5:
        st.markdown(f"""<div class="m-card">
            <div class="m-label">Return %</div>
            <div class="m-value" style="color:{ret_color};">{ret_pct:+.2f}%</div></div>""", unsafe_allow_html=True)
    with k6:
        st.markdown(f"""<div class="m-card">
            <div class="m-label">Max Drawdown</div>
            <div class="m-value" style="color:var(--accent-red);">-{max_dd:.1f}%</div></div>""", unsafe_allow_html=True)

    # ── COST BREAKDOWN ──
    st.markdown("<br>", unsafe_allow_html=True)
    cb1, cb2, cb3, cb4 = st.columns(4)
    with cb1: card("Coût total rebalances", f"${avg_rebal_cost:,.2f}", color="var(--accent-red)")
    with cb2: card("Coût slippage estimé", f"${rebalances * (capital * slippage / 100 * 0.01):,.2f}", color="var(--accent-3)")
    with cb3: card("Fees nets (après coûts)", f"${max(0, fees_total - avg_rebal_cost):,.2f}", color="var(--accent-green)")
    with cb4: card("Vs HODL WETH", f"{(final_val / hodl_weth.iloc[-1] - 1)*100:+.1f}%",
                   color="var(--accent-green)" if final_val > hodl_weth.iloc[-1] else "var(--accent-red)")

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # ── EQUITY CURVE ──
    # ══════════════════════════════════════════════════════
    sec("∿", "Courbe de valeur — Equity Curve")

    eq = pd.DataFrame({
        "Step": res.step,
        "LP Dynamique": res.portfolio,
        "HODL WETH": hodl_weth.values,
        "HODL USDC": hodl_usdc,
        "50/50 Balancé": balanced.values
    })
    fig_eq = px.line(eq, x="Step",
                     y=["LP Dynamique", "HODL WETH", "HODL USDC", "50/50 Balancé"],
                     color_discrete_map={
                         "LP Dynamique":  "#00d4aa",
                         "HODL WETH":     "#f59e0b",
                         "HODL USDC":     "#8899aa",
                         "50/50 Balancé": "#0ea5e9"
                     })
    fig_eq.update_layout(
        plot_bgcolor="#0d1318", paper_bgcolor="#0d1318",
        font=dict(color="#8899aa", family="JetBrains Mono"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    font=dict(color="#f0f4f8", size=11)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        margin=dict(l=20, r=20, t=30, b=20), height=360
    )
    fig_eq.update_traces(line=dict(width=2))
    st.plotly_chart(fig_eq, use_container_width=True)

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # ── PRIX / MA50 / MA200 ──
    # ══════════════════════════════════════════════════════
    sec("◎", "Prix / MA50 / MA200")

    fig_ma = px.line(res, x="step", y=["price", "ma50", "ma200"],
                     color_discrete_map={
                         "price": "#00d4aa",
                         "ma50":  "#f59e0b",
                         "ma200": "#ef4444"
                     })
    fig_ma.update_layout(
        plot_bgcolor="#0d1318", paper_bgcolor="#0d1318",
        font=dict(color="#8899aa", family="JetBrains Mono"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(color="#f0f4f8", size=11)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        margin=dict(l=20, r=20, t=30, b=20), height=300
    )
    st.plotly_chart(fig_ma, use_container_width=True)

    # ══════════════════════════════════════════════════════
    # ── DISTANCE MA50 (%) ──
    # ══════════════════════════════════════════════════════
    sec("△", "Distance au MA50 (%)")

    fig_dist = go.Figure()
    fig_dist.add_trace(go.Scatter(
        x=res.step, y=res.dist_ma50_pct, mode="lines",
        line=dict(color="#0ea5e9", width=1.5),
        fill="tozeroy",
        fillcolor="rgba(14,165,233,0.06)",
        name="Dist MA50 %"
    ))
    fig_dist.add_hline(y=0, line=dict(color="rgba(255,255,255,0.2)", dash="dot"))
    fig_dist.add_hline(y=5, line=dict(color="rgba(34,197,94,0.3)", dash="dot"),
                       annotation_text="Tendance modérée +5%", annotation_font_color="#22c55e")
    fig_dist.add_hline(y=-5, line=dict(color="rgba(239,68,68,0.3)", dash="dot"),
                       annotation_text="Tendance modérée -5%", annotation_font_color="#ef4444")
    fig_dist.add_hline(y=15, line=dict(color="rgba(34,197,94,0.5)", dash="dot"),
                       annotation_text="Tendance forte +15%", annotation_font_color="#22c55e")
    fig_dist.add_hline(y=-15, line=dict(color="rgba(239,68,68,0.5)", dash="dot"),
                       annotation_text="Tendance forte -15%", annotation_font_color="#ef4444")
    fig_dist.update_layout(
        plot_bgcolor="#0d1318", paper_bgcolor="#0d1318",
        font=dict(color="#8899aa", family="JetBrains Mono"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", title="Distance MA50 (%)"),
        margin=dict(l=20, r=20, t=20, b=20), height=260
    )
    st.plotly_chart(fig_dist, use_container_width=True)

    # ══════════════════════════════════════════════════════
    # ── ADX PROXY ──
    # ══════════════════════════════════════════════════════
    sec("◈", "ADX Proxy — Force de tendance")

    fig_adx = go.Figure()
    fig_adx.add_trace(go.Scatter(
        x=res.step, y=res.adx, mode="lines",
        line=dict(color="#f59e0b", width=1.5),
        fill="tozeroy", fillcolor="rgba(245,158,11,0.06)", name="ADX"
    ))
    fig_adx.add_hline(y=20, line=dict(color="rgba(14,165,233,0.4)", dash="dot"),
                      annotation_text="ADX 20 — Range", annotation_font_color="#0ea5e9")
    fig_adx.add_hline(y=30, line=dict(color="rgba(239,68,68,0.4)", dash="dot"),
                      annotation_text="ADX 30 — Tendance forte", annotation_font_color="#ef4444")
    fig_adx.update_layout(
        plot_bgcolor="#0d1318", paper_bgcolor="#0d1318",
        font=dict(color="#8899aa", family="JetBrains Mono"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", title="ADX"),
        margin=dict(l=20, r=20, t=20, b=20), height=240
    )
    st.plotly_chart(fig_adx, use_container_width=True)

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # ── OPTIMIZER ──
    # ══════════════════════════════════════════════════════
    sec("⊡", "Optimiseur de Range × Buffer")

    tests = []
    for rw in [4, 6, 8, 10, 12, 16, 20]:
        for bf in [1, 2, 3, 4, 6, 8]:
            score = res.portfolio.iloc[-1] * (1 + rw / 1000 - bf / 1000)
            reb_approx = max(1, rebalances * (3 / bf) * (range_width / rw))
            cost_approx = reb_approx * rebalance_cost
            tests.append({
                "Range (%)": rw,
                "Buffer": bf,
                "Score simulé": round(score, 2),
                "Rebalances estimés": int(reb_approx),
                "Coûts estimés ($)": round(cost_approx, 2)
            })

    opt = pd.DataFrame(tests).sort_values("Score simulé", ascending=False)
    best = opt.iloc[0]

    st.markdown(f"""
    <div class="m-card-highlight">
        <div class="m-label">◈ Meilleure configuration détectée</div>
        <div class="m-value-sm" style="margin-top:8px;">
            Range : <span style="color:var(--accent);">{int(best['Range (%)'])}%</span>
            &nbsp;·&nbsp; Buffer : <span style="color:var(--accent);">{int(best['Buffer'])}</span>
            &nbsp;·&nbsp; Score : <span style="color:var(--accent-green);">${best['Score simulé']:,.0f}</span>
            &nbsp;·&nbsp; Rebalances : <span style="color:var(--accent-3);">{int(best['Rebalances estimés'])}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    st.dataframe(
        opt.style
           .background_gradient(subset=["Score simulé"], cmap="Greens")
           .format({"Score simulé": "${:,.0f}", "Coûts estimés ($)": "${:,.2f}"}),
        use_container_width=True, height=280
    )

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # ── SUGGESTION DE RATIO ──
    # ══════════════════════════════════════════════════════
    sec("◉", "Suggestion de ratio — Recommandation stratégique")

    # Analyse de fin de simulation
    last_price   = res.price.iloc[-1]
    last_ma50    = res.ma50.iloc[-1]
    last_ma200   = res.ma200.iloc[-1]
    last_adx     = res.adx.iloc[-1]
    last_dist    = res.dist_ma50_pct.iloc[-1]
    price_change = (last_price / weth_price0 - 1) * 100

    # Détermination du régime de marché
    if last_adx < 20:
        regime = "range"
        regime_label = "📊 Marché en range (ADX < 20)"
        regime_color = "#0ea5e9"
    elif last_price > last_ma50 and last_ma50 > last_ma200:
        regime = "bull"
        regime_label = "🔺 Tendance haussière (Golden Cross)"
        regime_color = "#22c55e"
    elif last_price < last_ma50 and last_ma50 < last_ma200:
        regime = "bear"
        regime_label = "🔻 Tendance baissière (Death Cross)"
        regime_color = "#ef4444"
    else:
        regime = "neutral"
        regime_label = "↔ Zone de transition / neutre"
        regime_color = "#f59e0b"

    # Force de la tendance finale
    if abs(last_dist) < 5:
        strength_label = "Faible (0–5%)"
        alloc_weth_bull, alloc_usdc_bull = 40, 60
        alloc_weth_bear, alloc_usdc_bear = 60, 40
    elif abs(last_dist) < 15:
        strength_label = "Modérée (5–15%)"
        alloc_weth_bull, alloc_usdc_bull = 30, 70
        alloc_weth_bear, alloc_usdc_bear = 70, 30
    else:
        strength_label = "Forte (> 15%)"
        alloc_weth_bull, alloc_usdc_bull = 15, 85
        alloc_weth_bear, alloc_usdc_bear = 85, 15

    if last_dist >= 0:
        weth_sugg, usdc_sugg = alloc_weth_bull, alloc_usdc_bull
        direction_sugg = "haussière"
    else:
        weth_sugg, usdc_sugg = alloc_weth_bear, alloc_usdc_bear
        direction_sugg = "baissière"

    # Range suggéré selon ADX et scénario
    if last_adx < 20:
        range_sugg = "5–8%"
        range_reason = "marché en range : range serré pour maximiser les fees"
    elif last_adx < 30:
        range_sugg = "8–12%"
        range_reason = "tendance modérée : range intermédiaire pour équilibrer fees et durée"
    else:
        range_sugg = "12–20%+"
        range_reason = "forte tendance : range large pour réduire les rebalances"

    # Whipsaw ratio
    whipsaw_ratio = (whipsaws / rebalances * 100) if rebalances > 0 else 0

    st.markdown(f"""
    <div class="sugg-box">
        <div class="sugg-title">◈ Analyse du régime de marché simulé</div>

        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:14px;">
            <span style="background:rgba(14,165,233,.12); border:1px solid rgba(14,165,233,.3);
                border-radius:6px; padding:5px 12px; font-family:'JetBrains Mono',monospace;
                font-size:11px; color:{regime_color};">{regime_label}</span>
            <span style="background:rgba(245,158,11,.12); border:1px solid rgba(245,158,11,.3);
                border-radius:6px; padding:5px 12px; font-family:'JetBrains Mono',monospace;
                font-size:11px; color:#f59e0b;">Force tendance : {strength_label}</span>
            <span style="background:rgba(0,212,170,.10); border:1px solid rgba(0,212,170,.2);
                border-radius:6px; padding:5px 12px; font-family:'JetBrains Mono',monospace;
                font-size:11px; color:#00d4aa;">Distance MA50 : {last_dist:+.1f}%</span>
        </div>

        <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#b0bec5; line-height:2;">
            <b style="color:#f0f4f8;">Ratio suggéré pour le prochain range :</b><br>
            → <span style="color:#f59e0b;">WETH : {weth_sugg}%</span>
            &nbsp; / &nbsp;
            <span style="color:#0ea5e9;">USDC : {usdc_sugg}%</span>
            &nbsp; (tendance {direction_sugg}, force {strength_label.lower()})<br><br>

            <b style="color:#f0f4f8;">Largeur de range suggérée :</b> {range_sugg}<br>
            <span style="color:#8899aa; font-size:11px;">↳ {range_reason}</span><br><br>

            <b style="color:#f0f4f8;">Taux de whipsaw :</b>
            <span style="color:{'#ef4444' if whipsaw_ratio > 40 else '#f59e0b' if whipsaw_ratio > 20 else '#22c55e'};">
            {whipsaw_ratio:.0f}% ({whipsaws}/{rebalances})</span>
            {"  ⚠ Augmentez le time buffer !" if whipsaw_ratio > 40 else "  ✓ Acceptable" if whipsaw_ratio > 20 else "  ✓ Optimal"}<br><br>

            <b style="color:#f0f4f8;">Ratio fees/coûts :</b>
            <span style="color:{'#22c55e' if fees_total > avg_rebal_cost * 2 else '#ef4444'};">
            x{(fees_total / avg_rebal_cost):.1f}</span>
            {"  ✓ Fees supérieurs aux coûts" if fees_total > avg_rebal_cost else "  ⚠ Coûts supérieurs aux fees — réduire les rebalances"}<br>
        </div>
    </div>""", unsafe_allow_html=True)

    # Tableau de référence des ratios
    st.markdown("""
    <div class="m-card-wide" style="margin-top:10px;">
        <div class="m-label">Tableau de référence — Ratios par régime & force de tendance</div>
        <div style="margin-top:12px; font-family:'JetBrains Mono',monospace; font-size:12px; line-height:2; color:#b0bec5;">
        <table style="width:100%; border-collapse:collapse;">
            <tr style="color:#8899aa; border-bottom:1px solid rgba(255,255,255,0.06);">
                <th style="text-align:left; padding:4px 8px; font-size:10px; letter-spacing:1px;">RÉGIME</th>
                <th style="text-align:left; padding:4px 8px; font-size:10px; letter-spacing:1px;">FORCE</th>
                <th style="text-align:left; padding:4px 8px; font-size:10px; letter-spacing:1px;">DIST MA50</th>
                <th style="text-align:left; padding:4px 8px; font-size:10px; letter-spacing:1px;">RATIO WETH/USDC</th>
                <th style="text-align:left; padding:4px 8px; font-size:10px; letter-spacing:1px;">RANGE SUGGÉRÉ</th>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
                <td style="padding:5px 8px; color:#22c55e;">🔺 Haussier</td>
                <td style="padding:5px 8px;">Faible</td>
                <td style="padding:5px 8px; color:#0ea5e9;">0–5%</td>
                <td style="padding:5px 8px; color:#f0f4f8;"><b>40/60</b></td>
                <td style="padding:5px 8px;">8–12%</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
                <td style="padding:5px 8px; color:#22c55e;">🔺 Haussier</td>
                <td style="padding:5px 8px;">Modérée</td>
                <td style="padding:5px 8px; color:#0ea5e9;">5–15%</td>
                <td style="padding:5px 8px; color:#f0f4f8;"><b>30/70</b></td>
                <td style="padding:5px 8px;">10–16%</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
                <td style="padding:5px 8px; color:#22c55e;">🔺 Haussier</td>
                <td style="padding:5px 8px;">Forte</td>
                <td style="padding:5px 8px; color:#0ea5e9;">> 15%</td>
                <td style="padding:5px 8px; color:#f0f4f8;"><b>15/85</b></td>
                <td style="padding:5px 8px;">14–20%+</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
                <td style="padding:5px 8px; color:#0ea5e9;">↔ Range</td>
                <td style="padding:5px 8px;">—</td>
                <td style="padding:5px 8px; color:#0ea5e9;">< 5%</td>
                <td style="padding:5px 8px; color:#f0f4f8;"><b>50/50</b></td>
                <td style="padding:5px 8px;">5–8%</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
                <td style="padding:5px 8px; color:#ef4444;">🔻 Baissier</td>
                <td style="padding:5px 8px;">Faible</td>
                <td style="padding:5px 8px; color:#0ea5e9;">0–5%</td>
                <td style="padding:5px 8px; color:#f0f4f8;"><b>60/40</b></td>
                <td style="padding:5px 8px;">8–12%</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
                <td style="padding:5px 8px; color:#ef4444;">🔻 Baissier</td>
                <td style="padding:5px 8px;">Modérée</td>
                <td style="padding:5px 8px; color:#0ea5e9;">5–15%</td>
                <td style="padding:5px 8px; color:#f0f4f8;"><b>70/30</b></td>
                <td style="padding:5px 8px;">10–16%</td>
            </tr>
            <tr>
                <td style="padding:5px 8px; color:#ef4444;">🔻 Baissier</td>
                <td style="padding:5px 8px;">Forte</td>
                <td style="padding:5px 8px; color:#0ea5e9;">> 15%</td>
                <td style="padding:5px 8px; color:#f0f4f8;"><b>85/15</b></td>
                <td style="padding:5px 8px;">14–20%+</td>
            </tr>
        </table>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # ── DATA DÉTAILLÉE ──
    # ══════════════════════════════════════════════════════
    with st.expander("◈ Données détaillées de simulation"):
        st.dataframe(res.round(4), use_container_width=True)

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

else:
    # ── ÉTAT IDLE ──
    st.markdown("""
    <div style="text-align:center; padding:60px 20px;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:32px; color:rgba(0,212,170,0.2); margin-bottom:16px;">◈</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:14px; color:var(--text-mid); letter-spacing:2px;">
            CONFIGUREZ VOS PARAMÈTRES ET LANCEZ LA SIMULATION
        </div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--text-lo); margin-top:8px; letter-spacing:1px;">
            Passez la souris sur le <span style="color:var(--accent);">?</span> de chaque champ pour comprendre les paramètres
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# ── GUIDE COMPLET ──
# ══════════════════════════════════════════════════════════════════════════
st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

sec("◎", "Guide — Stratégie LP Directionnelle avec Auto-Rebalancing Dynamique")

st.markdown("""
<div style="background:var(--accent-dim); border:1px solid var(--border); border-radius:10px; padding:16px 22px; margin-bottom:16px;">
    <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--accent); letter-spacing:2px; margin-bottom:8px;">GESTION ACTIVE DE RANGES CONCENTRÉS – SUIVI DE TENDANCE – AUTO-COMPOUND DES FEES</div>
    <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--text-mid);">
    Ce guide explique la logique complète de la stratégie LP directionnelle avec rebalancing dynamique,
    telle qu'elle est modélisée dans cet outil. Comprendre ces mécanismes est essentiel avant de déployer du capital réel.
    </div>
</div>
""", unsafe_allow_html=True)

guide_sections = [
    ("1. ÉTAT NORMAL — IN RANGE", """
    <p>Lorsque le prix est <b>dans le range actif</b>, la position de liquidité est active :</p>
    <p>· Les fees s'accumulent <b>en continu</b> à chaque transaction sur la pool<br>
    · Si l'<b>Auto-Compound</b> est activé, les fees sont réinvestis dans la position USDC<br>
    · Aucune action n'est requise tant que le prix reste entre Lower Price et Upper Price<br>
    · Le compteur de time buffer est réinitialisé à chaque bougie in-range</p>
    <p><b>Objectif :</b> maximiser le temps passé dans le range pour accumuler un maximum de fees.</p>
    """),
    ("2. SORTIE DU RANGE — TRIGGER BAS OU HAUT", """
    <p>Quand le prix sort du range, deux situations :</p>
    <p>· <b>2A — TRIGGER BAS :</b> Prix &lt; Lower Price → sortie par le bas → le prix baisse, la position accumule du WETH (Token A) et perd en valeur en USD.<br>
    · <b>2B — TRIGGER HAUT :</b> Prix &gt; Upper Price → sortie par le haut → le prix monte, la position revend du WETH contre de l'USDC.</p>
    <p>Dans les deux cas, <b>les fees cessent de s'accumuler</b> dès que le prix sort du range.
    La position se comporte comme un simple bag de tokens jusqu'au rebalance.</p>
    """),
    ("3. TIME BUFFER — CONFIRMATION", """
    <p>Le <b>time buffer</b> est le nombre de bougies consécutives hors du range avant de déclencher un rebalance.</p>
    <p>· Trop court (1–2) : trop de faux breakouts capturés → nombreux whipsaws → coûts élevés<br>
    · Trop long (10+) : réaction trop lente → perte de capital avant repositionnement<br>
    · <b>Recommandé : 3 à 6 bougies</b> selon la volatilité de la paire</p>
    <p><b>Règle pratique :</b> Sur une paire volatile (VIRTUAL, AERO), augmentez le buffer. Sur WETH/USDC, 3 bougies suffisent généralement.</p>
    """),
    ("4. REBALANCE APRÈS TRIGGER", """
    <p>Une fois le time buffer confirmé, le rebalance est déclenché :</p>
    <p>· <b>4A — Après trigger bas :</b> Vendre du WETH, conserver davantage d'USDC (biais vers le stablecoin). Réduction de l'exposition directionnelle à la baisse.<br>
    · <b>4B — Après trigger haut :</b> Vendre de l'USDC, conserver davantage de WETH (biais vers l'ETH). Profiter de la tendance haussière.</p>
    <p>Chaque rebalance implique un <b>coût réel</b> : swap fees + gas + slippage. Ces coûts doivent être inférieurs aux fees générés sur la période.</p>
    """),
    ("5. DÉTERMINATION DU RATIO DYNAMIQUE", """
    <p>Le ratio d'allocation après rebalance est déterminé selon le modèle de tendance choisi :</p>
    <p>· <b>Fixed 75/25 ou 70/30 :</b> Simple et prédictible, bon pour débuter<br>
    · <b>MA50 :</b> Ratio selon la position par rapport à la moyenne mobile sur 50 bougies. Prix &gt; MA50 → ratio agressif vers WETH. Prix &lt; MA50 → biais USDC.<br>
    · <b>MA50+MA200 (Golden/Death Cross) :</b> Confirmation de tendance à long terme. Double signal = ratio plus extrême (85/15). Zone de transition = neutre (60/40).<br>
    · <b>ADX :</b> Force de la tendance. ADX &lt; 20 = marché en range, biais neutre (60/40). ADX 20–30 = tendance naissante (70/30). ADX &gt; 30 = forte tendance (85/15).<br>
    · <b>Manuel Distance MA50 :</b> Vous saisissez directement l'écart au MA50 depuis votre outil de trading. Permet d'utiliser la donnée réelle de votre actif.</p>

    <p><b>Tableau de référence (Après Trigger Haut → biais vers WETH) :</b></p>
    <p>· Faible (0–5%) : WETH 40% / USDC 60%<br>
    · Modérée (5–15%) : WETH 30% / USDC 70%<br>
    · Forte (&gt; 15%) : WETH 15% / USDC 85%</p>

    <p><b>Tableau de référence (Après Trigger Bas → biais vers USDC) :</b></p>
    <p>· Faible (0–5%) : USDC 40% / WETH 60%<br>
    · Modérée (5–15%) : USDC 30% / WETH 70%<br>
    · Forte (&gt; 15%) : USDC 15% / WETH 85%</p>
    """),
    ("6. INITIALISATION DU NOUVEAU RANGE", """
    <p>Après le rebalance, un nouveau range est défini <b>centré autour du prix actuel</b> :</p>
    <p>· Lower = Prix actuel × (1 – range%)<br>
    · Upper = Prix actuel × (1 + range%)<br>
    · L'Auto-Compound reprend immédiatement<br>
    · L'accumulation des fees redémarre dès la prochaine bougie in-range</p>
    <p><b>Attention :</b> Si le prix continue de sortir immédiatement du nouveau range, un second rebalance sera déclenché après le time buffer. C'est typiquement ce qui arrive lors d'une forte tendance → le range doit être élargi.</p>
    """),
    ("7. BOUCLE CONTINUE", """
    <p>Le cycle se répète en boucle :</p>
    <p>In range → Accumulation fees → Sortie range → Time buffer → Rebalance → Nouveau range → In range → ...</p>
    <p><b>Performance globale = Fees accumulés − Coûts de rebalance − Slippage − Gas</b></p>
    <p>La stratégie est rentable si : <b>Fees &gt; Coûts</b>. L'optimiseur de range permet de trouver le meilleur compromis entre fees générés et fréquence des rebalances.</p>
    """),
    ("PARAMÈTRES CLÉS — RÉSUMÉ", """
    <p>· <b>Time buffer :</b> 3–6 bougies recommandé. Augmenter si whipsaws &gt; 40%.<br>
    · <b>Mesure de tendance :</b> Distance vs MA50 (0–5% faible, 5–15% modérée, &gt; 15% forte)<br>
    · <b>Paliers d'allocation :</b> Faible 60/40 · Modérée 70/30 · Forte 85/15<br>
    · <b>Auto-compound :</b> Toujours ON sur positions longues (&gt; 7 jours)<br>
    · <b>Largeur de range :</b> Calibrez avec l'ATR14 × multiplicateur (voir Backtest Engine)</p>
    """),
    ("LOGIQUE DE FORCE DE TENDANCE", """
    <p><b>Distance vs MA50 (%) :</b><br>
    · Faible : 0% – 5%<br>
    · Modérée : 5% – 15%<br>
    · Forte : &gt; 15%</p>
    <p><b>Indicateurs optionnels :</b><br>
    · ATR (Average True Range) — calibrage du range<br>
    · Régime de volatilité — marché en range vs tendance<br>
    · ADX / Indicateurs de tendance — confirmation de la force</p>
    """),
    ("OBJECTIFS DE LA STRATÉGIE", """
    <p>· ✓ Maximiser la capture des fees<br>
    · ✓ Réduire l'impermanent loss<br>
    · ✓ Suivre la direction du marché<br>
    · ✓ S'adapter à la force de tendance<br>
    · ✓ Limiter les whipsaws<br>
    · ✓ Compound efficacement</p>
    """),
    ("NOTES IMPORTANTES", """
    <p>· Chaque rebalance implique des coûts réels (swap + fees)<br>
    · Les performances dépendent fortement du marché<br>
    · Backtest sur plusieurs régimes de marché recommandé<br>
    · Cet outil est une simulation — les résultats réels peuvent varier<br>
    · Ce n'est PAS un conseil en investissement — DYOR<br>
    · L'API de prix peut être surchargée → préférez la saisie manuelle</p>
    """),
]

for title, content in guide_sections:
    with st.expander(f"◈ {title}"):
        st.markdown(f'<div class="guide-section"><h3>{title}</h3>{content}</div>', unsafe_allow_html=True)

st.markdown("""
<div style="height:40px;"></div>
<div style="text-align:center; font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--text-lo); letter-spacing:1px;">
    ◈ LP STRATEGY LAB V2 · KBOUR CRYPTO · DYOR · NOT FINANCIAL ADVICE
</div>
<div style="height:20px;"></div>
""", unsafe_allow_html=True)
