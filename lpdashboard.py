import math
import time
import random
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="LP DASHBOARD",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== GLOBAL THEME (dark mode + design system) =====================
st.markdown("""
<style>

/* =========================
   MASQUER L'UI STREAMLIT
   ========================= */

#MainMenu { visibility: hidden; }
header[data-testid="stHeader"] { display: none; }
[data-testid="stToolbar"] { display: none; }
footer { display: none; }

/* =========================
   DARK MODE FORCÉ
   ========================= */

:root { color-scheme: dark; }
html, body { background: #0b0f19 !important; }
.stApp { background: #0b0f19 !important; }
[data-testid="stAppViewContainer"] { background: #0b0f19 !important; }
[data-testid="stMain"] { background: transparent !important; }
[data-testid="stSidebar"] { background: #111827 !important; }

body, p, span, label, div { color: #f8fafc; }

.block-container { padding-top: 90px !important; }

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

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-main) !important;
    color: var(--text-hi);
    font-family: var(--font-ui);
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

.nav-brand { display: flex; align-items: center; gap: 10px; }

.nav-glyph {
    width: 28px; height: 28px;
    border: 2px solid var(--accent);
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
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

.nav-links { display: flex; align-items: center; gap: 6px; }

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

.m-value-red { color: var(--accent-red); }
.m-value-green { color: var(--accent-green); }
.m-value-amber { color: var(--accent-3); }
.m-value-blue { color: var(--accent-2); }

.m-card-wide {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 10px;
    padding: 18px 20px;
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

/* ========== INPUTS ========== */
div[data-baseweb="input"] input,
.stNumberInput input,
.stTextInput input {
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

/* ========== SELECTBOX ========== */
.stSelectbox > div > div,
.stMultiSelect > div > div {
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

/* ========== RADIO / CHECKBOX / SLIDER ========== */
.stRadio label, .stCheckbox label { color: var(--text-hi) !important; font-size: 13px !important; }
.stSlider > div > div > div { background: var(--accent) !important; }

/* ========== EXPANDER ========== */
details { background: var(--bg-panel); border: 1px solid var(--border-soft); border-radius: 8px; padding: 4px 12px; }
summary { color: var(--accent); font-family: var(--font-mono); font-size: 12px; cursor: pointer; }

/* ========== ALERTS ========== */
.stAlert { background: var(--bg-panel); border-left: 3px solid var(--accent); color: var(--text-hi); border-radius: 8px; }

/* ========== HEADERS ========== */
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
.v2-divider { height: 1px; background: linear-gradient(90deg, var(--border), transparent); margin: 30px 0; }

/* ========== SCROLLBAR ========== */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-track { background: transparent; }

</style>
""", unsafe_allow_html=True)

# ========== TOP NAV BAR ==========
st.markdown("""
<div class="nav-bar">
    <div class="nav-brand">
        <div class="nav-glyph">◈</div>
        <div>
            <div class="nav-title">LP DASHBOARD</div>
            <div class="nav-subtitle"><span class="status-dot"></span>LIVE · RECOVERY SIMULATOR · ETH/USDC</div>
        </div>
    </div>
    <div class="nav-links">
        <a href="https://defi.krystal.app/referral?r=3JwR8YRQCRJT" target="_blank">Krystal</a>
        <a href="https://plusvalueimposable.streamlit.app/" target="_blank">Plus-value</a>
        <a href="https://strategylab.streamlit.app/">Strategy Lab</a>
        <a href="https://t.me/Pigeonchanceux" target="_blank">Telegram</a>
        <a href="https://shorturl.at/X3sYt" target="_blank">Formation</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== HELPERS ==========

def sec(icon, label):
    st.markdown(f"""
    <div class="sec-head">
        <div class="sec-head-icon">{icon}</div>
        <div class="sec-head-label">{label}</div>
    </div>""", unsafe_allow_html=True)

SECRET_CODE = st.secrets["Secret_Code"]

# ========== INIT SESSION STATE ==========
for k, v in [
    ("authenticated", False), ("content", []), ("finished", False),
    ("disclaimer_shown", False), ("secret_content", []),
    ("checklist_validee", False), ("checklist_content", [])
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
        "◈ LP DASHBOARD — INITIALIZING",
        "─────────────────────────────────────────",
        "▸ Chargement des modules...",
        "  [✓] Position LP | Range & Prix | Perte impermanente",
        "  [✓] Comparaison de stratégies post-sortie de range",
        "  [✓] Simulateur de levier (collatéral / emprunt)",
        "─────────────────────────────────────────",
        "▸ Optimisation en cours...",
        "  Vous pouvez analyser votre position hors range.",
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
        "Cet outil montre comment une position LP peut perdre",
        "malgré un APR affiché élevé, pas comment gagner à coup sûr.",
        "",
        "Accès réservé aux membres Team Élite",
        "",
        "Cet outil peut contenir des approximations",
        "Ceci n'est PAS un conseil en investissement",
        "",
        "Faites vos propres recherches (DYOR)",
        "Comprenez les risques des pools de liquidités concentrés",
        "et du levier (liquidation) avant toute décision",
        "──────────────────────────────────────────"
    ]
    for line in disc_lines:
        add_term_line(st.session_state.content, terminal_placeholder, line)
    st.session_state.disclaimer_shown = True

st.markdown("""
<div class="disc-bar">
  <span>⚠</span> Cet outil montre comment une position LP peut perdre malgré un APR affiché élevé, pas comment gagner à coup sûr.
</div>
""", unsafe_allow_html=True)

# ========== SECRET CODE ==========
if not st.session_state.authenticated:
    sec_placeholder = st.empty()
    if not st.session_state.secret_content:
        add_term_line(st.session_state.secret_content, sec_placeholder, "◈ ACCESS PROTOCOL — TEAM ÉLITE", "sec-term", "term-block")
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
    "J'ai défini un range cohérent avec la volatilité actuelle et la tendance du marché",
    "Je sais qu'un range trop étroit augmente les fees mais réduit le temps dans le range",
    "Je sais qu'un range trop large réduit le rendement",
    "Je comprends que hors range, ma position ne génère plus aucun frais",
    "J'ai évalué la perte impermanente déjà verrouillée sur ma position",
    "Je comprends les 4 façons de rejouer la suite (LP, spot, BTC, stables)",
    "Si j'utilise l'option levier (Aave), je comprends le risque de liquidation",
    "Je surveille mon health factor si je prends du levier sur mon collatéral",
    "Je n'utilise que du capital que je suis prêt à perdre en cas de liquidation",
]

cl_placeholder = st.empty()

if not st.session_state.checklist_validee:
    if not st.session_state.checklist_content:
        add_term_line(st.session_state.checklist_content, cl_placeholder, "$ init checklist_protocol --lp_safety", "cl-term", "term-block")
        add_term_line(st.session_state.checklist_content, cl_placeholder, "▸ auto-checking all items...", "cl-term", "term-block")
        for item in checklist_items:
            add_term_line(st.session_state.checklist_content, cl_placeholder, f"  [✓] {item}", "cl-term", "term-block")
        score = len(checklist_items)
        bar = "█" * 20
        add_term_line(st.session_state.checklist_content, cl_placeholder, f"▸ progress: [{bar}] {score}/{score} — READY", "cl-term", "term-block")
    else:
        render_term(cl_placeholder, st.session_state.checklist_content, "cl-term", "term-block")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    if st.button("◈ J'AI COMPRIS — ACCÉDER AU DASHBOARD", use_container_width=True):
        st.session_state.checklist_validee = True
        st.rerun()
    st.stop()

st.markdown("""
<div class="disc-bar">
  <span>◈</span> déverrouillage du dashboard...
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Fonctions de calcul — mécanique Uniswap v3 (liquidité concentrée)
# ----------------------------------------------------------------------

def lp_amounts(price, L, p_lower, p_upper):
    """Retourne (montant ETH, montant USDC) détenus par la position à un prix donné."""
    sqrt_p = math.sqrt(price)
    sqrt_pa = math.sqrt(p_lower)
    sqrt_pb = math.sqrt(p_upper)

    if price <= p_lower:
        x = L * (1 / sqrt_pa - 1 / sqrt_pb)   # tout en ETH
        y = 0.0
    elif price >= p_upper:
        x = 0.0
        y = L * (sqrt_pb - sqrt_pa)            # tout en USDC
    else:
        x = L * (1 / sqrt_p - 1 / sqrt_pb)
        y = L * (sqrt_p - sqrt_pa)
    return x, y


def lp_value(price, L, p_lower, p_upper):
    x, y = lp_amounts(price, L, p_lower, p_upper)
    return x * price + y


def compute_liquidity(deposit_usd, entry_price, p_lower, p_upper):
    """Déduit L à partir du montant déposé à l'entrée (doit être dans la range)."""
    sqrt_p0 = math.sqrt(entry_price)
    sqrt_pa = math.sqrt(p_lower)
    sqrt_pb = math.sqrt(p_upper)
    denom = (1 / sqrt_p0 - 1 / sqrt_pb) * entry_price + (sqrt_p0 - sqrt_pa)
    return deposit_usd / denom


# ----------------------------------------------------------------------
# UI — Section "Ta position"
# ----------------------------------------------------------------------

sec("◎", "TA POSITION")

st.markdown(
    "Ta position de liquidité concentrée ETH/USDC est sortie de sa range. "
    "Cet outil montre la perte impermanente déjà verrouillée, le temps "
    "nécessaire pour la récupérer via les frais, et ce qui arrive à ton "
    "capital selon quatre manières de jouer la suite."
)
st.caption("Position LP concentrée ETH / USDC. Modifie n'importe quelle valeur.")

col1, col2, col3 = st.columns(3)
with col1:
    deposit = st.number_input("Montant déposé ($)", min_value=0.0, value=10_000.0, step=100.0)
    entry_price = st.number_input("Prix d'entrée (ETH, $)", min_value=0.01, value=2200.0, step=10.0)
with col2:
    current_price = st.number_input("Prix actuel (ETH, $)", min_value=0.01, value=1700.0, step=10.0)
    range_width_pct = st.slider("Largeur de range (±%)", min_value=1, max_value=80, value=15)
with col3:
    fee_apr = st.number_input("APR de frais quand dans le range (%)", min_value=0.0, value=20.0, step=1.0)
    target_price = st.number_input("Si l'ETH remonte à ($)", min_value=0.01, value=2000.0, step=10.0)

col4, col5 = st.columns(2)
with col4:
    btc_price = st.number_input("Prix actuel du BTC ($)", min_value=0.01, value=60000.0, step=100.0)
with col5:
    btc_rel_strength = st.slider(
        "Force relative du BTC", min_value=0.0, max_value=2.0, value=0.85, step=0.05,
        help="1.0 = le BTC suit exactement l'ETH · <1 = le BTC est à la traîne · >1 = le BTC dépasse l'ETH",
    )

# Range de la position
p_lower = entry_price * (1 - range_width_pct / 100)
p_upper = entry_price * (1 + range_width_pct / 100)
out_of_range = current_price <= p_lower or current_price >= p_upper

L = compute_liquidity(deposit, entry_price, p_lower, p_upper)
x0, y0 = lp_amounts(entry_price, L, p_lower, p_upper)          # avoirs à l'entrée
x_now, y_now = lp_amounts(current_price, L, p_lower, p_upper)  # avoirs actuels

lp_value_now = x_now * current_price + y_now
hodl_value_now = x0 * current_price + y0  # aurait valu si on avait juste détenu x0/y0
il_dollar = lp_value_now - hodl_value_now
il_pct = (il_dollar / hodl_value_now * 100) if hodl_value_now else 0.0

daily_fee = lp_value_now * (fee_apr / 100) / 365
recoup_days = abs(il_dollar) / daily_fee if daily_fee > 0 else float("inf")

st.divider()

status_col, il_col, recoup_col = st.columns(3)
with status_col:
    st.metric("Statut de la position", "Hors range" if out_of_range else "Dans le range")
    st.caption(f"Range : ${p_lower:,.0f} — ${p_upper:,.0f}")
with il_col:
    st.metric("Perte impermanente verrouillée", f"${il_dollar:,.0f}", f"{il_pct:,.1f}%")
with recoup_col:
    if math.isfinite(recoup_days):
        st.metric("Temps de récupération par les frais", f"{recoup_days:,.0f} jours")
    else:
        st.metric("Temps de récupération par les frais", "—")
    st.caption("Valable une fois *revenu* dans le range — hors range, la position ne génère aucun frais.")

st.caption(f"Répartition actuelle : {x_now:,.4f} ETH (${x_now*current_price:,.0f}) · {y_now:,.0f} USDC")

# ----------------------------------------------------------------------
# Comparaison des 4 stratégies
# ----------------------------------------------------------------------

sec("◫", "OÙ ATTERRIT TON ARGENT")
st.caption("Valeur du portefeuille selon la trajectoire de prix de l'ETH — pour chacune des 4 stratégies.")

price_range = np.linspace(current_price * 0.3, current_price * 2.5, 200)

# 1. Rester dans le LP
stay_lp = [lp_value(p, L, p_lower, p_upper) for p in price_range]

# 2. Retirer et détenir de l'ETH spot (tout converti en ETH au prix actuel)
eth_equiv_now = lp_value_now / current_price
hold_eth = [eth_equiv_now * p for p in price_range]

# 3. Moitié -> BTC
half_usd = lp_value_now / 2
eth_half_amount = half_usd / current_price
btc_amount = half_usd / btc_price
half_btc = [
    eth_half_amount * p + btc_amount * (btc_price * (1 + btc_rel_strength * (p / current_price - 1)))
    for p in price_range
]

# 4. Sortie totale en stables
exit_stables = [lp_value_now for _ in price_range]

strategies = {
    "Rester dans le LP": stay_lp,
    "Détenir ETH spot": hold_eth,
    "Moitié → BTC": half_btc,
    "Sortir en stables": exit_stables,
}

selected = st.multiselect(
    "Stratégies à afficher", list(strategies.keys()), default=list(strategies.keys())
)

fig = go.Figure()
for name in selected:
    fig.add_trace(go.Scatter(x=price_range, y=strategies[name], mode="lines", name=name))

fig.add_vline(x=current_price, line_dash="dot", line_color="gray",
              annotation_text="prix actuel", annotation_position="top")
fig.add_vline(x=target_price, line_dash="dot", line_color="orange",
              annotation_text="prix cible", annotation_position="top")

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Prix ETH ($)",
    yaxis_title="Valeur du portefeuille ($)",
    height=480,
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig, use_container_width=True)

# Valeurs au prix cible
st.subheader(f"Valeurs si l'ETH atteint ${target_price:,.0f}")
target_cols = st.columns(len(strategies))
for col, (name, values) in zip(target_cols, strategies.items()):
    val_at_target = np.interp(target_price, price_range, values)
    col.metric(name, f"${val_at_target:,.0f}")

# ----------------------------------------------------------------------
# Option E — Extraire son ETH, emprunter, redéployer
# ----------------------------------------------------------------------

sec("⚡", "OPTION E · JEU AVANCÉ")
st.caption(
    "Au lieu de vendre, dépose ton ETH en collatéral (ex. sur Aave), emprunte des "
    "stablecoins contre ce collatéral, puis redéploie ce capital. Tu gardes 100% de "
    "l'upside ETH — mais tu prends un risque de liquidation si le prix continue de baisser."
)

colA, colB, colC = st.columns(3)
with colA:
    eth_collateral = st.number_input(
        "ETH en collatéral (Ξ)", min_value=0.0, value=float(round(eth_equiv_now, 4)), step=0.01
    )
    ltv = st.slider("LTV d'emprunt (%)", min_value=1, max_value=90, value=50) / 100
with colB:
    liq_threshold = st.slider("Seuil de liquidation (%)", min_value=1, max_value=95, value=80) / 100
    borrow_apr = st.number_input("APR d'emprunt (%)", min_value=0.0, value=6.0, step=0.5)
with colC:
    deploy_apy = st.number_input("APY du capital redéployé (%)", min_value=0.0, value=12.0, step=0.5)
    horizon_months = st.slider("Horizon (mois)", min_value=1, max_value=36, value=12)

borrowable = eth_collateral * current_price * ltv
t = horizon_months / 12
debt_owed = borrowable * (1 + borrow_apr / 100 * t)
deployed_value = borrowable * (1 + deploy_apy / 100 * t)

liquidation_price = (borrowable / (eth_collateral * liq_threshold)) if eth_collateral > 0 else float("nan")
health_factor = (
    (eth_collateral * current_price * liq_threshold) / borrowable if borrowable > 0 else float("inf")
)
price_buffer_pct = (
    (current_price - liquidation_price) / current_price * 100 if current_price else float("nan")
)

net_equity_target = eth_collateral * target_price - debt_owed + deployed_value
edge_vs_hold = deployed_value - debt_owed  # == net_equity_target - (eth_collateral*target_price)

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Tu peux emprunter", f"${borrowable:,.0f}")
m2.metric("Prix de liquidation", f"${liquidation_price:,.0f}")
m3.metric("Health factor", f"{health_factor:,.2f}", help="1.0 = liquidation")

m4, m5, m6 = st.columns(3)
m4.metric("Marge de prix avant liquidation", f"{price_buffer_pct:,.1f}%")
m5.metric(f"Équité nette si ETH → ${target_price:,.0f}", f"${net_equity_target:,.0f}")
m6.metric("Avantage vs. simplement détenir de l'ETH", f"${edge_vs_hold:,.0f}")

if health_factor < 1.1 and math.isfinite(health_factor):
    st.warning("Health factor proche ou sous 1.0 — risque de liquidation élevé avec ces paramètres.")
