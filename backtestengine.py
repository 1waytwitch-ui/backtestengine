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
import time
import random

# Forcer mode écran large
st.set_page_config(layout="wide")

# --------- CONFIG ----------
st.set_page_config(
    page_title="BACKTEST ENGINE LP",
    page_icon="💧",
    layout="centered"
)

# ---- HEADER FIXE ----
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




# --- résumé ---
# --- STYLE ---
st.markdown("""
<style>
body {
    background-color: #0b0f0c;
}

.terminal {
    background-color: #000000;
    color: #00ff88;
    font-family: monospace;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 0 15px rgba(0,255,150,0.15);
    font-size: 14px;
    line-height: 1.4;

    max-height: 450px;
    overflow-y: auto;
}

.cursor {
    display: inline-block;
    width: 10px;
    background-color: #00ff88;
    margin-left: 5px;
    animation: blink 1s infinite;
}

@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0; }
    100% { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# --- STATE ---
if "content" not in st.session_state:
    st.session_state.content = []
    st.session_state.finished = False

if "disclaimer_shown" not in st.session_state:
    st.session_state.disclaimer_shown = False

terminal_placeholder = st.empty()

def render():
    terminal_placeholder.markdown(
        """
        <div id='terminal' class='terminal'>
        """ + "<br>".join(st.session_state.content) + """
        <span class='cursor'></span>
        </div>

        <script>
        const term = document.getElementById("terminal");
        if (term) {
            term.scrollTop = term.scrollHeight;
        }
        </script>
        """,
        unsafe_allow_html=True
    )

# --- TYPING REALISTE ---
def type_line(line):
    current = ""
    for char in line:
        current += char
        st.session_state.content[-1] = current
        render()
        time.sleep(random.uniform(0.008, 0.03))

# --- GLITCH SUBTIL ---
def subtle_glitch(line, chance=0.2):
    if random.random() < chance:
        chars = list("█▓▒░<>/\\|#@$%&*")
        glitched = "".join(random.choice(chars) for _ in range(len(line)))
        st.session_state.content[-1] = glitched
        render()
        time.sleep(0.05)

# --- AJOUT LIGNE ---
def add_line(line, glitch=False):
    st.session_state.content.append("")
    if glitch:
        subtle_glitch(line)
    type_line(line)
    time.sleep(random.uniform(0.05, 0.2))

# --- LOADING BAR ---
def loading_bar(total=20):
    bar = ["░"] * total
    for i in range(total):
        bar[i] = "█"
        line = "> decrypting disclaimer... [" + "".join(bar) + "]"
        st.session_state.content[-1] = line
        render()
        time.sleep(0.06)

# --- ANIMATION PRINCIPALE ---
if not st.session_state.finished:

    add_line("$ backtest-engine-lp --update", glitch=True)

    add_line("> Modules chargés :")

    tools = [
        "✔ Pool Setup | Price & Range | Automation avancée",
        "✔ IL Simulator | APR réel | ATR avancée",
        "✔ Break Even | Zeroswap Rebalance | Refill LP",
        "✔ Guide complet + Atelier vidéo IL & Calculatrice"
    ]

    for t in tools:
        add_line(t)

    add_line("> Vérification des nouveautés...")

    updates = [
        "✔ LP Health Score activé",
        "✔ Auto Range disponible",
        "✔ Optimal Range Finder ajouté"
    ]

    for u in updates:
        add_line(u)

    add_line('$ echo "Optimisation des outils en cours..."', glitch=True)
    add_line("Optimisation des outils en cours... vous pouvez optimiser vos stratégies")

    st.session_state.finished = True


# --- DISCLAIMER FX ---
if st.session_state.finished and not st.session_state.disclaimer_shown:

    add_line("> Initializing secure buffer...", glitch=True)

    st.session_state.content.append("")
    loading_bar()

    add_line("> ACCESSING ENCRYPTED DISCLAIMER FILE", glitch=True)

    disclaimer_lines = [
        "",
        "$ cat disclaimer.txt",
        "> [!] SYSTEM WARNING — DISCLAIMER LOADED",
        "> ----------------------------------------",
        "> ⚠️ DISCLAIMER IMPORTANT",
        ">",
        "> Un backtest en DeFi n’explique pas comment gagner,",
        "> mais comment une stratégie peut perdre malgré des APY élevés.",
        ">",
        "> Accès réservé aux membres Team Élite (KBOUR Crypto)",
        "> Code disponible dans le canal privé 'DEFI Académie'",
        ">",
        "> Cet outil peut contenir des approximations",
        "> Ceci n’est PAS un conseil en investissement",
        ">",
        "> Faites vos propres recherches (DYOR)",
        "> Comprenez les risques des pools de liquidités concentrés",
        ">",
        "> Si l’API est surchargée → saisie manuelle requise",
        "> ----------------------------------------"
    ]

    for line in disclaimer_lines:
        add_line(line)

    st.session_state.disclaimer_shown = True

# ======= DISCLAIMER fixe ======
st.markdown("""
<div style='color:#00ff88; font-family:monospace; font-size:13px; margin-top:10px;'>
> Un backtest en DeFi n’explique pas comment gagner, mais comment une stratégie peut perdre malgré des APY élevés.
</div>
""", unsafe_allow_html=True)


# -----------------------
# CODE SECRET - THEME TERMINAL AVEC BOUTON VALIDER + TYPING
# -----------------------
SECRET_CODE = st.secrets["Secret_Code"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "secret_content" not in st.session_state:
    st.session_state.secret_content = []

terminal_placeholder = st.empty()

# ======= RENDER ======
def render():
    terminal_placeholder.markdown(
        """
        <div id='secret-terminal' class='checklist-terminal'>
        """ + "<br>".join(st.session_state.secret_content) + """
        <span class='cursor'></span>
        </div>
        <script>
        const term = document.getElementById("secret-terminal");
        if (term) { term.scrollTop = term.scrollHeight; }
        </script>
        """,
        unsafe_allow_html=True
    )

# ======= STYLE TERMINAL ======
st.markdown("""
<style>
.checklist-terminal {
    background-color: #000000;
    border: 1px solid #00ff88;
    border-radius: 8px;
    padding: 15px;
    margin-top: 20px;
    box-shadow: 0 0 12px rgba(0,255,150,0.15);
    font-family: monospace;
    font-size: 13px;
    line-height: 1.3;
    max-height: 400px;
    overflow-y: auto;
}
.cursor {
    display: inline-block;
    width: 8px;
    background-color: #00ff88;
    margin-left: 3px;
    animation: blink 1s infinite;
}
@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0; }
    100% { opacity: 1; }
}
.stButton>button {
    background-color: black;
    color: #00ff88;
    border: 1px solid #00ff88;
    font-family: monospace;
}
</style>
""", unsafe_allow_html=True)

# ======= TYPING / GLITCH ======
def type_line(line):
    st.session_state.secret_content.append("")
    current = ""
    for char in line:
        current += char
        st.session_state.secret_content[-1] = current
        render()
        time.sleep(random.uniform(0.01, 0.03))

def subtle_glitch(line, chance=0.15):
    if not st.session_state.secret_content:
        return  # ✅ sécurité ajoutée

    if random.random() < chance:
        chars = list("█▓▒░<>/\\|#@$%&*")
        glitched = "".join(random.choice(chars) for _ in range(len(line)))
        st.session_state.secret_content[-1] = glitched
        render()
        time.sleep(0.03)

def add_line(line, glitch=False):
    type_line(line)  # ✅ corrigé (avant glitch)
    if glitch:
        subtle_glitch(line)
    time.sleep(random.uniform(0.05, 0.15))

# ======= TERMINAL AUTHENTICATION ======
if not st.session_state.authenticated:

    if not st.session_state.secret_content:
        add_line("$ ACCESS PROTOCOL INITIALIZATION", glitch=True)
        add_line("> Vérification des droits de la Team Élite KBOUR Crypto...")
        add_line("> Veuillez saisir le code d'accès ci-dessous")

    # INPUT STREAMLIT
    code_input = st.text_input("Code d'accès", key="secret_code", type="password")

    # BOUTON STREAMLIT
    if st.button("Valider", use_container_width=True):
        if code_input == SECRET_CODE:
            st.session_state.authenticated = True
            st.rerun()
        else:
            add_line("> [!] CODE INCORRECT", glitch=True)
            st.error("Code incorrect")
    st.stop()

# ======= UNLOCK MESSAGE ======
st.markdown("""
<div style='color:#00ff88; font-family:monospace; font-size:13px; margin-top:10px;'>
> ACCÈS AUTORISÉ — Bonjour et bienvenue !
</div>
""", unsafe_allow_html=True)

# ======= STYLE CHECKLIST TERMINAL ======
# Forcer mode écran large
st.set_page_config(layout="wide")

st.markdown("""
<style>
.checklist-terminal {
    background-color: #000000;
    border: 1px solid #00ff88;
    border-radius: 8px;
    padding: 10px;
    margin-top: 15px;
    box-shadow: 0 0 10px rgba(0,255,150,0.1);
    font-family: monospace;
    font-size: 12px;
    line-height: 1.3;
    max-height: 450px;
    overflow-y: auto;
}
.checklist-header {
    color: #00ff88;
    font-size: 14px;
    margin-bottom: 8px;
}
.stButton>button {
    background-color: black;
    color: #00ff88;
    border: 1px solid #00ff88;
    font-family: monospace;
}
.warning-box {
    background-color:#000000;
    border:1px solid #00ff88;
    border-radius:6px;
    padding:10px;
    color:#00ff88;
    font-family: monospace;
    font-size:12px;
    margin-bottom:15px;
}
.cursor {
    display: inline-block;
    width: 8px;
    background-color: #00ff88;
    margin-left: 3px;
    animation: blink 1s infinite;
}
@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0; }
    100% { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# ======= STATE ======
if "checklist_validee" not in st.session_state:
    st.session_state.checklist_validee = False
if "checklist_content" not in st.session_state:
    st.session_state.checklist_content = []

min_valid = 9

# ======= ITEMS ======
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

# ======= PLACEHOLDER ======
terminal_placeholder = st.empty()

# ======= RENDER ======
def render():
    terminal_placeholder.markdown(
        """
        <div id='checklist-terminal' class='checklist-terminal'>
        """ + "<br>".join(st.session_state.checklist_content) + """
        <span class='cursor'></span>
        </div>
        <script>
        const term = document.getElementById("checklist-terminal");
        if (term) { term.scrollTop = term.scrollHeight; }
        </script>
        """,
        unsafe_allow_html=True
    )

# ======= TYPING LINE ======
def type_line(line):
    current = ""
    st.session_state.checklist_content.append("")
    for char in line:
        current += char
        st.session_state.checklist_content[-1] = current
        render()
        time.sleep(random.uniform(0.008, 0.03))

# ======= GLITCH OPTIONNEL ======
def subtle_glitch(line, chance=0.15):
    if not st.session_state.checklist_content:
        return  # ✅ sécurité ajoutée

    if random.random() < chance:
        chars = list("█▓▒░<>/\\|#@$%&*")
        glitched = "".join(random.choice(chars) for _ in range(len(line)))
        st.session_state.checklist_content[-1] = glitched
        render()
        time.sleep(0.03)

# ======= ADD LINE ======
def add_line(line, glitch=False):
    type_line(line)  # ✅ corrigé (avant glitch)
    if glitch:
        subtle_glitch(line)
    time.sleep(random.uniform(0.05, 0.2))

# ======= DISPLAY CHECKLIST ======
if not st.session_state.checklist_validee:

    if not st.session_state.checklist_content:
        add_line("$ init checklist_protocol --lp_safety", glitch=True)
        add_line("> auto-checking all items...", glitch=True)
        for item in checklist_items:
            add_line(f"[✔] {item}")
        # Progress bar
        score = len(checklist_items)
        total = len(checklist_items)
        progress = int((score / total) * 20)
        bar = "█" * progress + "░" * (20 - progress)
        add_line(f"> progress: [{bar}] {score}/{total}")

    # Bouton final pour valider
    if st.button("$ J'AI COMPRIS !"):
        st.session_state.checklist_validee = True
        st.rerun()

    st.stop()

# ======= UNLOCK MESSAGE ======
st.markdown("""
<div style='color:#00ff88; font-family:monospace; font-size:13px; margin-top:10px;'>
> déverouillage des outils...
</div>
""", unsafe_allow_html=True)



# =======================
# METEO DEFI CONFIG
# =======================
# Forcer mode écran large
st.set_page_config(layout="wide")

METEO = {
    "title": "METEO DeFi☀️ RANGE LP hebdo #8",
    "market": "Volatilité BTC/ETH ↑ → marché en range.",
    "strategies": [
        "WETH/USDC → 18% ATR ⌛130$ ⤴️",
        "USDC/cbBTC → 14% ATR ⌛3087$ ⤴️",
        "WETH/cbBTC → 8% ATR 🔜 130$ → 3087$"
    ],
    "conclusion": "On capte la vol, pas la direction."
}

# =======================
# STYLE COMPACT
# =======================

st.markdown("""
<style>
.defi-meteo-box {
    background-color: #000;
    padding: 10px 12px;
    border-radius: 6px;
    border: 1px solid #00ff88;
    color: #00ff88;
    font-family: "Courier New", monospace;
    font-size: 12px;
    line-height: 1.4;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =======================
# BUILD (1 seule fois)
# =======================

if "meteo_cached" not in st.session_state:

    lines = []
    lines.append(f"> {METEO['title']}")
    lines.append(f"> {METEO['market']}")
    lines.append("> LP:")

    for strat in METEO["strategies"]:
        lines.append(f"  - {strat}")

    lines.append(f"> {METEO['conclusion']}")

    st.session_state.meteo_cached = "<br>".join(lines)

# =======================
# DISPLAY (statique)
# =======================

st.markdown(
    f"<div class='defi-meteo-box'>{st.session_state.meteo_cached}</div>",
    unsafe_allow_html=True
)
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

.small-label {
    font-size: 12px;
    opacity: 0.7;
    margin-bottom: 2px;
}
</style>
""", unsafe_allow_html=True)


# =================== INPUTS ===================
st.markdown('<div class="section-title">Impermanent Loss</div>', unsafe_allow_html=True)

row1_col1, row1_col2, row1_col3 = st.columns([1,1,1])
with row1_col1:
    st.markdown('<div class="small-label">P_deposit</div>', unsafe_allow_html=True)
    P_deposit = st.number_input("P_deposit", value=3000.0, format="%.6f", step=0.001, label_visibility="collapsed")
with row1_col2:
    st.markdown('<div class="small-label">P_now</div>', unsafe_allow_html=True)
    P_now = st.number_input("P_now", value=3000.0, format="%.6f", step=0.001, label_visibility="collapsed")
with row1_col3:
    st.markdown('<div class="small-label">Valeur deposit (USD)</div>', unsafe_allow_html=True)
    v_deposit = st.number_input("Valeur deposit (USD)", value=500.0, format="%.6f", step=0.01, label_visibility="collapsed")

row2_col1, row2_col2 = st.columns([1,1])
with row2_col1:
    st.markdown('<div class="small-label">P_lower</div>', unsafe_allow_html=True)
    P_lower = st.number_input("P_lower", value=2800.0, format="%.6f", step=0.001, label_visibility="collapsed")
with row2_col2:
    st.markdown('<div class="small-label">P_upper</div>', unsafe_allow_html=True)
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

fig.add_trace(go.Scatter(
    x=prices, y=IL_curve, mode="lines", name="IL(%)",
    line=dict(color="red", width=3)
))

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

fig.update_layout(
    height=380,
    plot_bgcolor="#0b0f14",
    paper_bgcolor="#0b0f14",
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

atr_low = asset_price*(1-range_total_pct*low_weight/100)
atr_high= asset_price*(1+range_total_pct*high_weight/100)
low_pct_display = (atr_low/asset_price-1)*100
high_pct_display = (atr_high/asset_price-1)*100

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


# ======================= BE LP (Terminal Style Complet) =======================

# --- Header Terminal Style ---
st.markdown("""
<br>
<div style="
    background-color: #0f141b;
    border: 1px solid #1f2a36;
    border-radius: 10px;
    padding: 16px 20px;
    margin-top: 20px;
    margin-bottom: 20px;
    font-family: 'Courier New', monospace;
    color: #e6edf3;
">
    <span style="
        color: #00ff88;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: 1px;
    ">
        CALCULATRICE BREAK-EVEN LP
    </span>
</div>
""", unsafe_allow_html=True)

# ================= TERMINAL THEME CSS =================
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

cols = st.columns(len(cards))
for i, card in enumerate(cards):
    with cols[i]:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-title">{card['title']}</div>
            <div class="result-value" style="color:{card['color']};">{card['value']}</div>
        </div>
        """, unsafe_allow_html=True)

# ======================= LESS IL / ZERO SWAP TERMINAL STYLE =======================


# --- Header Terminal Style ---
st.markdown("""
<br>
<div style="
    background-color: #0f141b;
    border: 1px solid #1f2a36;
    border-radius: 10px;
    padding: 16px 20px;
    margin-top: 20px;
    margin-bottom: 20px;
    font-family: 'Courier New', monospace;
    color: #e6edf3;
">
    <span style="
        color: #00ff88;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: 1px;
    ">
        Zero Swap Rebalance
    </span>
</div>
""", unsafe_allow_html=True)

# ================= TERMINAL THEME CSS =================
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

label {
    font-size: 12px !important;
    opacity: 0.7;
}

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

col_low, col_high, col_dir = st.columns(3)

with col_low:
    new_P_low = st.number_input("New Plow (dump)", value=P_low * 0.9, step=1.0)

with col_high:
    new_P_high = st.number_input("New Phigh (pump)", value=P_high * 1.1, step=1.0)

with col_dir:
    direction_select = st.selectbox(
        "Mode de recalcul",
        options=["Auto", "Dump", "Pump"]
    )

# 🔥 NOUVEAU : sélection du rebalance partiel
rebalance_pct = st.selectbox(
    "Rebalance partiel (%)",
    options=[25, 50, 75, 100],
    index=3
) / 100

# Sauvegarde des anciennes bornes
old_P_low = P_low
old_P_high = P_high

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

# =================== 🔥 APPLICATION REBALANCE PARTIEL ===================
adj_P_low = old_P_low + (new_P_low - old_P_low) * rebalance_pct
adj_P_high = old_P_high + (new_P_high - old_P_high) * rebalance_pct

# =================== RESULTATS REBALANCE ===================
st.markdown('<div class="section-title">Résultats - Rebalance / Élargissement</div>', unsafe_allow_html=True)

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
<div class="result-value">{adj_P_low:.2f}</div>
</div>
""", unsafe_allow_html=True)

with r3:
    st.markdown(f"""
<div class="result-card">
<div class="result-title">Nouvelle borne haute</div>
<div class="result-value">{adj_P_high:.2f}</div>
</div>
""", unsafe_allow_html=True)

# =================== 🔥 INTERPRETATION ===================
if rebalance_pct == 0.25:
    interp = "🟢 Ajustement léger : conserve majoritairement la position initiale (faible impact, faible coût implicite)."
elif rebalance_pct == 0.50:
    interp = "🟡 Ajustement équilibré : compromis entre conservation et adaptation au marché."
elif rebalance_pct == 0.75:
    interp = "🟠 Ajustement agressif : forte adaptation au nouveau range, risque de swap implicite plus élevé."
else:
    interp = "🔴 Rebalance complet (100%) : Zero Swap pur, repositionnement total."

st.markdown(f"""
<div class="result-card">
<div class="result-title">Interprétation</div>
<div class="result-value">{interp}</div>
</div>
""", unsafe_allow_html=True)

# =================== RESSERREMENT DU RANGE ===================
st.markdown('<div class="section-title">Resserrement du range</div>', unsafe_allow_html=True)

tighten_percent = st.number_input("Tighten (%)", value=5.0, step=0.5)

if tighten_percent > 0:

    P_rebalance = P_current
    new_tight_plow = P_rebalance * (1 - tighten_percent / 100)

    sqrtP_reb = math.sqrt(P_rebalance)
    sqrtPl_reb = math.sqrt(new_tight_plow)
    sqrtPh_reb = math.sqrt(adj_P_high)

    ratio_reb = (sqrtPh_reb - sqrtP_reb) / (
        sqrtP_reb * sqrtPh_reb * (sqrtP_reb - sqrtPl_reb)
    )

    denominator = 1 - ratio_reb * sqrtP_reb * (sqrtP_reb - sqrtPl_reb)

    if denominator > 0:
        sqrt_new_tight_ph = sqrtP_reb / denominator
        new_tight_phigh = sqrt_new_tight_ph ** 2
    else:
        new_tight_phigh = None

# =================== RESULTATS RESSERREMENT ===================
if tighten_percent > 0 and new_tight_phigh:

    st.markdown('<div class="section-title">Résultats - Resserrement du range</div>', unsafe_allow_html=True)

    rt1, rt2 = st.columns(2)

    with rt1:
        st.markdown(f"""
<div class="result-card">
<div class="result-title">Tight Plow</div>
<div class="result-value">{new_tight_plow:.2f}</div>
</div>
""", unsafe_allow_html=True)

    with rt2:
        st.markdown(f"""
<div class="result-card">
<div class="result-title">Tight Phigh</div>
<div class="result-value">{new_tight_phigh:.2f}</div>
</div>
""", unsafe_allow_html=True)

# =================== LP REFILL BACKTEST ===================
st.markdown('<div class="section-title">LP Refill BACKTEST</div>', unsafe_allow_html=True)

# =================== INPUTS ===================

c1, c2, c3 = st.columns(3)

with c1:
    tokenA_price = st.number_input("Prix Token A ($)", value=1900.0)

with c2:
    tokenB_price = st.number_input("Prix Token B ($)", value=1.0)

with c3:
    refill_amount = st.number_input("Montant à ajouter ($)", value=1000.0)

# LP state

q1, q2 = st.columns(2)

with q1:
    tokenA_lp = st.number_input("Quantité Token A dans la LP", value=4.0)

with q2:
    tokenB_lp = st.number_input("Quantité Token B dans la LP", value=3000.0)

# Range

r1, r2 = st.columns(2)

with r1:
    P_low = st.number_input("Borne basse", value=1700.0)

with r2:
    P_high = st.number_input("Borne haute", value=2100.0)

# =================== CALCUL POSITION ===================

lp_value = tokenA_lp * tokenA_price + tokenB_lp * tokenB_price

ratio_A = (tokenA_lp * tokenA_price) / lp_value
ratio_B = (tokenB_lp * tokenB_price) / lp_value

# =================== DETECTION MOMENT REFILL ===================

zone_bottom = P_low + (P_high - P_low) * 0.15

good_moment = False
message = ""

if tokenA_price < P_low:
    message = "🔴 Prix sous le range : risque directionnel élevé"

elif tokenA_price <= zone_bottom:
    good_moment = True
    message = "🟢 Bon moment : prix proche du bas de range"

elif tokenA_price < P_high:
    message = "🟡 Prix encore dans le range mais pas optimal"

else:
    message = "🔴 Prix au-dessus du range"

# =================== REFILL SIMULATION ===================

# Position du prix dans le range
price_position = (tokenA_price - P_low) / (P_high - P_low)
price_position = max(0, min(1, price_position))

# Ratio cible basé sur le range
target_ratio_A = 1 - price_position
target_ratio_B = price_position

# Allocation du refill
tokenA_value_added = refill_amount * target_ratio_A
tokenB_value_added = refill_amount * target_ratio_B

# Conversion en quantité
tokenA_added = tokenA_value_added / tokenA_price
tokenB_added = tokenB_value_added / tokenB_price

new_tokenA = tokenA_lp + tokenA_added
new_tokenB = tokenB_lp + tokenB_added

new_value = new_tokenA * tokenA_price + new_tokenB * tokenB_price

new_ratio_A = (new_tokenA * tokenA_price) / new_value
new_ratio_B = (new_tokenB * tokenB_price) / new_value

# =================== RESULTATS ===================

st.markdown('<div class="section-title">Analyse</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="result-card">
    <div class="result-title">Etat du marché</div>
    <div class="result-value">{message}</div>
</div>
""", unsafe_allow_html=True)

# =================== POSITION ACTUELLE ===================

st.markdown('<div class="section-title">Position actuelle</div>', unsafe_allow_html=True)

r1, r2, r3 = st.columns(3)

with r1:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Valeur LP</div>
        <div class="result-value">${lp_value:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Ratio Token A</div>
        <div class="result-value">{ratio_A*100:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Ratio Token B</div>
        <div class="result-value">{ratio_B*100:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

# =================== APRES REFILL ===================

st.markdown('<div class="section-title">Projection après Refill</div>', unsafe_allow_html=True)

rr1, rr2, rr3 = st.columns(3)

with rr1:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Token A ajouté</div>
        <div class="result-value">{tokenA_added:.4f}</div>
    </div>
    """, unsafe_allow_html=True)

with rr2:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Token B ajouté</div>
        <div class="result-value">{tokenB_added:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with rr3:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Valeur LP future</div>
        <div class="result-value">${new_value:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="result-card-wide">
    <div class="result-title">Nouveau ratio LP</div>
    <div class="result-value">
        Token A : {new_ratio_A*100:.2f}%  |  Token B : {new_ratio_B*100:.2f}%
    </div>
</div>
""", unsafe_allow_html=True)

# =================== FORMULES ===================
with st.expander("Résumé stratégique : Gestion et timing de l’ajout de liquidité (LP Refill)"):

    # Texte d’intro
    st.markdown(
        '<div style="font-size:12px; color:#aaa; margin-bottom:10px; font-family: Courier, monospace;">'
        "Cet outil permet d'évaluer si un ajout de liquidité dans une position LP est stratégique ou risqué. "
        "Il analyse la position actuelle, la proximité avec le bas de range et simule l’impact d’un refill "
        "sur l’exposition et le ratio de la position."
        '</div>',
        unsafe_allow_html=True
    )

    # =================== OBJECTIF ===================

    st.markdown(
        '<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Objectif de l’outil</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="font-size:12px; color:#bbb; font-family: Courier, monospace;">'
        "L’ajout de liquidité ne doit pas être une réaction émotionnelle à une baisse du prix. "
        "Cet outil aide à déterminer si le prix est dans une zone stratégique pour renforcer une LP "
        "sans augmenter excessivement le risque directionnel."
        "</div>",
        unsafe_allow_html=True
    )

    # =================== MAUVAIS MOMENT ===================

    st.markdown(
        '<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Mauvais moment pour ajouter de la liquidité</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="font-size:12px; color:#bbb; font-family: Courier, monospace;">'
        "Ajouter après une cassure nette du bas de range peut transformer une position LP neutre "
        "en position directionnelle fortement exposée à la baisse. "
        "<br><br>"
        "Situations à éviter :"
        "<br>• Prix sous la range active"
        "<br>• Forte accélération baissière"
        "<br>• Absence de plan de capital maximum"
        "<br>• Moyennage agressif sans paliers"
        "<br><br>"
        "Dans ces conditions, le risque devient exponentiel si la tendance continue."
        "</div>",
        unsafe_allow_html=True
    )

    # =================== BON MOMENT ===================

    st.markdown(
        '<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Meilleur moment pour un refill</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="font-size:12px; color:#bbb; font-family: Courier, monospace;">'
        "Le moment idéal pour ajouter de la liquidité est lorsque le prix reste encore dans le range "
        "mais se rapproche de la borne basse."
        "<br><br>"
        "Conditions favorables :"
        "<br>• Prix proche du bas de range"
        "<br>• Baisse en ralentissement"
        "<br>• LP toujours active dans la fourchette"
        "<br>• Impermanent loss encore non réalisée"
        "<br><br>"
        "Dans ce cas, le refill permet d’augmenter légèrement l’exposition tout en abaissant le prix moyen."
        "</div>",
        unsafe_allow_html=True
    )

    # =================== STRUCTURE MARCHE ===================

    st.markdown(
        '<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Importance de la structure de marché</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="font-size:12px; color:#bbb; font-family: Courier, monospace;">'
        "Avant d’ajouter du capital, il est important d’évaluer la structure du marché."
        "<br><br>"
        "Questions clés :"
        "<br>• La baisse est-elle technique ou structurelle ?"
        "<br>• La volatilité augmente-t-elle ou réduit elle ?"
        "<br>• Le capital disponible permet-il d’absorber une baisse supplémentaire ?"
        "<br><br>"
        "Si la tendance est fortement baissière, ne rien faire reste souvent la décision la plus prudente."
        "</div>",
        unsafe_allow_html=True
    )

    # =================== STRATEGIE PALIER ===================

    st.markdown(
        '<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Stratégie d’ajout progressif</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="font-size:12px; color:#bbb; font-family: Courier, monospace;">'
        "Les ajouts doivent être planifiés sous forme de paliers afin d’éviter un surdimensionnement de la position."
        "<br><br>"
        "Exemple d’allocation :"
        "<br>• Position initiale : capital principal"
        "<br>• Palier 1 : proche du bas de range"
        "<br>• Palier 2 : si la baisse continue"
        "<br>• Palier 3 : dernier ajout planifié"
        "<br><br>"
        "Chaque palier doit être défini à l’avance afin d’éviter les décisions impulsives."
        "</div>",
        unsafe_allow_html=True
    )

    # =================== CONCLUSION ===================

    st.markdown(
        '<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Principe clé</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="font-size:12px; color:#bbb; font-family: Courier, monospace;">'
        "La discipline de capital est plus importante que le timing parfait."
        "<br><br>"
        "Ajouter trop tôt expose à la tendance."
        "<br>Ajouter trop tard augmente le risque directionnel."
        "<br><br>"
        "Un refill doit toujours être planifié, limité et intégré dans une stratégie globale de gestion du risque."
        "</div>",
        unsafe_allow_html=True
    )

# =================== FORMULES ===================
with st.expander("Formules avancées utilisées pour l'analyse Refill LP"):

    st.markdown(
        '<div style="font-size:12px; color:#aaa; margin-bottom:10px; font-family: Courier, monospace;">'
        "Ces formules permettent d'analyser l’exposition réelle d’une position LP concentrée, "
        "de simuler un refill et d’estimer l’impact sur le ratio et la valeur de la position."
        '</div>',
        unsafe_allow_html=True
    )

    # =================== PRIX ===================

    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Prix du pool</div>', unsafe_allow_html=True)

    st.latex(r"P = \frac{Price_{TokenA}}{Price_{TokenB}}")

    st.markdown(
        '<div style="font-size:12px; color:#bbb; font-family: Courier, monospace;">'
        "Le prix de la pool est simplement le ratio entre les deux actifs."
        '</div>',
        unsafe_allow_html=True
    )

    # =================== VALEUR LP ===================

    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Valeur totale de la position LP</div>', unsafe_allow_html=True)

    st.latex(r"V = (A \cdot P_A) + (B \cdot P_B)")

    st.markdown(
        '<div style="font-size:12px; color:#bbb; font-family: Courier, monospace;">'
        "Permet de mesurer la valeur totale de la position en dollars."
        '</div>',
        unsafe_allow_html=True
    )

    # =================== RATIO LP ===================

    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Ratio d’exposition Token A</div>', unsafe_allow_html=True)

    st.latex(r"""
    Ratio_A =
    \frac{A \cdot P_A}
    {(A \cdot P_A) + (B \cdot P_B)}
    """)

    st.latex(r"Ratio_B = 1 - Ratio_A")

    st.markdown(
        '<div style="font-size:12px; color:#bbb; font-family: Courier, monospace;">'
        "Mesure l’exposition directionnelle réelle de la LP."
        '</div>',
        unsafe_allow_html=True
    )

    # =================== REFILL ===================

    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Ajout de liquidité (refill)</div>', unsafe_allow_html=True)

    st.latex(r"""
    A_{added} =
    \frac{Capital/2}{P_A}
    """)

    st.latex(r"""
    B_{added} =
    \frac{Capital}{2}
    """)

    st.markdown(
        '<div style="font-size:12px; color:#bbb; font-family: Courier, monospace;">'
        "Un refill standard ajoute 50% de chaque actif pour maintenir l'équilibre initial."
        '</div>',
        unsafe_allow_html=True
    )

    # =================== NOUVELLE POSITION ===================

    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Nouvelle position après refill</div>', unsafe_allow_html=True)

    st.latex(r"A_{new} = A_{current} + A_{added}")

    st.latex(r"B_{new} = B_{current} + B_{added}")

    st.latex(r"""
    V_{new} =
    (A_{new} \cdot P_A) +
    (B_{new} \cdot P_B)
    """)

    # =================== IMPERMANENT LOSS ===================

    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Impermanent Loss (AMM)</div>', unsafe_allow_html=True)

    st.latex(r"""
    IL =
    \frac{2\sqrt{r}}
    {1+r}
    -1
    """)

    st.latex(r"r = \frac{P_{new}}{P_{entry}}")

    st.markdown(
        '<div style="font-size:12px; color:#bbb; font-family: Courier, monospace;">'
        "Cette formule mesure la perte relative par rapport à un simple holding des actifs."
        '</div>',
        unsafe_allow_html=True
    )

    # =================== PRIX MOYEN ===================

    st.markdown('<div style="font-family: Courier, monospace; font-weight: 700; font-size: 14px; color: #ddd; margin-top: 15px;">Prix moyen après refill</div>', unsafe_allow_html=True)

    st.latex(r"""
    P_{avg} =
    \frac{Capital_{total}}
    {TokenA_{total}}
    """)

    st.markdown(
        '<div style="font-size:12px; color:#bbb; font-family: Courier, monospace;">'
        "Permet d'évaluer si le refill améliore réellement le prix moyen d'exposition."
        '</div>',
        unsafe_allow_html=True
    )

# =================== LP HEALTH SCORE ===================
st.markdown('<div class="section-title">LP Health Score</div>', unsafe_allow_html=True)

# =================== INPUTS ===================

c1, c2 = st.columns(2)

with c1:
    tokenA_price_h = st.number_input("Prix Token A ($) ", value=1900.0, key="h_a_price")

with c2:
    tokenB_price_h = st.number_input("Prix Token B ($) ", value=1.0, key="h_b_price")

q1, q2 = st.columns(2)

with q1:
    tokenA_lp_h = st.number_input("Quantité Token A LP ", value=4.0, key="h_a_lp")

with q2:
    tokenB_lp_h = st.number_input("Quantité Token B LP ", value=3000.0, key="h_b_lp")

r1, r2 = st.columns(2)

with r1:
    P_low_h = st.number_input("Borne basse ", value=1700.0, key="h_low")

with r2:
    P_high_h = st.number_input("Borne haute ", value=2100.0, key="h_high")

# ATR input (manuel)
atr = st.number_input("ATR ($)", value=80.0)

# =================== CALCULS ===================

lp_value_h = tokenA_lp_h * tokenA_price_h + tokenB_lp_h * tokenB_price_h

ratio_A_h = (tokenA_lp_h * tokenA_price_h) / lp_value_h
ratio_B_h = (tokenB_lp_h * tokenB_price_h) / lp_value_h

range_width = P_high_h - P_low_h

# Position dans le range
price_position_h = (tokenA_price_h - P_low_h) / range_width
price_position_h = max(0, min(1, price_position_h))

# =================== SCORE 1 : POSITION ===================

position_score = (1 - price_position_h) * 100

# =================== SCORE 2 : EQUILIBRE ===================

target_ratio_A_h = 1 - price_position_h
imbalance = abs(ratio_A_h - target_ratio_A_h)

balance_score = max(0, 100 - imbalance * 200)

# =================== SCORE 3 : EXPOSITION ===================

if price_position_h < 0.3:
    exposure_penalty = ratio_B_h
elif price_position_h > 0.7:
    exposure_penalty = ratio_A_h
else:
    exposure_penalty = abs(ratio_A_h - 0.5)

exposure_score = max(0, 100 - exposure_penalty * 100)

# =================== SCORE 4 : VOLATILITE (ATR) ===================

# Ratio ATR vs range
atr_ratio = atr / range_width

# Si ATR élevé → plus de risque → score baisse
volatility_score = max(0, 100 - atr_ratio * 150)

# =================== SCORE FINAL ===================

health_score = (
    position_score * 0.3 +
    balance_score * 0.25 +
    exposure_score * 0.2 +
    volatility_score * 0.25
)

# =================== REBALANCE LOGIC ===================

rebalance_needed = False
rebalance_reason = ""

# Cas 1 : trop déséquilibré
if imbalance > 0.2:
    rebalance_needed = True
    rebalance_reason = "Déséquilibre des tokens"

# Cas 2 : prix proche des extrêmes
elif price_position_h < 0.1 or price_position_h > 0.9:
    rebalance_needed = True
    rebalance_reason = "Prix proche des bornes"

# Cas 3 : volatilité dangereuse
elif atr_ratio > 0.25:
    rebalance_needed = True
    rebalance_reason = "Volatilité élevée (ATR)"

# =================== INTERPRETATION ===================

if health_score > 80:
    status = "🟢 Position optimale"
elif health_score > 60:
    status = "🟡 Position correcte"
elif health_score > 40:
    status = "🟠 Position à surveiller"
else:
    status = "🔴 Position risquée"

# =================== DISPLAY ===================

st.markdown('<div class="section-title">Résultat</div>', unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Health Score</div>
        <div class="result-value">{health_score:.1f} / 100</div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Position</div>
        <div class="result-value">{position_score:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Balance</div>
        <div class="result-value">{balance_score:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Volatilité</div>
        <div class="result-value">{volatility_score:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# Status global
st.markdown(f"""
<div class="result-card-wide">
    <div class="result-title">Statut</div>
    <div class="result-value">{status}</div>
</div>
""", unsafe_allow_html=True)

# Rebalance alert
if rebalance_needed:
    st.markdown(f"""
    <div class="result-card-wide" style="border:2px solid #ff4b4b;">
        <div class="result-title">⚠️ Rebalance recommandé</div>
        <div class="result-value">{rebalance_reason}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="result-card-wide">
        <div class="result-title">Rebalance</div>
        <div class="result-value">Aucune action nécessaire</div>
    </div>
    """, unsafe_allow_html=True)

# =================== AUTO RANGE (STRUCTURE CONSERVEE) ===================
st.markdown('<div class="section-title">Auto Range</div>', unsafe_allow_html=True)

# =================== INPUT ===================

col1, col2 = st.columns(2)

with col1:
    atr_auto = st.number_input("ATR pour optimisation ($)", value=80.0, key="auto_atr")

with col2:
    multiplier = st.slider("Facteur de range", 1.0, 4.0, 2.0, 0.5)

# =================== POSITION ACTUELLE ===================

old_range_width = P_high_h - P_low_h

old_position = (tokenA_price_h - P_low_h) / old_range_width
old_position = max(0, min(1, old_position))

# =================== NOUVEAU RANGE ===================

new_range_width = atr_auto * multiplier * 2

optimal_low = tokenA_price_h - (old_position * new_range_width)
optimal_high = optimal_low + new_range_width

if optimal_low < 0:
    optimal_low = 0
    optimal_high = new_range_width

# =================== VERIFICATION ===================

new_position = (tokenA_price_h - optimal_low) / new_range_width

# =================== DISPLAY ===================

r1, r2, r3 = st.columns(3)

with r1:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Range bas</div>
        <div class="result-value">{optimal_low:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Range haut</div>
        <div class="result-value">{optimal_high:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Largeur %</div>
        <div class="result-value">{(new_range_width/tokenA_price_h)*100:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

# =================== OPTIMAL RANGE FINDER ===================
st.markdown('<div class="section-title">Optimal Range Finder</div>', unsafe_allow_html=True)

# =================== INPUT ===================

double_volatile = st.checkbox("Analyser une pair double volatile", value=False)

if double_volatile:
    c1, c2 = st.columns(2)
    with c1:
        price_a = st.number_input("Prix Token A ($)", value=1900.0, key="orf_price_a")
    with c2:
        atr_a = st.number_input("ATR Token A ($)", value=80.0, key="orf_atr_a")
    
    c3, c4 = st.columns(2)
    with c3:
        price_b = st.number_input("Prix Token B ($)", value=50.0, key="orf_price_b")
    with c4:
        atr_b = st.number_input("ATR Token B ($)", value=5.0, key="orf_atr_b")
    
    # ATR pondéré par volatilité relative
    atr_pct_a = atr_a / price_a
    atr_pct_b = atr_b / price_b
    atr_combined_pct = max(atr_pct_a, atr_pct_b)
    price_orf = (price_a + price_b)/2
    atr_orf = atr_combined_pct * price_orf
    
else:
    c1, c2 = st.columns(2)
    with c1:
        price_orf = st.number_input("Prix actuel ($)", value=1900.0, key="orf_price")
    with c2:
        atr_orf = st.number_input("ATR ($)", value=80.0, key="orf_atr")

# =================== MULTIPLIERS ===================

safe_mult = 3.0
balanced_mult = 2.0
aggressive_mult = 1.2

# =================== CALCULS ===================

def compute_range(price, atr, mult):
    low = price - (atr * mult)
    high = price + (atr * mult)
    width_pct = ((high - low) / price) * 100
    return low, high, width_pct

safe_low, safe_high, safe_width = compute_range(price_orf, atr_orf, safe_mult)
bal_low, bal_high, bal_width = compute_range(price_orf, atr_orf, balanced_mult)
agg_low, agg_high, agg_width = compute_range(price_orf, atr_orf, aggressive_mult)

# =================== DISPLAY ===================

st.markdown('<div class="section-title">Suggestions</div>', unsafe_allow_html=True)

s1, s2, s3 = st.columns(3)

with s1:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Safe</div>
        <div class="result-value">
            {safe_low:.0f} → {safe_high:.0f}<br>
            {safe_width:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Balanced</div>
        <div class="result-value">
            {bal_low:.0f} → {bal_high:.0f}<br>
            {bal_width:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">Aggressive</div>
        <div class="result-value">
            {agg_low:.0f} → {agg_high:.0f}<br>
            {agg_width:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

# =================== INSIGHT ===================

st.markdown(f"""
<div class="result-card-wide">
    <div class="result-title">RAPPEL</div>
    <div class="result-value">
        Safe = moins de sorties | Aggressive = plus de fees mais plus de risque
    </div>
</div>
""", unsafe_allow_html=True)


# --- GUIDE COMPLET TERMINAL STYLE ---
# --- CALCULATRICE IMPERMANENT LOSS (Terminal Style) ---
st.markdown("""
<br>
<div style="
    background-color: #0f141b;
    border: 1px solid #1f2a36;
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 20px;
    margin-bottom: 20px;
    font-family: 'Courier New', monospace;
    color: #e6edf3;
">
    <span style="
        color: #00ff88;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: 1px;
    ">
        GUIDE COMPLET - ENGAGER DU CAPITAL SUR UNE LP
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
# --- CALCULATRICE IMPERMANENT LOSS (Terminal Style) ---
st.markdown("""
<br>
<div style="
    background-color: #0f141b;
    border: 1px solid #1f2a36;
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 20px;
    margin-bottom: 20px;
    font-family: 'Courier New', monospace;
    color: #e6edf3;
">
    <span style="
        color: #00ff88;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: 1px;
    ">
        CALCULATRICE IMPERMANENT LOSS
    </span>
</div>
""", unsafe_allow_html=True)


# colonne unique large
col, = st.columns(1)

with col:
    st.video("https://www.youtube.com/watch?v=uQPeyXsQNrs")

# ======================= outil atelier IL =======================
import streamlit.components.v1 as components

# --- ATELIER IMPERMANENT LOSS (Terminal Style) ---
st.markdown("""
<br>
<div style="
    background-color: #0f141b;
    border: 1px solid #1f2a36;
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 20px;
    margin-bottom: 20px;
    font-family: 'Courier New', monospace;
    color: #e6edf3;
">
    <span style="
        color: #00ff88;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: 1px;
    ">
        ATELIER IMPERMANENT LOSS
    </span>
</div>
""", unsafe_allow_html=True)



desmos_url = "https://www.desmos.com/calculator/i7mnoyyqdb?lang=fr"

components.iframe(
    src=desmos_url,
    width="100%",
    height=700,
    scrolling=True
)
