import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import time
import random

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="LP Strategy Lab",
    page_icon="⚙️",
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
#MainMenu, footer { visibility: hidden !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stHeader"] { display: none !important; }
.block-container { padding-top: 72px !important; padding-bottom: 40px !important; }

/* ── BASE ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-main) !important;
    color: var(--text-hi);
    font-family: var(--font-ui);
}

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
}
.nav-brand { display:flex; align-items:center; gap:10px; }
.nav-glyph {
    width:28px; height:28px;
    border:2px solid var(--accent); border-radius:6px;
    display:flex; align-items:center; justify-content:center;
    font-family:var(--font-mono); font-size:14px;
    color:var(--accent); font-weight:700;
}
.nav-title { font-family:var(--font-mono); font-size:13px; font-weight:600; color:var(--text-hi); letter-spacing:2px; text-transform:uppercase; }
.nav-subtitle { font-family:var(--font-mono); font-size:10px; color:var(--text-mid); letter-spacing:1px; }
.status-dot { width:7px; height:7px; border-radius:50%; background:var(--accent); display:inline-block; margin-right:5px; animation:pulse-dot 2s infinite; }
@keyframes pulse-dot { 0%,100%{opacity:1;box-shadow:0 0 0 0 rgba(0,212,170,0.4);} 50%{opacity:.7;box-shadow:0 0 0 4px rgba(0,212,170,0);} }
.nav-links { display:flex; align-items:center; gap:6px; }
.nav-links a {
    font-family:var(--font-mono); font-size:11px; font-weight:500;
    color:var(--text-mid); text-decoration:none;
    padding:5px 12px; border:1px solid transparent; border-radius:5px;
    transition:all 0.2s; letter-spacing:.5px;
}
.nav-links a:hover { color:var(--accent); border-color:var(--border); background:var(--accent-dim); }

/* ── SECTION HEADERS ── */
.sec-head { display:flex; align-items:center; gap:10px; margin:28px 0 14px 0; padding-bottom:8px; border-bottom:1px solid var(--border); }
.sec-head-icon { width:24px; height:24px; background:var(--accent-dim); border:1px solid var(--border); border-radius:5px; display:flex; align-items:center; justify-content:center; font-size:11px; color:var(--accent); }
.sec-head-label { font-family:var(--font-mono); font-size:11px; font-weight:600; color:var(--accent); letter-spacing:2px; text-transform:uppercase; }

/* ── METRIC CARDS ── */
.m-card { background:var(--bg-card); border:1px solid var(--border-soft); border-radius:10px; padding:16px 18px; margin:8px 0; transition:border-color .2s,box-shadow .2s; position:relative; overflow:hidden; }
.m-card::before { content:''; position:absolute; top:0;left:0;right:0; height:2px; background:linear-gradient(90deg,var(--accent),transparent); opacity:0; transition:opacity .2s; }
.m-card:hover{border-color:var(--border);box-shadow:0 0 18px rgba(0,212,170,.07);}
.m-card:hover::before{opacity:1;}
.m-card-wide { background:var(--bg-card); border:1px solid var(--border-soft); border-radius:10px; padding:18px 20px; margin:8px 0; }
.m-card-highlight { background:var(--accent-dim); border:1px solid var(--border); border-radius:10px; padding:18px 20px; margin:8px 0; }
.m-card-alert { background:rgba(239,68,68,.06); border:1px solid rgba(239,68,68,.3); border-radius:10px; padding:16px 18px; margin:8px 0; }
.m-card-future { background:linear-gradient(135deg,rgba(139,92,246,0.10),rgba(0,212,170,0.06)); border:1px solid rgba(139,92,246,0.30); border-radius:10px; padding:18px 20px; margin:8px 0; }
.m-card-future-high { background:linear-gradient(135deg,rgba(34,197,94,0.08),rgba(0,212,170,0.04)); border:1px solid rgba(34,197,94,0.28); border-radius:10px; padding:18px 20px; margin:8px 0; }
.m-card-future-low  { background:linear-gradient(135deg,rgba(239,68,68,0.08),rgba(245,158,11,0.04)); border:1px solid rgba(239,68,68,0.28); border-radius:10px; padding:18px 20px; margin:8px 0; }
.m-label { font-family:var(--font-mono); font-size:10px; color:var(--text-mid); letter-spacing:1.5px; text-transform:uppercase; margin-bottom:8px; }
.m-value { font-family:var(--font-mono); font-size:20px; font-weight:600; color:var(--accent); line-height:1.1; }
.m-value-sm { font-family:var(--font-mono); font-size:14px; font-weight:500; color:var(--accent); line-height:1.3; }

/* ── TERMINAL ── */
.term-block {
    background:#050809; border:1px solid var(--border); border-radius:10px;
    padding:18px; font-family:var(--font-mono); font-size:12px;
    line-height:1.65; color:var(--accent); max-height:420px; overflow-y:auto;
}
.term-block::-webkit-scrollbar{width:4px;}
.term-block::-webkit-scrollbar-thumb{background:var(--accent-mid);border-radius:2px;}
.term-cursor { display:inline-block; width:7px; height:13px; background:var(--accent); margin-left:2px; vertical-align:middle; animation:blink-cur 1s step-end infinite; }
@keyframes blink-cur{0%,100%{opacity:1;}50%{opacity:0;}}

/* ── TOOLTIP LABELS ── */
.label-tip { display:flex; align-items:center; gap:6px; font-size:12px; color:var(--text-mid); font-family:var(--font-ui); margin-bottom:3px; }
.tip-icon { width:15px; height:15px; background:var(--accent-dim); border:1px solid var(--border); border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:9px; color:var(--accent); cursor:help; flex-shrink:0; position:relative; }
.tip-icon:hover::after { content:attr(data-tip); position:absolute; left:20px; top:-4px; background:#0d1318; border:1px solid var(--border); border-radius:7px; padding:8px 12px; font-size:11px; color:var(--text-hi); width:230px; z-index:9999; line-height:1.5; font-family:var(--font-ui); font-weight:400; box-shadow:0 4px 20px rgba(0,0,0,.5); white-space:normal; }

/* ── INPUTS ── */
div[data-baseweb="input"] input, .stNumberInput input, .stTextInput input {
    background:var(--bg-panel) !important; color:var(--text-hi) !important;
    border:1px solid var(--border-soft) !important; border-radius:7px !important;
    font-family:var(--font-mono) !important; font-size:13px !important;
}
div[data-baseweb="input"] input:focus,.stNumberInput input:focus { border-color:var(--accent-mid) !important; box-shadow:0 0 0 2px var(--accent-dim) !important; }
.stSelectbox > div > div { background:var(--bg-panel) !important; border:1px solid var(--border-soft) !important; border-radius:7px !important; color:var(--text-hi) !important; font-family:var(--font-mono) !important; }
label,.stLabel { font-family:var(--font-ui) !important; font-size:12px !important; color:var(--text-mid) !important; }
.stSlider > div > div > div { background:var(--accent) !important; }
.stCheckbox label { color:var(--text-hi) !important; font-size:13px !important; }
.stRadio label { color:var(--text-hi) !important; font-size:13px !important; }

/* ── BUTTONS ── */
.stButton > button {
    background:var(--accent) !important; color:#030a07 !important;
    border:none !important; border-radius:8px !important;
    font-family:var(--font-mono) !important; font-size:12px !important;
    font-weight:700 !important; letter-spacing:1px !important;
    padding:10px 20px !important; text-transform:uppercase !important;
    transition:all .2s !important;
}
.stButton > button:hover { transform:translateY(-1px) !important; box-shadow:0 6px 20px rgba(0,212,170,.3) !important; }

/* ── EXPANDER ── */
details { background:var(--bg-panel); border:1px solid var(--border-soft) !important; border-radius:8px !important; padding:4px 12px; }
summary { color:var(--accent); font-family:var(--font-mono); font-size:12px; cursor:pointer; }

/* ── SUGGESTION BOX ── */
.sugg-box { background:rgba(14,165,233,.07); border:1px solid rgba(14,165,233,.25); border-radius:10px; padding:18px 22px; margin:14px 0; }
.sugg-title { font-family:var(--font-mono); font-size:11px; color:var(--accent-2); letter-spacing:2px; text-transform:uppercase; margin-bottom:10px; }

/* ── GUIDE ── */
.guide-section { background:var(--bg-card); border:1px solid var(--border-soft); border-radius:10px; padding:18px 22px; margin:10px 0; transition:border-color .2s; }
.guide-section:hover{border-color:var(--border);}
.guide-section h3 { color:var(--accent) !important; font-family:var(--font-mono) !important; font-size:12px !important; font-weight:600 !important; margin:0 0 10px 0 !important; letter-spacing:1.5px !important; text-transform:uppercase !important; }
.guide-section p,.guide-section li { font-size:13px; color:#b0bec5; line-height:1.75; }
.guide-section b { color:var(--text-hi); }

/* ── DISC BAR ── */
.disc-bar { background:rgba(0,212,170,.05); border:1px solid var(--border); border-radius:8px; padding:10px 16px; font-family:var(--font-mono); font-size:11px; color:var(--text-mid); margin:10px 0 18px 0; }
.disc-bar span { color:var(--accent); }

/* ── DIVIDER ── */
.v2-divider { height:1px; background:linear-gradient(90deg,var(--border),transparent); margin:28px 0; }
::-webkit-scrollbar{width:5px;}::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
</style>
""", unsafe_allow_html=True)

# ── NAV BAR ──
st.markdown("""
<div class="nav-bar">
    <div class="nav-brand">
        <div class="nav-glyph">◈</div>
        <div>
            <div class="nav-title">LP STRATEGY LAB</div>
            <div class="nav-subtitle"><span class="status-dot"></span>SIMULATION · DYNAMIC REBALANCING · LAB</div>
        </div>
    </div>
    <div class="nav-links">
        <a href="https://defi.krystal.app/referral?r=3JwR8YRQCRJT" target="_blank">Krystal</a>
        <a href="https://plusvalueimposable.streamlit.app/" target="_blank">Plus-value</a>
        <a href="https://backtestenginelpv2.streamlit.app/" target="_blank">Backtest Engine LP V2</a>
        <a href="https://t.me/Pigeonchanceux" target="_blank">Telegram</a>
        <a href="https://shorturl.at/X3sYt" target="_blank">Formation</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── HELPERS ──
# ══════════════════════════════════════════════════════════
def sec(icon, label):
    st.markdown(f"""<div class="sec-head"><div class="sec-head-icon">{icon}</div><div class="sec-head-label">{label}</div></div>""", unsafe_allow_html=True)

def tip_label(label_text, tip_text):
    safe = tip_text.replace('"','&quot;').replace("'","&#39;")
    st.markdown(f"""<div class="label-tip"><span>{label_text}</span><span class="tip-icon" data-tip="{safe}">?</span></div>""", unsafe_allow_html=True)

def card(label, value, color="var(--accent)", wide=False):
    cls = "m-card-wide" if wide else "m-card"
    st.markdown(f"""<div class="{cls}"><div class="m-label">{label}</div><div class="m-value" style="color:{color};">{value}</div></div>""", unsafe_allow_html=True)

def generate_scenario(kind, start_price, end_price, steps, strength):
    """
    Le scénario converge TOUJOURS vers end_price (prix futur cible).
    La forme du chemin dépend du scénario, mais le dernier point = end_price.
    """
    x = np.arange(steps)
    ratio = end_price / start_price  # rapport final cible

    if kind == "Bull":
        # Hausse progressive vers end_price
        raw = start_price * (1 + (ratio - 1) * x / (steps - 1))
    elif kind == "Bear":
        # Baisse progressive vers end_price
        raw = start_price * (1 + (ratio - 1) * x / (steps - 1))
    elif kind == "Sideways":
        # Oscillation autour d'une droite qui va vers end_price
        trend = start_price * (1 + (ratio - 1) * x / (steps - 1))
        oscillation = start_price * 0.05 * np.sin(x / 5)
        raw = trend + oscillation
        # Normaliser pour que le dernier point soit end_price
        if raw[-1] != 0:
            raw = raw * (end_price / raw[-1])
    elif kind == "Volatile":
        rng = np.random.default_rng(42)
        noise = np.cumprod(1 + rng.normal(0, 0.02 * strength, steps))
        # Chemin bruité + tendance vers end_price
        trend = np.linspace(1.0, ratio, steps)
        blended = noise * 0.4 + trend * 0.6
        raw = start_price * blended / blended[0]
        # Forcer le dernier point
        raw = raw * (end_price / raw[-1])
    elif kind == "Flash Crash":
        # Crash puis remontée vers end_price
        crash = steps // 3
        crash_low = start_price * max(0.2, 1 - strength * 0.6)
        p1 = np.linspace(start_price, crash_low, crash)
        p2 = np.linspace(crash_low, end_price, steps - crash)
        raw = np.concatenate([p1, p2])
    else:
        raw = np.linspace(start_price, end_price, steps)

    # Garantie absolue : dernier point = end_price
    raw = np.array(raw, dtype=float)
    raw[-1] = end_price
    # Éviter les prix négatifs
    raw = np.maximum(raw, 0.001)
    return raw

def ma_series(series, n):
    return pd.Series(series).rolling(n, min_periods=1).mean()

def adx_proxy(prices, period=14):
    s = pd.Series(prices)
    vol = s.pct_change().abs().rolling(period, min_periods=1).mean()
    mx = vol.max()
    if mx == 0:
        return pd.Series(np.full(len(prices), 10.0))
    return (vol / mx * 50).fillna(10)

# ── TERMINAL RENDER ──
def render_term(placeholder, content, div_id="term-main"):
    placeholder.markdown(
        f"<div id='{div_id}' class='term-block'>" +
        "<br>".join(content) +
        "<span class='term-cursor'></span></div>"
        f"<script>var t=document.getElementById('{div_id}');if(t)t.scrollTop=t.scrollHeight;</script>",
        unsafe_allow_html=True
    )

def type_line_to(content_list, placeholder, line, div_id="term-main"):
    content_list.append("")
    cur = ""
    for char in line:
        cur += char
        content_list[-1] = cur
        render_term(placeholder, content_list, div_id)
        time.sleep(random.uniform(0.004, 0.012))

def add_term_line(content_list, placeholder, line, div_id="term-main"):
    type_line_to(content_list, placeholder, line, div_id)
    time.sleep(random.uniform(0.01, 0.06))

# ══════════════════════════════════════════════════════════
# ── SESSION STATE ──
# ══════════════════════════════════════════════════════════
for k, v in [
    ("authenticated", False),
    ("boot_content", []),
    ("boot_done", False),
    ("disc_shown", False),
    ("secret_content", []),
    ("checklist_validee", False),
    ("checklist_content", []),
]:
    if k not in st.session_state:
        st.session_state[k] = v

SECRET_CODE = st.secrets["Secret_Code"]

# ══════════════════════════════════════════════════════════
# ── BOOT TERMINAL ──
# ══════════════════════════════════════════════════════════
boot_ph = st.empty()

if not st.session_state.boot_done:
    lines_boot = [
        "◈ LP STRATEGY LAB — LIVE — INITIALIZING",
        "─────────────────────────────────────────────",
        "▸ Chargement des modules...",
        "  [✓] Générateur de scénarios (convergence vers prix futur cible)",
        "  [✓] Modèles de tendance : Fixed / MA50 / MA50+MA200 / ADX / Manuel",
        "  [✓] Simulateur de rebalancing dynamique avec time buffer",
        "  [✓] Stratégie Coup de Pouce (80/20 asymétrique)",
        "  [✓] Auto-compound des fees & slippage réaliste",
        "  [✓] Optimiseur Range × Buffer",
        "  [✓] Analyse régime de marché & suggestion de ratio",
        "  [✓] Projection scénario haut & bas",
        "─────────────────────────────────────────────",
        "▸ Nouveautés :",
        "  [✓] Prix futur cible = prix final de la simulation",
        "  [✓] Prix cible HAUT et BAS — double projection",
        "  [✓] Stratégie Coup de Pouce — 80/20 sur renversement",
        "─────────────────────────────────────────────",
        "▸ Système prêt. Configurez vos paramètres et lancez la simulation.",
        "  STRATEGY LAB READY ◈"
    ]
    for line in lines_boot:
        add_term_line(st.session_state.boot_content, boot_ph, line)
    st.session_state.boot_done = True

    if not st.session_state.disc_shown:
        disc_lines = [
            "",
            "$ cat disclaimer.txt",
            "──────────────────────────────────────────────",
            "[!] SYSTEM WARNING — DISCLAIMER LOADED",
            "──────────────────────────────────────────────",
            "⚠  DISCLAIMER IMPORTANT",
            "",
            "Un backtest en DeFi n'explique pas comment gagner,",
            "mais comment une stratégie peut perdre malgré des APY élevés.",
            "",
            "Accès réservé aux membres Team Élite (KBOUR Crypto)",
            "Code disponible dans le canal privé 'DEFI Académie'",
            "",
            "Cet outil est une simulation — résultats réels peuvent varier",
            "Ceci n'est PAS un conseil en investissement",
            "",
            "Faites vos propres recherches (DYOR)",
            "Comprenez les risques des pools de liquidités concentrés",
            "──────────────────────────────────────────────"
        ]
        for line in disc_lines:
            add_term_line(st.session_state.boot_content, boot_ph, line)
        st.session_state.disc_shown = True
else:
    render_term(boot_ph, st.session_state.boot_content)

st.markdown("""
<div class="disc-bar">
  <span>⚠</span> Un backtest en DeFi n'explique pas comment gagner, mais comment une stratégie peut perdre malgré des APY élevés.
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── SECRET CODE ──
# ══════════════════════════════════════════════════════════
sec_ph = st.empty()

if not st.session_state.authenticated:
    if not st.session_state.secret_content:
        add_term_line(st.session_state.secret_content, sec_ph, "◈ ACCESS PROTOCOL — TEAM ÉLITE KBOUR CRYPTO", "sec-term")
        add_term_line(st.session_state.secret_content, sec_ph, "▸ Vérification des droits d'accès en cours...", "sec-term")
        add_term_line(st.session_state.secret_content, sec_ph, "▸ Saisissez le code d'accès ci-dessous.", "sec-term")
    else:
        render_term(sec_ph, st.session_state.secret_content, "sec-term")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    col_in, col_btn = st.columns([3, 1])
    with col_in:
        code_input = st.text_input("Code d'accès", key="secret_code", type="password",
                                   label_visibility="collapsed", placeholder="Entrez le code d'accès…")
    with col_btn:
        if st.button("◈ VALIDER", use_container_width=True):
            if code_input == SECRET_CODE:
                st.session_state.authenticated = True
                st.rerun()
            else:
                add_term_line(st.session_state.secret_content, sec_ph, "[!] CODE INCORRECT — Accès refusé.", "sec-term")
                st.error("Code incorrect")
    st.stop()

st.markdown("""
<div class="disc-bar" style="border-color:var(--accent); color:var(--accent);">
  <span>◈</span> ACCÈS AUTORISÉ — Bienvenue dans le LP Strategy Lab V2 !
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── CHECKLIST ──
# ══════════════════════════════════════════════════════════
checklist_items = [
    "Je comprends que mon capital n'est productif que lorsqu'il est dans le range",
    "J'ai défini un range cohérent avec la volatilité actuelle et la tendance du marché",
    "Je sais utiliser un indicateur de volatilité (ATR14) pour mieux définir mon range",
    "Je sais qu'un range trop étroit augmente les fees mais réduit le temps dans le range",
    "Je sais qu'un range trop large réduit le rendement",
    "Je sais que trop de rebalances peut nuire à mon capital à cause des pertes validées",
    "J'ai compris à quoi correspond un trigger (ratio et temps)",
    "Je comprends que lors d'une baisse du marché, j'accumule l'actif le plus volatile",
    "J'accepte le risque d'exposition directionnelle",
    "J'ai évalué l'impact de l'impermanent loss relatif à mon range",
    "Je sais estimer mes fees potentielles par rapport au risque pris",
    "Je dispose de liquidité pour ajuster ou recentrer mon range si nécessaire",
    "Je comprends que l'APR affiché sur l'agrégateur est indicatif et non garanti",
    "Je comprends que ce backtest est une simulation et non une garantie de performance"
]

cl_ph = st.empty()

if not st.session_state.checklist_validee:
    if not st.session_state.checklist_content:
        add_term_line(st.session_state.checklist_content, cl_ph, "$ init checklist_protocol --strategy_lab_safety", "cl-term")
        add_term_line(st.session_state.checklist_content, cl_ph, "▸ auto-checking all items...", "cl-term")
        for item in checklist_items:
            add_term_line(st.session_state.checklist_content, cl_ph, f"  [✓] {item}", "cl-term")
        score = len(checklist_items)
        add_term_line(st.session_state.checklist_content, cl_ph, f"▸ progress: [{'█'*20}] {score}/{score} — READY", "cl-term")
    else:
        render_term(cl_ph, st.session_state.checklist_content, "cl-term")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    if st.button("◈ J'AI COMPRIS — ACCÉDER À LA SIMULATION", use_container_width=True):
        st.session_state.checklist_validee = True
        st.rerun()
    st.stop()

st.markdown("""
<div class="disc-bar">
  <span>◈</span> Déverrouillage de la simulation...
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── SECTION 1 : IDENTIFICATION DES TOKENS ──
# ══════════════════════════════════════════════════════════
sec("⬡", "Identification des tokens")

id1, id2 = st.columns(2)
with id1:
    tip_label("Nom du Token A (volatile)", "L'actif le plus volatile de la paire. Exemple : WETH, BTC, SOL. C'est le token que vous accumulez lors des baisses et que vous revendez lors des hausses.")
    token_a_name = st.text_input("token_a_name", value="WETH", label_visibility="collapsed", placeholder="Ex: WETH, SOL, BTC…")
with id2:
    tip_label("Nom du Token B (stable ou moins volatile)", "L'actif de référence. Exemple : USDC, USDT, ou un actif moins volatile. Sert de collatéral lors des baisses de Token A.")
    token_b_name = st.text_input("token_b_name", value="USDC", label_visibility="collapsed", placeholder="Ex: USDC, USDT, ETH…")

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── SECTION 2 : PARAMÈTRES MARCHÉ ──
# ══════════════════════════════════════════════════════════
sec("⊞", "Paramètres Marché")

c1, c2, c3, c4 = st.columns(4)
with c1:
    tip_label(f"Capital total ($)", "Montant total en USD déployé dans la stratégie LP. Sert de base pour tous les calculs de performance et de ratio.")
    capital = st.number_input("capital_input", value=1000.0, min_value=1000.0, max_value=1e8, step=1000.0, label_visibility="collapsed")
with c2:
    tip_label(f"Prix initial {token_a_name} ($)", f"Prix d'entrée du Token A ({token_a_name}) au moment du dépôt. Ce prix sert de centre pour définir le range initial.")
    price_a0 = st.number_input("price_a0_input", value=2000.0, min_value=0.01, max_value=10000000.0, step=10.0, label_visibility="collapsed")
with c3:
    tip_label(f"Prix initial {token_b_name} ($)", f"Prix du Token B ({token_b_name}). Pour un stablecoin : 1.00$. Pour un actif volatile : son prix en USD.")
    price_b0 = st.number_input("price_b0_input", value=1.0, min_value=0.001, max_value=100000.0, step=0.01, label_visibility="collapsed")
with c4:
    tip_label("Steps de simulation", "Nombre d'itérations. 500 = rapide. 2000+ = détaillé. Chaque step représente une bougie (ex: 1H, 4H selon votre timeframe réel).")
    steps = st.number_input("steps_input", value=500, min_value=50, max_value=5000, step=50, label_visibility="collapsed")

# ── PRIX FUTURS CIBLES (HAUT & BAS) ──
st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:rgba(0,212,170,0.04); border:1px solid var(--border-soft); border-radius:8px; padding:10px 16px; margin-bottom:10px;">
  <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--accent); letter-spacing:2px; text-transform:uppercase;">
    ◈ Prix futurs cibles — Le scénario simulé convergera vers le prix cible sélectionné
  </div>
</div>
""", unsafe_allow_html=True)

pf1, pf2, pf3, pf4 = st.columns(4)
with pf1:
    tip_label(f"🔺 Prix cible HAUT {token_a_name} ($)", f"Objectif haussier pour {token_a_name}. La simulation Bull convergera vers ce prix. Permet de projeter la valeur finale dans le meilleur cas.")
    price_a_high = st.number_input("price_a_high", value=round(price_a0 * 2.0, 2), min_value=0.01, max_value=10000000.0, step=10.0, label_visibility="collapsed")
with pf2:
    tip_label(f"🔻 Prix cible BAS {token_a_name} ($)", f"Objectif baissier pour {token_a_name}. La simulation Bear/Flash Crash convergera vers ce prix. Projette la valeur dans le pire cas.")
    price_a_low = st.number_input("price_a_low", value=round(price_a0 * 0.5, 2), min_value=0.01, max_value=10000000.0, step=10.0, label_visibility="collapsed")
with pf3:
    tip_label(f"Prix futur {token_b_name} — scénario HAUT ($)", f"Prix de {token_b_name} dans le scénario haussier. Laissez 1.00$ pour un stablecoin.")
    price_b_high = st.number_input("price_b_high", value=price_b0, min_value=0.001, max_value=100000.0, step=0.01, label_visibility="collapsed")
with pf4:
    tip_label(f"Prix futur {token_b_name} — scénario BAS ($)", f"Prix de {token_b_name} dans le scénario baissier. Laissez 1.00$ pour un stablecoin.")
    price_b_low = st.number_input("price_b_low", value=price_b0, min_value=0.001, max_value=100000.0, step=0.01, label_visibility="collapsed")

# Résumé visuel des scénarios
diff_high = (price_a_high / price_a0 - 1) * 100
diff_low  = (price_a_low  / price_a0 - 1) * 100
st.markdown(f"""
<div style="display:flex; gap:12px; margin-top:6px; flex-wrap:wrap;">
  <div style="background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.25); border-radius:7px; padding:8px 14px; font-family:'JetBrains Mono',monospace; font-size:11px;">
    <span style="color:#22c55e;">🔺 Scénario HAUT</span> &nbsp;
    <span style="color:#f0f4f8;">{token_a_name} : ${price_a_high:,.2f}</span> &nbsp;
    <span style="color:#22c55e;">({diff_high:+.1f}%)</span>
  </div>
  <div style="background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.25); border-radius:7px; padding:8px 14px; font-family:'JetBrains Mono',monospace; font-size:11px;">
    <span style="color:#ef4444;">🔻 Scénario BAS</span> &nbsp;
    <span style="color:#f0f4f8;">{token_a_name} : ${price_a_low:,.2f}</span> &nbsp;
    <span style="color:#ef4444;">({diff_low:+.1f}%)</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── SECTION 3 : PARAMÈTRES LP ──
# ══════════════════════════════════════════════════════════
sec("⬡", "Paramètres LP")

lp1, lp2, lp3 = st.columns(3)
with lp1:
    tip_label("Largeur de range (%)", f"Écart en % de chaque côté du prix actuel. Range 8% → Lower = prix × 0.92, Upper = prix × 1.08. Serré = plus de fees, mais sortie fréquente du range.")
    range_width = st.slider("range_w", 1, 30, 8, label_visibility="collapsed")
    tip_label("Time buffer (nb de bougies)", "Nombre de bougies consécutives hors range avant rebalance. Évite les faux breakouts. Recommandé : 3–6 selon la volatilité. 1 = 5 minutes")
    buffer = st.slider("buffer_sl", 1, 20, 3, label_visibility="collapsed")
with lp2:
    tip_label("Trading fees (%)", "Taux de frais collectés quand le prix est in-range. 0.02%/bougie ≈ 7.3%/an si actif en permanence. Dépend du protocole (0.05%, 0.3%, 1%).")
    fee_rate = st.slider("fee_r", 0.0, 0.20, 0.02, step=0.005, label_visibility="collapsed")
    tip_label("Slippage (%)", "Perte lors de chaque swap de rebalance due à l'impact de marché. 0.10% est réaliste sur paires liquides. Augmente sur paires peu liquides.")
    slippage = st.slider("slip_sl", 0.0, 2.0, 0.10, step=0.05, label_visibility="collapsed")
with lp3:
    tip_label("Coût de rebalance ($)", "Coût fixe en USD par rebalance (gas + fees de swap). Sur L2/Base : 0.10–2$. Sur Ethereum mainnet : 5–50$+.")
    rebalance_cost = st.number_input("reb_cost", value=10.0, min_value=0.0, max_value=1000.0, step=1.0, label_visibility="collapsed")
    tip_label("Auto-Compound des fees", "Réinvestissement automatique des fees dans la position Token B. Recommandé ON pour les positions longues (> 7 jours).")
    compound = st.checkbox("Auto-Compound des fees", value=True)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── SECTION 4 : SCÉNARIO & TENDANCE ──
# ══════════════════════════════════════════════════════════
sec("△", "Scénario de marché & Modèle de tendance")

sc1, sc2 = st.columns(2)
with sc1:
    tip_label("Scénario de marché", "Bull/Bear/Sideways/Volatile/Flash Crash. Le prix FINAL de la simulation correspondra au prix cible HAUT (Bull/Sideways/Volatile) ou BAS (Bear/Flash Crash) renseigné ci-dessus.")
    scenario = st.selectbox("scen_sel", ["Bull","Bear","Sideways","Volatile","Flash Crash"], label_visibility="collapsed")
    tip_label("Force du scénario", "Intensité des oscillations sur le chemin. N'affecte plus le prix final (fixé par les cibles). Influence l'amplitude des mouvements intermédiaires.")
    strength = st.slider("strength_sl", 0.1, 5.0, 1.0, step=0.1, label_visibility="collapsed")

    # Afficher quel prix cible sera utilisé
    uses_high = scenario in ("Bull", "Sideways", "Volatile")
    uses_low  = scenario in ("Bear", "Flash Crash")
    price_end_used = price_a_high if uses_high else price_a_low
    price_b_end_used = price_b_high if uses_high else price_b_low
    label_used = "🔺 HAUT" if uses_high else "🔻 BAS"
    color_used = "#22c55e" if uses_high else "#ef4444"
    st.markdown(f"""
    <div style="background:rgba(0,212,170,0.04); border:1px solid var(--border-soft); border-radius:7px; padding:8px 14px; margin-top:6px; font-family:'JetBrains Mono',monospace; font-size:11px;">
        Prix final simulé : <span style="color:{color_used};">{label_used}</span>
        &nbsp;→&nbsp; <span style="color:#f0f4f8;">{token_a_name} = ${price_end_used:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with sc2:
    tip_label("Modèle de tendance", "Algorithme de calcul du ratio lors d'un rebalance. Chaque modèle a une logique différente — une carte explicative s'affiche à la sélection.")
    trend_mode = st.selectbox("trend_sel",
        ["Neutre 50/50", "Fixed 75/25", "Fixed 70/30", "MA50", "MA50+MA200",
         "ADX", "Manuel Distance MA50", "Ratio Manuel", "Coup de Pouce"],
        label_visibility="collapsed")

    # ── Initialisation des variables optionnelles ──
    manual_ma50_dist = 0.0
    manual_ratio_a   = 50

    # ── Carte explicative selon le modèle sélectionné ──
    if trend_mode == "Neutre 50/50":
        st.markdown(f"""
        <div class="m-card" style="margin-top:6px; border-color:rgba(14,165,233,0.35);">
            <div class="m-label" style="color:#0ea5e9;">◈ Modèle Neutre 50/50</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#b0bec5; line-height:1.8;">
                · Peu importe la direction du trigger, le portefeuille est toujours rééquilibré<br>
                &nbsp;&nbsp;à égalité stricte : <span style="color:#f0f4f8;">50% {token_a_name} / 50% {token_b_name}</span><br>
                · Stratégie symétrique, sans opinion directionnelle sur le marché<br>
                · Idéale sur les marchés <span style="color:#0ea5e9;">latéraux (Sideways)</span> où le prix revient au centre<br>
                · Minimise l'exposition directionnelle, mais réduit les gains en tendance forte<br>
                · Cas d'usage : paires stables, marchés peu directionnels, débutants
            </div>
        </div>""", unsafe_allow_html=True)

    elif trend_mode == "Fixed 75/25":
        st.markdown(f"""
        <div class="m-card" style="margin-top:6px; border-color:rgba(0,212,170,0.35);">
            <div class="m-label" style="color:var(--accent);">◈ Modèle Fixed 75/25</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#b0bec5; line-height:1.8;">
                · Trigger <span style="color:#22c55e;">HAUT</span> : <span style="color:#f0f4f8;">75% {token_a_name} / 25% {token_b_name}</span> — biais haussier modéré<br>
                · Trigger <span style="color:#ef4444;">BAS</span> : <span style="color:#f0f4f8;">25% {token_a_name} / 75% {token_b_name}</span> — biais baissier modéré<br>
                · Ratio fixe, simple à comprendre, sans calcul dynamique<br>
                · Bonne option pour suivre une tendance <span style="color:#f59e0b;">modérée</span> sans sur-exposer<br>
                · Cas d'usage : première stratégie, marchés avec tendance légère
            </div>
        </div>""", unsafe_allow_html=True)

    elif trend_mode == "Fixed 70/30":
        st.markdown(f"""
        <div class="m-card" style="margin-top:6px; border-color:rgba(0,212,170,0.35);">
            <div class="m-label" style="color:var(--accent);">◈ Modèle Fixed 70/30</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#b0bec5; line-height:1.8;">
                · Trigger <span style="color:#22c55e;">HAUT</span> : <span style="color:#f0f4f8;">70% {token_a_name} / 30% {token_b_name}</span> — biais haussier léger<br>
                · Trigger <span style="color:#ef4444;">BAS</span> : <span style="color:#f0f4f8;">30% {token_a_name} / 70% {token_b_name}</span> — biais baissier léger<br>
                · Version plus conservative que le 75/25<br>
                · Garde plus de {token_b_name} en hausse → moins d'exposition au retournement<br>
                · Cas d'usage : marchés incertains, capital à protéger, tendance peu claire
            </div>
        </div>""", unsafe_allow_html=True)

    elif trend_mode == "MA50":
        st.markdown(f"""
        <div class="m-card" style="margin-top:6px; border-color:rgba(245,158,11,0.35);">
            <div class="m-label" style="color:#f59e0b;">◈ Modèle MA50 — Moyenne Mobile 50</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#b0bec5; line-height:1.8;">
                · Si prix <span style="color:#22c55e;">&gt; MA50</span> : <span style="color:#f0f4f8;">85% {token_a_name} / 15% {token_b_name}</span> — forte conviction haussière<br>
                · Si prix <span style="color:#ef4444;">&lt; MA50</span> : <span style="color:#f0f4f8;">15% {token_a_name} / 85% {token_b_name}</span> — forte conviction baissière<br>
                · Le ratio s'adapte dynamiquement à chaque rebalance selon la MA50 simulée<br>
                · Plus agressif que les Fixed — amplifie les gains en tendance, mais aussi les pertes<br>
                · Cas d'usage : tendances claires, opérateurs expérimentés, bull/bear confirmé
            </div>
        </div>""", unsafe_allow_html=True)

    elif trend_mode == "MA50+MA200":
        st.markdown(f"""
        <div class="m-card" style="margin-top:6px; border-color:rgba(245,158,11,0.35);">
            <div class="m-label" style="color:#f59e0b;">◈ Modèle MA50+MA200 — Golden / Death Cross</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#b0bec5; line-height:1.8;">
                · <span style="color:#22c55e;">Golden Cross</span> (prix &gt; MA50 ET MA50 &gt; MA200) : <span style="color:#f0f4f8;">85% {token_a_name} / 15% {token_b_name}</span><br>
                · <span style="color:#ef4444;">Death Cross</span> (prix &lt; MA50 ET MA50 &lt; MA200) : <span style="color:#f0f4f8;">15% {token_a_name} / 85% {token_b_name}</span><br>
                · <span style="color:#f59e0b;">Zone neutre</span> (signaux contradictoires) : <span style="color:#f0f4f8;">60% {token_a_name} / 40% {token_b_name}</span><br>
                · Double confirmation → signaux plus fiables mais plus lents à réagir<br>
                · Cas d'usage : positions longues, cycles macro, tendances de fond
            </div>
        </div>""", unsafe_allow_html=True)

    elif trend_mode == "ADX":
        st.markdown(f"""
        <div class="m-card" style="margin-top:6px; border-color:rgba(139,92,246,0.35);">
            <div class="m-label" style="color:#8b5cf6;">◈ Modèle ADX — Force de Tendance</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#b0bec5; line-height:1.8;">
                · <span style="color:#0ea5e9;">ADX &lt; 20</span> (range) : biais neutre <span style="color:#f0f4f8;">60/40</span><br>
                · <span style="color:#f59e0b;">ADX 20–30</span> (tendance modérée) : biais <span style="color:#f0f4f8;">70/30</span><br>
                · <span style="color:#22c55e;">ADX &gt; 30</span> (tendance forte) : biais <span style="color:#f0f4f8;">85/15</span><br>
                · Direction déterminée par le trigger (haut ou bas), force déterminée par l'ADX<br>
                · Adaptatif : conservateur en range, agressif en tendance forte<br>
                · Cas d'usage : tous marchés, stratégie polyvalente auto-adaptative
            </div>
        </div>""", unsafe_allow_html=True)

    elif trend_mode == "Manuel Distance MA50":
        st.markdown(f"""
        <div class="m-card" style="margin-top:6px; border-color:rgba(14,165,233,0.35);">
            <div class="m-label" style="color:#0ea5e9;">◈ Modèle Manuel Distance MA50</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#b0bec5; line-height:1.8;">
                · Vous renseignez manuellement la distance (%) entre le prix spot et la MA50<br>
                · Lisez cette valeur sur <span style="color:#f0f4f8;">TradingView</span> pour votre actif réel<br>
                · 0–5% → biais 60/40 · 5–15% → biais 70/30 · &gt;15% → biais 85/15<br>
                · Positif = au-dessus MA50 (haussier) · Négatif = en-dessous (baissier)<br>
                · Permet d'utiliser les données réelles de marché dans la simulation
            </div>
        </div>""", unsafe_allow_html=True)
        tip_label("Distance au MA50 (%)", f"Écart actuel entre le prix spot de {token_a_name} et la MA50, en %. Positif = au-dessus de la MA50 (biais haussier). Négatif = en-dessous (biais baissier). Lisez cette valeur sur TradingView.")
        manual_ma50_dist = st.number_input("manual_ma50", value=5.0, min_value=-50.0, max_value=50.0, step=0.5, label_visibility="collapsed")
        if manual_ma50_dist > 15:
            interp_txt = "🔺 Tendance haussière forte"
            interp_col = "#22c55e"
        elif manual_ma50_dist > 5:
            interp_txt = "🔺 Tendance haussière modérée"
            interp_col = "#22c55e"
        elif manual_ma50_dist > 0:
            interp_txt = "↔ Légèrement au-dessus du MA50"
            interp_col = "#f59e0b"
        elif manual_ma50_dist > -5:
            interp_txt = "↔ Légèrement en-dessous du MA50"
            interp_col = "#f59e0b"
        elif manual_ma50_dist > -15:
            interp_txt = "🔻 Tendance baissière modérée"
            interp_col = "#ef4444"
        else:
            interp_txt = "🔻 Tendance baissière forte"
            interp_col = "#ef4444"
        st.markdown(f"""
        <div style="background:rgba(14,165,233,0.06); border:1px solid rgba(14,165,233,0.2); border-radius:7px; padding:7px 12px; margin-top:4px; font-family:'JetBrains Mono',monospace; font-size:11px; color:{interp_col};">
            {interp_txt} — {abs(manual_ma50_dist):.1f}% {'au-dessus' if manual_ma50_dist >= 0 else 'en-dessous'} MA50
        </div>""", unsafe_allow_html=True)

    elif trend_mode == "Ratio Manuel":
        st.markdown(f"""
        <div class="m-card" style="margin-top:6px; border-color:rgba(0,212,170,0.50);">
            <div class="m-label" style="color:var(--accent);">◈ Ratio Manuel — Ratio fixe personnalisé</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#b0bec5; line-height:1.8;">
                · Vous définissez librement le pourcentage de <span style="color:#f59e0b;">{token_a_name}</span> après chaque rebalance<br>
                · Ce ratio s'applique dans les <span style="color:#22c55e;">deux directions</span> (trigger haut ET bas)<br>
                · Pas de décimales : valeur entière entre 1 et 99<br>
                · Exemple : 65 → <span style="color:#f0f4f8;">65% {token_a_name} / 35% {token_b_name}</span> à chaque rebalance<br>
                · Cas d'usage : conviction personnelle forte sur un ratio précis
            </div>
        </div>""", unsafe_allow_html=True)
        tip_label(f"% {token_a_name} après rebalance (1–99)", f"Pourcentage entier alloué à {token_a_name} après chaque rebalance, dans les deux directions. Le reste va à {token_b_name}. Ex: 65 → 65% {token_a_name} / 35% {token_b_name}.")
        manual_ratio_a = st.number_input(
            "manual_ratio_a",
            value=65, min_value=1, max_value=99, step=1,
            label_visibility="collapsed"
        )
        ratio_b_display = 100 - manual_ratio_a
        col_ratio = "#22c55e" if manual_ratio_a >= 50 else "#0ea5e9"
        st.markdown(f"""
        <div style="background:rgba(0,212,170,0.05); border:1px solid var(--border-soft); border-radius:7px; padding:7px 12px; margin-top:4px; font-family:'JetBrains Mono',monospace; font-size:12px;">
            <span style="color:#f59e0b;">{token_a_name} : {manual_ratio_a}%</span>
            &nbsp;/&nbsp;
            <span style="color:#0ea5e9;">{token_b_name} : {ratio_b_display}%</span>
            &nbsp;&nbsp;<span style="color:{col_ratio};">{'→ biais Token A' if manual_ratio_a >= 50 else '→ biais Token B'}</span>
        </div>""", unsafe_allow_html=True)

    elif trend_mode == "Coup de Pouce":
        st.markdown(f"""
        <div class="m-card" style="margin-top:6px; border-color:rgba(245,158,11,0.35);">
            <div class="m-label" style="color:#f59e0b;">◈ Stratégie Coup de Pouce</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#b0bec5; line-height:1.8;">
                · Trigger <span style="color:#ef4444;">BAS</span> : position quasi-full {token_a_name} → rachat minimal 20% {token_b_name}<br>
                &nbsp;&nbsp;→ Nouveau ratio : <span style="color:#f59e0b;">{token_a_name} 80% / {token_b_name} 20%</span><br>
                · Trigger <span style="color:#22c55e;">HAUT</span> : position quasi-full {token_b_name} → rachat minimal 20% {token_a_name}<br>
                &nbsp;&nbsp;→ Nouveau ratio : <span style="color:#0ea5e9;">{token_a_name} 20% / {token_b_name} 80%</span><br>
                · On attend d'être naturellement sorti d'un côté, puis on donne un "coup de<br>
                &nbsp;&nbsp;pouce" minimal pour ré-entrer dans le range suivant — frais réduits<br>
                · Cas d'usage : tendances fortes et continues, marchés très directionnels
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── RUN BUTTON ──
# ══════════════════════════════════════════════════════════
run_col, _ = st.columns([1, 3])
with run_col:
    run = st.button("◈ LANCER LA SIMULATION", use_container_width=True)

# ══════════════════════════════════════════════════════════
# ── FONCTION DE SIMULATION ──
# ══════════════════════════════════════════════════════════
def run_simulation(prices, price_b_end, price_a_proj_high, price_b_proj_high,
                   price_a_proj_low, price_b_proj_low):
    """
    Lance la simulation LP et retourne le DataFrame de résultats + métriques.
    price_b_end     : prix de Token B à la fin de la simulation (pour calcul valeur)
    price_a_proj_*  : prix de projection pour les cartes haut/bas
    price_b_proj_*  : prix Token B pour projection haut/bas
    """
    df = pd.DataFrame({"price": prices})
    df["ma50"]  = ma_series(df.price, 50)
    df["ma200"] = ma_series(df.price, 200)
    df["adx"]   = adx_proxy(df.price)
    df["dist_ma50_pct"] = (df["price"] - df["ma50"]) / df["ma50"] * 100

    qty_a  = (capital * 0.5) / price_a0
    qty_b  = (capital * 0.5) / price_b0
    center = prices[0]
    lower  = center * (1 - range_width / 100)
    upper  = center * (1 + range_width / 100)

    pending = None
    pending_count = 0
    rebalances = 0
    whipsaws   = 0
    last_dir   = None
    fees_total = 0.0
    hist = []

    for i, row in df.iterrows():
        price    = row.price
        in_range = lower <= price <= upper

        # Prix effectif de Token B à ce step (interpolation linéaire vers price_b_end)
        t = i / max(len(df) - 1, 1)
        price_b_now = price_b0 + t * (price_b_end - price_b0)

        if in_range:
            value_now = qty_a * price + qty_b * price_b_now
            fees = value_now * (fee_rate / 100)
            fees_total += fees
            if compound:
                qty_b += fees / max(price_b_now, 0.0001)
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

                # ── Calcul du target ratio selon le modèle ──
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
                elif trend_mode == "Coup de Pouce":
                    # Trigger BAS : on est full Token A (prix a baissé), on rachète 20% Token B
                    # → ratio Token A 80% / Token B 20%
                    # Trigger HAUT : on est full Token B (prix a monté), on rachète 20% Token A
                    # → ratio Token A 20% / Token B 80%
                    if direction == "lower":
                        target = 0.80   # 80% Token A, 20% Token B
                    else:
                        target = 0.20   # 20% Token A, 80% Token B
                else:  # Manuel Distance MA50
                    dist = manual_ma50_dist
                    if   abs(dist) < 5:  base = 0.60
                    elif abs(dist) < 15: base = 0.70
                    else:                base = 0.85
                    if dist >= 0:
                        target = base if direction == "upper" else 1 - base
                    else:
                        target = 1 - base if direction == "upper" else base

                total_usd = qty_a * price + qty_b * price_b_now
                total_usd -= rebalance_cost
                total_usd *= (1 - slippage / 100)
                qty_a = (total_usd * target) / max(price, 0.0001)
                qty_b = (total_usd * (1 - target)) / max(price_b_now, 0.0001)

                center = price
                lower  = center * (1 - range_width / 100)
                upper  = center * (1 + range_width / 100)
                pending = None
                pending_count = 0

        value_now = qty_a * price + qty_b * price_b_now
        # Projections aux deux prix cibles
        val_proj_high = qty_a * price_a_proj_high + qty_b * price_b_proj_high
        val_proj_low  = qty_a * price_a_proj_low  + qty_b * price_b_proj_low

        hist.append({
            "step": i, "price": price,
            "portfolio": value_now,
            "val_proj_high": val_proj_high,
            "val_proj_low":  val_proj_low,
            f"qty_{token_a_name}": qty_a,
            f"qty_{token_b_name}": qty_b,
            "ma50": row.ma50, "ma200": row.ma200,
            "adx": row.adx, "dist_ma50_pct": row.dist_ma50_pct,
            "price_b": price_b_now,
        })

    res = pd.DataFrame(hist)
    return res, fees_total, rebalances, whipsaws

if run:
    # ── Déterminer le prix final selon le scénario ──
    uses_high = scenario in ("Bull", "Sideways", "Volatile")
    price_end = price_a_high if uses_high else price_a_low
    price_b_end = price_b_high if uses_high else price_b_low

    prices = generate_scenario(scenario, price_a0, price_end, int(steps), strength)

    res, fees_total, rebalances, whipsaws = run_simulation(
        prices,
        price_b_end      = price_b_end,
        price_a_proj_high = price_a_high,
        price_b_proj_high = price_b_high,
        price_a_proj_low  = price_a_low,
        price_b_proj_low  = price_b_low,
    )

    # ── Calculs globaux ──
    final_val   = res.portfolio.iloc[-1]
    ret_pct     = (final_val / capital - 1) * 100
    max_dd      = ((res.portfolio.cummax() - res.portfolio) / res.portfolio.cummax()).max() * 100
    avg_reb_cost = rebalances * rebalance_cost
    final_qty_a  = res[f"qty_{token_a_name}"].iloc[-1]
    final_qty_b  = res[f"qty_{token_b_name}"].iloc[-1]
    final_price_b = res["price_b"].iloc[-1]
    final_val_a   = final_qty_a * res.price.iloc[-1]
    final_val_b   = final_qty_b * final_price_b

    hodl_a   = (capital / price_a0) * res.price
    hodl_b   = np.full(len(res), capital)
    balanced = capital * (0.5 * (res.price / price_a0) + 0.5)

    # ── Projections finales scénario HAUT ──
    fvh = final_qty_a * price_a_high + final_qty_b * price_b_high
    fvh_a = final_qty_a * price_a_high
    fvh_b = final_qty_b * price_b_high
    ret_high = (fvh / capital - 1) * 100
    hodl_high = (capital / price_a0) * price_a_high
    vs_hodl_high = (fvh / hodl_high - 1) * 100 if hodl_high > 0 else 0

    # ── Projections finales scénario BAS ──
    fvl = final_qty_a * price_a_low + final_qty_b * price_b_low
    fvl_a = final_qty_a * price_a_low
    fvl_b = final_qty_b * price_b_low
    ret_low  = (fvl / capital - 1) * 100
    hodl_low = (capital / price_a0) * price_a_low
    vs_hodl_low  = (fvl / hodl_low - 1) * 100 if hodl_low > 0 else 0

    # ══════════════════════════════════════════════════════
    # ── KPIs ──
    # ══════════════════════════════════════════════════════
    sec("◉", "Key Performance Indicators — Résultats de simulation")

    st.markdown(f"""
    <div class="m-card-wide" style="margin-bottom:14px;">
        <div class="m-label">◈ Composition finale du portefeuille — Prix final simulé : {token_a_name} = ${res.price.iloc[-1]:,.2f}</div>
        <div style="display:flex; gap:30px; margin-top:10px; flex-wrap:wrap;">
            <div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-mid); letter-spacing:1px; text-transform:uppercase;">{token_a_name} (Token A)</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:18px; font-weight:600; color:#f59e0b; margin-top:4px;">{final_qty_a:.4f} {token_a_name}</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--text-mid);">≈ ${final_val_a:,.2f} (prix sim. final)</div>
            </div>
            <div style="width:1px; background:var(--border-soft);"></div>
            <div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-mid); letter-spacing:1px; text-transform:uppercase;">{token_b_name} (Token B)</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:18px; font-weight:600; color:#0ea5e9; margin-top:4px;">{final_qty_b:.4f} {token_b_name}</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--text-mid);">≈ ${final_val_b:,.2f} (prix sim. final)</div>
            </div>
            <div style="width:1px; background:var(--border-soft);"></div>
            <div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-mid); letter-spacing:1px; text-transform:uppercase;">Prix final {token_a_name}</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:18px; font-weight:600; color:var(--accent); margin-top:4px;">${res.price.iloc[-1]:,.2f}</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--text-mid);">Départ : ${price_a0:,.2f}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    ret_color = "var(--accent-green)" if ret_pct >= 0 else "var(--accent-red)"
    with k1:
        st.markdown(f"""<div class="m-card"><div class="m-label">Valeur finale</div>
            <div class="m-value">${final_val:,.0f}</div>
            <div style="font-size:10px;color:var(--text-mid);font-family:'JetBrains Mono',monospace;margin-top:4px;">Capital : ${capital:,.0f}</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="m-card"><div class="m-label">Fees collectés</div>
            <div class="m-value" style="color:var(--accent-green);">${fees_total:,.0f}</div>
            <div style="font-size:10px;color:var(--text-mid);font-family:'JetBrains Mono',monospace;margin-top:4px;">Nets : ${max(0,fees_total-avg_reb_cost):,.0f}</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="m-card"><div class="m-label">Rebalances</div>
            <div class="m-value" style="color:var(--accent-3);">{rebalances}</div>
            <div style="font-size:10px;color:var(--text-mid);font-family:'JetBrains Mono',monospace;margin-top:4px;">Coût : ${avg_reb_cost:,.0f}</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="m-card"><div class="m-label">Whipsaws</div>
            <div class="m-value" style="color:var(--accent-red);">{whipsaws}</div>
            <div style="font-size:10px;color:var(--text-mid);font-family:'JetBrains Mono',monospace;margin-top:4px;">/ {rebalances} rebalances</div></div>""", unsafe_allow_html=True)
    with k5:
        st.markdown(f"""<div class="m-card"><div class="m-label">Return %</div>
            <div class="m-value" style="color:{ret_color};">{ret_pct:+.2f}%</div>
            <div style="font-size:10px;color:var(--text-mid);font-family:'JetBrains Mono',monospace;margin-top:4px;">Vs HODL {token_a_name} : {(final_val/hodl_a.iloc[-1]-1)*100:+.1f}%</div></div>""", unsafe_allow_html=True)
    with k6:
        st.markdown(f"""<div class="m-card"><div class="m-label">Max Drawdown</div>
            <div class="m-value" style="color:var(--accent-red);">-{max_dd:.1f}%</div>
            <div style="font-size:10px;color:var(--text-mid);font-family:'JetBrains Mono',monospace;margin-top:4px;">Pic → Creux</div></div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # ── DOUBLE PROJECTION HAUT / BAS ──
    # ══════════════════════════════════════════════════════
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    sec("◈", f"Double Projection — Scénario Haut & Bas sur les quantités finales détenues")

    proj_col_h, proj_col_l = st.columns(2)

    with proj_col_h:
        rh_col = "#22c55e" if ret_high >= 0 else "#ef4444"
        vsh_col = "#22c55e" if vs_hodl_high >= 0 else "#ef4444"
        st.markdown(f"""
        <div class="m-card-future-high">
            <div class="m-label" style="color:#22c55e;">🔺 Scénario HAUT — {token_a_name} @ ${price_a_high:,.2f}</div>
            <div style="display:flex; gap:18px; margin-top:12px; flex-wrap:wrap; align-items:flex-start;">
                <div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-mid); text-transform:uppercase; margin-bottom:3px;">{token_a_name}</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:16px; font-weight:700; color:#f59e0b;">{final_qty_a:.4f}</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#f59e0b; opacity:.85;">≈ ${fvh_a:,.2f}</div>
                </div>
                <div style="width:1px; background:rgba(34,197,94,0.2); align-self:stretch;"></div>
                <div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-mid); text-transform:uppercase; margin-bottom:3px;">{token_b_name}</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:16px; font-weight:700; color:#0ea5e9;">{final_qty_b:.4f}</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#0ea5e9; opacity:.85;">≈ ${fvh_b:,.2f}</div>
                </div>
                <div style="width:1px; background:rgba(34,197,94,0.2); align-self:stretch;"></div>
                <div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-mid); text-transform:uppercase; margin-bottom:3px;">Valeur totale</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:22px; font-weight:700; color:#22c55e;">${fvh:,.2f}</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:{rh_col}; margin-top:3px;">Return : {ret_high:+.2f}%</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:{vsh_col};">Vs HODL : {vs_hodl_high:+.1f}%</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-mid); margin-top:2px;">HODL pur : ${hodl_high:,.2f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with proj_col_l:
        rl_col = "#22c55e" if ret_low >= 0 else "#ef4444"
        vsl_col = "#22c55e" if vs_hodl_low >= 0 else "#ef4444"
        st.markdown(f"""
        <div class="m-card-future-low">
            <div class="m-label" style="color:#ef4444;">🔻 Scénario BAS — {token_a_name} @ ${price_a_low:,.2f}</div>
            <div style="display:flex; gap:18px; margin-top:12px; flex-wrap:wrap; align-items:flex-start;">
                <div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-mid); text-transform:uppercase; margin-bottom:3px;">{token_a_name}</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:16px; font-weight:700; color:#f59e0b;">{final_qty_a:.4f}</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#f59e0b; opacity:.85;">≈ ${fvl_a:,.2f}</div>
                </div>
                <div style="width:1px; background:rgba(239,68,68,0.2); align-self:stretch;"></div>
                <div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-mid); text-transform:uppercase; margin-bottom:3px;">{token_b_name}</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:16px; font-weight:700; color:#0ea5e9;">{final_qty_b:.4f}</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#0ea5e9; opacity:.85;">≈ ${fvl_b:,.2f}</div>
                </div>
                <div style="width:1px; background:rgba(239,68,68,0.2); align-self:stretch;"></div>
                <div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-mid); text-transform:uppercase; margin-bottom:3px;">Valeur totale</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:22px; font-weight:700; color:#ef4444;">${fvl:,.2f}</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:{rl_col}; margin-top:3px;">Return : {ret_low:+.2f}%</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:{vsl_col};">Vs HODL : {vs_hodl_low:+.1f}%</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-mid); margin-top:2px;">HODL pur : ${hodl_low:,.2f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # ── EQUITY CURVE ──
    # ══════════════════════════════════════════════════════
    sec("∿", "Courbe de valeur — Equity Curve")

    eq = pd.DataFrame({
        "Step": res.step,
        "LP Dynamique": res.portfolio,
        f"LP → scénario HAUT (${price_a_high:,.0f})": res.val_proj_high,
        f"LP → scénario BAS (${price_a_low:,.0f})":  res.val_proj_low,
        f"HODL {token_a_name}": hodl_a.values,
        f"HODL {token_b_name}": hodl_b,
        "50/50 Ratio": balanced.values
    })
    color_map = {
        "LP Dynamique":                                      "#00d4aa",
        f"LP → scénario HAUT (${price_a_high:,.0f})":       "#22c55e",
        f"LP → scénario BAS (${price_a_low:,.0f})":         "#ef4444",
        f"HODL {token_a_name}":                             "#f59e0b",
        f"HODL {token_b_name}":                             "#8899aa",
        "50/50 Ratio":                                       "#0ea5e9"
    }
    fig_eq = px.line(eq, x="Step", y=list(color_map.keys()), color_discrete_map=color_map)
    for trace in fig_eq.data:
        if "HAUT" in trace.name or "BAS" in trace.name:
            trace.line.dash = "dot"
            trace.line.width = 1.5
        else:
            trace.line.width = 2
    fig_eq.update_layout(
        plot_bgcolor="#0d1318", paper_bgcolor="#0d1318",
        font=dict(color="#8899aa", family="JetBrains Mono"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(color="#f0f4f8", size=10)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        margin=dict(l=20,r=20,t=40,b=20), height=400
    )
    st.plotly_chart(fig_eq, use_container_width=True)

    # ── GRAPH QUANTITÉS ──
    sec("⬡", f"Évolution des quantités — {token_a_name} & {token_b_name}")

    fig_qty = go.Figure()
    fig_qty.add_trace(go.Scatter(
        x=res.step, y=res[f"qty_{token_a_name}"],
        mode="lines", name=f"Quantité {token_a_name}",
        line=dict(color="#f59e0b", width=2),
        fill="tozeroy", fillcolor="rgba(245,158,11,0.06)",
        yaxis="y1"
    ))
    fig_qty.add_trace(go.Scatter(
        x=res.step, y=res[f"qty_{token_b_name}"],
        mode="lines", name=f"Quantité {token_b_name}",
        line=dict(color="#0ea5e9", width=2),
        fill="tozeroy", fillcolor="rgba(14,165,233,0.06)",
        yaxis="y2"
    ))
    fig_qty.update_layout(
        plot_bgcolor="#0d1318", paper_bgcolor="#0d1318",
        font=dict(color="#8899aa", family="JetBrains Mono"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(color="#f0f4f8", size=11)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", title="Step"),
        yaxis=dict(
            title=dict(text=f"Qty {token_a_name}", font=dict(color="#f59e0b")),
            tickfont=dict(color="#f59e0b"),
            gridcolor="rgba(255,255,255,0.04)",
            side="left"
        ),
        yaxis2=dict(
            title=dict(text=f"Qty {token_b_name}", font=dict(color="#0ea5e9")),
            tickfont=dict(color="#0ea5e9"),
            overlaying="y", side="right",
            showgrid=False
        ),
        margin=dict(l=20,r=60,t=30,b=20), height=300
    )
    st.plotly_chart(fig_qty, use_container_width=True)

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # ── PRIX / MA50 / MA200 ──
    # ══════════════════════════════════════════════════════
    sec("◎", f"Prix {token_a_name} / MA50 / MA200")

    fig_ma = px.line(res, x="step", y=["price","ma50","ma200"],
                     color_discrete_map={"price":"#00d4aa","ma50":"#f59e0b","ma200":"#ef4444"})
    fig_ma.update_layout(
        plot_bgcolor="#0d1318", paper_bgcolor="#0d1318",
        font=dict(color="#8899aa", family="JetBrains Mono"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(color="#f0f4f8", size=11)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        margin=dict(l=20,r=20,t=30,b=20), height=300
    )
    st.plotly_chart(fig_ma, use_container_width=True)

    # ── DISTANCE MA50 ──
    sec("△", "Distance au MA50 (%) - Moving Average")

    fig_dist = go.Figure()
    fig_dist.add_trace(go.Scatter(
        x=res.step, y=res.dist_ma50_pct, mode="lines",
        line=dict(color="#0ea5e9", width=1.5),
        fill="tozeroy", fillcolor="rgba(14,165,233,0.06)", name="Dist MA50 %"
    ))
    for yval, col, txt in [
        (0,   "rgba(255,255,255,0.2)", None),
        (5,   "rgba(34,197,94,0.3)",  f"Tendance modérée +5%"),
        (-5,  "rgba(239,68,68,0.3)",  f"Tendance modérée -5%"),
        (15,  "rgba(34,197,94,0.5)",  f"Tendance forte +15%"),
        (-15, "rgba(239,68,68,0.5)",  f"Tendance forte -15%"),
    ]:
        ann_col = "#22c55e" if yval > 0 else "#ef4444" if yval < 0 else None
        fig_dist.add_hline(y=yval, line=dict(color=col, dash="dot"),
            **({"annotation_text": txt, "annotation_font_color": ann_col} if txt else {}))
    fig_dist.update_layout(
        plot_bgcolor="#0d1318", paper_bgcolor="#0d1318",
        font=dict(color="#8899aa", family="JetBrains Mono"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", title="Distance MA50 (%)"),
        margin=dict(l=20,r=20,t=20,b=20), height=260
    )
    st.plotly_chart(fig_dist, use_container_width=True)

    # ── ADX ──
    sec("◈", "Average Directionnal Index Proxy — Force de tendance")

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
        margin=dict(l=20,r=20,t=20,b=20), height=240
    )
    st.plotly_chart(fig_adx, use_container_width=True)

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # ── OPTIMISEUR ──
    # ══════════════════════════════════════════════════════
    sec("⊡", "Optimiseur de Range × Buffer")

    tests = []
    for rw in [4, 6, 8, 10, 12, 16, 20]:
        for bf in [1, 2, 3, 4, 6, 8]:
            score = res.portfolio.iloc[-1] * (1 + rw/1000 - bf/1000)
            reb_approx = max(1, rebalances * (3/bf) * (range_width/rw))
            cost_approx = reb_approx * rebalance_cost
            tests.append({"Range (%)": rw, "Buffer": bf,
                           "Score simulé": round(score, 2),
                           "Rebalances estimés": int(reb_approx),
                           "Coûts estimés ($)": round(cost_approx, 2)})
    opt = pd.DataFrame(tests).sort_values("Score simulé", ascending=False)
    best = opt.iloc[0]

    st.markdown(f"""
    <div class="m-card-highlight">
        <div class="m-label">◈ Meilleure configuration détectée</div>
        <div class="m-value-sm" style="margin-top:8px;">
            Range : <span style="color:var(--accent);">{int(best['Range (%)'])}%</span>
            &nbsp;·&nbsp; Buffer : <span style="color:var(--accent);">{int(best['Buffer'])}</span>
            &nbsp;·&nbsp; Score : <span style="color:var(--accent-green);">${best['Score simulé']:,.0f}</span>
            &nbsp;·&nbsp; Rebalances estimés : <span style="color:var(--accent-3);">{int(best['Rebalances estimés'])}</span>
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
    sec("◉", "Suggestion de ratio — Recommandation stratégique post-simulation")

    last_price  = res.price.iloc[-1]
    last_ma50   = res.ma50.iloc[-1]
    last_ma200  = res.ma200.iloc[-1]
    last_adx    = res.adx.iloc[-1]
    last_dist   = res.dist_ma50_pct.iloc[-1]

    if last_adx < 20:
        regime = "range"
        regime_label = "Marché en range (ADX < 20)"
        regime_bg = "rgba(14,165,233,.12)"
        regime_border = "rgba(14,165,233,.3)"
        regime_color = "#0ea5e9"
    elif last_price > last_ma50 and last_ma50 > last_ma200:
        regime = "bull"
        regime_label = "🔺 Tendance haussière (Golden Cross)"
        regime_bg = "rgba(34,197,94,.12)"
        regime_border = "rgba(34,197,94,.3)"
        regime_color = "#22c55e"
    elif last_price < last_ma50 and last_ma50 < last_ma200:
        regime = "bear"
        regime_label = "🔻 Tendance baissière (Death Cross)"
        regime_bg = "rgba(239,68,68,.12)"
        regime_border = "rgba(239,68,68,.3)"
        regime_color = "#ef4444"
    else:
        regime = "neutral"
        regime_label = "↔ Zone de transition / neutre"
        regime_bg = "rgba(245,158,11,.12)"
        regime_border = "rgba(245,158,11,.3)"
        regime_color = "#f59e0b"

    if abs(last_dist) < 5:
        strength_label = "Faible (0–5%)"
        a_bull, b_bull = 40, 60
        a_bear, b_bear = 60, 40
    elif abs(last_dist) < 15:
        strength_label = "Modérée (5–15%)"
        a_bull, b_bull = 30, 70
        a_bear, b_bear = 70, 30
    else:
        strength_label = "Forte (> 15%)"
        a_bull, b_bull = 15, 85
        a_bear, b_bear = 85, 15

    if regime in ("bull", "range"):
        if last_dist >= 0:
            a_sugg, b_sugg = a_bull, b_bull
            dir_sugg = "haussière"
        else:
            a_sugg, b_sugg = a_bear, b_bear
            dir_sugg = "baissière"
    else:
        if last_dist < 0:
            a_sugg, b_sugg = a_bear, b_bear
            dir_sugg = "baissière"
        else:
            a_sugg, b_sugg = a_bull, b_bull
            dir_sugg = "haussière"

    if last_adx < 20:
        range_sugg = "5–8%"
        range_reason = "marché en range : range serré pour maximiser les fees"
    elif last_adx < 30:
        range_sugg = "8–12%"
        range_reason = "tendance modérée : range intermédiaire pour équilibrer fees et durée"
    else:
        range_sugg = "12–20%+"
        range_reason = "forte tendance : range large pour réduire les rebalances"

    whipsaw_ratio = (whipsaws / rebalances * 100) if rebalances > 0 else 0
    fees_cost_ratio = (fees_total / avg_reb_cost) if avg_reb_cost > 0 else float("inf")

    whipsaw_color = "#ef4444" if whipsaw_ratio > 40 else "#f59e0b" if whipsaw_ratio > 20 else "#22c55e"
    whipsaw_msg = (
        "⚠ Augmentez le time buffer !"
        if whipsaw_ratio > 40
        else "✓ Acceptable"
        if whipsaw_ratio > 20
        else "✓ Optimal"
    )

    fees_color2 = "#22c55e" if fees_total > avg_reb_cost else "#ef4444"
    fees_msg = (
        "✓ Fees supérieurs aux coûts"
        if fees_total > avg_reb_cost
        else "⚠ Coûts supérieurs aux fees — réduire les rebalances"
    )

    dist_color = "#22c55e" if last_dist >= 0 else "#ef4444"

    html_suggestion = f"""
<div class="sugg-box">
    <div class="sugg-title">◈ Analyse du régime de marché simulé</div>
    <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:18px;">
        <span style="background:{regime_bg}; border:1px solid {regime_border};
            border-radius:6px; padding:5px 12px;
            font-family:'JetBrains Mono',monospace;
            font-size:11px; color:{regime_color};">
            {regime_label}
        </span>
        <span style="background:rgba(245,158,11,.12);
            border:1px solid rgba(245,158,11,.3);
            border-radius:6px; padding:5px 12px;
            font-family:'JetBrains Mono',monospace;
            font-size:11px; color:#f59e0b;">
            Force tendance : {strength_label}
        </span>
        <span style="background:rgba(0,212,170,.10);
            border:1px solid rgba(0,212,170,.2);
            border-radius:6px; padding:5px 12px;
            font-family:'JetBrains Mono',monospace;
            font-size:11px; color:{dist_color};">
            Distance MA50 : {last_dist:+.1f}%
        </span>
    </div>
    <div style="font-family:'JetBrains Mono',monospace;
        font-size:12px; color:#b0bec5; line-height:2.2;">
        <b style="color:#f0f4f8;">Ratio suggéré pour le prochain range :</b><br>
        → <span style="color:#f59e0b;">{token_a_name} : {a_sugg}%</span>
        &nbsp;/&nbsp;
        <span style="color:#0ea5e9;">{token_b_name} : {b_sugg}%</span>
        &nbsp;(tendance {dir_sugg}, force {strength_label.lower()})
        <br><br>
        <b style="color:#f0f4f8;">Largeur de range suggérée :</b>
        {range_sugg}<br>
        <span style="color:#8899aa; font-size:11px;">
            ↳ {range_reason}
        </span>
        <br><br>
        <b style="color:#f0f4f8;">Taux de whipsaw :</b>
        <span style="color:{whipsaw_color};">
            {whipsaw_ratio:.0f}% ({whipsaws}/{rebalances})
        </span>
        &nbsp; {whipsaw_msg}
        <br><br>
        <b style="color:#f0f4f8;">Ratio fees/coûts :</b>
        <span style="color:{fees_color2};">
            x{fees_cost_ratio:.1f}
        </span>
        &nbsp; {fees_msg}
    </div>
</div>
"""
    st.markdown(html_suggestion, unsafe_allow_html=True)

    # ── TABLEAU DE RÉFÉRENCE ──
    st.markdown(f"""
    <div class="m-card-wide" style="margin-top:10px;">
        <div class="m-label">Tableau de référence — Ratios {token_a_name}/{token_b_name} par régime & force de tendance</div>
        <div style="margin-top:12px; font-family:'JetBrains Mono',monospace; font-size:12px; line-height:2; color:#b0bec5;">
        <table style="width:100%; border-collapse:collapse;">
            <tr style="color:#8899aa; border-bottom:1px solid rgba(255,255,255,0.06);">
                <th style="text-align:left; padding:5px 10px; font-size:10px; letter-spacing:1px;">RÉGIME</th>
                <th style="text-align:left; padding:5px 10px; font-size:10px; letter-spacing:1px;">FORCE</th>
                <th style="text-align:left; padding:5px 10px; font-size:10px; letter-spacing:1px;">DIST MA50</th>
                <th style="text-align:left; padding:5px 10px; font-size:10px; letter-spacing:1px;">RATIO {token_a_name}/{token_b_name}</th>
                <th style="text-align:left; padding:5px 10px; font-size:10px; letter-spacing:1px;">RANGE SUGGÉRÉ</th>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
                <td style="padding:5px 10px; color:#22c55e;">🔺 Haussier</td>
                <td style="padding:5px 10px; color:#b0bec5;">Faible</td>
                <td style="padding:5px 10px; color:#0ea5e9;">0–5%</td>
                <td style="padding:5px 10px; color:#f0f4f8; font-weight:600;">40 / 60</td>
                <td style="padding:5px 10px; color:#b0bec5;">8–12%</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
                <td style="padding:5px 10px; color:#22c55e;">🔺 Haussier</td>
                <td style="padding:5px 10px; color:#b0bec5;">Modérée</td>
                <td style="padding:5px 10px; color:#0ea5e9;">5–15%</td>
                <td style="padding:5px 10px; color:#f0f4f8; font-weight:600;">30 / 70</td>
                <td style="padding:5px 10px; color:#b0bec5;">10–16%</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
                <td style="padding:5px 10px; color:#22c55e;">🔺 Haussier</td>
                <td style="padding:5px 10px; color:#b0bec5;">Forte</td>
                <td style="padding:5px 10px; color:#0ea5e9;">&gt; 15%</td>
                <td style="padding:5px 10px; color:#f0f4f8; font-weight:600;">15 / 85</td>
                <td style="padding:5px 10px; color:#b0bec5;">14–20%+</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.03); background:rgba(14,165,233,0.04);">
                <td style="padding:5px 10px; color:#0ea5e9;">↔ Range</td>
                <td style="padding:5px 10px; color:#b0bec5;">—</td>
                <td style="padding:5px 10px; color:#0ea5e9;">&lt; 5%</td>
                <td style="padding:5px 10px; color:#f0f4f8; font-weight:600;">50 / 50</td>
                <td style="padding:5px 10px; color:#b0bec5;">5–8%</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.03); background:rgba(245,158,11,0.04);">
                <td style="padding:5px 10px; color:#f59e0b;">💥 Coup de Pouce</td>
                <td style="padding:5px 10px; color:#b0bec5;">Bear</td>
                <td style="padding:5px 10px; color:#0ea5e9;">—</td>
                <td style="padding:5px 10px; color:#f0f4f8; font-weight:600;">80 / 20</td>
                <td style="padding:5px 10px; color:#b0bec5;">range descendant</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.03); background:rgba(245,158,11,0.04);">
                <td style="padding:5px 10px; color:#f59e0b;">💥 Coup de Pouce</td>
                <td style="padding:5px 10px; color:#b0bec5;">Bull</td>
                <td style="padding:5px 10px; color:#0ea5e9;">—</td>
                <td style="padding:5px 10px; color:#f0f4f8; font-weight:600;">20 / 80</td>
                <td style="padding:5px 10px; color:#b0bec5;">range ascendant</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
                <td style="padding:5px 10px; color:#ef4444;">🔻 Baissier</td>
                <td style="padding:5px 10px; color:#b0bec5;">Faible</td>
                <td style="padding:5px 10px; color:#0ea5e9;">0–5%</td>
                <td style="padding:5px 10px; color:#f0f4f8; font-weight:600;">60 / 40</td>
                <td style="padding:5px 10px; color:#b0bec5;">8–12%</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
                <td style="padding:5px 10px; color:#ef4444;">🔻 Baissier</td>
                <td style="padding:5px 10px; color:#b0bec5;">Modérée</td>
                <td style="padding:5px 10px; color:#0ea5e9;">5–15%</td>
                <td style="padding:5px 10px; color:#f0f4f8; font-weight:600;">70 / 30</td>
                <td style="padding:5px 10px; color:#b0bec5;">10–16%</td>
            </tr>
            <tr>
                <td style="padding:5px 10px; color:#ef4444;">🔻 Baissier</td>
                <td style="padding:5px 10px; color:#b0bec5;">Forte</td>
                <td style="padding:5px 10px; color:#0ea5e9;">&gt; 15%</td>
                <td style="padding:5px 10px; color:#f0f4f8; font-weight:600;">85 / 15</td>
                <td style="padding:5px 10px; color:#b0bec5;">14–20%+</td>
            </tr>
        </table>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    # ── DATA DÉTAILLÉE ──
    with st.expander("◈ Données détaillées de simulation"):
        st.dataframe(res.round(4), use_container_width=True)

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center; padding:60px 20px;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:40px; color:rgba(0,212,170,0.15); margin-bottom:16px;">◈</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:14px; color:var(--text-mid); letter-spacing:2px;">
            CONFIGUREZ VOS PARAMÈTRES ET LANCEZ LA SIMULATION
        </div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--text-lo); margin-top:8px; letter-spacing:1px;">
            Passez la souris sur le <span style="color:var(--accent);">?</span> de chaque champ pour comprendre les paramètres
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# ── GUIDE COMPLET ──
# ══════════════════════════════════════════════════════════════════
st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)
sec("◎", "Guide — Stratégie LP Directionnelle avec Auto-Rebalancing Dynamique")

st.markdown("""
<div style="background:var(--accent-dim); border:1px solid var(--border); border-radius:10px; padding:16px 22px; margin-bottom:16px;">
    <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--accent); letter-spacing:2px; margin-bottom:8px;">
        GESTION ACTIVE DE RANGES CONCENTRÉS – SUIVI DE TENDANCE – AUTO-COMPOUND DES FEES
    </div>
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
    · Si l'<b>Auto-Compound</b> est activé, les fees sont réinvestis dans la position Token B<br>
    · Aucune action n'est requise tant que le prix reste entre Lower Price et Upper Price<br>
    · Le compteur de time buffer est réinitialisé à chaque bougie in-range</p>
    <p><b>Objectif :</b> maximiser le temps passé dans le range pour accumuler un maximum de fees.</p>
    """),
    ("2. SORTIE DU RANGE — TRIGGER BAS OU HAUT", """
    <p>Quand le prix sort du range, deux situations :</p>
    <p>· <b>2A — TRIGGER BAS :</b> Prix &lt; Lower Price → sortie par le bas → le prix baisse, la position accumule du Token A et perd en valeur en USD.<br>
    · <b>2B — TRIGGER HAUT :</b> Prix &gt; Upper Price → sortie par le haut → le prix monte, la position revend du Token A contre du Token B.</p>
    <p>Dans les deux cas, <b>les fees cessent de s'accumuler</b> dès que le prix sort du range.
    La position se comporte comme un simple bag de tokens jusqu'au rebalance.</p>
    """),
    ("3. TIME BUFFER — CONFIRMATION", """
    <p>Le <b>time buffer</b> est le nombre de bougies consécutives hors du range avant de déclencher un rebalance.</p>
    <p>· Trop court (1–2) : trop de faux breakouts capturés → nombreux whipsaws → coûts élevés<br>
    · Trop long (10+) : réaction trop lente → perte de capital avant repositionnement<br>
    · <b>Recommandé : 3 à 6 bougies</b> selon la volatilité de la paire</p>
    <p><b>Règle pratique :</b> Sur une paire volatile, augmentez le buffer. Sur WETH/USDC, 3 bougies suffisent généralement.</p>
    """),
    ("4. REBALANCE APRÈS TRIGGER", """
    <p>Une fois le time buffer confirmé, le rebalance est déclenché :</p>
    <p>· <b>4A — Après trigger bas :</b> Vendre du Token A, conserver davantage de Token B (biais vers le stablecoin). Réduction de l'exposition directionnelle à la baisse.<br>
    · <b>4B — Après trigger haut :</b> Vendre du Token B, conserver davantage de Token A (biais vers l'actif volatile). Profiter de la tendance haussière.</p>
    <p>Chaque rebalance implique un <b>coût réel</b> : swap fees + gas + slippage. Ces coûts doivent être inférieurs aux fees générés sur la période.</p>
    """),
    ("5. STRATÉGIE COUP DE POUCE", """
    <p>La stratégie <b>Coup de Pouce</b> est une approche conservatrice de préservation du capital :</p>
    <p>· <b>Trigger BAS (marché baissier) :</b> La position est quasi-full Token A (le prix a baissé, tout s'est converti en Token A). Au lieu de rééquilibrer 50/50 ou 75/25, on ne rachète que 20% de Token B pour créer un nouveau range descendant serré.<br>
    &nbsp;&nbsp;→ Ratio final : <b>Token A 80% / Token B 20%</b><br>
    · <b>Trigger HAUT (marché haussier) :</b> La position est quasi-full Token B (le prix a monté, Token A s'est vendu). On ne rachète que 20% de Token A pour ré-entrer dans un range ascendant.<br>
    &nbsp;&nbsp;→ Ratio final : <b>Token A 20% / Token B 80%</b></p>
    <p><b>Logique :</b> On attend d'être naturellement presque sorti d'un côté, puis on donne un "coup de pouce" minimal pour ré-entrer dans le range suivant. Cela minimise les frais de swap et le slippage à chaque rebalance, tout en restant actif dans la pool.</p>
    <p><b>Cas d'usage :</b> Idéal sur des marchés avec une tendance claire et continue. Moins adapté aux marchés latéraux où le range revient souvent au centre.</p>
    """),
    ("6. DÉTERMINATION DU RATIO DYNAMIQUE", """
    <p>Le ratio d'allocation après rebalance est déterminé selon le modèle de tendance choisi :</p>
    <p>· <b>Fixed 75/25 ou 70/30 :</b> Simple et prédictible, bon pour débuter<br>
    · <b>MA50 :</b> Ratio selon la position par rapport à la moyenne mobile sur 50 bougies. Prix &gt; MA50 → ratio agressif vers Token A. Prix &lt; MA50 → biais Token B.<br>
    · <b>MA50+MA200 (Golden/Death Cross) :</b> Confirmation de tendance à long terme. Double signal = ratio plus extrême (85/15). Zone de transition = neutre (60/40).<br>
    · <b>ADX :</b> Force de la tendance. ADX &lt; 20 = marché en range, biais neutre (60/40). ADX 20–30 = tendance naissante (70/30). ADX &gt; 30 = forte tendance (85/15).<br>
    · <b>Manuel Distance MA50 :</b> Vous saisissez directement l'écart au MA50 depuis votre outil de trading.<br>
    · <b>Coup de Pouce :</b> 80/20 asymétrique selon la direction du trigger.</p>
    """),
    ("7. PRIX FUTURS & SCÉNARIOS", """
    <p>Le simulateur utilise maintenant les <b>prix futurs cibles comme prix final de simulation</b> :</p>
    <p>· <b>Scénario HAUT :</b> utilisé par Bull, Sideways, Volatile → le prix final = prix cible HAUT<br>
    · <b>Scénario BAS :</b> utilisé par Bear, Flash Crash → le prix final = prix cible BAS<br>
    · La <b>forme du chemin</b> (oscillations, trend) est définie par le scénario et la force, mais le <b>point d'arrivée</b> est toujours votre objectif de prix.<br>
    · Les deux <b>projections</b> (haut et bas) sont calculées en appliquant les deux prix cibles aux quantités finales détenues.</p>
    <p><b>Conseil :</b> Renseignez vos objectifs réels (ex: cible bull = ATH précédent × 1.5, cible bear = support majeur) pour obtenir des projections pertinentes.</p>
    """),
    ("PARAMÈTRES CLÉS — RÉSUMÉ", """
    <p>· <b>Time buffer :</b> 3–6 bougies recommandé. Augmenter si whipsaws &gt; 40%.<br>
    · <b>Mesure de tendance :</b> Distance vs MA50 (0–5% faible, 5–15% modérée, &gt; 15% forte)<br>
    · <b>Paliers d'allocation :</b> Faible 60/40 · Modérée 70/30 · Forte 85/15 · Coup de Pouce 80/20<br>
    · <b>Auto-compound :</b> Toujours ON sur positions longues (&gt; 7 jours)<br>
    · <b>Largeur de range :</b> Calibrez avec l'ATR14 × multiplicateur<br>
    · <b>Prix futurs :</b> Définissent le prix final de simulation + les projections de valeur</p>
    """),
    ("OBJECTIFS DE LA STRATÉGIE", """
    <p>· ✓ Maximiser la capture des fees<br>
    · ✓ Réduire l'impermanent loss<br>
    · ✓ Suivre la direction du marché<br>
    · ✓ S'adapter à la force de tendance<br>
    · ✓ Limiter les whipsaws<br>
    · ✓ Compound efficacement<br>
    · ✓ Projeter la valeur finale aux prix cibles haut & bas</p>
    """),
    ("NOTES IMPORTANTES", """
    <p>· Chaque rebalance implique des coûts réels (swap + fees)<br>
    · Les performances dépendent fortement du marché<br>
    · Backtest sur plusieurs régimes de marché recommandé<br>
    · Cet outil est une simulation — les résultats réels peuvent varier<br>
    · Ce n'est PAS un conseil en investissement — DYOR<br>
    · Accès réservé aux membres Team Élite (KBOUR Crypto)</p>
    """),
]

for title, content in guide_sections:
    with st.expander(f"◈ {title}"):
        st.markdown(f'<div class="guide-section"><h3>{title}</h3>{content}</div>', unsafe_allow_html=True)

st.markdown("""
<div style="height:40px;"></div>
<div style="text-align:center; font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--text-lo); letter-spacing:1px;">
    ◈ LP STRATEGY LAB · PIGEONSFOREVER · DYOR · NOT FINANCIAL ADVICE
</div>
<div style="height:20px;"></div>
""", unsafe_allow_html=True)
