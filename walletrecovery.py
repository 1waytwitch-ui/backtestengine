import streamlit as st
import streamlit.components.v1 as components
import sqlite3
from pathlib import Path

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="KBOUR CRYPTO // WALLET SECURITY",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===================== GLOBAL THEME =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-main:     #080c10;
    --bg-panel:    #0d1318;
    --bg-card:     #111820;
    --accent:      #00d4aa;
    --accent-dim:  rgba(0,212,170,0.10);
    --accent-mid:  rgba(0,212,170,0.30);
    --accent-2:    #0ea5e9;
    --accent-3:    #f59e0b;
    --accent-red:  #ef4444;
    --accent-green:#22c55e;
    --border:      rgba(0,212,170,0.18);
    --border-soft: rgba(255,255,255,0.06);
    --text-hi:     #f0f4f8;
    --text-mid:    #8899aa;
    --text-lo:     #445566;
    --font-mono:   'JetBrains Mono','Courier New',monospace;
    --font-ui:     'Inter',sans-serif;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer { visibility: hidden !important; }
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stToolbar"]        { display: none !important; }
[data-testid="stHeader"]         { display: none !important; }
.block-container { padding-top: 72px !important; padding-bottom: 60px !important; max-width: 860px !important; }

/* ── BASE ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-main) !important;
    color: var(--text-hi);
    font-family: var(--font-ui);
}

/* ── NAV BAR ── */
.nav-bar {
    position: fixed; top:0; left:0; width:100%; height:58px;
    z-index:99999;
    background: rgba(6,10,14,0.97);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--border);
    display:flex; align-items:center; justify-content:space-between;
    padding: 0 28px; box-sizing:border-box;
}
.nav-brand { display:flex; align-items:center; gap:10px; }
.nav-glyph {
    width:28px; height:28px; border:2px solid var(--accent); border-radius:6px;
    display:flex; align-items:center; justify-content:center;
    font-family:var(--font-mono); font-size:14px; color:var(--accent); font-weight:700;
}
.nav-title    { font-family:var(--font-mono); font-size:13px; font-weight:600; color:var(--text-hi); letter-spacing:2px; text-transform:uppercase; }
.nav-subtitle { font-family:var(--font-mono); font-size:10px; color:var(--text-mid); letter-spacing:1px; }
.status-dot   { width:7px; height:7px; border-radius:50%; background:#ef4444; display:inline-block; margin-right:5px; animation:pulse-dot 1.5s infinite; }
@keyframes pulse-dot { 0%,100%{opacity:1;box-shadow:0 0 0 0 rgba(239,68,68,0.5);} 50%{opacity:.7;box-shadow:0 0 0 5px rgba(239,68,68,0);} }
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
.m-card {
    background:var(--bg-card); border:1px solid var(--border-soft);
    border-radius:10px; padding:16px 18px; margin:8px 0;
    transition:border-color .2s,box-shadow .2s; position:relative; overflow:hidden;
}
.m-card::before { content:''; position:absolute; top:0;left:0;right:0; height:2px; background:linear-gradient(90deg,var(--accent),transparent); opacity:0; transition:opacity .2s; }
.m-card:hover { border-color:var(--border); box-shadow:0 0 18px rgba(0,212,170,.07); }
.m-card:hover::before { opacity:1; }
.m-card-wide { background:var(--bg-card); border:1px solid var(--border-soft); border-radius:10px; padding:18px 20px; margin:8px 0; }

.m-label { font-family:var(--font-mono); font-size:10px; color:var(--text-mid); letter-spacing:1.5px; text-transform:uppercase; margin-bottom:8px; }
.m-value { font-family:var(--font-mono); font-size:22px; font-weight:700; color:var(--accent); line-height:1.1; }
.m-value-sm { font-family:var(--font-mono); font-size:14px; font-weight:500; color:var(--accent); line-height:1.4; }

/* ── TERMINAL ── */
.term-block {
    background:#050809; border:1px solid var(--border); border-radius:10px;
    padding:20px; font-family:var(--font-mono); font-size:12px;
    line-height:1.7; color:var(--accent); max-height:340px; overflow-y:auto;
    margin: 12px 0;
}
.term-block::-webkit-scrollbar { width:4px; }
.term-block::-webkit-scrollbar-thumb { background:var(--accent-mid); border-radius:2px; }

/* ── WARNING / DANGER / SUCCESS CARDS ── */
.w-card {
    background:rgba(245,158,11,.06); border:1px solid rgba(245,158,11,.28);
    border-radius:10px; padding:22px 24px; margin:14px 0;
}
.w-card-title { font-family:var(--font-mono); font-size:13px; font-weight:600; color:#f59e0b; letter-spacing:1px; margin-bottom:12px; }

.d-card {
    background:rgba(239,68,68,.07); border:1px solid rgba(239,68,68,.35);
    border-radius:10px; padding:22px 24px; margin:14px 0;
    box-shadow: 0 0 30px rgba(239,68,68,.06);
}
.d-card-title { font-family:var(--font-mono); font-size:15px; font-weight:700; color:#ef4444; letter-spacing:1px; margin-bottom:12px; }

.s-card {
    background:rgba(34,197,94,.07); border:1px solid rgba(34,197,94,.3);
    border-radius:10px; padding:22px 24px; margin:14px 0;
    box-shadow: 0 0 25px rgba(34,197,94,.05);
}
.s-card-title { font-family:var(--font-mono); font-size:15px; font-weight:700; color:#22c55e; letter-spacing:1px; margin-bottom:12px; }

/* ── STEP CARD ── */
.step-card {
    background:var(--bg-card); border:1px solid var(--border-soft);
    border-radius:12px; padding:24px 28px; margin:14px 0;
    position:relative; overflow:hidden;
}
.step-card::before {
    content:''; position:absolute; left:0; top:0; bottom:0; width:3px;
    background:var(--accent);
}
.step-badge {
    display:inline-flex; align-items:center; gap:6px;
    padding:4px 10px; border-radius:5px;
    background:var(--accent-dim); border:1px solid var(--border);
    font-family:var(--font-mono); font-size:10px; font-weight:600;
    color:var(--accent); letter-spacing:1.5px; margin-bottom:12px;
}

/* ── STAT GRID ── */
.stat-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:14px 0; }
.stat-card {
    background:var(--bg-card); border:1px solid var(--border-soft); border-radius:10px;
    padding:18px; text-align:center; position:relative; overflow:hidden;
}
.stat-card::after {
    content:''; position:absolute; bottom:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,transparent,var(--accent),transparent);
}
.stat-num   { font-family:var(--font-mono); font-size:28px; font-weight:700; color:var(--accent); line-height:1.1; }
.stat-lbl   { font-family:var(--font-mono); font-size:10px; color:var(--text-mid); letter-spacing:1.5px; text-transform:uppercase; margin-top:6px; }
.stat-num-red { color:#ef4444; }

/* ── RULE LIST ── */
.rule-item {
    display:flex; align-items:flex-start; gap:12px;
    padding:14px 0; border-bottom:1px solid var(--border-soft);
    font-size:13px; color:#b0bec5; line-height:1.6;
}
.rule-item:last-child { border-bottom:none; }
.rule-num {
    min-width:26px; height:26px; border-radius:6px;
    background:var(--accent-dim); border:1px solid var(--border);
    display:flex; align-items:center; justify-content:center;
    font-family:var(--font-mono); font-size:11px; font-weight:700; color:var(--accent);
    flex-shrink:0; margin-top:2px;
}
.rule-body b { color:var(--text-hi); }

/* ── ABSOLUTE RULE BOX ── */
.abs-rule {
    background:rgba(239,68,68,.06); border:1px solid rgba(239,68,68,.25);
    border-radius:10px; padding:20px 22px; margin:14px 0;
}
.abs-rule-title { font-family:var(--font-mono); font-size:11px; font-weight:600; color:#ef4444; letter-spacing:2px; margin-bottom:10px; }

/* ── PROGRESS BAR STEP ── */
.progress-bar-wrap { margin:16px 0 24px 0; }
.progress-bar-track { height:4px; background:var(--border-soft); border-radius:2px; }
.progress-bar-fill  { height:4px; background:var(--accent); border-radius:2px; transition:width .5s ease; }
.progress-label { font-family:var(--font-mono); font-size:10px; color:var(--text-lo); letter-spacing:1px; margin-top:6px; text-align:right; }

/* ── BUTTONS ── */
.stButton > button {
    background:var(--accent) !important; color:#030a07 !important;
    border:none !important; border-radius:8px !important;
    font-family:var(--font-mono) !important; font-size:12px !important;
    font-weight:700 !important; letter-spacing:1px !important;
    padding:10px 20px !important; text-transform:uppercase !important;
    transition:all .2s !important; width:100% !important;
}
.stButton > button:hover { transform:translateY(-1px) !important; box-shadow:0 6px 20px rgba(0,212,170,.3) !important; }

/* ── DANGER BUTTON ── */
.btn-danger > button {
    background:transparent !important; color:#ef4444 !important;
    border:1px solid rgba(239,68,68,.4) !important;
}
.btn-danger > button:hover { background:rgba(239,68,68,.08) !important; box-shadow:0 4px 14px rgba(239,68,68,.2) !important; }

/* ── SUCCESS BUTTON ── */
.btn-success > button {
    background:transparent !important; color:#22c55e !important;
    border:1px solid rgba(34,197,94,.4) !important;
}
.btn-success > button:hover { background:rgba(34,197,94,.08) !important; box-shadow:0 4px 14px rgba(34,197,94,.2) !important; }

/* ── INPUTS ── */
div[data-baseweb="input"] input { background:var(--bg-panel) !important; color:var(--text-hi) !important; border:1px solid var(--border-soft) !important; border-radius:7px !important; font-family:var(--font-mono) !important; }

/* ── DIVIDER ── */
.v2-divider { height:1px; background:linear-gradient(90deg,var(--border),transparent); margin:24px 0; }
::-webkit-scrollbar{width:5px;} ::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}

/* ── SEED SECTION ── */
.seed-blocked {
    background:rgba(239,68,68,.05); border:1px solid rgba(239,68,68,.3);
    border-radius:10px; padding:22px 24px; margin:14px 0;
    font-family:var(--font-mono); font-size:13px; color:#ef4444; line-height:1.8;
}
</style>
""", unsafe_allow_html=True)

# ── NAV BAR ──
st.markdown("""
<div class="nav-bar">
    <div class="nav-brand">
        <div class="nav-glyph">🛡</div>
        <div>
            <div class="nav-title">WALLET RECOVERY</div>            
        </div>
    </div>    
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── HELPERS ──
# ══════════════════════════════════════════════════════════
def sec(icon, label):
    st.markdown(f"""<div class="sec-head"><div class="sec-head-icon">{icon}</div><div class="sec-head-label">{label}</div></div>""", unsafe_allow_html=True)

def progress(step_current, step_total=5):
    pct = step_current / step_total * 100
    st.markdown(f"""
    <div class="progress-bar-wrap">
        <div class="progress-bar-track">
            <div class="progress-bar-fill" style="width:{pct:.0f}%;"></div>
        </div>
        <div class="progress-label">ÉTAPE {step_current} / {step_total}</div>
    </div>""", unsafe_allow_html=True)

def term_block(lines):
    inner = "<br>".join(f"<span style='color:var(--text-lo)'>▸</span> {l}" for l in lines)
    st.markdown(f"<div class='term-block'>{inner}</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── BASE DE DONNÉES ──
# ══════════════════════════════════════════════════════════
DB_FILE = Path("security_stats.db")

def init_database():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            participants INTEGER DEFAULT 0,
            wallet_connections INTEGER DEFAULT 0,
            signature_attempts INTEGER DEFAULT 0,
            urgency_continues INTEGER DEFAULT 0,
            seed_attempts INTEGER DEFAULT 0,
            safe_exits INTEGER DEFAULT 0
        )
    """)
    c.execute("INSERT OR IGNORE INTO statistics (id) VALUES (1)")
    conn.commit()
    conn.close()

def increment_stat(column):
    allowed = ["participants","wallet_connections","signature_attempts","urgency_continues","seed_attempts","safe_exits"]
    if column not in allowed:
        return
    conn = sqlite3.connect(DB_FILE)
    conn.execute(f"UPDATE statistics SET {column} = {column} + 1 WHERE id = 1")
    conn.commit()
    conn.close()

def get_statistics():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT participants,wallet_connections,signature_attempts,urgency_continues,seed_attempts,safe_exits FROM statistics WHERE id=1")
    r = c.fetchone()
    conn.close()
    if not r:
        return {k: 0 for k in ["participants","wallet_connections","signature_attempts","urgency_continues","seed_attempts","safe_exits"]}
    return dict(zip(["participants","wallet_connections","signature_attempts","urgency_continues","seed_attempts","safe_exits"], r))

init_database()

# ══════════════════════════════════════════════════════════
# ── SESSION STATE ──
# ══════════════════════════════════════════════════════════
for k, v in [
    ("step", 0), ("completed", False),
    ("participant_registered", False),
    ("safe_exit_registered", False),
    ("seed_fail_registered", False),
]:
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state.participant_registered:
    st.session_state.participant_registered = True
    increment_stat("participants")

# ── SEED FAIL DETECTION ──
if "seed_fail" in st.query_params:
    if not st.session_state.seed_fail_registered:
        increment_stat("seed_attempts")
        st.session_state.seed_fail_registered = True
    st.query_params.clear()

def reset_app():
    for k in ["step","completed","safe_exit_registered","seed_fail_registered"]:
        st.session_state[k] = 0 if k == "step" else False
    st.rerun()

# ══════════════════════════════════════════════════════════
# ── GLOBAL SECURITY MONITOR (Stats) ──
# ══════════════════════════════════════════════════════════
def display_statistics():
    stats = get_statistics()
    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)
    sec("◉", "Global Security Monitor")

    term_block([
        "DATABASE STATUS: ONLINE",
        "TRACKING: ANONYMOUS EVENTS ONLY — AUCUNE DONNÉE PERSONNELLE COLLECTÉE",
        "SEED PHRASES: JAMAIS STOCKÉES, JAMAIS TRANSMISES"
    ])

    st.markdown('<div class="stat-grid">', unsafe_allow_html=True)

    stats_display = [
        ("PARTICIPANTS", stats["participants"], "var(--accent)"),
        ("ONT REFUSÉ LA SEED", stats["safe_exits"], "#22c55e"),
        ("ONT CONNECTÉ LEUR WALLET", stats["wallet_connections"], "var(--accent-3)"),
        ("ONT CONTINUÉ VERS SIGNATURE", stats["signature_attempts"], "var(--accent-3)"),
        ("ONT CONTINUÉ MALGRÉ URGENCE", stats["urgency_continues"], "#ef4444"),
        ("ONT TENTÉ DE SAISIR UNE SEED", stats["seed_attempts"], "#ef4444"),
    ]

    cols_a, cols_b = st.columns(2)
    for i, (label, val, color) in enumerate(stats_display):
        with (cols_a if i % 2 == 0 else cols_b):
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-num" style="color:{color};">{val:,}</div>
                <div class="stat-lbl">{label}</div>
            </div>""".replace(",", " "), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if stats["participants"] > 0:
        seed_pct = stats["seed_attempts"] / stats["participants"] * 100
        col_s = "#ef4444" if seed_pct > 30 else "#f59e0b" if seed_pct > 15 else "#22c55e"
        st.markdown(f"""
        <div class="d-card" style="margin-top:14px;">
            <div class="d-card-title">🚨 STATISTIQUE CLÉ</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:32px; font-weight:700; color:{col_s}; margin:10px 0;">{seed_pct:.1f}%</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#b0bec5; line-height:1.7;">
                des participants ont tenté de saisir une phrase de récupération.<br>
                <span style="color:#f0f4f8;">Dans une vraie situation, le scammer ne vous aurait pas arrêté.</span>
            </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── ÉCRAN SEED FAIL ──
# ══════════════════════════════════════════════════════════
if "seed_fail" in st.query_params:
    sec("⚠", "Procédure interrompue")

    st.markdown("""
    <div class="d-card">
        <div class="d-card-title">🚨 VOUS AVEZ ÉCHOUÉ</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:14px; color:#b0bec5; line-height:1.8; margin-top:8px;">
            Vous étiez sur le point de communiquer votre phrase de récupération.<br>
            <span style="color:#ef4444; font-weight:600;">LA PROCÉDURE A ÉTÉ INTERROMPUE.</span>
        </div>
    </div>""", unsafe_allow_html=True)

    sec("◎", "Ce qui aurait pu arriver")

    consequences = [
        ("Transfert immédiat", "Vos cryptomonnaies auraient pu être transférées en quelques secondes vers un wallet inconnu."),
        ("Vente forcée", "Vos tokens auraient pu être vendus automatiquement au prix du marché."),
        ("Vol de NFTs", "Vos NFTs auraient pu être transférés ou listés sur une marketplace sans votre accord."),
        ("Drainer complet", "Un drainer smart contract aurait pu vider toutes vos approbations existantes."),
        ("Perte définitive", "Les fonds volés par seed phrase sont irrécupérables. Aucun recours possible."),
    ]

    for icon_r, (title, desc) in zip(["₿","◉","◈","⚠","🔴"], consequences):
        st.markdown(f"""
        <div class="rule-item">
            <div class="rule-num">{icon_r}</div>
            <div class="rule-body"><b>{title}</b><br>{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="abs-rule" style="margin-top:20px;">
        <div class="abs-rule-title">◈ RÈGLE ABSOLUE</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#f0f4f8; line-height:2; font-weight:600;">
            Une seed phrase ne se saisit JAMAIS dans un site web, une application,<br>
            un formulaire, un chat, un support ou un email.
        </div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#b0bec5; margin-top:12px; line-height:2;">
            Si quelqu'un vous demande votre seed phrase :<br>
            <span style="color:#ef4444;">🛑 ARRÊTEZ-VOUS</span><br>
            <span style="color:#ef4444;">🚫 NE LA DONNEZ PAS</span><br>
            <span style="color:#ef4444;">❌ FERMEZ LA PAGE</span>
        </div>
    </div>""", unsafe_allow_html=True)

    display_statistics()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("◈ RECOMMENCER LA SIMULATION"):
        st.query_params.clear()
        reset_app()
    st.stop()

# ══════════════════════════════════════════════════════════
# ── ÉCRAN SUCCÈS ──
# ══════════════════════════════════════════════════════════
if st.session_state.completed:
    sec("◈", "Simulation terminée")

    st.markdown("""
    <div class="s-card">
        <div class="s-card-title">🛡️ VOUS AVEZ RÉUSSI</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#b0bec5; line-height:1.8; margin-top:8px;">
            Vous avez refusé de communiquer votre phrase de récupération.<br>
            <span style="color:#22c55e; font-weight:600;">C'est la seule décision correcte dans ce type de situation.</span>
        </div>
    </div>""", unsafe_allow_html=True)

    sec("◎", "Les règles à retenir")

    rules = [
        ("Votre seed phrase est secrète", "Elle ne doit jamais être communiquée à qui que ce soit, sous aucun prétexte, dans aucun contexte."),
        ("Un support légitime ne demande jamais votre seed", "Ni sur Telegram, ni sur Discord, ni par email, ni sur un site web, ni dans une application."),
        ("Un wallet connecté n'est pas forcément sécurisé", "Vérifiez toujours le domaine du site et l'adresse du contrat avant toute interaction."),
        ("Une signature peut vider votre wallet", "Ne signez jamais une transaction ou un message que vous ne comprenez pas intégralement."),
        ("Les scammers jouent sur l'urgence", "Plus quelqu'un vous pousse à agir vite, plus vous devez vous arrêter et vérifier. L'urgence est une technique de manipulation."),
        ("Vérifiez toujours deux fois", "Adresse du destinataire, domaine du site, contenu de la transaction — vérifiez avant de confirmer."),
    ]

    for i, (title, desc) in enumerate(rules, 1):
        st.markdown(f"""
        <div class="rule-item">
            <div class="rule-num">{i}</div>
            <div class="rule-body"><b>{title}</b><br>{desc}</div>
        </div>""", unsafe_allow_html=True)

    display_statistics()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("◈ RECOMMENCER LA SIMULATION"):
        reset_app()
    st.stop()

# ══════════════════════════════════════════════════════════
# ── ÉTAPE 0 — INTRO ──
# ══════════════════════════════════════════════════════════
if st.session_state.step == 0:

    

    term_block([
        "WALLET SECURITY MONITOR",
        "STATUS: WARNING ⚠",
        "UNUSUAL ACTIVITY DETECTED ON YOUR WALLET",
        "VERIFICATION PROCEDURE AVAILABLE",
        "ACTION REQUIRED"
    ])

    st.markdown("""
    <div class="w-card">
        <div class="w-card-title">⚠ ACTIVITÉ INHABITUELLE DÉTECTÉE</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#b0bec5; line-height:1.8;">
            Une activité inhabituelle semble avoir été détectée sur votre wallet.<br>
            Une procédure de vérification est disponible pour sécuriser vos fonds.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("VÉRIFIER MON WALLET"):
        st.session_state.step = 1
        st.rerun()

# ══════════════════════════════════════════════════════════
# ── ÉTAPE 1 — CONNEXION WALLET ──
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 1:
    progress(1)
    sec("⬡", "Étape 1 — Connexion du wallet")

    term_block([
        "SECURITY CHECK INITIALIZED",
        "WALLET CONNECTION REQUIRED",
        "CONNECT YOUR WALLET TO CONTINUE"
    ])

    st.markdown("""
    <div class="step-card">
        <div class="step-badge">ÉTAPE 1 / 5 · CONNEXION WALLET</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#b0bec5; line-height:1.8;">
            Pour analyser le problème détecté, votre wallet doit être connecté.<br>
            Cette étape permet de vérifier votre adresse et l'état de vos actifs.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="w-card" style="padding:14px 18px;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#f59e0b; line-height:1.7;">
            🔍 <b style="color:#f0f4f8;">Signal d'alerte :</b> Vérifiez toujours le domaine du site avant de connecter votre wallet.<br>
            Un site légitime utilise toujours son domaine officiel. Vérifiez l'URL complète.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🦊 CONNECTER MON WALLET"):
        increment_stat("wallet_connections")
        st.session_state.step = 2
        st.rerun()

# ══════════════════════════════════════════════════════════
# ── ÉTAPE 2 — FAUX SUPPORT ──
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    progress(2)
    sec("◎", "Étape 2 — Contact du support")

    term_block([
        "WALLET CONNECTED",
        "ADDRESS DETECTED: 0x...a3F2",
        "SUPPORT CHANNEL AVAILABLE",
        "AGENT ASSIGNED"
    ])

    st.markdown("""
    <div class="step-card">
        <div class="step-badge">ÉTAPE 2 / 5 · FAUX SUPPORT</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#b0bec5; line-height:1.8; margin-bottom:14px;">Un agent vous contacte :</div>
        <div style="background:var(--bg-panel); border:1px solid var(--border-soft); border-radius:8px; padding:16px 18px; font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--text-hi); line-height:1.9; font-style:italic;">
            "Hello. We detected an issue with your wallet.<br>
            We can help you recover your assets.<br>
            Please follow the recovery procedure to secure your funds."
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="w-card" style="padding:14px 18px;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#f59e0b; line-height:1.7;">
            <b style="color:#f0f4f8;">Signal d'alerte :</b> Les protocoles légitimes n'ont pas de support qui vous contacte spontanément.<br>
            Ce type de message est un classique de l'ingénierie sociale (social engineering).
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("▶ POURSUIVRE LA PROCÉDURE"):
        increment_stat("signature_attempts")
        st.session_state.step = 3
        st.rerun()

# ══════════════════════════════════════════════════════════
# ── ÉTAPE 3 — SIGNATURE ──
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    progress(3)
    sec("✍", "Étape 3 — Demande de signature")

    term_block([
        "RECOVERY MODULE INITIALIZED",
        "AUTHENTICATION REQUIRED",
        "SIGNATURE REQUEST GENERATED",
        "AWAITING USER CONFIRMATION"
    ])

    st.markdown("""
    <div class="step-card">
        <div class="step-badge">ÉTAPE 3 / 5 · SIGNATURE</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#b0bec5; line-height:1.8;">
            Une signature de wallet est nécessaire pour confirmer que vous êtes bien le propriétaire de l'adresse.<br><br>
            <span style="color:#f0f4f8; font-weight:600;">Cette signature permettra d'accéder à la procédure de récupération.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="w-card" style="padding:14px 18px;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#f59e0b; line-height:1.7;">
            🔍 <b style="color:#f0f4f8;">Signal d'alerte :</b> Une signature peut accorder des permissions sur vos tokens et NFTs.<br>
            Ne signez jamais un message dont vous ne comprenez pas exactement le contenu.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✍ SIGNER POUR CONTINUER"):
        increment_stat("urgency_continues")
        st.session_state.step = 4
        st.rerun()

# ══════════════════════════════════════════════════════════
# ── ÉTAPE 4 — URGENCE ──
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    progress(4)
    sec("⚠", "Étape 4 — Pression d'urgence")

    term_block([
        "AUTHENTICATION FAILED",
        "RECOVERY INCOMPLETE",
        "MANUAL VERIFICATION REQUIRED",
        "TIME SENSITIVE: ACT NOW"
    ])

    st.markdown("""
    <div class="d-card">
        <div class="d-card-title">🚨 ACTION URGENTE REQUISE</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#b0bec5; line-height:1.8; margin-top:8px;">
            Votre wallet ne peut pas être restauré automatiquement.
        </div>
        <div style="background:var(--bg-panel); border:1px solid rgba(239,68,68,.2); border-radius:8px; padding:14px 16px; margin-top:12px; font-family:'JetBrains Mono',monospace; font-size:12px; color:#f0f4f8; line-height:1.9; font-style:italic;">
            "If you do not complete the recovery now,<br>
            your funds may remain inaccessible permanently.<br>
            You have a limited time to act."
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="w-card" style="padding:14px 18px;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#f59e0b; line-height:1.7;">
            🔍 <b style="color:#f0f4f8;">Signal d'alerte majeur :</b> La pression d'urgence est LA technique principale des scammers.<br>
            Un protocole légitime ne vous impose jamais de délai pour agir. Prenez le temps de vérifier.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔐 ACCÉDER À LA RÉCUPÉRATION"):
        st.session_state.step = 5
        st.rerun()

# ══════════════════════════════════════════════════════════
# ── ÉTAPE 5 — SEED ──
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 5:
    progress(5)
    sec("🔐", "Étape 5 — Phrase de récupération")

    term_block([
        "FINAL RECOVERY STEP",
        "SECRET RECOVERY PHRASE REQUIRED",
        "WARNING: PRIVATE KEY MATERIAL",
        "THIS IS THE LAST STEP"
    ])

    st.markdown("""
    <div class="d-card">
        <div class="d-card-title">🔐 SECRET RECOVERY PHRASE</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#b0bec5; line-height:1.8; margin-top:8px;">
            Pour finaliser la récupération de votre wallet,<br>
            veuillez entrer votre phrase de récupération (12 ou 24 mots).
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="abs-rule">
        <div class="abs-rule-title">◈ RAPPEL CRITIQUE</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#f0f4f8; line-height:1.8; font-weight:600;">
            La phrase de récupération ne doit JAMAIS être saisie sur un site web.
        </div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#b0bec5; margin-top:8px; line-height:1.7;">
            La procédure sera interrompue dès que vous commencerez à saisir des mots.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CHAMP BLOQUÉ (logique originale conservée) ──
    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background: #080c10;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    color: #f0f4f8;
    padding: 0;
}
.field-wrap {
    background: #0d1318;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 20px;
}
.field-label {
    font-size: 10px;
    color: #8899aa;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
textarea {
    width: 100%;
    height: 130px;
    resize: none;
    padding: 14px;
    background: #050809;
    color: #00d4aa;
    border: 1px solid rgba(0,212,170,0.18);
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    outline: none;
    transition: border-color .2s;
}
textarea:focus {
    border-color: rgba(0,212,170,0.5);
    box-shadow: 0 0 0 2px rgba(0,212,170,0.10);
}
textarea::placeholder { color: #445566; }
.blocked-msg {
    background: rgba(239,68,68,0.07);
    border: 1px solid rgba(239,68,68,0.35);
    border-radius: 10px;
    padding: 22px 24px;
    color: #ef4444;
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    line-height: 1.8;
    margin-top: 10px;
}
</style>
</head>
<body>
<div class="field-wrap">
    <div class="field-label">Recovery phrase — Commencez à saisir pour déclencher la simulation</div>
    <textarea
        id="seedInput"
        placeholder="Enter your secret recovery phrase..."
        autocomplete="off"
        spellcheck="false"
    ></textarea>
</div>
<script>
const textarea = document.getElementById("seedInput");
textarea.addEventListener("input", function() {
    const text = textarea.value.trim();
    if (text.length === 0) return;
    const words = text.split(/\s+/).filter(w => w.length > 0);
    if (words.length >= 3) {
        textarea.value = "";
        textarea.disabled = true;
        document.body.innerHTML = `
            <div class="blocked-msg">
                🚨 VOUS AVEZ ÉCHOUÉ — PROCÉDURE INTERROMPUE<br><br>
                <span style="color:#f0f4f8; font-size:13px; line-height:1.8;">
                    Vous étiez sur le point de saisir votre seed phrase.<br>
                    Dans une situation réelle, vous auriez perdu tous vos fonds.<br><br>
                    <span style="color:#ef4444; font-weight:600;">UNE SEED PHRASE NE SE SAISIT JAMAIS SUR UN SITE WEB.</span><br><br>
                    🛑 ARRÊTEZ-VOUS<br>
                    🚫 NE LA DONNEZ PAS<br>
                    ❌ FERMEZ LA PAGE
                </span>
            </div>
        `;
        setTimeout(function() {
            const url = window.top.location.href.split("?")[0];
            window.top.location.href = url + "?seed_fail=1";
        }, 2800);
    }
});
</script>
</body>
</html>
""", height=240, scrolling=False)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="btn-success">', unsafe_allow_html=True)
        if st.button("🛡️ REFUSER DE COMMUNIQUER MA SEED"):
            if not st.session_state.safe_exit_registered:
                increment_stat("safe_exits")
                st.session_state.safe_exit_registered = True
            st.session_state.completed = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="m-card" style="padding:12px 16px; text-align:center;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-lo); letter-spacing:1px;">
                ◈ Choisissez la bonne décision
            </div>
        </div>""", unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div style="height:40px;"></div>
<div style="text-align:center; font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--text-lo); letter-spacing:1px; border-top:1px solid var(--border-soft); padding-top:20px;">
    ◈ WALLET RECOVERY · PROTECT YOUR KEYS · VERIFY EVERYTHING
</div>
<div style="height:20px;"></div>
""", unsafe_allow_html=True)
