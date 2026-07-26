# -*- coding: utf-8 -*-

import streamlit as st
import streamlit.components.v1 as components
import sqlite3
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="WALLET RECOVERY",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# GLOBAL THEME
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-main: #080c10;
    --bg-panel: #0d1318;
    --bg-card: #111820;
    --accent: #00d4aa;
    --accent-dim: rgba(0,212,170,0.10);
    --accent-mid: rgba(0,212,170,0.30);
    --accent-2: #0ea5e9;
    --accent-3: #f59e0b;
    --accent-red: #ef4444;
    --accent-green: #22c55e;
    --border: rgba(0,212,170,0.18);
    --border-soft: rgba(255,255,255,0.06);
    --text-hi: #f0f4f8;
    --text-mid: #8899aa;
    --text-lo: #445566;
    --font-mono: 'JetBrains Mono','Courier New',monospace;
    --font-ui: 'Inter',sans-serif;
}

#MainMenu,
footer,
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
[data-testid="stToolbar"],
[data-testid="stHeader"] {
    display: none !important;
}

.block-container {
    padding-top: 72px !important;
    padding-bottom: 60px !important;
    max-width: 1400px !important;
}

html,
body,
[data-testid="stAppViewContainer"] {
    background-color: var(--bg-main) !important;
    color: var(--text-hi);
    font-family: var(--font-ui);
}

/* ============================================================
   NAV
============================================================ */

.nav-bar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 58px;
    z-index: 99999;
    background: rgba(6,10,14,0.98);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(239,68,68,0.25);
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
    width: 28px;
    height: 28px;
    border: 2px solid #ef4444;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    color: #ef4444;
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

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #ef4444;
    display: inline-block;
    margin-right: 5px;
    animation: pulse-red 1.2s infinite;
}

@keyframes pulse-red {
    0%,100% {
        opacity: 1;
        box-shadow: 0 0 0 0 rgba(239,68,68,0.5);
    }

    50% {
        opacity: .8;
        box-shadow: 0 0 0 5px rgba(239,68,68,0);
    }
}

/* ============================================================
   SECTION
============================================================ */

.sec-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 28px 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}

.sec-head-icon {
    width: 24px;
    height: 24px;
    background: var(--accent-dim);
    border: 1px solid var(--border);
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
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

/* ============================================================
   CARDS
============================================================ */

.m-card-wide {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 10px;
    padding: 18px 20px;
    margin: 8px 0;
}

/* ============================================================
   FAKE BROWSER
============================================================ */

.fake-browser {
    width: 100%;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    margin: 16px 0;
}

.fake-browser-bar {
    background: #1a1f2e;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.fake-dots {
    display: flex;
    gap: 6px;
}

.dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

.dot-r { background: #ff5f57; }
.dot-y { background: #febc2e; }
.dot-g { background: #28c840; }

.fake-url-bar {
    flex: 1;
    background: #0d1117;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    padding: 5px 12px;
    font-family: var(--font-mono);
    font-size: 11px;
    color: #8899aa;
    display: flex;
    align-items: center;
    gap: 6px;
}

.fake-lock {
    color: #22c55e;
}

.fake-url-host {
    color: #f0f4f8;
    font-weight: 600;
}

.fake-browser-content {
    background: #0d1117;
    padding: 28px;
}

/* ============================================================
   CHAT
============================================================ */

.chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin: 16px 0;
}

.chat-bubble-left {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    max-width: 85%;
}

.chat-bubble-right {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    max-width: 85%;
    align-self: flex-end;
    flex-direction: row-reverse;
}

.chat-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}

.avatar-support {
    background: linear-gradient(135deg,#0ea5e9,#0369a1);
}

.avatar-user {
    background: linear-gradient(135deg,#374151,#1f2937);
    color: #f0f4f8;
    font-size: 12px;
    font-weight: 700;
}

.chat-content-left {
    background: #111820;
    border: 1px solid var(--border-soft);
    border-radius: 0 10px 10px 10px;
    padding: 12px 16px;
    font-size: 13px;
    color: #b0bec5;
    line-height: 1.7;
}

.chat-content-right {
    background: #1a2535;
    border: 1px solid rgba(14,165,233,0.2);
    border-radius: 10px 0 10px 10px;
    padding: 12px 16px;
    font-size: 13px;
    color: #f0f4f8;
    line-height: 1.7;
}

.chat-name {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-mid);
    letter-spacing: 1px;
    margin-bottom: 4px;
}

/* ============================================================
   ALERT CARDS
============================================================ */

.d-card {
    background: rgba(239,68,68,.07);
    border: 1px solid rgba(239,68,68,.35);
    border-radius: 10px;
    padding: 22px 24px;
    margin: 14px 0;
    box-shadow: 0 0 30px rgba(239,68,68,.06);
}

.d-card-title {
    font-family: var(--font-mono);
    font-size: 15px;
    font-weight: 700;
    color: #ef4444;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.s-card {
    background: rgba(34,197,94,.07);
    border: 1px solid rgba(34,197,94,.3);
    border-radius: 10px;
    padding: 22px 24px;
    margin: 14px 0;
}

.s-card-title {
    font-family: var(--font-mono);
    font-size: 15px;
    font-weight: 700;
    color: #22c55e;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

/* ============================================================
   PROGRESS
============================================================ */

.progress-bar-wrap {
    margin: 16px 0 24px 0;
}

.progress-bar-track {
    height: 3px;
    background: var(--border-soft);
    border-radius: 2px;
}

.progress-bar-fill {
    height: 3px;
    background: #ef4444;
    border-radius: 2px;
    transition: width .5s ease;
    box-shadow: 0 0 8px rgba(239,68,68,0.5);
}

.progress-label {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-lo);
    letter-spacing: 1px;
    margin-top: 6px;
    text-align: right;
}

/* ============================================================
   RULES
============================================================ */

.rule-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 16px 0;
    border-bottom: 1px solid var(--border-soft);
    font-size: 13px;
    color: #b0bec5;
    line-height: 1.6;
}

.rule-item:last-child {
    border-bottom: none;
}

.rule-num {
    min-width: 28px;
    height: 28px;
    border-radius: 6px;
    background: rgba(239,68,68,.1);
    border: 1px solid rgba(239,68,68,.25);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    color: #ef4444;
    flex-shrink: 0;
    margin-top: 1px;
}

/* ============================================================
   STATS
============================================================ */

.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 10px;
}

.stat-num {
    font-family: var(--font-mono);
    font-size: 30px;
    font-weight: 700;
    color: var(--accent);
    line-height: 1.1;
}

.stat-lbl {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-mid);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 8px;
}

/* ============================================================
   BUTTONS
============================================================ */

.stButton > button {
    background: #ef4444 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 12px 20px !important;
    text-transform: uppercase !important;
    transition: all .2s !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(239,68,68,.35) !important;
}

/* ============================================================
   INPUT
============================================================ */

.stTextInput input {
    background: #111820 !important;
    color: #f0f4f8 !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: 8px !important;
    font-size: 13px !important;
}

.stTextInput label {
    display: none !important;
}

.v2-divider {
    height: 1px;
    background: linear-gradient(90deg,var(--border),transparent);
    margin: 28px 0;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# NAV BAR
# ============================================================

st.markdown("""
<div class="nav-bar">
    <div class="nav-brand">
        <div class="nav-glyph">🛡</div>
        <div>
            <div class="nav-title">WALLET RECOVERY</div>
            <div class="nav-subtitle">
                <span class="status-dot"></span>
                SECURITY VERIFICATION REQUIRED
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE
# ============================================================

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

    c.execute(
        "INSERT OR IGNORE INTO statistics (id) VALUES (1)"
    )

    conn.commit()
    conn.close()


def increment_stat(col):

    allowed = [
        "participants",
        "wallet_connections",
        "signature_attempts",
        "urgency_continues",
        "seed_attempts",
        "safe_exits"
    ]

    if col not in allowed:
        return

    conn = sqlite3.connect(DB_FILE)

    conn.execute(
        f"UPDATE statistics SET {col} = {col} + 1 WHERE id = 1"
    )

    conn.commit()
    conn.close()


def get_statistics():

    conn = sqlite3.connect(DB_FILE)

    c = conn.cursor()

    c.execute("""
        SELECT
            participants,
            wallet_connections,
            signature_attempts,
            urgency_continues,
            seed_attempts,
            safe_exits
        FROM statistics
        WHERE id = 1
    """)

    row = c.fetchone()

    conn.close()

    keys = [
        "participants",
        "wallet_connections",
        "signature_attempts",
        "urgency_continues",
        "seed_attempts",
        "safe_exits"
    ]

    if not row:
        return {key: 0 for key in keys}

    return dict(zip(keys, row))


init_database()


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "step": 0,
    "completed": False,
    "outcome": None,
    "participant_registered": False,
    "safe_exit_registered": False,
    "seed_fail_registered": False,
    "chat_step": 0,
    "user_messages": [],
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# PARTICIPANT
# ============================================================

if not st.session_state.participant_registered:

    st.session_state.participant_registered = True

    increment_stat("participants")


# ============================================================
# SEED FAIL REDIRECT
# ============================================================

if "seed_fail" in st.query_params:

    if not st.session_state.seed_fail_registered:

        increment_stat("seed_attempts")

        st.session_state.seed_fail_registered = True

    st.query_params.clear()

    st.session_state.outcome = "fail"

    st.session_state.completed = False

    st.session_state.step = 99

    st.rerun()


# ============================================================
# RESET
# ============================================================

def reset_app():

    for key in defaults:

        st.session_state[key] = defaults[key]

    st.rerun()


# ============================================================
# HELPERS
# ============================================================

def sec(icon, label, color="var(--accent)"):

    st.markdown(
        f"""
        <div class="sec-head">
            <div class="sec-head-icon"
                 style="color:{color};">
                {icon}
            </div>

            <div class="sec-head-label"
                 style="color:{color};">
                {label}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def progress_bar(n, total=5):

    pct = n / total * 100

    st.markdown(
        f"""
        <div class="progress-bar-wrap">

            <div class="progress-bar-track">

                <div class="progress-bar-fill"
                     style="width:{pct:.0f}%;">
                </div>

            </div>

            <div class="progress-label">
                ÉTAPE {n} / {total}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


def url_bar(path=""):

    return f"""
    <div class="fake-browser-bar">

        <div class="fake-dots">

            <div class="dot dot-r"></div>
            <div class="dot dot-y"></div>
            <div class="dot dot-g"></div>

        </div>

        <div class="fake-url-bar">

            <span class="fake-lock">
                🔒
            </span>

            <span style="color:#b0bec5;">
                https://
            </span>

            <span class="fake-url-host">
                uniswap-security.protocol-verify.com
            </span>

            <span style="color:#8899aa;">
                {path}
            </span>

        </div>

    </div>
    """


# ============================================================
# PEDAGOGY
# ============================================================

def show_pedagogy(outcome):

    stats = get_statistics()

    if outcome == "fail":

        st.markdown("""
        <div class="d-card"
             style="text-align:center;padding:45px;">

            <div style="font-size:56px;">
                💀
            </div>

            <div class="d-card-title"
                 style="font-size:25px;text-align:center;">

                VOUS AVEZ ÉTÉ SCAMMÉ

            </div>

            <div style="
                font-family:'JetBrains Mono',monospace;
                font-size:13px;
                color:#b0bec5;
                line-height:1.9;
                margin-top:14px;
            ">

                Vous avez saisi votre phrase de récupération
                sur un site web.

                <br>

                <span style="
                    color:#ef4444;
                    font-weight:700;
                    font-size:15px;
                ">

                    Dans une situation réelle :
                    wallet vidé en moins de 30 secondes.

                </span>

            </div>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="s-card"
             style="text-align:center;padding:45px;">

            <div style="font-size:56px;">
                🛡️
            </div>

            <div class="s-card-title"
                 style="font-size:25px;text-align:center;">

                VOUS AVEZ RÉSISTÉ

            </div>

            <div style="
                font-family:'JetBrains Mono',monospace;
                font-size:13px;
                color:#b0bec5;
                line-height:1.9;
                margin-top:14px;
            ">

                Vous avez refusé de communiquer
                votre phrase de récupération.

                <br>

                <span style="
                    color:#22c55e;
                    font-weight:700;
                ">

                    C'est la seule décision correcte.

                </span>

            </div>

        </div>
        """, unsafe_allow_html=True)


    st.markdown(
        "<div class='v2-divider'></div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # CE QUI S'EST PASSÉ
    # ========================================================

    sec(
        "◈",
        "Ce qui vient de se passer",
        "#ef4444"
    )

    st.markdown("""
    <div class="m-card-wide">

        <div style="
            font-family:'JetBrains Mono',monospace;
            font-size:13px;
            color:#b0bec5;
            line-height:2.1;
        ">

            Vous venez de traverser une
            <b style="color:#f0f4f8;">
                simulation de phishing DeFi
            </b>.

            <br>

            Chaque étape reproduit des techniques
            utilisées par de vrais scammers :

            <br><br>

            <span style="color:#ef4444;">1.</span>
            Fausse alerte de sécurité — création de panique

            <br>

            <span style="color:#ef4444;">2.</span>
            Fausse page de connexion wallet — établissement de confiance

            <br>

            <span style="color:#ef4444;">3.</span>
            Faux agent support — humanisation de l'arnaque

            <br>

            <span style="color:#ef4444;">4.</span>
            Fausse demande de signature — banalisation des autorisations

            <br>

            <span style="color:#ef4444;">5.</span>
            Compte à rebours — pression psychologique

            <br>

            <span style="color:#ef4444;">6.</span>
            Demande de seed phrase —
            <b style="color:#ef4444;">
                l'objectif final.
            </b>

        </div>

    </div>
    """, unsafe_allow_html=True)


    st.markdown(
        "<div class='v2-divider'></div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # REGLES
    # ========================================================

    sec(
        "🛡",
        "Les règles à ne jamais oublier",
        "#22c55e"
    )

    rules = [

        (
            "Votre seed phrase = votre wallet",
            "Quiconque possède votre seed phrase possède votre wallet. Aucun support légitime, protocole ou application ne vous la demandera."
        ),

        (
            "L'urgence est une arme",
            "Les scammers créent une pression artificielle pour vous empêcher de réfléchir. Plus quelqu'un vous presse, plus vous devez vous arrêter."
        ),

        (
            "Un support légitime ne demande jamais votre seed",
            "Aucun protocole DeFi sérieux ne vous demandera votre phrase de récupération."
        ),

        (
            "Vérifiez toujours l'URL",
            "Un seul caractère peut suffire à vous faire basculer sur un site clone."
        ),

        (
            "Une signature peut être dangereuse",
            "Lisez toujours ce que vous signez et vérifiez les autorisations accordées à vos tokens."
        ),

        (
            "Ne faites jamais confiance à un contact non sollicité",
            "Telegram, Discord, X ou email : un faux support peut facilement usurper une identité."
        ),

    ]

    for i, (title, desc) in enumerate(rules, 1):

        st.markdown(
            f"""
            <div class="rule-item">

                <div class="rule-num">
                    {i}
                </div>

                <div>

                    <b style="color:#f0f4f8;">
                        {title}
                    </b>

                    <br>

                    {desc}

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        "<div class='v2-divider'></div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # STATS
    # ========================================================

    sec(
        "◉",
        "Statistiques de la simulation"
    )

    st.markdown("""
    <div class="m-card-wide">

        <div style="
            font-family:'JetBrains Mono',monospace;
            font-size:12px;
            color:var(--text-mid);
            line-height:1.8;
        ">

            Données collectées de manière
            <b style="color:#f0f4f8;">
                100% anonyme
            </b>.

            <br>

            Aucune seed phrase n'est jamais stockée
            ou transmise par cette simulation.

        </div>

    </div>
    """, unsafe_allow_html=True)


    c1, c2 = st.columns(2)

    metrics = [

        (
            "PARTICIPANTS",
            stats["participants"],
            "var(--accent)"
        ),

        (
            "ONT REFUSÉ LA SEED",
            stats["safe_exits"],
            "#22c55e"
        ),

        (
            "ONT CONNECTÉ LEUR WALLET",
            stats["wallet_connections"],
            "var(--accent-3)"
        ),

        (
            "ONT SIGNÉ",
            stats["signature_attempts"],
            "var(--accent-3)"
        ),

        (
            "ONT CÉDÉ À L'URGENCE",
            stats["urgency_continues"],
            "#ef4444"
        ),

        (
            "ONT SAISI LEUR SEED",
            stats["seed_attempts"],
            "#ef4444"
        ),

    ]


    for i, (label, value, color) in enumerate(metrics):

        with c1 if i % 2 == 0 else c2:

            st.markdown(
                f"""
                <div class="stat-card">

                    <div class="stat-num"
                         style="color:{color};">

                        {value}

                    </div>

                    <div class="stat-lbl">

                        {label}

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # ========================================================
    # MESSAGE FINAL
    # ========================================================

    st.markdown("""
    <div class="d-card"
         style="text-align:center;padding:30px;">

        <div class="d-card-title"
             style="text-align:center;">

            🚨 À RETENIR

        </div>

        <div style="
            font-family:'JetBrains Mono',monospace;
            font-size:14px;
            color:#b0bec5;
            line-height:1.9;
        ">

            Une seed phrase ne doit jamais être saisie
            sur un site web.

            <br><br>

            <span style="color:#22c55e;font-weight:700;">

                Pas même pour une récupération.
                Pas même pour un support.
                Pas même en cas d'urgence.

            </span>

        </div>

    </div>
    """, unsafe_allow_html=True)


    st.markdown(
        "<div class='v2-divider'></div>",
        unsafe_allow_html=True
    )


    if st.button("◈ RECOMMENCER LA SIMULATION"):

        reset_app()


    st.markdown("""
    <div style="
        height:40px;
    "></div>

    <div style="
        text-align:center;
        font-family:'JetBrains Mono',monospace;
        font-size:11px;
        color:var(--text-lo);
        letter-spacing:1px;
        border-top:1px solid var(--border-soft);
        padding-top:20px;
    ">

        ◈ KBOUR CRYPTO
        · WALLET SECURITY AWARENESS
        · PROTECT YOUR KEYS
        · VERIFY EVERYTHING

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# ROUTING
# ============================================================

if st.session_state.step == 99:

    show_pedagogy("fail")

    st.stop()


if st.session_state.completed:

    show_pedagogy("success")

    st.stop()


# ============================================================
# ETAPE 0
# ============================================================

if st.session_state.step == 0:

    st.markdown(
        f"""
        <div class="fake-browser">

            {url_bar()}

            <div class="fake-browser-content">

                <div style="
                    display:flex;
                    align-items:center;
                    gap:12px;
                    margin-bottom:20px;
                ">

                    <div style="
                        width:36px;
                        height:36px;
                        background:linear-gradient(135deg,#ff007a,#ff6b00);
                        border-radius:50%;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-size:18px;
                    ">

                        🦄

                    </div>

                    <div>

                        <div style="
                            font-family:'JetBrains Mono',monospace;
                            font-size:14px;
                            font-weight:700;
                            color:#f0f4f8;
                        ">

                            Uniswap Protocol

                        </div>

                        <div style="
                            font-family:'JetBrains Mono',monospace;
                            font-size:10px;
                            color:#8899aa;
                        ">

                            Security Center

                        </div>

                    </div>

                </div>


                <div style="
                    background:rgba(239,68,68,0.08);
                    border:1px solid rgba(239,68,68,0.3);
                    border-radius:8px;
                    padding:18px;
                    margin-bottom:16px;
                ">

                    <div style="
                        font-family:'JetBrains Mono',monospace;
                        font-size:12px;
                        color:#ef4444;
                        font-weight:700;
                        margin-bottom:8px;
                    ">

                        ⚠ SECURITY ALERT — ACTION REQUIRED

                    </div>

                    <div style="
                        font-size:13px;
                        color:#b0bec5;
                        line-height:1.7;
                    ">

                        We have detected
                        <b style="color:#f0f4f8;">
                            unauthorized access attempts
                        </b>
                        on your wallet.

                        <br>

                        Your funds may be at risk.

                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button("🔍 VÉRIFIER MON WALLET"):

        st.session_state.step = 1

        st.rerun()


# ============================================================
# ETAPE 1
# ============================================================

elif st.session_state.step == 1:

    progress_bar(1)

    st.markdown(
        f"""
        <div class="fake-browser">

            {url_bar('/wallet/connect')}

            <div class="fake-browser-content">

                <div style="
                    font-family:'JetBrains Mono',monospace;
                    font-size:13px;
                    font-weight:600;
                    color:#f0f4f8;
                    margin-bottom:6px;
                ">

                    Wallet Verification

                </div>

                <div style="
                    font-size:13px;
                    color:#8899aa;
                    margin-bottom:20px;
                ">

                    Connect your wallet to proceed.

                </div>

                <div style="
                    background:#1a2535;
                    border:1px solid rgba(239,68,68,0.3);
                    border-radius:8px;
                    padding:14px;
                ">

                    🦊 MetaMask

                </div>

                <br>

                <div style="
                    background:#1a2535;
                    border:1px solid var(--border-soft);
                    border-radius:8px;
                    padding:14px;
                ">

                    🐇 Rabby Wallet

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button("🦊 CONNECTER MON WALLET"):

        increment_stat("wallet_connections")

        st.session_state.step = 2

        st.rerun()


# ============================================================
# ETAPE 2 — CHAT
# ============================================================

elif st.session_state.step == 2:

    progress_bar(2)

    support_openers = [

        "Hi, I'm Alex from Uniswap's Security Team. I've been assigned to your case #SC-2024-A39F2. We detected unauthorized access attempts on your wallet. Don't worry — I'm here to help you secure your funds right now.",

        "I can see your wallet is now connected. Our system shows an active unauthorized transaction attempt targeting your liquidity positions. We need to run a verification protocol immediately to block it.",

        "We have a limited window — approximately 12 minutes — before the unauthorized transaction is finalized. Please follow my instructions and we'll have this resolved in under 2 minutes."

    ]


    chat_step = st.session_state.chat_step


    st.markdown(
        f"""
        <div class="fake-browser">

            {url_bar('/support/live')}

            <div class="fake-browser-content">

                <div class="chat-wrap">

        """,
        unsafe_allow_html=True
    )


    for i in range(
        min(
            chat_step + 1,
            len(support_openers)
        )
    ):

        st.markdown(
            f"""
            <div class="chat-bubble-left">

                <div class="chat-avatar avatar-support">
                    👤
                </div>

                <div>

                    <div class="chat-name">
                        Alex · Uniswap Security ✓
                    </div>

                    <div class="chat-content-left">

                        {support_openers[i]}

                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        if i < len(st.session_state.user_messages):

            msg = st.session_state.user_messages[i]

            st.markdown(
                f"""
                <div class="chat-bubble-right">

                    <div class="chat-avatar avatar-user">
                        MOI
                    </div>

                    <div>

                        <div class="chat-name">
                            Moi
                        </div>

                        <div class="chat-content-right">

                            {msg["user"]}

                        </div>

                    </div>

                </div>

                <div class="chat-bubble-left">

                    <div class="chat-avatar avatar-support">
                        👤
                    </div>

                    <div class="chat-content-left">

                        {msg["reply"]}

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    st.markdown(
        """
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    with st.form(
        key="chat_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns([4, 1])


        with col1:

            user_msg = st.text_input(
                "msg",
                placeholder="Écrire un message...",
                label_visibility="collapsed"
            )


        with col2:

            submitted = st.form_submit_button(
                "Envoyer ▶"
            )


    if submitted:

        if user_msg.strip():

            st.session_state.user_messages.append(
                {
                    "user": user_msg.strip(),
                    "reply": "I understand your concern. Please follow the security verification procedure."
                }
            )

        if chat_step < len(support_openers) - 1:

            st.session_state.chat_step += 1

        st.rerun()


    if chat_step >= len(support_openers) - 1:

        if st.button(
            "▶ POURSUIVRE LA PROCÉDURE"
        ):

            increment_stat("signature_attempts")

            st.session_state.step = 3

            st.rerun()


# ============================================================
# ETAPE 3 — SIGNATURE
# ============================================================

elif st.session_state.step == 3:

    progress_bar(3)

    st.markdown(
        f"""
        <div class="fake-browser">

            {url_bar('/auth/sign')}

            <div class="fake-browser-content">

                <div style="
                    font-family:'JetBrains Mono',monospace;
                    color:#8899aa;
                    margin-bottom:16px;
                ">

                    MetaMask · Signature Request

                </div>

                <div style="
                    background:#0d1117;
                    border:1px solid rgba(255,255,255,0.08);
                    border-radius:8px;
                    padding:16px;
                ">

                    <span style="color:#ef4444;">

                        setApprovalForAll(..., true)

                    </span>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button("✅ SIGNER ET CONTINUER"):

        increment_stat("urgency_continues")

        st.session_state.step = 4

        st.rerun()


# ============================================================
# ETAPE 4 — URGENCE
# ============================================================

elif st.session_state.step == 4:

    progress_bar(4)

    st.markdown(
        f"""
        <div class="fake-browser">

            {url_bar('/recovery/urgent')}

            <div class="fake-browser-content">

                <div style="
                    background:rgba(239,68,68,0.08);
                    border:1px solid rgba(239,68,68,0.35);
                    border-radius:8px;
                    padding:20px;
                    text-align:center;
                ">

                    <div style="font-size:32px;">
                        🚨
                    </div>

                    <div style="
                        font-family:'JetBrains Mono',monospace;
                        font-size:14px;
                        font-weight:700;
                        color:#ef4444;
                    ">

                        AUTOMATIC RECOVERY FAILED

                    </div>

                    <br>

                    <div style="
                        font-family:'JetBrains Mono',monospace;
                        font-size:28px;
                        color:#ef4444;
                    ">

                        11:47

                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "🔒 PROCÉDER À LA RÉCUPÉRATION MANUELLE"
    ):

        st.session_state.step = 5

        st.rerun()


# ============================================================
# ETAPE 5 — SEED
# ============================================================

elif st.session_state.step == 5:

    progress_bar(5)

    st.markdown(
        f"""
        <div class="fake-browser">

            {url_bar('/recovery/manual')}

            <div class="fake-browser-content">

                <div style="
                    display:flex;
                    align-items:center;
                    gap:12px;
                    margin-bottom:20px;
                ">

                    <div style="font-size:28px;">
                        👤
                    </div>

                    <div>

                        <div style="
                            font-family:'JetBrains Mono',monospace;
                            font-size:12px;
                            font-weight:600;
                            color:#f0f4f8;
                        ">

                            Alex — Uniswap Security Team ✓

                        </div>

                    </div>

                </div>

                <div class="chat-content-left"
                     style="margin-bottom:20px;">

                    To complete the manual recovery,
                    I need you to enter your Secret Recovery Phrase
                    in the secure field below.

                    <br><br>

                    This is the only way to re-sign your wallet's ownership.

                </div>

                <div style="
                    background:#080c10;
                    border:1px solid rgba(239,68,68,0.25);
                    border-radius:10px;
                    padding:18px;
                ">

                    <div style="
                        font-family:'JetBrains Mono',monospace;
                        font-size:10px;
                        color:#8899aa;
                        letter-spacing:1.5px;
                        margin-bottom:12px;
                    ">

                        🔒 SECRET RECOVERY PHRASE

                    </div>

        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # SEED FIELD
    # ========================================================

    components.html(
        """
        <!DOCTYPE html>

        <html>

        <head>

            <meta charset="utf-8">

            <style>

                * {
                    box-sizing:border-box;
                    margin:0;
                    padding:0;
                }

                body {
                    background:#080c10;
                    font-family:monospace;
                }

                textarea {

                    width:100%;
                    height:110px;
                    resize:none;
                    padding:14px;

                    background:#030608;
                    color:#00d4aa;

                    border:1px solid rgba(239,68,68,0.3);
                    border-radius:8px;

                    font-family:monospace;
                    font-size:14px;

                    outline:none;

                    display:block;

                }

                textarea::placeholder {
                    color:#2a3a4a;
                }

            </style>

        </head>

        <body>

            <textarea
                id="seed"
                placeholder="Enter your 12 or 24-word secret recovery phrase..."
                autocomplete="off"
                spellcheck="false"
            ></textarea>


            <script>

                let done = false;


                function checkWords() {

                    if (done) {
                        return;
                    }


                    const textarea =
                        document.getElementById("seed");


                    const value =
                        textarea.value.trim();


                    const words =
                        value.split(/\s+/).filter(Boolean);


                    if (words.length >= 3) {

                        done = true;


                        // IMPORTANT :
                        // La seed est immédiatement supprimée
                        // du champ et n'est jamais envoyée.

                        textarea.value = "";

                        textarea.disabled = true;


                        document.body.innerHTML = `

                            <div style="
                                padding:25px;
                                border:1px solid #ff3333;
                                border-radius:10px;
                                background:rgba(255,0,0,0.08);
                                color:#ff4444;
                                font-family:monospace;
                                font-size:20px;
                                line-height:1.6;
                            ">

                                <strong>
                                    🚨 VOUS AVEZ ÉTÉ PIÉGÉ
                                </strong>

                                <br><br>

                                LA PROCÉDURE A ÉTÉ INTERROMPUE.

                                <br><br>

                                UNE SEED PHRASE NE DOIT JAMAIS
                                ÊTRE SAISIE SUR UN SITE WEB.

                            </div>

                        `;


                        setTimeout(
                            function() {

                                const base =
                                    window.location.href.split("?")[0];


                                window.location.href =
                                    base + "?seed_fail=1";

                            },
                            2500
                        );

                    }

                }


                document
                    .getElementById("seed")
                    .addEventListener(
                        "input",
                        checkWords
                    );

            </script>

        </body>

        </html>
        """,
        height=170,
        scrolling=False
    )


    st.markdown(
        """
                    <div style="
                        font-family:'JetBrains Mono',monospace;
                        font-size:10px;
                        color:#445566;
                        margin-top:10px;
                    ">

                        256-bit encryption
                        · Never stored
                        · One-time use only

                    </div>

                </div>

            </div>

        </div>

        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # BOUTON REFUSER
    # ========================================================

    st.markdown(
        "<div style='height:120px;'></div>",
        unsafe_allow_html=True
    )


    if not st.session_state.completed:

        if st.button(
            "DECLINE / REFUSE PROCEDURE"
        ):

            if not st.session_state.safe_exit_registered:

                increment_stat("safe_exits")

                st.session_state.safe_exit_registered = True


            st.session_state.completed = True

            st.session_state.outcome = "success"

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        height:20px;
    "></div>

    <div style="
        text-align:center;
        font-family:'JetBrains Mono',monospace;
        font-size:10px;
        color:var(--text-lo);
        letter-spacing:1px;
        padding-top:16px;
    ">

        ◈ WALLET RECOVERY
        · SESSION LOCKED
        · SECURITY ALERT ACTIVE

    </div>

    <div style="
        height:20px;
    "></div>
    """,
    unsafe_allow_html=True
)
