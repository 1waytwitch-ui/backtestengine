import math
import re
import time
import random
import numpy as np
import plotly.graph_objects as go
import streamlit as st


def html(content):
    """Affiche du HTML. Collapse tous les retours à la ligne / l'indentation en un
    seul espace : le moteur Markdown de Streamlit interprète sinon les lignes
    indentées (4+ espaces) comme un bloc de code, ce qui casse le rendu dès que
    le HTML multi-ligne est un peu complexe (ex: plusieurs cartes concaténées)."""
    st.markdown(re.sub(r"\s+", " ", content).strip(), unsafe_allow_html=True)

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="LP DASHBOARD",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== GLOBAL THEME (dark mode + design system) =====================
html("""
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

.sec-sub {
    font-family: var(--font-ui);
    font-size: 12.5px;
    color: var(--text-mid);
    margin: -10px 0 16px 0;
    line-height: 1.6;
}

.list-head {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-mid);
    letter-spacing: 1px;
    text-transform: uppercase;
    padding-bottom: 4px;
}

/* ========== METRIC / TILE CARDS ========== */
.m-card {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 10px;
    padding: 16px 18px;
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
    font-size: 21px;
    font-weight: 600;
    color: var(--accent);
    line-height: 1.15;
}

.m-value-red { color: var(--accent-red); }
.m-value-green { color: var(--accent-green); }
.m-value-amber { color: var(--accent-3); }
.m-value-blue { color: var(--accent-2); }

.m-sub {
    font-size: 11px;
    color: var(--text-mid);
    margin-top: 7px;
    line-height: 1.5;
}

.tile-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 12px;
    margin: 6px 0 20px 0;
}

.info-box {
    background: var(--accent-dim);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 10px 0 18px 0;
    font-size: 13px;
    line-height: 1.7;
    color: #d7e3ea;
}

.info-box b { color: var(--text-hi); }

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

/* Compact delete/add buttons inside asset rows */
.row-btn button {
    padding: 6px 10px !important;
    font-size: 11px !important;
    background: rgba(239,68,68,0.12) !important;
    color: var(--accent-red) !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
}

.add-btn button {
    background: transparent !important;
    color: var(--accent) !important;
    border: 1px dashed var(--border) !important;
    width: 100% !important;
}

.add-btn button:hover {
    background: var(--accent-dim) !important;
    box-shadow: none !important;
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

/* ==========================================================
   TOOLTIPS (icône "?" + info-bulle au survol des champs)
   Streamlit rend ça via BaseWeb — on force la visibilité et
   le style pour matcher le design (fond sombre, bord teal).
   ========================================================== */

[data-testid="stTooltipIcon"],
[data-testid="stTooltipHoverTarget"] svg {
    color: var(--accent) !important;
    fill: var(--accent) !important;
    opacity: 0.9 !important;
}

[data-testid="stTooltipIcon"]:hover,
[data-testid="stTooltipHoverTarget"]:hover svg {
    opacity: 1 !important;
}

/* Le popover Streamlit s'affiche dans un portail à la racine du DOM (pas
   forcément dans .stApp), donc on cible large et on force le fond à TOUS
   les niveaux d'imbrication (popover > wrapper > contenu markdown). */
div[data-baseweb="popover"],
div[data-baseweb="popover"] div,
div[data-baseweb="tooltip"],
div[data-baseweb="tooltip"] div,
[role="tooltip"],
[role="tooltip"] div,
[data-testid="stTooltipContent"],
[data-testid="stTooltipContent"] * {
    background-color: #0d1720 !important;
    background: #0d1720 !important;
    color: #eef4f8 !important;
}

div[data-baseweb="popover"],
div[data-baseweb="tooltip"],
[role="tooltip"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.55) !important;
    padding: 12px 16px !important;
    max-width: 280px !important;
    z-index: 999999 !important;
}

div[data-baseweb="popover"] *,
div[data-baseweb="tooltip"] *,
[role="tooltip"] * {
    color: #eef4f8 !important;
    font-family: var(--font-ui) !important;
    font-size: 12.5px !important;
    line-height: 1.6 !important;
}

</style>
""")

# ========== TOP NAV BAR ==========
html("""
<div class="nav-bar">
    <div class="nav-brand">
        <div class="nav-glyph">◈</div>
        <div>
            <div class="nav-title">LP DASHBOARD</div>
            <div class="nav-subtitle"><span class="status-dot"></span>LIVE · RECOVERY SIMULATOR · TOUTE PAIRE</div>
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
""")

# ========== HELPERS ==========

def sec(icon, label, sub=None):
    html(f"""
    <div class="sec-head">
        <div class="sec-head-icon">{icon}</div>
        <div class="sec-head-label">{label}</div>
    </div>""")
    if sub:
        st.markdown(f"<div class='sec-sub'>{sub}</div>", unsafe_allow_html=True)

def tile(label, value, sub="", value_class="m-value"):
    # IMPORTANT : tout sur une seule ligne, sans indentation — un HTML multi-ligne
    # indenté ici est interprété comme un bloc de code par le moteur Markdown
    # de Streamlit dès que plusieurs tuiles sont concaténées.
    sub_html = f'<div class="m-sub">{sub}</div>' if sub else ""
    return f'<div class="m-card"><div class="m-label">{label}</div><div class="{value_class}">{value}</div>{sub_html}</div>'

def tile_grid(tiles_html):
    st.markdown(f'<div class="tile-grid">{"".join(tiles_html)}</div>', unsafe_allow_html=True)

SECRET_CODE = st.secrets["Secret_Code"]

# ========== INIT SESSION STATE ==========
for k, v in [
    ("authenticated", False), ("content", []), ("finished", False),
    ("disclaimer_shown", False), ("secret_content", []),
    ("checklist_validee", False), ("checklist_content", []),
    ("extra_collaterals", []), ("extra_borrows", []),
    ("col_counter", 0), ("bor_counter", 0),
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
        "  [✓] Pool générique Token A / Token B",
        "  [✓] Position LP | Range & Prix | Perte impermanente",
        "  [✓] Comparaison de stratégies post-sortie de range",
        "  [✓] Collatéral & levier multi-actifs (alternative au rebalancing)",
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

html("""
<div class="disc-bar">
  <span>⚠</span> Cet outil montre comment une position LP peut perdre malgré un APR affiché élevé, pas comment gagner à coup sûr.
</div>
""")

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

html("""
<div class="disc-bar" style="border-color:var(--accent); color:var(--accent);">
  <span>◈</span> ACCÈS AUTORISÉ — Bonjour et bienvenue !
</div>
""")

# ========== CHECKLIST ==========
checklist_items = [
    "Je comprends que mon capital n'est productif que lorsqu'il est dans le range",
    "J'ai défini un range cohérent avec la volatilité actuelle et la tendance du marché",
    "Je sais qu'un range trop étroit augmente les fees mais réduit le temps dans le range",
    "Je sais qu'un range trop large réduit le rendement",
    "Je comprends que hors range, ma position ne génère plus aucun frais",
    "J'ai évalué la perte impermanente déjà verrouillée sur ma position",
    "Je comprends les 4 façons de rejouer la suite (LP, spot, BTC, sortie)",
    "Si j'utilise l'option collatéral & levier, je comprends le risque de liquidation",
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

html("""
<div class="disc-bar">
  <span>◈</span> déverrouillage du dashboard...
</div>
""")

# ----------------------------------------------------------------------
# Fonctions de calcul — mécanique Uniswap v3 (liquidité concentrée)
# Convention : "P" est le prix de Token A exprimé en Token B (P = prix_A / prix_B)
# ----------------------------------------------------------------------

def lp_amounts(P, L, p_lower, p_upper):
    """Retourne (montant Token A, montant Token B) détenus par la position à un prix de pool P donné."""
    sqrt_p = math.sqrt(max(P, 1e-12))
    sqrt_pa = math.sqrt(p_lower)
    sqrt_pb = math.sqrt(p_upper)

    if P <= p_lower:
        x = L * (1 / sqrt_pa - 1 / sqrt_pb)   # tout en Token A
        y = 0.0
    elif P >= p_upper:
        x = 0.0
        y = L * (sqrt_pb - sqrt_pa)            # tout en Token B
    else:
        x = L * (1 / sqrt_p - 1 / sqrt_pb)
        y = L * (sqrt_p - sqrt_pa)
    return x, y


def compute_liquidity(deposit_in_b, P0, p_lower, p_upper):
    """Déduit L à partir du montant déposé à l'entrée, exprimé en unités de Token B (P0 doit être dans la range)."""
    sqrt_p0 = math.sqrt(P0)
    sqrt_pa = math.sqrt(p_lower)
    sqrt_pb = math.sqrt(p_upper)
    denom = (1 / sqrt_p0 - 1 / sqrt_pb) * P0 + (sqrt_p0 - sqrt_pa)
    return deposit_in_b / denom


def lp_value_usd(prix_a, prix_b, L, p_lower, p_upper):
    """Valeur en $ de la position LP pour des prix (en $) de Token A et Token B donnés."""
    P = prix_a / prix_b
    x, y = lp_amounts(P, L, p_lower, p_upper)
    return x * prix_a + y * prix_b


# ----------------------------------------------------------------------
# UI — Section "Ta position"
# ----------------------------------------------------------------------

sec("◎", "TA POSITION LP",
    "Renseigne les deux actifs de ta pool Uniswap v3. Les valeurs par défaut (WETH/USDC) sont un exemple — remplace-les par ta propre paire.")

col_sym_a, col_sym_b = st.columns(2)
with col_sym_a:
    token_a_symbol = st.text_input(
        "Nom du Token A (volatile)", value="WETH",
        help="L'actif le plus volatile de la paire. Exemple : WETH, BTC, SOL. C'est le token que vous accumulez lors des baisses et que vous revendez lors des hausses."
    ).strip() or "TOKEN A"
with col_sym_b:
    token_b_symbol = st.text_input(
        "Nom du Token B (référence)", value="USDC",
        help="Le second actif de la pool, souvent un stablecoin (USDC). Le prix de la pool est exprimé en Token B par Token A."
    ).strip() or "TOKEN B"

st.markdown(
    f"Ta position de liquidité concentrée **{token_a_symbol}/{token_b_symbol}** est sortie de sa range. "
    "Cet outil montre la perte impermanente déjà verrouillée, le temps "
    "nécessaire pour la récupérer via les frais, et ce qui arrive à ton "
    "capital selon quatre manières de jouer la suite."
)

col_price_a, col_price_b = st.columns(2)
with col_price_a:
    st.markdown(f"**Prix de {token_a_symbol} ($)**")
    prix_a_entry = st.number_input(
        f"{token_a_symbol} — prix d'entrée ($)", min_value=0.000001, value=2200.0, step=10.0,
        help=f"Prix de {token_a_symbol} en dollars au moment où tu as ouvert ta position LP."
    )
    prix_a_now = st.number_input(
        f"{token_a_symbol} — prix actuel ($)", min_value=0.000001, value=1700.0, step=10.0,
        help=f"Prix actuel de {token_a_symbol} en dollars."
    )
    prix_a_target = st.number_input(
        f"{token_a_symbol} — prix cible / futur ($)", min_value=0.000001, value=2000.0, step=10.0,
        help=f"Le prix que tu veux tester pour {token_a_symbol} dans le scénario futur (ex. un objectif de retour de prix)."
    )
with col_price_b:
    st.markdown(f"**Prix de {token_b_symbol} ($)**")
    prix_b_entry = st.number_input(
        f"{token_b_symbol} — prix d'entrée ($)", min_value=0.000001, value=1.0, step=0.01,
        help=f"Prix de {token_b_symbol} en dollars au moment de l'entrée. Laisse 1.0 si c'est un stablecoin."
    )
    prix_b_now = st.number_input(
        f"{token_b_symbol} — prix actuel ($)", min_value=0.000001, value=1.0, step=0.01,
        help=f"Prix actuel de {token_b_symbol} en dollars. Laisse 1.0 si c'est un stablecoin."
    )
    prix_b_target = st.number_input(
        f"{token_b_symbol} — prix cible / futur ($)", min_value=0.000001, value=1.0, step=0.01,
        help=f"Le prix que tu veux tester pour {token_b_symbol} dans le scénario futur. Laisse 1.0 si c'est un stablecoin."
    )

col1, col2, col3 = st.columns(3)
with col1:
    deposit = st.number_input(
        "Montant déposé ($)", min_value=0.0, value=10_000.0, step=100.0,
        help="Valeur totale en dollars que tu as déposée dans la position LP à l'ouverture."
    )
with col2:
    range_width_pct = st.slider(
        "Largeur de range (±%)", min_value=1, max_value=80, value=15,
        help="Amplitude de ta range autour du prix d'entrée. Un range étroit concentre les frais mais sort plus vite de la range ; un range large reste plus longtemps actif mais dilue le rendement."
    )
with col3:
    fee_apr = st.number_input(
        "APR de frais quand dans le range (%)", min_value=0.0, value=20.0, step=1.0,
        help="Rendement annualisé en frais de swap généré par la position UNIQUEMENT lorsqu'elle est dans le range. Utilisé pour estimer le temps de récupération de l'IL."
    )

col4, col5 = st.columns(2)
with col4:
    btc_price = st.number_input(
        "Prix actuel du BTC ($)", min_value=0.01, value=60000.0, step=100.0,
        help="Prix actuel du BTC, utilisé uniquement pour la stratégie de comparaison 'Moitié → BTC'."
    )
with col5:
    btc_rel_strength = st.slider(
        "Force relative du BTC", min_value=0.0, max_value=2.0, value=0.85, step=0.05,
        help=f"1.0 = le BTC suit exactement les variations de {token_a_symbol} · <1 = le BTC est à la traîne · >1 = le BTC amplifie les mouvements de {token_a_symbol}.",
    )

html(f"""
<div class="info-box">
  <b>Ce que change la force relative du BTC :</b> ce curseur ne fixe pas un prix, il fixe une <b>sensibilité</b>.
  Si {token_a_symbol} bouge de +30% et que la force relative est réglée à <b>1.5</b>, le BTC est simulé comme bougeant de +45%
  (il amplifie la hausse — mais amplifierait aussi une baisse). À <b>0.5</b>, le BTC ne bougerait que de +15% :
  il protège en cas de baisse de {token_a_symbol} mais capte moins d'upside en cas de hausse.
  Concrètement, plus la valeur est haute, plus la stratégie « Moitié → BTC » devient un pari directionnel volatil ;
  plus elle est basse, plus cette moitié du portefeuille se comporte comme un amortisseur.
</div>
""")

# Range de la position (le prix de pool P = prix_A / prix_B)
P_entry = prix_a_entry / prix_b_entry
P_now = prix_a_now / prix_b_now
P_target = prix_a_target / prix_b_target

p_lower = P_entry * (1 - range_width_pct / 100)
p_upper = P_entry * (1 + range_width_pct / 100)
out_of_range = P_now <= p_lower or P_now >= p_upper

value_b_deposit = deposit / prix_b_entry
L = compute_liquidity(value_b_deposit, P_entry, p_lower, p_upper)
x0, y0 = lp_amounts(P_entry, L, p_lower, p_upper)          # avoirs à l'entrée
x_now, y_now = lp_amounts(P_now, L, p_lower, p_upper)      # avoirs actuels

lp_value_now = x_now * prix_a_now + y_now * prix_b_now
hodl_value_now = x0 * prix_a_now + y0 * prix_b_now  # aurait valu si on avait juste détenu x0/y0 sans bouger
il_dollar = lp_value_now - hodl_value_now
il_pct = (il_dollar / hodl_value_now * 100) if hodl_value_now else 0.0

daily_fee = lp_value_now * (fee_apr / 100) / 365
recoup_days = abs(il_dollar) / daily_fee if daily_fee > 0 else float("inf")

st.divider()

tile_grid([
    tile(
        "Statut de la position",
        "Hors range" if out_of_range else "Dans le range",
        f"Range : {p_lower:,.6f} — {p_upper:,.6f} {token_b_symbol}/{token_a_symbol}",
        "m-value-red" if out_of_range else "m-value-green",
    ),
    tile(
        "Perte impermanente verrouillée",
        f"${il_dollar:,.0f}",
        f"{il_pct:,.1f}%",
        "m-value-red" if il_dollar < 0 else "m-value-green",
    ),
    tile(
        "Récupération par les frais",
        f"{recoup_days:,.0f} jours" if math.isfinite(recoup_days) else "—",
        "Valable une fois revenu dans le range — hors range, la position ne génère aucun frais.",
        "m-value-amber",
    ),
])

st.caption(
    f"Répartition actuelle : {x_now:,.4f} {token_a_symbol} (${x_now*prix_a_now:,.0f}) · "
    f"{y_now:,.4f} {token_b_symbol} (${y_now*prix_b_now:,.0f})"
)

# ----------------------------------------------------------------------
# Comparaison des 4 stratégies
# ----------------------------------------------------------------------

sec("◫", "COMPARAISON DES STRATÉGIES",
    f"Valeur du portefeuille selon la trajectoire de prix de {token_a_symbol} — pour chacune des 4 stratégies. "
    f"Pour isoler l'effet du prix de {token_a_symbol}, le graphique suppose {token_b_symbol} constant au prix actuel "
    f"(${prix_b_now:,.4f}). Le tableau de scénario exact ci-dessous, lui, utilise tes deux prix cibles.")

price_a_range = np.linspace(prix_a_now * 0.3, prix_a_now * 2.5, 200)

# 1. Rester dans le LP
stay_lp = [lp_value_usd(p, prix_b_now, L, p_lower, p_upper) for p in price_a_range]

# 2. Retirer et détenir Token A spot (tout converti en Token A au prix actuel)
qty_a_hodl_now = lp_value_now / prix_a_now
hold_a = [qty_a_hodl_now * p for p in price_a_range]

# 3. Moitié -> BTC
half_usd = lp_value_now / 2
a_half_amount = half_usd / prix_a_now
btc_amount = half_usd / btc_price
half_btc = [
    a_half_amount * p + btc_amount * (btc_price * (1 + btc_rel_strength * (p / prix_a_now - 1)))
    for p in price_a_range
]

# 4. Sortir et détenir Token B (valeur figée au moment de la sortie, en unités de Token B)
qty_b_hodl_now = lp_value_now / prix_b_now
exit_b = [qty_b_hodl_now * prix_b_now for _ in price_a_range]  # B supposé constant sur ce graphique

strategies = {
    "Rester dans le LP": stay_lp,
    f"Détenir {token_a_symbol} spot": hold_a,
    "Moitié → BTC": half_btc,
    f"Sortir en {token_b_symbol}": exit_b,
}

selected = st.multiselect(
    "Stratégies à afficher", list(strategies.keys()), default=list(strategies.keys()),
    help="Choisis les courbes à comparer sur le graphique."
)

fig = go.Figure()
for name in selected:
    fig.add_trace(go.Scatter(x=price_a_range, y=strategies[name], mode="lines", name=name))

fig.add_vline(x=prix_a_now, line_dash="dot", line_color="gray",
              annotation_text="prix actuel", annotation_position="top left")
fig.add_vline(x=prix_a_target, line_dash="dot", line_color="orange",
              annotation_text="prix cible", annotation_position="top right")

fig.update_layout(
    template="plotly_dark",
    xaxis_title=f"Prix {token_a_symbol} ($)",
    yaxis_title="Valeur du portefeuille ($)",
    height=520,
    margin=dict(t=60, b=90),
    legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig, use_container_width=True)

# Valeurs exactes au scénario cible (utilise les DEUX prix cibles saisis, A et B)
st.subheader(f"Scénario exact — {token_a_symbol} → ${prix_a_target:,.4f} et {token_b_symbol} → ${prix_b_target:,.4f}")

x_t, y_t = lp_amounts(P_target, L, p_lower, p_upper)
btc_price_target = btc_price * (1 + btc_rel_strength * (prix_a_target / prix_a_now - 1))

target_values = {
    "Rester dans le LP": x_t * prix_a_target + y_t * prix_b_target,
    f"Détenir {token_a_symbol} spot": qty_a_hodl_now * prix_a_target,
    "Moitié → BTC": a_half_amount * prix_a_target + btc_amount * btc_price_target,
    f"Sortir en {token_b_symbol}": qty_b_hodl_now * prix_b_target,
}

tile_grid([tile(name, f"${val:,.0f}") for name, val in target_values.items()])

# ----------------------------------------------------------------------
# Collatéral & levier — alternative au rebalancing
# ----------------------------------------------------------------------

sec("⚡", "COLLATÉRAL & LEVIER — ALTERNATIVE AU REBALANCING")

html("""
<div class="info-box">
  <b>Pourquoi cette option plutôt qu'un rebalancing ?</b> Rebalancer une position hors range implique de la retirer,
  de swapper une partie des actifs pour revenir à un ratio 50/50, puis de rouvrir un nouveau range — ce qui
  <b>réalise définitivement la perte</b> et paie des frais de swap supplémentaires. L'alternative consiste à sortir
  tout ou partie de la position <b>sans vendre</b> : tu déposes le ou les actifs obtenus en collatéral sur un
  protocole de lending (ex. Aave), tu empruntes contre ce collatéral, puis tu redéploies le capital emprunté pour
  générer un rendement additionnel. Tu conserves ainsi <b>100% de l'exposition à la hausse</b> de ton collatéral,
  tout en faisant travailler le capital emprunté — au prix d'un risque de liquidation si le prix baisse trop.
</div>
""")

# ---------- Collatéral : ligne de base (Token A) + lignes ajoutées ----------
st.markdown("**Actifs en collatéral**")
head = st.columns([1.3, 1, 1, 1, 0.8, 0.8, 0.9, 0.4])
for c, h in zip(head, ["Actif", "Quantité", "Prix actuel ($)", "Prix cible ($)", "LTV %", "Liq. %", "Rend. natif %", ""]):
    c.markdown(f"<div class='list-head'>{h}</div>", unsafe_allow_html=True)

base_row = st.columns([1.3, 1, 1, 1, 0.8, 0.8, 0.9, 0.4])
base_row[0].markdown(
    f"<div style='padding-top:8px;'><b>{token_a_symbol}</b><br>"
    f"<span style='font-size:10px;color:var(--text-mid);'>issu de ta position</span></div>",
    unsafe_allow_html=True,
)
base_row[1].markdown(f"<div style='padding-top:8px;'>{qty_a_hodl_now:,.4f}</div>", unsafe_allow_html=True)
base_row[2].markdown(f"<div style='padding-top:8px;'>${prix_a_now:,.4f}</div>", unsafe_allow_html=True)
base_row[3].markdown(f"<div style='padding-top:8px;'>${prix_a_target:,.4f}</div>", unsafe_allow_html=True)
base_ltv = base_row[4].number_input(
    "LTV base", min_value=1, max_value=90, value=50, step=1, label_visibility="collapsed", key="base_ltv",
    help=f"Loan-to-Value appliqué à ton {token_a_symbol} en collatéral : quel % de sa valeur tu peux emprunter."
)
base_liq = base_row[5].number_input(
    "Liq base", min_value=1, max_value=95, value=80, step=1, label_visibility="collapsed", key="base_liq",
    help=f"Seuil de liquidation défini par le protocole de lending pour {token_a_symbol}."
)
base_native = base_row[6].number_input(
    "Rend base", min_value=0.0, value=0.0, step=0.5, label_visibility="collapsed", key="base_native",
    help=f"Rendement natif (ex. staking) que {token_a_symbol} génère simplement en le détenant en collatéral, en plus de sa variation de prix."
)

collateral_rows = [{
    "symbol": token_a_symbol, "qty": qty_a_hodl_now, "price_now": prix_a_now,
    "price_target": prix_a_target, "ltv": base_ltv, "liq": base_liq, "native_apy": base_native,
}]

for item in list(st.session_state.extra_collaterals):
    uid = item["uid"]
    row = st.columns([1.3, 1, 1, 1, 0.8, 0.8, 0.9, 0.4])
    symbol = row[0].text_input(
        "sym", value=item.get("symbol", ""), label_visibility="collapsed", key=f"col_sym_{uid}",
        placeholder="ex. stETH", help="Symbole de cet actif additionnel mis en collatéral."
    )
    qty = row[1].number_input(
        "qty", value=item.get("qty", 0.0), min_value=0.0, step=0.01, label_visibility="collapsed",
        key=f"col_qty_{uid}", help="Quantité de cet actif que tu détiens et comptes déposer en collatéral."
    )
    price_now_i = row[2].number_input(
        "pn", value=item.get("price_now", 1.0), min_value=0.000001, step=0.01, label_visibility="collapsed",
        key=f"col_pn_{uid}", help="Prix actuel de cet actif en dollars."
    )
    price_target_i = row[3].number_input(
        "pt", value=item.get("price_target", 1.0), min_value=0.000001, step=0.01, label_visibility="collapsed",
        key=f"col_pt_{uid}", help="Prix cible testé pour cet actif dans le scénario futur."
    )
    ltv_i = row[4].number_input(
        "ltv", value=item.get("ltv", 50), min_value=1, max_value=90, step=1, label_visibility="collapsed",
        key=f"col_ltv_{uid}", help="LTV applicable à cet actif sur le protocole de lending."
    )
    liq_i = row[5].number_input(
        "liq", value=item.get("liq", 80), min_value=1, max_value=95, step=1, label_visibility="collapsed",
        key=f"col_liq_{uid}", help="Seuil de liquidation de cet actif."
    )
    native_i = row[6].number_input(
        "nat", value=item.get("native_apy", 0.0), min_value=0.0, step=0.5, label_visibility="collapsed",
        key=f"col_nat_{uid}", help="Rendement natif (staking) de cet actif, en plus de sa variation de prix."
    )
    with row[7]:
        st.markdown('<div class="row-btn">', unsafe_allow_html=True)
        if st.button("🗑", key=f"col_del_{uid}"):
            st.session_state.extra_collaterals = [c for c in st.session_state.extra_collaterals if c["uid"] != uid]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    collateral_rows.append({
        "symbol": symbol or "ACTIF", "qty": qty, "price_now": price_now_i,
        "price_target": price_target_i, "ltv": ltv_i, "liq": liq_i, "native_apy": native_i,
    })

st.markdown('<div class="add-btn">', unsafe_allow_html=True)
if st.button("➕ Ajouter un actif en collatéral", key="add_collateral"):
    st.session_state.col_counter += 1
    st.session_state.extra_collaterals.append({"uid": st.session_state.col_counter})
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Emprunt : lignes ajoutées librement ----------
st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
st.markdown("**Actifs empruntés**")

if not st.session_state.extra_borrows:
    st.caption("Aucun emprunt ajouté — clique sur « + » pour simuler un emprunt contre ton collatéral.")
else:
    head_b = st.columns([1.3, 1, 1, 1, 0.4])
    for c, h in zip(head_b, ["Actif emprunté", "Quantité empruntée", "Prix actuel ($)", "APR d'emprunt %", ""]):
        c.markdown(f"<div class='list-head'>{h}</div>", unsafe_allow_html=True)

borrow_rows = []
for item in list(st.session_state.extra_borrows):
    uid = item["uid"]
    row = st.columns([1.3, 1, 1, 1, 0.4])
    symbol = row[0].text_input(
        "bsym", value=item.get("symbol", token_b_symbol), label_visibility="collapsed", key=f"bor_sym_{uid}",
        placeholder="ex. USDC", help="Symbole de l'actif que tu empruntes contre ton collatéral."
    )
    qty = row[1].number_input(
        "bqty", value=item.get("qty", 0.0), min_value=0.0, step=1.0, label_visibility="collapsed",
        key=f"bor_qty_{uid}", help="Quantité de cet actif que tu empruntes."
    )
    price_now_i = row[2].number_input(
        "bpn", value=item.get("price_now", 1.0), min_value=0.000001, step=0.01, label_visibility="collapsed",
        key=f"bor_pn_{uid}", help="Prix actuel de l'actif emprunté en dollars. Laisse 1.0 si c'est un stablecoin."
    )
    apr_i = row[3].number_input(
        "bapr", value=item.get("apr", 6.0), min_value=0.0, step=0.5, label_visibility="collapsed",
        key=f"bor_apr_{uid}", help="Taux d'intérêt annuel payé sur cette dette."
    )
    with row[4]:
        st.markdown('<div class="row-btn">', unsafe_allow_html=True)
        if st.button("🗑", key=f"bor_del_{uid}"):
            st.session_state.extra_borrows = [b for b in st.session_state.extra_borrows if b["uid"] != uid]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    borrow_rows.append({"symbol": symbol or "DETTE", "qty": qty, "price_now": price_now_i, "apr": apr_i})

st.markdown('<div class="add-btn">', unsafe_allow_html=True)
if st.button("➕ Ajouter un actif emprunté", key="add_borrow"):
    st.session_state.bor_counter += 1
    st.session_state.extra_borrows.append({"uid": st.session_state.bor_counter})
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
colD, colE = st.columns(2)
with colD:
    deploy_apy = st.number_input(
        "APY du capital redéployé (%)", min_value=0.0, value=12.0, step=0.5,
        help="Rendement annualisé obtenu en réutilisant la valeur totale empruntée (ex. farming, prêt, autre stratégie)."
    )
with colE:
    horizon_months = st.slider(
        "Horizon (mois)", min_value=1, max_value=36, value=12,
        help="Durée sur laquelle tu simules cette stratégie de collatéral et levier."
    )

# ---------- Calculs agrégés ----------
t = horizon_months / 12

total_collateral_now = sum(r["qty"] * r["price_now"] for r in collateral_rows)
total_collateral_target = sum(r["qty"] * r["price_target"] for r in collateral_rows)
total_borrow_capacity = sum(r["qty"] * r["price_now"] * r["ltv"] / 100 for r in collateral_rows)
total_liq_weighted = sum(r["qty"] * r["price_now"] * r["liq"] / 100 for r in collateral_rows)
collateral_native_yield = sum(r["qty"] * r["price_now"] * (r["native_apy"] / 100 * t) for r in collateral_rows)

total_debt_now = sum(b["qty"] * b["price_now"] for b in borrow_rows)
total_debt_future = sum(b["qty"] * b["price_now"] * (1 + b["apr"] / 100 * t) for b in borrow_rows)

deployed_value = total_debt_now * (1 + deploy_apy / 100 * t)

health_factor = total_liq_weighted / total_debt_now if total_debt_now > 0 else float("inf")
marge_liquidation_pct = (health_factor - 1) * 100 if math.isfinite(health_factor) else float("inf")

net_equity_target = total_collateral_target - total_debt_future + deployed_value + collateral_native_yield
edge_vs_hold = deployed_value - total_debt_future

st.divider()

tiles = [
    tile("Capacité d'emprunt totale", f"${total_borrow_capacity:,.0f}", "Basée sur le LTV de chaque actif en collatéral"),
    tile("Dette actuelle", f"${total_debt_now:,.0f}"),
    tile("Dette au terme (+ intérêts)", f"${total_debt_future:,.0f}", f"Horizon : {horizon_months} mois"),
]
if total_debt_now > 0:
    tiles += [
        tile(
            "Health factor", f"{health_factor:,.2f}", "1.0 = liquidation",
            "m-value-red" if health_factor < 1.1 else "m-value-green",
        ),
        tile(
            "Marge avant liquidation", f"{marge_liquidation_pct:,.1f}%",
            "Approximation : suppose une baisse uniforme de tous les collatéraux",
            "m-value-red" if marge_liquidation_pct < 10 else "m-value-amber",
        ),
    ]
tiles += [
    tile("Équité nette au scénario cible", f"${net_equity_target:,.0f}"),
    tile(
        "Avantage vs. détenir sans levier", f"${edge_vs_hold:,.0f}", "",
        "m-value-green" if edge_vs_hold >= 0 else "m-value-red",
    ),
]
tile_grid(tiles)

if total_debt_now == 0:
    st.caption("Ajoute au moins un actif emprunté pour calculer le health factor et la marge avant liquidation.")
elif health_factor < 1.1:
    st.warning("Health factor proche ou sous 1.0 — risque de liquidation élevé avec ces paramètres.")
