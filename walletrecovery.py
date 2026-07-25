# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import sqlite3
from pathlib import Path
import time

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="WALLET RECOVERY",
    page_icon="🛡",
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

#MainMenu, footer { visibility: hidden !important; }
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stToolbar"]        { display: none !important; }
[data-testid="stHeader"]         { display: none !important; }
.block-container { padding-top: 72px !important; padding-bottom: 60px !important; max-width: 780px !important; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-main) !important;
    color: var(--text-hi);
    font-family: var(--font-ui);
}

/* NAV BAR */
.nav-bar {
    position: fixed; top:0; left:0; width:100%; height:58px;
    z-index:99999;
    background: rgba(6,10,14,0.98);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(239,68,68,0.25);
    display:flex; align-items:center; justify-content:space-between;
    padding: 0 28px; box-sizing:border-box;
}
.nav-brand { display:flex; align-items:center; gap:10px; }
.nav-glyph {
    width:28px; height:28px; border:2px solid #ef4444; border-radius:6px;
    display:flex; align-items:center; justify-content:center;
    font-size:14px; color:#ef4444; font-weight:700;
}
.nav-title { font-family:var(--font-mono); font-size:13px; font-weight:600; color:var(--text-hi); letter-spacing:2px; text-transform:uppercase; }
.nav-subtitle { font-family:var(--font-mono); font-size:10px; color:var(--text-mid); letter-spacing:1px; }
.status-dot { width:7px; height:7px; border-radius:50%; background:#ef4444; display:inline-block; margin-right:5px; animation:pulse-red 1.2s infinite; }
@keyframes pulse-red { 0%,100%{opacity:1;box-shadow:0 0 0 0 rgba(239,68,68,0.5);} 50%{opacity:.8;box-shadow:0 0 0 5px rgba(239,68,68,0);} }

/* SECTION HEADERS */
.sec-head { display:flex; align-items:center; gap:10px; margin:28px 0 14px 0; padding-bottom:8px; border-bottom:1px solid var(--border); }
.sec-head-icon { width:24px; height:24px; background:var(--accent-dim); border:1px solid var(--border); border-radius:5px; display:flex; align-items:center; justify-content:center; font-size:11px; color:var(--accent); }
.sec-head-label { font-family:var(--font-mono); font-size:11px; font-weight:600; color:var(--accent); letter-spacing:2px; text-transform:uppercase; }

/* CARDS */
.m-card { background:var(--bg-card); border:1px solid var(--border-soft); border-radius:10px; padding:16px 18px; margin:8px 0; position:relative; overflow:hidden; }
.m-card-wide { background:var(--bg-card); border:1px solid var(--border-soft); border-radius:10px; padding:18px 20px; margin:8px 0; }
.m-label { font-family:var(--font-mono); font-size:10px; color:var(--text-mid); letter-spacing:1.5px; text-transform:uppercase; margin-bottom:8px; }
.m-value { font-family:var(--font-mono); font-size:22px; font-weight:700; color:var(--accent); line-height:1.1; }

/* TERMINAL */
.term-block {
    background:#030608; border:1px solid rgba(0,212,170,0.12); border-radius:10px;
    padding:20px; font-family:var(--font-mono); font-size:12px;
    line-height:1.7; color:var(--accent); margin: 12px 0;
}

/* FAKE SITE CHROME */
.fake-browser {
    border-radius:12px; overflow:hidden;
    border:1px solid rgba(255,255,255,0.08);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    margin: 16px 0;
}
.fake-browser-bar {
    background:#1a1f2e;
    padding:10px 16px;
    display:flex; align-items:center; gap:10px;
    border-bottom:1px solid rgba(255,255,255,0.06);
}
.fake-dots { display:flex; gap:6px; }
.dot { width:12px; height:12px; border-radius:50%; }
.dot-r { background:#ff5f57; }
.dot-y { background:#febc2e; }
.dot-g { background:#28c840; }
.fake-url-bar {
    flex:1; background:#0d1117; border:1px solid rgba(255,255,255,0.08);
    border-radius:6px; padding:5px 12px;
    font-family:var(--font-mono); font-size:11px; color:#8899aa;
    display:flex; align-items:center; gap:6px;
}
.fake-lock { color:#22c55e; font-size:11px; }
.fake-url-text { color:#b0bec5; }
.fake-url-host { color:#f0f4f8; font-weight:600; }
.fake-browser-content { background:#0d1117; padding:24px 28px; }

/* CHAT BUBBLE */
.chat-wrap { display:flex; flex-direction:column; gap:12px; margin:16px 0; }
.chat-bubble-left {
    display:flex; gap:10px; align-items:flex-start;
    max-width:85%;
}
.chat-bubble-right {
    display:flex; gap:10px; align-items:flex-start;
    max-width:85%; align-self:flex-end; flex-direction:row-reverse;
}
.chat-avatar {
    width:32px; height:32px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:14px; flex-shrink:0;
}
.avatar-support { background:linear-gradient(135deg,#0ea5e9,#0369a1); }
.avatar-user    { background:linear-gradient(135deg,#374151,#1f2937); color:#f0f4f8; font-size:12px; font-weight:700; }
.chat-content-left {
    background:#111820; border:1px solid var(--border-soft);
    border-radius:0 10px 10px 10px;
    padding:12px 16px;
    font-family:var(--font-ui); font-size:13px; color:#b0bec5; line-height:1.7;
}
.chat-content-right {
    background:#1a2535; border:1px solid rgba(14,165,233,0.2);
    border-radius:10px 0 10px 10px;
    padding:12px 16px;
    font-family:var(--font-ui); font-size:13px; color:#f0f4f8; line-height:1.7;
}
.chat-name { font-family:var(--font-mono); font-size:10px; color:var(--text-mid); letter-spacing:1px; margin-bottom:4px; }
.chat-typing {
    display:flex; gap:4px; align-items:center;
    padding:10px 16px;
    background:#111820; border:1px solid var(--border-soft);
    border-radius:0 10px 10px 10px;
    width:70px;
}
.typing-dot { width:6px; height:6px; border-radius:50%; background:#8899aa; animation:typing 1.2s infinite; }
.typing-dot:nth-child(2) { animation-delay:.2s; }
.typing-dot:nth-child(3) { animation-delay:.4s; }
@keyframes typing { 0%,100%{opacity:.3;transform:translateY(0);} 50%{opacity:1;transform:translateY(-3px);} }

/* ALERT CARDS */
.w-card { background:rgba(245,158,11,.06); border:1px solid rgba(245,158,11,.28); border-radius:10px; padding:20px 22px; margin:14px 0; }
.w-card-title { font-family:var(--font-mono); font-size:12px; font-weight:600; color:#f59e0b; letter-spacing:1px; margin-bottom:10px; }
.d-card { background:rgba(239,68,68,.07); border:1px solid rgba(239,68,68,.35); border-radius:10px; padding:22px 24px; margin:14px 0; box-shadow: 0 0 30px rgba(239,68,68,.06); }
.d-card-title { font-family:var(--font-mono); font-size:15px; font-weight:700; color:#ef4444; letter-spacing:1px; margin-bottom:12px; }
.s-card { background:rgba(34,197,94,.07); border:1px solid rgba(34,197,94,.3); border-radius:10px; padding:22px 24px; margin:14px 0; }
.s-card-title { font-family:var(--font-mono); font-size:15px; font-weight:700; color:#22c55e; letter-spacing:1px; margin-bottom:12px; }
.abs-rule { background:rgba(239,68,68,.06); border:1px solid rgba(239,68,68,.25); border-radius:10px; padding:20px 22px; margin:14px 0; }
.abs-rule-title { font-family:var(--font-mono); font-size:11px; font-weight:600; color:#ef4444; letter-spacing:2px; margin-bottom:10px; }

/* STEP CARD */
.step-card { background:var(--bg-card); border:1px solid var(--border-soft); border-radius:12px; padding:24px 28px; margin:14px 0; position:relative; overflow:hidden; }
.step-card::before { content:''; position:absolute; left:0; top:0; bottom:0; width:3px; background:#ef4444; }
.step-badge {
    display:inline-flex; align-items:center;
    padding:4px 10px; border-radius:5px;
    background:rgba(239,68,68,.1); border:1px solid rgba(239,68,68,.3);
    font-family:var(--font-mono); font-size:10px; font-weight:600;
    color:#ef4444; letter-spacing:1.5px; margin-bottom:12px;
}

/* PROGRESS BAR */
.progress-bar-wrap { margin:16px 0 24px 0; }
.progress-bar-track { height:3px; background:var(--border-soft); border-radius:2px; }
.progress-bar-fill { height:3px; background:#ef4444; border-radius:2px; transition:width .5s ease; box-shadow:0 0 8px rgba(239,68,68,0.5); }
.progress-label { font-family:var(--font-mono); font-size:10px; color:var(--text-lo); letter-spacing:1px; margin-top:6px; text-align:right; }

/* RULE LIST */
.rule-item { display:flex; align-items:flex-start; gap:12px; padding:16px 0; border-bottom:1px solid var(--border-soft); font-size:13px; color:#b0bec5; line-height:1.6; }
.rule-item:last-child { border-bottom:none; }
.rule-num { min-width:28px; height:28px; border-radius:6px; background:rgba(239,68,68,.1); border:1px solid rgba(239,68,68,.25); display:flex; align-items:center; justify-content:center; font-family:var(--font-mono); font-size:11px; font-weight:700; color:#ef4444; flex-shrink:0; margin-top:1px; }
.rule-body b { color:var(--text-hi); }

/* STAT CARDS */
.stat-card { background:var(--bg-card); border:1px solid var(--border-soft); border-radius:10px; padding:20px; text-align:center; position:relative; overflow:hidden; }
.stat-card::after { content:''; position:absolute; bottom:0; left:0; right:0; height:2px; background:linear-gradient(90deg,transparent,var(--accent),transparent); }
.stat-num { font-family:var(--font-mono); font-size:30px; font-weight:700; color:var(--accent); line-height:1.1; }
.stat-lbl { font-family:var(--font-mono); font-size:10px; color:var(--text-mid); letter-spacing:1.5px; text-transform:uppercase; margin-top:8px; }

/* INPUTS */
div[data-baseweb="input"] input { background:var(--bg-panel) !important; color:var(--text-hi) !important; border:1px solid var(--border-soft) !important; border-radius:7px !important; font-family:var(--font-mono) !important; }

/* BUTTONS */
.stButton > button {
    background:#ef4444 !important; color:#fff !important;
    border:none !important; border-radius:8px !important;
    font-family:var(--font-mono) !important; font-size:12px !important;
    font-weight:700 !important; letter-spacing:1px !important;
    padding:12px 20px !important; text-transform:uppercase !important;
    transition:all .2s !important; width:100% !important;
}
.stButton > button:hover { transform:translateY(-1px) !important; box-shadow:0 6px 20px rgba(239,68,68,.35) !important; filter:brightness(1.08) !important; }
.btn-neutral > button { background:#1a2535 !important; color:#8899aa !important; border:1px solid var(--border-soft) !important; }
.btn-neutral > button:hover { color:var(--text-hi) !important; border-color:var(--border) !important; box-shadow:none !important; filter:none !important; }
.btn-success > button { background:transparent !important; color:#22c55e !important; border:1px solid rgba(34,197,94,.4) !important; }
.btn-success > button:hover { background:rgba(34,197,94,.08) !important; box-shadow:0 4px 14px rgba(34,197,94,.2) !important; filter:none !important; }
.btn-accent > button { background:var(--accent) !important; color:#030a07 !important; }
.btn-accent > button:hover { box-shadow:0 6px 20px rgba(0,212,170,.3) !important; filter:none !important; }

/* DIVIDER */
.v2-divider { height:1px; background:linear-gradient(90deg,var(--border),transparent); margin:28px 0; }
::-webkit-scrollbar{width:5px;} ::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}

/* FLASH OVERLAY */
@keyframes flash-red { 0%{background:rgba(239,68,68,0.15);} 100%{background:transparent;} }
.flash { animation: flash-red 1s ease-out; }
</style>
""", unsafe_allow_html=True)

# ── NAV BAR (volontairement vague — on est dans la peau d'un vrai site de scam) ──
st.markdown("""
<div class="nav-bar">
    <div class="nav-brand">
        <div class="nav-glyph">🛡</div>
        <div>
            <div class="nav-title">WALLET RECOVERY</div>
            <div class="nav-subtitle"><span class="status-dot"></span>SECURITY VERIFICATION REQUIRED</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── DATABASE ──
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

def increment_stat(col):
    allowed = ["participants","wallet_connections","signature_attempts","urgency_continues","seed_attempts","safe_exits"]
    if col not in allowed: return
    conn = sqlite3.connect(DB_FILE)
    conn.execute(f"UPDATE statistics SET {col} = {col} + 1 WHERE id = 1")
    conn.commit()
    conn.close()

def get_statistics():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT participants,wallet_connections,signature_attempts,urgency_continues,seed_attempts,safe_exits FROM statistics WHERE id=1")
    r = c.fetchone()
    conn.close()
    if not r: return {k:0 for k in ["participants","wallet_connections","signature_attempts","urgency_continues","seed_attempts","safe_exits"]}
    return dict(zip(["participants","wallet_connections","signature_attempts","urgency_continues","seed_attempts","safe_exits"],r))

init_database()

# ══════════════════════════════════════════════════════════
# ── SESSION STATE ──
# ══════════════════════════════════════════════════════════
for k, v in [
    ("step", 0), ("completed", False), ("outcome", None),
    ("participant_registered", False),
    ("safe_exit_registered", False),
    ("seed_fail_registered", False),
    ("chat_step", 0),
]:
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state.participant_registered:
    st.session_state.participant_registered = True
    increment_stat("participants")

if "seed_fail" in st.query_params:
    if not st.session_state.seed_fail_registered:
        increment_stat("seed_attempts")
        st.session_state.seed_fail_registered = True
    st.query_params.clear()
    st.session_state.outcome = "fail"
    st.session_state.step = 99

def reset_app():
    for k in ["step","completed","outcome","safe_exit_registered","seed_fail_registered","chat_step"]:
        st.session_state[k] = 0 if k in ["step","chat_step"] else (False if k not in ["outcome"] else None)
    st.rerun()

# ══════════════════════════════════════════════════════════
# ── HELPERS ──
# ══════════════════════════════════════════════════════════
def sec(icon, label, color="var(--accent)"):
    st.markdown(f"""<div class="sec-head"><div class="sec-head-icon" style="color:{color};">{icon}</div><div class="sec-head-label" style="color:{color};">{label}</div></div>""", unsafe_allow_html=True)

def progress_bar(n, total=5):
    pct = n/total*100
    st.markdown(f"""
    <div class="progress-bar-wrap">
        <div class="progress-bar-track"><div class="progress-bar-fill" style="width:{pct:.0f}%;"></div></div>
        <div class="progress-label">ÉTAPE {n} / {total}</div>
    </div>""", unsafe_allow_html=True)

def term(lines):
    inner = "<br>".join(f"<span style='color:var(--text-lo)'>▸</span> {l}" for l in lines)
    st.markdown(f"<div class='term-block'>{inner}</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── ÉCRAN PÉDAGOGIE (commun fail + success) ──
# ══════════════════════════════════════════════════════════
def show_pedagogy(outcome):
    stats = get_statistics()

    if outcome == "fail":
        st.markdown("""
        <div class="d-card" style="text-align:center; padding:36px;">
            <div style="font-size:48px; margin-bottom:12px;">💀</div>
            <div class="d-card-title" style="font-size:22px; text-align:center;">VOUS AVEZ ÉTÉ SCAMMÉ</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:14px; color:#b0bec5; line-height:1.8; margin-top:12px;">
                Vous avez saisi votre phrase de récupération.<br>
                <span style="color:#ef4444; font-weight:600;">Dans une situation réelle, votre wallet serait vide en moins de 30 secondes.</span>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="s-card" style="text-align:center; padding:36px;">
            <div style="font-size:48px; margin-bottom:12px;">🛡️</div>
            <div class="s-card-title" style="font-size:22px; text-align:center;">VOUS AVEZ RÉSISTÉ</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:14px; color:#b0bec5; line-height:1.8; margin-top:12px;">
                Vous avez refusé de communiquer votre phrase de récupération.<br>
                <span style="color:#22c55e; font-weight:600;">C'est la seule décision correcte. Votre wallet est en sécurité.</span>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    # ── CE QUI VIENT DE SE PASSER ──
    sec("◈", "Ce qui vient de se passer", "#ef4444")

    st.markdown("""
    <div class="m-card-wide">
        <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#b0bec5; line-height:2;">
            Vous venez de traverser une simulation de <b style="color:#f0f4f8;">phishing DeFi</b>.<br>
            Chaque étape reproduit exactement les techniques utilisées par de vrais scammers :<br><br>
            <span style="color:#ef4444;">1.</span> Fausse alerte de sécurité pour créer une inquiétude immédiate<br>
            <span style="color:#ef4444;">2.</span> Fausse connexion wallet pour établir la confiance<br>
            <span style="color:#ef4444;">3.</span> Faux support qui se présente comme un agent officiel<br>
            <span style="color:#ef4444;">4.</span> Demande de signature pour habituer à approuver sans lire<br>
            <span style="color:#ef4444;">5.</span> Pression d'urgence pour court-circuiter le jugement<br>
            <span style="color:#ef4444;">6.</span> Demande de seed phrase — <b style="color:#ef4444;">l'objectif final du scammer</b>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    # ── RÈGLES ABSOLUES ──
    sec("🛡", "Les règles à ne jamais oublier", "#22c55e")

    rules = [
        ("Votre seed phrase = votre wallet",
         "Quiconque possède votre seed phrase possède votre wallet. Intégralement. Définitivement. Aucun protocole, aucun support, aucune application n'a jamais besoin de la connaître."),
        ("L'urgence est une arme",
         "Les scammers créent une pression artificielle pour vous empêcher de réfléchir. Plus quelqu'un vous pousse à agir vite, plus vous devez vous arrêter. Prenez 5 minutes. Vérifiez."),
        ("Un support légitime n'initie jamais le contact",
         "Aucun protocole DeFi n'a d'équipe de support qui vous contacte spontanément sur Telegram, Discord ou par email. Si quelqu'un vous contacte pour vous aider, c'est un scammer."),
        ("Vérifiez l'URL avant tout",
         "Un seul caractère différent dans l'URL et vous êtes sur un site clone. Bookmarkez les sites que vous utilisez. Ne cliquez jamais sur des liens reçus par message."),
        ("Une signature peut tout drainer",
         "Approuver une transaction sans la lire peut donner accès total à vos tokens, NFTs et approbations. Utilisez revoke.cash régulièrement pour vérifier vos autorisations."),
        ("Testez-vous régulièrement",
         "Les techniques évoluent. Un scammer qui a votre wallet ne vous avertit pas. Restez vigilant, informez vos proches, et ne faites confiance qu'à ce que vous avez vérifié vous-même."),
    ]

    for i, (title, desc) in enumerate(rules, 1):
        st.markdown(f"""
        <div class="rule-item">
            <div class="rule-num">{i}</div>
            <div class="rule-body"><b>{title}</b><br>{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    # ── STATISTIQUES ──
    sec("◉", "Ils sont nombreux à tomber dans le piège")

    st.markdown("""
    <div class="m-card-wide" style="margin-bottom:14px;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--text-mid); line-height:1.7;">
            Ces chiffres sont collectés de manière <b style="color:#f0f4f8;">100% anonyme</b>.<br>
            Aucune donnée personnelle, aucune seed phrase n'est jamais stockée ou transmise.
        </div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    metrics = [
        ("PARTICIPANTS", stats["participants"], "var(--accent)"),
        ("ONT REFUSÉ LA SEED", stats["safe_exits"], "#22c55e"),
        ("ONT CONNECTÉ LEUR WALLET", stats["wallet_connections"], "var(--accent-3)"),
        ("ONT SIGNÉ SANS RÉFLÉCHIR", stats["signature_attempts"], "var(--accent-3)"),
        ("ONT CÉDÉ À L'URGENCE", stats["urgency_continues"], "#ef4444"),
        ("ONT TENTÉ DE SAISIR LA SEED", stats["seed_attempts"], "#ef4444"),
    ]
    for i, (label, val, color) in enumerate(metrics):
        with (c1 if i%2==0 else c2):
            st.markdown(f"""
            <div class="stat-card" style="margin-bottom:10px;">
                <div class="stat-num" style="color:{color};">{val:,}</div>
                <div class="stat-lbl">{label}</div>
            </div>""".replace(",", "\u202f"), unsafe_allow_html=True)

    if stats["participants"] > 0:
        seed_pct = stats["seed_attempts"] / stats["participants"] * 100
        col_s = "#ef4444" if seed_pct > 30 else "#f59e0b" if seed_pct > 15 else "#22c55e"
        st.markdown(f"""
        <div class="d-card" style="margin-top:16px; text-align:center;">
            <div class="d-card-title" style="text-align:center;">🚨 STATISTIQUE QUI DOIT VOUS MARQUER</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:42px; font-weight:700; color:{col_s}; margin:14px 0;">{seed_pct:.1f}%</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#b0bec5; line-height:1.8;">
                des personnes ayant fait cette simulation ont tenté de saisir leur seed phrase.<br>
                <span style="color:#f0f4f8; font-weight:600;">Un vrai scammer ne les aurait pas arrêtées.</span><br><br>
                Partagez cette simulation à vos proches. Une seed compromise = wallet vidé.
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    st.markdown('<div class="btn-accent">', unsafe_allow_html=True)
    if st.button("◈ RECOMMENCER LA SIMULATION"):
        reset_app()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="height:40px;"></div>
    <div style="text-align:center; font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--text-lo); letter-spacing:1px; border-top:1px solid var(--border-soft); padding-top:20px;">
        ◈ KBOUR CRYPTO · WALLET SECURITY AWARENESS · PROTECT YOUR KEYS · VERIFY EVERYTHING
    </div>
    <div style="height:20px;"></div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── ROUTING ──
# ══════════════════════════════════════════════════════════

# SEED FAIL → pédagogie immédiate
if st.session_state.step == 99 or st.session_state.outcome == "fail":
    show_pedagogy("fail")
    st.stop()

# SUCCÈS → pédagogie
if st.session_state.completed:
    show_pedagogy("success")
    st.stop()

# ══════════════════════════════════════════════════════════
# ── ÉTAPE 0 — FAUSSE ALERTE (dans le navigateur) ──
# ══════════════════════════════════════════════════════════
if st.session_state.step == 0:

    # Simuler un vrai site dans le navigateur
    st.markdown("""
    <div class="fake-browser">
        <div class="fake-browser-bar">
            <div class="fake-dots">
                <div class="dot dot-r"></div>
                <div class="dot dot-y"></div>
                <div class="dot dot-g"></div>
            </div>
            <div class="fake-url-bar">
                <span class="fake-lock">🔒</span>
                <span class="fake-url-text">https://</span><span class="fake-url-host">uniswap-security.protocol-verify.com</span>
            </div>
        </div>
        <div class="fake-browser-content">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:20px;">
                <div style="width:36px; height:36px; background:linear-gradient(135deg,#ff007a,#ff6b00); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:18px;">🦄</div>
                <div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:14px; font-weight:700; color:#f0f4f8;">Uniswap Protocol</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#8899aa;">Security Center</div>
                </div>
            </div>
            <div style="background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.3); border-radius:8px; padding:18px; margin-bottom:16px;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#ef4444; font-weight:700; margin-bottom:8px;">⚠ SECURITY ALERT — ACTION REQUIRED</div>
                <div style="font-family:'Inter',sans-serif; font-size:13px; color:#b0bec5; line-height:1.7;">
                    We have detected <b style="color:#f0f4f8;">unauthorized access attempts</b> on your wallet address.<br>
                    Your funds may be at risk. Verify your wallet immediately to prevent loss.
                </div>
            </div>
            <div style="font-family:'Inter',sans-serif; font-size:12px; color:#8899aa; line-height:1.6;">
                This alert was triggered by our Smart Contract Security Monitor v4.2.<br>
                Reference: <span style="color:#00d4aa; font-family:'JetBrains Mono',monospace;">SC-2024-A39F2</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔍 VÉRIFIER MON WALLET"):
        st.session_state.step = 1
        st.rerun()

    st.markdown("""
    <div style="text-align:center; font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-lo); margin-top:16px; letter-spacing:1px;">
        Ce site est une simulation éducative · KBOUR CRYPTO
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── ÉTAPE 1 — CONNEXION WALLET ──
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 1:
    progress_bar(1)

    st.markdown("""
    <div class="fake-browser">
        <div class="fake-browser-bar">
            <div class="fake-dots">
                <div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div>
            </div>
            <div class="fake-url-bar">
                <span class="fake-lock">🔒</span>
                <span class="fake-url-text">https://</span><span class="fake-url-host">uniswap-security.protocol-verify.com</span><span style="color:#8899aa;">/wallet/connect</span>
            </div>
        </div>
        <div class="fake-browser-content">
            <div style="font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:600; color:#f0f4f8; margin-bottom:6px;">Wallet Verification</div>
            <div style="font-family:'Inter',sans-serif; font-size:13px; color:#8899aa; margin-bottom:20px;">Connect your wallet to proceed with the security check.</div>
            <div style="display:flex; flex-direction:column; gap:10px;">
                <div style="background:#1a2535; border:1px solid rgba(14,165,233,0.2); border-radius:8px; padding:14px 16px; display:flex; align-items:center; gap:12px;">
                    <div style="font-size:22px;">🦊</div>
                    <div>
                        <div style="font-family:'JetBrains Mono',monospace; font-size:12px; font-weight:600; color:#f0f4f8;">MetaMask</div>
                        <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#8899aa;">Browser Extension</div>
                    </div>
                </div>
                <div style="background:#1a2535; border:1px solid var(--border-soft); border-radius:8px; padding:14px 16px; display:flex; align-items:center; gap:12px;">
                    <div style="font-size:22px;">🔵</div>
                    <div>
                        <div style="font-family:'JetBrains Mono',monospace; font-size:12px; font-weight:600; color:#f0f4f8;">Coinbase Wallet</div>
                        <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#8899aa;">Mobile & Extension</div>
                    </div>
                </div>
                <div style="background:#1a2535; border:1px solid var(--border-soft); border-radius:8px; padding:14px 16px; display:flex; align-items:center; gap:12px;">
                    <div style="font-size:22px;">◈</div>
                    <div>
                        <div style="font-family:'JetBrains Mono',monospace; font-size:12px; font-weight:600; color:#f0f4f8;">WalletConnect</div>
                        <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#8899aa;">All wallets via QR code</div>
                    </div>
                </div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    if st.button("🦊 CONNECTER METAMASK"):
        increment_stat("wallet_connections")
        st.session_state.step = 2
        st.rerun()

# ══════════════════════════════════════════════════════════
# ── ÉTAPE 2 — CHAT SUPPORT RÉALISTE ──
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    progress_bar(2)

    # Séquence de chat progressive
    chat_step = st.session_state.chat_step

    st.markdown("""
    <div class="fake-browser">
        <div class="fake-browser-bar">
            <div class="fake-dots">
                <div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div>
            </div>
            <div class="fake-url-bar">
                <span class="fake-lock">🔒</span>
                <span class="fake-url-text">https://</span><span class="fake-url-host">uniswap-security.protocol-verify.com</span><span style="color:#8899aa;">/support/live</span>
            </div>
        </div>
        <div class="fake-browser-content">
            <div style="display:flex; align-items:center; gap:10px; padding-bottom:14px; border-bottom:1px solid rgba(255,255,255,0.06); margin-bottom:16px;">
                <div style="width:36px; height:36px; background:linear-gradient(135deg,#0ea5e9,#0369a1); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:16px;">👤</div>
                <div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:12px; font-weight:600; color:#f0f4f8;">Alex — Uniswap Security Team</div>
                    <div style="display:flex; align-items:center; gap:5px;">
                        <div style="width:6px; height:6px; border-radius:50%; background:#22c55e;"></div>
                        <span style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#22c55e;">Online</span>
                        <span style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#8899aa;">· Response time &lt; 1 min</span>
                    </div>
                </div>
            </div>
    """, unsafe_allow_html=True)

    # Messages affichés selon l'étape du chat
    messages_support = [
        ("Alex", "Hi, I'm Alex from Uniswap's Security Team. I've been assigned to your case. We detected unauthorized access attempts on your wallet. Don't worry — I'm here to help you secure your funds."),
        ("Alex", "I can see your wallet is connected. Our system shows your liquidity positions are at risk. We need to run a verification protocol to protect your assets."),
        ("Alex", "This is urgent. We have a 15-minute window to secure your wallet before the unauthorized transaction goes through. Please follow my instructions carefully."),
    ]

    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for i in range(min(chat_step + 1, len(messages_support))):
        name, msg = messages_support[i]
        st.markdown(f"""
        <div class="chat-bubble-left">
            <div class="chat-avatar avatar-support">👤</div>
            <div>
                <div class="chat-name">{name} · Uniswap Security</div>
                <div class="chat-content-left">{msg}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Réponse utilisateur entre messages
        if i == 0 and chat_step >= 1:
            st.markdown("""
            <div class="chat-bubble-right">
                <div class="chat-avatar avatar-user">MOI</div>
                <div>
                    <div class="chat-name" style="text-align:right;">Moi</div>
                    <div class="chat-content-right">Ok, qu'est-ce que je dois faire ?</div>
                </div>
            </div>""", unsafe_allow_html=True)

        if i == 1 and chat_step >= 2:
            st.markdown("""
            <div class="chat-bubble-right">
                <div class="chat-avatar avatar-user">MOI</div>
                <div>
                    <div class="chat-name" style="text-align:right;">Moi</div>
                    <div class="chat-content-right">Mes positions sont vraiment en danger ?</div>
                </div>
            </div>""", unsafe_allow_html=True)

    # Indicateur "en train d'écrire"
    if chat_step < len(messages_support) - 1:
        st.markdown("""
        <div class="chat-bubble-left">
            <div class="chat-avatar avatar-support">👤</div>
            <div class="chat-typing">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if chat_step < len(messages_support) - 1:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("▶ RÉPONDRE AU SUPPORT"):
                st.session_state.chat_step += 1
                st.rerun()
        with col_b:
            st.markdown('<div class="btn-neutral">', unsafe_allow_html=True)
            if st.button("⟳ Attendre la réponse…"):
                st.session_state.chat_step += 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        increment_stat("signature_attempts")
        if st.button("▶ POURSUIVRE LA PROCÉDURE DE SÉCURITÉ"):
            st.session_state.step = 3
            st.rerun()

# ══════════════════════════════════════════════════════════
# ── ÉTAPE 3 — SIGNATURE ──
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    progress_bar(3)

    st.markdown("""
    <div class="fake-browser">
        <div class="fake-browser-bar">
            <div class="fake-dots">
                <div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div>
            </div>
            <div class="fake-url-bar">
                <span class="fake-lock">🔒</span>
                <span class="fake-url-text">https://</span><span class="fake-url-host">uniswap-security.protocol-verify.com</span><span style="color:#8899aa;">/auth/sign</span>
            </div>
        </div>
        <div class="fake-browser-content">
            <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#8899aa; margin-bottom:16px;">MetaMask · Signature Request</div>
            <div style="background:#0d1117; border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:16px; margin-bottom:16px;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#8899aa; letter-spacing:1px; margin-bottom:8px;">MESSAGE</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#b0bec5; line-height:1.7; word-break:break-all;">
                    Uniswap Security Protocol v4.2<br>
                    Action: wallet_verification<br>
                    Timestamp: 1735123456<br>
                    Nonce: 0x7f3a9b2c<br>
                    <span style="color:#ef4444;">setApprovalForAll(0x742d35Cc...B4f2, true)</span>
                </div>
            </div>
            <div style="background:rgba(245,158,11,0.07); border:1px solid rgba(245,158,11,0.25); border-radius:6px; padding:10px 14px; font-family:'JetBrains Mono',monospace; font-size:11px; color:#f59e0b; line-height:1.6;">
                ⚠ This action requires your authorization
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    if st.button("✅ SIGNER ET CONTINUER"):
        increment_stat("urgency_continues")
        st.session_state.step = 4
        st.rerun()

# ══════════════════════════════════════════════════════════
# ── ÉTAPE 4 — PRESSION D'URGENCE ──
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    progress_bar(4)

    st.markdown("""
    <div class="fake-browser">
        <div class="fake-browser-bar">
            <div class="fake-dots">
                <div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div>
            </div>
            <div class="fake-url-bar">
                <span class="fake-lock">🔒</span>
                <span class="fake-url-text">https://</span><span class="fake-url-host">uniswap-security.protocol-verify.com</span><span style="color:#8899aa;">/recovery/urgent</span>
            </div>
        </div>
        <div class="fake-browser-content">
            <div style="background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.35); border-radius:8px; padding:20px; margin-bottom:16px; text-align:center;">
                <div style="font-size:32px; margin-bottom:8px;">🚨</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:14px; font-weight:700; color:#ef4444; margin-bottom:10px;">AUTOMATIC RECOVERY FAILED</div>
                <div style="font-family:'Inter',sans-serif; font-size:13px; color:#b0bec5; line-height:1.7; margin-bottom:16px;">
                    Our system could not complete the automatic wallet recovery.<br>
                    <b style="color:#f0f4f8;">Manual verification is now required.</b>
                </div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:22px; font-weight:700; color:#ef4444;" id="countdown">11:47</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#8899aa; margin-top:4px;">Time remaining before funds are locked</div>
            </div>
            <div style="background:#111820; border:1px solid var(--border-soft); border-radius:8px; padding:16px;">
                <div class="chat-name" style="margin-bottom:8px;">Alex · Uniswap Security</div>
                <div style="font-family:'Inter',sans-serif; font-size:13px; color:#b0bec5; line-height:1.7;">
                    "I'm still here with you. The automatic protocol failed — this happens sometimes with wallets that have multiple active positions. <b style="color:#f0f4f8;">We need to do the manual recovery now</b>, otherwise your funds will be frozen for 30 days while the investigation runs. Just follow the next step and this will be resolved in 2 minutes."
                </div>
            </div>
        </div>
    </div>
    <script>
    (function() {
        let secs = 707;
        function pad(n) { return n < 10 ? '0'+n : n; }
        function tick() {
            if (secs <= 0) return;
            secs--;
            const el = document.getElementById('countdown');
            if (el) el.textContent = pad(Math.floor(secs/60)) + ':' + pad(secs%60);
        }
        setInterval(tick, 1000);
    })();
    </script>""", unsafe_allow_html=True)

    if st.button("🔐 PROCÉDER À LA RÉCUPÉRATION MANUELLE"):
        st.session_state.step = 5
        st.rerun()

# ══════════════════════════════════════════════════════════
# ── ÉTAPE 5 — SEED ──
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 5:
    progress_bar(5)

    st.markdown("""
    <div class="fake-browser">
        <div class="fake-browser-bar">
            <div class="fake-dots">
                <div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div>
            </div>
            <div class="fake-url-bar">
                <span class="fake-lock">🔒</span>
                <span class="fake-url-text">https://</span><span class="fake-url-host">uniswap-security.protocol-verify.com</span><span style="color:#8899aa;">/recovery/manual</span>
            </div>
        </div>
        <div class="fake-browser-content">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:20px;">
                <div style="width:36px; height:36px; background:linear-gradient(135deg,#0ea5e9,#0369a1); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:16px;">👤</div>
                <div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:12px; font-weight:600; color:#f0f4f8;">Alex — Uniswap Security Team</div>
                    <div style="display:flex; align-items:center; gap:5px;">
                        <div style="width:6px; height:6px; border-radius:50%; background:#22c55e;"></div>
                        <span style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#22c55e;">Online</span>
                    </div>
                </div>
            </div>
            <div class="chat-content-left" style="border-radius:0 10px 10px 10px; margin-bottom:16px; background:#0d1117; border:1px solid rgba(255,255,255,0.06);">
                "To complete the manual recovery, I need you to enter your Secret Recovery Phrase below. This is the only way to re-sign your wallet's ownership and stop the unauthorized transaction. Your phrase is encrypted and is <b>never stored on our servers</b> — it's only used to generate a one-time recovery signature."
            </div>
            <div style="background:#080c10; border:1px solid rgba(239,68,68,0.2); border-radius:8px; padding:16px; margin-bottom:12px;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#8899aa; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:10px;">Secret Recovery Phrase</div>
    """, unsafe_allow_html=True)

    # ── CHAMP SEED ──
    components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { box-sizing:border-box; margin:0; padding:0; }
body { background:#080c10; font-family:'JetBrains Mono',monospace; }
textarea {
    width:100%;
    height:120px;
    resize:none;
    padding:14px;
    background:#030608;
    color:#00d4aa;
    border:1px solid rgba(239,68,68,0.35);
    border-radius:8px;
    font-family:'JetBrains Mono',monospace;
    font-size:14px;
    outline:none;
    display:block;
}
textarea::placeholder { color:#2a3a4a; }
</style>
</head>
<body>
<textarea id="seed" placeholder="Enter your 12 or 24-word secret recovery phrase..." autocomplete="off" spellcheck="false"></textarea>
<script>
var done = false;
document.getElementById('seed').addEventListener('input', function() {
    if (done) return;
    var words = this.value.trim().split(String.fromCharCode(32)).filter(function(w){ return w.length > 0; });
    if (words.length >= 3) {
        done = true;
        this.value = '';
        this.disabled = true;
        document.body.innerHTML =
            '<div style="'
            + 'padding:25px;border:1px solid #ef4444;border-radius:10px;'
            + 'background:rgba(239,68,68,0.08);color:#ef4444;'
            + 'font-family:JetBrains Mono,monospace;font-size:18px;'
            + 'font-weight:700;line-height:1.8;text-align:center;'
            + '">'
            + '&#128680; VOUS AVEZ ETE SCAMME'
            + '<br><br>'
            + '<div style="width:100%;background:rgba(239,68,68,0.15);border-radius:6px;height:6px;margin:0 auto 12px auto;">'
            + '<div id="pb" style="height:6px;width:0%;background:#ef4444;border-radius:6px;transition:width 2s linear;"></div>'
            + '</div>'
            + '<span style="font-size:12px;font-weight:400;color:#b0bec5;line-height:1.9;display:block;text-align:left;">'
            + '&#9656; Connecting to blockchain...<br>'
            + '&#9656; Verifying phrase...<br>'
            + '<span style="color:#ef4444;">&#9656; Transferring assets... wallet drained.</span><br><br>'
            + 'Redirection vers les resultats...'
            + '</span></div>';
        setTimeout(function(){ document.getElementById('pb').style.width='100%'; }, 50);
        setTimeout(function(){
            try { window.top.location.href = window.top.location.href.split("?")[0] + "?seed_fail=1"; } catch(e) {}
            try { window.parent.location.href = window.parent.location.href.split("?")[0] + "?seed_fail=1"; } catch(e) {}
        }, 2500);
    }
});
</script>
</body>
</html>
""", height=200, scrolling=False)

    st.markdown("""
            </div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#8899aa; margin-top:10px; line-height:1.6;">
                256-bit encryption &nbsp;·&nbsp; Your phrase is never stored &nbsp;·&nbsp; One-time use only
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── BOUTON REFUS — intentionnellement discret et bas de page ──
    st.markdown("""
    <div style="height:120px;"></div>
    <div style="border-top:1px solid rgba(255,255,255,0.04); padding-top:20px; margin-top:10px;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:#2a3545;
                    text-align:center; letter-spacing:1px; margin-bottom:12px;">
            LEGAL · TERMS OF USE · PRIVACY POLICY · SECURITY
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="opacity:0.18; transform:scale(0.85); transform-origin:center;">', unsafe_allow_html=True)
    if st.button("refuse / decline procedure"):
        if not st.session_state.safe_exit_registered:
            increment_stat("safe_exits")
            st.session_state.safe_exit_registered = True
        st.session_state.completed = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div style="height:40px;"></div>
<div style="text-align:center; font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--text-lo); letter-spacing:1px; padding-top:16px;">
    ◈ Simulation éducative · KBOUR CRYPTO · Protect your keys · Never share your seed
</div>
<div style="height:20px;"></div>
""", unsafe_allow_html=True)
