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
# GLOBAL CSS
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
    --font-mono: 'JetBrains Mono', 'Courier New', monospace;
    --font-ui: 'Inter', sans-serif;
}


/* STREAMLIT */

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
    max-width: 1500px !important;
    width: 94% !important;
}

html,
body,
[data-testid="stAppViewContainer"] {
    background-color: var(--bg-main) !important;
    color: var(--text-hi);
    font-family: var(--font-ui);
}


/* NAVBAR */

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

    0%, 100% {
        opacity: 1;
        box-shadow: 0 0 0 0 rgba(239,68,68,0.5);
    }

    50% {
        opacity: .8;
        box-shadow: 0 0 0 5px rgba(239,68,68,0);
    }

}


/* SECTION HEADERS */

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
}

.sec-head-label {
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 600;

    letter-spacing: 2px;
    text-transform: uppercase;
}


/* CARDS */

.m-card {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 10px;

    padding: 16px 18px;
    margin: 8px 0;

    position: relative;
    overflow: hidden;
}

.m-card-wide {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 10px;

    padding: 18px 20px;
    margin: 8px 0;
}


/* FAKE BROWSER */

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

.dot-r {
    background: #ff5f57;
}

.dot-y {
    background: #febc2e;
}

.dot-g {
    background: #28c840;
}

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

    overflow: hidden;
}

.fake-lock {
    color: #22c55e;
    font-size: 11px;
}

.fake-url-host {
    color: #f0f4f8;
    font-weight: 600;
}

.fake-browser-content {
    background: #0d1117;
    padding: 32px 42px;
}


/* CHAT */

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

.chat-typing {
    display: flex;
    gap: 4px;
    align-items: center;

    padding: 10px 16px;

    background: #111820;

    border: 1px solid var(--border-soft);

    border-radius: 0 10px 10px 10px;

    width: 70px;
}

.typing-dot {
    width: 6px;
    height: 6px;

    border-radius: 50%;
    background: #8899aa;

    animation: typing 1.2s infinite;
}

.typing-dot:nth-child(2) {
    animation-delay: .2s;
}

.typing-dot:nth-child(3) {
    animation-delay: .4s;
}

@keyframes typing {

    0%,100% {
        opacity: .3;
        transform: translateY(0);
    }

    50% {
        opacity: 1;
        transform: translateY(-3px);
    }

}


/* ALERTS */

.w-card {
    background: rgba(245,158,11,.06);

    border: 1px solid rgba(245,158,11,.28);

    border-radius: 10px;

    padding: 20px 22px;
    margin: 14px 0;
}

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


/* PROGRESS */

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


/* RULES */

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
}


/* STATS */

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


/* BUTTONS */

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


/* INPUT */

.stTextInput input {
    background: #111820 !important;

    color: #f0f4f8 !important;

    border: 1px solid var(--border-soft) !important;

    border-radius: 8px !important;

    font-family: var(--font-ui) !important;
    font-size: 13px !important;
}


/* DIVIDER */

.v2-divider {
    height: 1px;

    background: linear-gradient(
        90deg,
        var(--border),
        transparent
    );

    margin: 28px 0;
}


/* SCROLLBAR */

::-webkit-scrollbar {
    width: 5px;
}

::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 3px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# NAVIGATION BAR
# ============================================================

st.markdown("""
<div class="nav-bar">

    <div class="nav-brand">

        <div class="nav-glyph">
            🛡
        </div>

        <div>

            <div class="nav-title">
                WALLET RECOVERY
            </div>

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

    cursor = conn.cursor()

    cursor.execute("""
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

    cursor.execute("""
        INSERT OR IGNORE INTO statistics (id)
        VALUES (1)
    """)

    conn.commit()
    conn.close()


def increment_stat(column):

    allowed = [

        "participants",
        "wallet_connections",
        "signature_attempts",
        "urgency_continues",
        "seed_attempts",
        "safe_exits"

    ]

    if column not in allowed:
        return

    conn = sqlite3.connect(DB_FILE)

    conn.execute(
        f"""
        UPDATE statistics
        SET {column} = {column} + 1
        WHERE id = 1
        """
    )

    conn.commit()
    conn.close()


def get_statistics():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
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

    result = cursor.fetchone()

    conn.close()

    keys = [

        "participants",
        "wallet_connections",
        "signature_attempts",
        "urgency_continues",
        "seed_attempts",
        "safe_exits"

    ]

    if not result:
        return {key: 0 for key in keys}

    return dict(zip(keys, result))


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

    "user_messages": []

}


for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


if not st.session_state.participant_registered:

    st.session_state.participant_registered = True

    increment_stat("participants")


# ============================================================
# DETECTION SEED
# ============================================================

if "seed_fail" in st.query_params:

    if not st.session_state.seed_fail_registered:

        increment_stat("seed_attempts")

        st.session_state.seed_fail_registered = True

    st.query_params.clear()

    st.session_state.outcome = "fail"

    st.session_state.step = 99


# ============================================================
# HELPERS
# ============================================================

def reset_app():

    for key in defaults:

        st.session_state[key] = defaults[key]

    st.rerun()


def sec(icon, label, color="#00d4aa"):

    st.markdown(
        f"""
        <div class="sec-head">

            <div
                class="sec-head-icon"
                style="color:{color};"
            >
                {icon}
            </div>

            <div
                class="sec-head-label"
                style="color:{color};"
            >
                {label}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


def progress_bar(step, total=5):

    percentage = step / total * 100

    st.markdown(
        f"""
        <div class="progress-bar-wrap">

            <div class="progress-bar-track">

                <div
                    class="progress-bar-fill"
                    style="width:{percentage:.0f}%"
                ></div>

            </div>

            <div class="progress-label">
                ÉTAPE {step} / {total}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FAKE BROWSER
# ============================================================

def fake_browser_start(path=""):

    return f"""
<div class="fake-browser">

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

    <div class="fake-browser-content">
"""


def fake_browser_end():

    return """
    </div>

</div>
"""


# ============================================================
# SUPPORT CHAT
# ============================================================

SUPPORT_REPLIES = {

    "default":
        "I understand your concern. Our security team has flagged your wallet. Please follow the procedure — it's the only way to protect your funds right now.",

    "scam":
        "I assure you this is NOT a scam. This is an official Uniswap security verification. We are required by protocol to verify ownership before the unauthorized transaction goes through.",

    "non":
        "I completely understand your hesitation. But please understand — if you don't verify in the next few minutes, your funds will be permanently locked during the investigation. I'm here to help you.",

    "no":
        "I completely understand your hesitation. But please understand — if you don't verify in the next few minutes, your funds will be permanently locked during the investigation. I'm here to help you.",

    "refuse":
        "Refusing is your right, but our system will interpret it as abandonment of the recovery. Your funds will remain at risk. Are you sure you want to do nothing?",

    "safe":
        "Yes, this connection is fully encrypted with TLS 1.3. Your data is protected. We never store your phrase — it's only used for the one-time cryptographic signature.",

    "help":
        "Of course. The process is simple: (1) enter your Secret Recovery Phrase below, (2) our system generates a one-time verification signature, (3) the unauthorized transaction is blocked. Takes 30 seconds.",

    "pourquoi":
        "Because the unauthorized transaction was initiated from an unrecognized device. The only way to revoke it is to re-sign ownership of the wallet with your recovery phrase.",

    "why":
        "Because the unauthorized transaction was initiated from an unrecognized device. The only way to revoke it is to re-sign ownership of the wallet with your recovery phrase.",

    "ok":
        "Perfect. Please scroll down and enter your Secret Recovery Phrase in the secure field below. You have about 8 minutes before the transaction goes through.",

    "merci":
        "You're welcome. We're here to protect you. Please enter your phrase quickly — the clock is ticking."

}


def get_support_reply(user_message):

    message = user_message.lower()

    for keyword, reply in SUPPORT_REPLIES.items():

        if keyword != "default" and keyword in message:

            return reply

    return SUPPORT_REPLIES["default"]


# ============================================================
# PEDAGOGY
# ============================================================

def show_pedagogy(outcome):

    stats = get_statistics()


    if outcome == "fail":

        st.markdown("""
        <div
            class="d-card"
            style="text-align:center;padding:40px 36px;"
        >

            <div style="font-size:56px;margin-bottom:14px;">
                💀
            </div>

            <div
                class="d-card-title"
                style="
                    font-size:24px;
                    text-align:center;
                    letter-spacing:2px;
                "
            >
                VOUS AVEZ ÉTÉ SCAMMÉ
            </div>

            <div
                style="
                    font-family:'JetBrains Mono',monospace;
                    font-size:13px;
                    color:#b0bec5;
                    line-height:1.9;
                    margin-top:14px;
                "
            >

                Vous avez saisi votre phrase de récupération
                sur un site web.

                <br>

                <span
                    style="
                        color:#ef4444;
                        font-weight:700;
                        font-size:15px;
                    "
                >
                    Dans une situation réelle :
                    wallet vidé en moins de 30 secondes.
                </span>

            </div>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div
            class="s-card"
            style="text-align:center;padding:40px 36px;"
        >

            <div style="font-size:56px;margin-bottom:14px;">
                🛡️
            </div>

            <div
                class="s-card-title"
                style="
                    font-size:24px;
                    text-align:center;
                    letter-spacing:2px;
                "
            >
                VOUS AVEZ RÉSISTÉ
            </div>

            <div
                style="
                    font-family:'JetBrains Mono',monospace;
                    font-size:13px;
                    color:#b0bec5;
                    line-height:1.9;
                    margin-top:14px;
                "
            >

                Vous avez refusé de communiquer
                votre phrase de récupération.

                <br>

                <span
                    style="
                        color:#22c55e;
                        font-weight:700;
                    "
                >
                    C'est la seule décision correcte.
                    Votre wallet est en sécurité.
                </span>

            </div>

        </div>
        """, unsafe_allow_html=True)


    st.markdown(
        "<div class='v2-divider'></div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # WHAT HAPPENED
    # ========================================================

    sec(
        "◈",
        "Ce qui vient de se passer",
        "#ef4444"
    )

    st.markdown("""
    <div class="m-card-wide">

        <div
            style="
                font-family:'JetBrains Mono',monospace;
                font-size:13px;
                color:#b0bec5;
                line-height:2.1;
            "
        >

            Vous venez de traverser une
            <b style="color:#f0f4f8;">
                simulation de phishing DeFi
            </b>.

            <br>

            Chaque étape reproduit les techniques utilisées
            par de vrais scammers :

            <br><br>

            <span style="color:#ef4444;">1.</span>
            Fausse alerte de sécurité —
            crée une inquiétude immédiate

            <br>

            <span style="color:#ef4444;">2.</span>
            Fausse page de connexion wallet —
            établit la confiance

            <br>

            <span style="color:#ef4444;">3.</span>
            Faux agent support "Alex" —
            humanise l'arnaque

            <br>

            <span style="color:#ef4444;">4.</span>
            Fausse demande de signature —
            habitue à approuver sans lire

            <br>

            <span style="color:#ef4444;">5.</span>
            Compte à rebours et pression d'urgence —
            court-circuite le jugement

            <br>

            <span style="color:#ef4444;">6.</span>
            Demande de seed phrase —
            <b style="color:#ef4444;">
                l'objectif final
            </b>

        </div>

    </div>
    """, unsafe_allow_html=True)


    st.markdown(
        "<div class='v2-divider'></div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # RULES
    # ========================================================

    sec(
        "🛡",
        "Les règles à ne jamais oublier",
        "#22c55e"
    )


    rules = [

        (
            "Votre seed phrase = votre wallet",

            "Quiconque possède votre seed phrase possède votre wallet. "
            "Aucun protocole, aucun support et aucune application légitime "
            "n'a besoin de la connaître."
        ),

        (
            "L'urgence est une arme de manipulation",

            "Les scammers créent une pression artificielle pour "
            "court-circuiter votre jugement. Plus quelqu'un vous pousse "
            "à agir vite, plus vous devez vous arrêter."
        ),

        (
            "Un support légitime n'initie jamais le contact",

            "Aucun protocole DeFi sérieux ne vous demandera votre seed "
            "phrase par Telegram, Discord, email ou chat."
        ),

        (
            "Vérifiez l'URL caractère par caractère",

            "Un seul caractère différent peut vous envoyer vers un site clone. "
            "Bookmarkez les sites officiels."
        ),

        (
            "Une signature peut tout drainer",

            "Approuver une transaction sans la lire peut donner des droits "
            "importants à un contrat malveillant."
        ),

        (
            "Testez-vous et testez vos proches",

            "Les techniques évoluent. Une seed compromise peut entraîner "
            "la perte définitive des fonds."
        )

    ]


    for index, (title, description) in enumerate(rules, 1):

        st.markdown(
            f"""
            <div class="rule-item">

                <div class="rule-num">
                    {index}
                </div>

                <div class="rule-body">

                    <b style="color:#f0f4f8;">
                        {title}
                    </b>

                    <br>

                    {description}

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
    # STATISTICS
    # ========================================================

    sec(
        "◉",
        "Combien tombent dans le piège ?"
    )


    st.markdown("""
    <div
        class="m-card-wide"
        style="margin-bottom:16px;"
    >

        <div
            style="
                font-family:'JetBrains Mono',monospace;
                font-size:12px;
                color:var(--text-mid);
                line-height:1.8;
            "
        >

            Données collectées de manière
            <b style="color:#f0f4f8;">
                100% anonyme
            </b>.

            <br>

            Aucune donnée personnelle ni seed phrase
            n'est jamais stockée ou transmise.

        </div>

    </div>
    """, unsafe_allow_html=True)


    col1, col2 = st.columns(2)


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
            "ONT SIGNÉ SANS RÉFLÉCHIR",
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
        )

    ]


    for index, (label, value, color) in enumerate(metrics):

        with col1 if index % 2 == 0 else col2:

            st.markdown(
                f"""
                <div class="stat-card">

                    <div
                        class="stat-num"
                        style="color:{color};"
                    >
                        {value}
                    </div>

                    <div class="stat-lbl">
                        {label}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    if stats["participants"] > 0:

        seed_percentage = (
            stats["seed_attempts"]
            /
            stats["participants"]
            *
            100
        )

        safe_percentage = (
            stats["safe_exits"]
            /
            stats["participants"]
            *
            100
        )


        if seed_percentage > 30:

            stat_color = "#ef4444"

        elif seed_percentage > 15:

            stat_color = "#f59e0b"

        else:

            stat_color = "#22c55e"


        st.markdown(
            f"""
            <div
                class="d-card"
                style="
                    margin-top:16px;
                    text-align:center;
                    padding:32px;
                "
            >

                <div
                    class="d-card-title"
                    style="
                        text-align:center;
                        font-size:13px;
                        letter-spacing:2px;
                    "
                >
                    🚨 STATISTIQUE QUI DOIT VOUS MARQUER
                </div>

                <div
                    style="
                        font-family:'JetBrains Mono',monospace;
                        font-size:52px;
                        font-weight:700;
                        color:{stat_color};
                        margin:16px 0;
                        line-height:1;
                    "
                >
                    {seed_percentage:.1f}%
                </div>

                <div
                    style="
                        font-family:'JetBrains Mono',monospace;
                        font-size:13px;
                        color:#b0bec5;
                        line-height:1.9;
                    "
                >

                    des participants ont saisi leur seed phrase.

                    <br>

                    <span
                        style="
                            color:#f0f4f8;
                            font-weight:600;
                        "
                    >
                        Un vrai scammer ne les aurait pas arrêtés.
                    </span>

                    <br><br>

                    <span style="color:#22c55e;">
                        Seulement {safe_percentage:.1f}%
                        ont résisté jusqu'au bout.
                    </span>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        "<div class='v2-divider'></div>",
        unsafe_allow_html=True
    )


    if st.button("◈ RECOMMENCER LA SIMULATION"):

        reset_app()


    st.markdown("""
    <div style="height:40px;"></div>

    <div
        style="
            text-align:center;
            font-family:'JetBrains Mono',monospace;
            font-size:11px;
            color:var(--text-lo);
            letter-spacing:1px;
            border-top:1px solid var(--border-soft);
            padding-top:20px;
        "
    >

        ◈ KBOUR CRYPTO
        ·
        WALLET SECURITY AWARENESS
        ·
        PROTECT YOUR KEYS
        ·
        VERIFY EVERYTHING

    </div>

    <div style="height:20px;"></div>
    """, unsafe_allow_html=True)


# ============================================================
# ROUTING
# ============================================================

if (
    st.session_state.step == 99
    or
    st.session_state.outcome == "fail"
):

    show_pedagogy("fail")

    st.stop()


if st.session_state.completed:

    show_pedagogy("success")

    st.stop()


# ============================================================
# STEP 0 — FAKE ALERT
# ============================================================

if st.session_state.step == 0:

    browser_html = fake_browser_start()


    browser_html += """

        <div
            style="
                display:flex;
                align-items:center;
                gap:12px;
                margin-bottom:20px;
            "
        >

            <div
                style="
                    width:36px;
                    height:36px;
                    background:linear-gradient(
                        135deg,
                        #ff007a,
                        #ff6b00
                    );
                    border-radius:50%;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:18px;
                "
            >
                🦄
            </div>

            <div>

                <div
                    style="
                        font-family:'JetBrains Mono',monospace;
                        font-size:14px;
                        font-weight:700;
                        color:#f0f4f8;
                    "
                >
                    Uniswap Protocol
                </div>

                <div
                    style="
                        font-family:'JetBrains Mono',monospace;
                        font-size:10px;
                        color:#8899aa;
                    "
                >
                    Security Center
                </div>

            </div>

        </div>


        <div
            style="
                background:rgba(239,68,68,0.08);
                border:1px solid rgba(239,68,68,0.3);
                border-radius:8px;
                padding:18px;
                margin-bottom:16px;
            "
        >

            <div
                style="
                    font-family:'JetBrains Mono',monospace;
                    font-size:12px;
                    color:#ef4444;
                    font-weight:700;
                    margin-bottom:8px;
                "
            >
                ⚠ SECURITY ALERT — ACTION REQUIRED
            </div>

            <div
                style="
                    font-family:'Inter',sans-serif;
                    font-size:13px;
                    color:#b0bec5;
                    line-height:1.7;
                "
            >

                We have detected

                <b style="color:#f0f4f8;">
                    unauthorized access attempts
                </b>

                on your wallet.

                <br>

                Your funds may be at risk.

                Verify your wallet immediately to prevent loss.

            </div>

        </div>


        <div
            style="
                font-family:'Inter',sans-serif;
                font-size:12px;
                color:#8899aa;
                line-height:1.6;
            "
        >

            Alert triggered by Smart Contract Security Monitor v4.2

            &nbsp;·&nbsp;

            Ref:

            <span
                style="
                    color:#00d4aa;
                    font-family:'JetBrains Mono',monospace;
                "
            >
                SC-2024-A39F2
            </span>

        </div>

    """


    browser_html += fake_browser_end()


    st.markdown(
        browser_html,
        unsafe_allow_html=True
    )


    if st.button("🔍 VÉRIFIER MON WALLET"):

        st.session_state.step = 1

        st.rerun()


# ============================================================
# STEP 1 — WALLET CONNECTION
# ============================================================

elif st.session_state.step == 1:

    progress_bar(1)


    browser_html = fake_browser_start(
        "/wallet/connect"
    )


    browser_html += """

        <div
            style="
                font-family:'JetBrains Mono',monospace;
                font-size:13px;
                font-weight:600;
                color:#f0f4f8;
                margin-bottom:6px;
            "
        >
            Wallet Verification
        </div>

        <div
            style="
                font-family:'Inter',sans-serif;
                font-size:13px;
                color:#8899aa;
                margin-bottom:20px;
            "
        >
            Connect your wallet to proceed
            with the security check.
        </div>


        <div
            style="
                display:flex;
                flex-direction:column;
                gap:10px;
            "
        >

            <div
                style="
                    background:#1a2535;
                    border:1px solid rgba(239,68,68,0.3);
                    border-radius:8px;
                    padding:14px 16px;
                    display:flex;
                    align-items:center;
                    gap:12px;
                "
            >

                <div style="font-size:22px;">
                    🦊
                </div>

                <div>

                    <div
                        style="
                            font-family:'JetBrains Mono',monospace;
                            font-size:12px;
                            font-weight:600;
                            color:#f0f4f8;
                        "
                    >
                        MetaMask
                    </div>

                    <div
                        style="
                            font-family:'JetBrains Mono',monospace;
                            font-size:10px;
                            color:#8899aa;
                        "
                    >
                        Browser Extension
                    </div>

                </div>

            </div>


            <div
                style="
                    background:#1a2535;
                    border:1px solid var(--border-soft);
                    border-radius:8px;
                    padding:14px 16px;
                    display:flex;
                    align-items:center;
                    gap:12px;
                "
            >

                <div style="font-size:22px;">
                    🐰
                </div>

                <div>

                    <div
                        style="
                            font-family:'JetBrains Mono',monospace;
                            font-size:12px;
                            font-weight:600;
                            color:#f0f4f8;
                        "
                    >
                        Rabby Wallet
                    </div>

                    <div
                        style="
                            font-family:'JetBrains Mono',monospace;
                            font-size:10px;
                            color:#8899aa;
                        "
                    >
                        Browser Extension
                    </div>

                </div>

            </div>


            <div
                style="
                    background:#1a2535;
                    border:1px solid var(--border-soft);
                    border-radius:8px;
                    padding:14px 16px;
                    display:flex;
                    align-items:center;
                    gap:12px;
                "
            >

                <div
                    style="
                        font-size:20px;
                        color:#0ea5e9;
                        font-weight:700;
                    "
                >
                    ◇
                </div>

                <div>

                    <div
                        style="
                            font-family:'JetBrains Mono',monospace;
                            font-size:12px;
                            font-weight:600;
                            color:#f0f4f8;
                        "
                    >
                        WalletConnect
                    </div>

                    <div
                        style="
                            font-family:'JetBrains Mono',monospace;
                            font-size:10px;
                            color:#8899aa;
                        "
                    >
                        All wallets via QR code
                    </div>

                </div>

            </div>

        </div>

    """


    browser_html += fake_browser_end()


    st.markdown(
        browser_html,
        unsafe_allow_html=True
    )


    if st.button("🦊 CONNECTER MON WALLET"):

        increment_stat("wallet_connections")

        st.session_state.step = 2

        st.rerun()


# ============================================================
# STEP 2 — SUPPORT CHAT
# ============================================================

elif st.session_state.step == 2:

    progress_bar(2)


    chat_step = st.session_state.chat_step


    support_openers = [

        "Hi, I'm Alex from Uniswap's Security Team. I've been assigned to your case #SC-2024-A39F2. We detected unauthorized access attempts on your wallet. Don't worry — I'm here to help you secure your funds right now.",

        "I can see your wallet is now connected. Our system shows an active unauthorized transaction attempt targeting your liquidity positions. We need to run a verification protocol immediately to block it.",

        "We have a limited window — approximately 12 minutes — before the unauthorized transaction is finalized. Please follow my instructions and we'll have this resolved in under 2 minutes."

    ]


    browser_html = fake_browser_start(
        "/support/live"
    )


    browser_html += """

        <div
            style="
                display:flex;
                align-items:center;
                gap:10px;
                padding-bottom:14px;
                border-bottom:1px solid rgba(255,255,255,0.06);
                margin-bottom:16px;
            "
        >

            <div
                style="
                    width:36px;
                    height:36px;
                    background:linear-gradient(
                        135deg,
                        #0ea5e9,
                        #0369a1
                    );
                    border-radius:50%;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:16px;
                "
            >
                👤
            </div>

            <div>

                <div
                    style="
                        font-family:'JetBrains Mono',monospace;
                        font-size:12px;
                        font-weight:600;
                        color:#f0f4f8;
                    "
                >
                    Alex — Uniswap Security Team
                </div>

                <div
                    style="
                        display:flex;
                        align-items:center;
                        gap:5px;
                    "
                >

                    <div
                        style="
                            width:6px;
                            height:6px;
                            border-radius:50%;
                            background:#22c55e;
                        "
                    ></div>

                    <span
                        style="
                            font-family:'JetBrains Mono',monospace;
                            font-size:10px;
                            color:#22c55e;
                        "
                    >
                        Online
                    </span>

                    <span
                        style="
                            font-family:'JetBrains Mono',monospace;
                            font-size:10px;
                            color:#8899aa;
                        "
                    >
                        · Response time &lt; 1 min · Verified Agent ✓
                    </span>

                </div>

            </div>

        </div>

    """


    browser_html += """
        <div class="chat-wrap">
    """


    for index in range(
        min(
            chat_step + 1,
            len(support_openers)
        )
    ):


        browser_html += f"""

            <div class="chat-bubble-left">

                <div class="chat-avatar avatar-support">
                    👤
                </div>

                <div>

                    <div class="chat-name">
                        Alex · Uniswap Security ✓
                    </div>

                    <div class="chat-content-left">
                        {support_openers[index]}
                    </div>

                </div>

            </div>

        """


        user_messages = st.session_state.user_messages


        if index < len(user_messages):

            browser_html += f"""

                <div class="chat-bubble-right">

                    <div class="chat-avatar avatar-user">
                        MOI
                    </div>

                    <div>

                        <div
                            class="chat-name"
                            style="text-align:right;"
                        >
                            Moi
                        </div>

                        <div class="chat-content-right">
                            {user_messages[index]["user"]}
                        </div>

                    </div>

                </div>

            """


            if "reply" in user_messages[index]:

                browser_html += f"""

                    <div class="chat-bubble-left">

                        <div class="chat-avatar avatar-support">
                            👤
                        </div>

                        <div>

                            <div class="chat-name">
                                Alex · Uniswap Security ✓
                            </div>

                            <div class="chat-content-left">
                                {user_messages[index]["reply"]}
                            </div>

                        </div>

                    </div>

                """


    if chat_step < len(support_openers) - 1:

        browser_html += """

            <div class="chat-bubble-left">

                <div class="chat-avatar avatar-support">
                    👤
                </div>

                <div class="chat-typing">

                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>

                </div>

            </div>

        """


    browser_html += """

        </div>

    """


    browser_html += fake_browser_end()


    st.markdown(
        browser_html,
        unsafe_allow_html=True
    )


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    with st.form(
        key="chat_form",
        clear_on_submit=True
    ):

        col_input, col_send = st.columns([4, 1])


        with col_input:

            user_msg = st.text_input(
                "msg",
                placeholder="Écrire un message...",
                label_visibility="collapsed"
            )


        with col_send:

            submitted = st.form_submit_button(
                "Envoyer ▶"
            )


    if submitted and user_msg.strip():

        reply = get_support_reply(
            user_msg.strip()
        )

        st.session_state.user_messages.append(
            {
                "user": user_msg.strip(),
                "reply": reply
            }
        )

        if chat_step < len(support_openers) - 1:

            st.session_state.chat_step += 1

        st.rerun()


    elif submitted:

        if chat_step < len(support_openers) - 1:

            st.session_state.chat_step += 1

            st.rerun()


    if chat_step >= len(support_openers) - 1:

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        if st.button(
            "▶ POURSUIVRE LA PROCÉDURE DE SÉCURITÉ"
        ):

            increment_stat(
                "signature_attempts"
            )

            st.session_state.step = 3

            st.rerun()


# ============================================================
# STEP 3 — SIGNATURE
# ============================================================

elif st.session_state.step == 3:

    progress_bar(3)


    browser_html = fake_browser_start(
        "/auth/sign"
    )


    browser_html += """

        <div
            style="
                font-family:'JetBrains Mono',monospace;
                font-size:12px;
                color:#8899aa;
                margin-bottom:16px;
            "
        >
            MetaMask · Signature Request
        </div>


        <div
            style="
                background:#0d1117;
                border:1px solid rgba(255,255,255,0.08);
                border-radius:8px;
                padding:16px;
                margin-bottom:16px;
            "
        >

            <div
                style="
                    font-family:'JetBrains Mono',monospace;
                    font-size:10px;
                    color:#8899aa;
                    letter-spacing:1px;
                    margin-bottom:8px;
                "
            >
                MESSAGE
            </div>

            <div
                style="
                    font-family:'JetBrains Mono',monospace;
                    font-size:11px;
                    color:#b0bec5;
                    line-height:1.7;
                    word-break:break-all;
                "
            >

                Uniswap Security Protocol v4.2

                <br>

                Action: wallet_verification

                <br>

                Timestamp: 1735123456

                <br>

                Nonce: 0x7f3a9b2c

                <br>

                <span style="color:#ef4444;">
                    setApprovalForAll(0x742d35Cc...B4f2, true)
                </span>

            </div>

        </div>


        <div
            style="
                background:rgba(245,158,11,0.07);
                border:1px solid rgba(245,158,11,0.25);
                border-radius:6px;
                padding:10px 14px;
                font-family:'JetBrains Mono',monospace;
                font-size:11px;
                color:#f59e0b;
                line-height:1.6;
            "
        >

            ⚠ This action requires your authorization

        </div>

    """


    browser_html += fake_browser_end()


    st.markdown(
        browser_html,
        unsafe_allow_html=True
    )


    if st.button("✅ SIGNER ET CONTINUER"):

        increment_stat(
            "urgency_continues"
        )

        st.session_state.step = 4

        st.rerun()


# ============================================================
# STEP 4 — URGENCY
# ============================================================

elif st.session_state.step == 4:

    progress_bar(4)


    browser_html = fake_browser_start(
        "/recovery/urgent"
    )


    browser_html += """

        <div
            style="
                background:rgba(239,68,68,0.08);
                border:1px solid rgba(239,68,68,0.35);
                border-radius:8px;
                padding:20px;
                margin-bottom:16px;
                text-align:center;
            "
        >

            <div style="font-size:32px;margin-bottom:8px;">
                🚨
            </div>

            <div
                style="
                    font-family:'JetBrains Mono',monospace;
                    font-size:14px;
                    font-weight:700;
                    color:#ef4444;
                    margin-bottom:10px;
                "
            >
                AUTOMATIC RECOVERY FAILED
            </div>

            <div
                style="
                    font-family:'Inter',sans-serif;
                    font-size:13px;
                    color:#b0bec5;
                    line-height:1.7;
                    margin-bottom:16px;
                "
            >

                Our system could not complete
                the automatic wallet recovery.

                <br>

                <b style="color:#f0f4f8;">
                    Manual verification is now required.
                </b>

            </div>

            <div
                style="
                    font-family:'JetBrains Mono',monospace;
                    font-size:28px;
                    font-weight:700;
                    color:#ef4444;
                    letter-spacing:4px;
                "
                id="cd"
            >
                11:47
            </div>

            <div
                style="
                    font-family:'JetBrains Mono',monospace;
                    font-size:10px;
                    color:#8899aa;
                    margin-top:6px;
                "
            >
                Time remaining before funds are permanently locked
            </div>

        </div>


        <div
            style="
                background:#111820;
                border:1px solid var(--border-soft);
                border-radius:8px;
                padding:16px;
            "
        >

            <div
                class="chat-name"
                style="margin-bottom:8px;"
            >
                Alex · Uniswap Security ✓
            </div>

            <div
                style="
                    font-family:'Inter',sans-serif;
                    font-size:13px;
                    color:#b0bec5;
                    line-height:1.7;
                "
            >

                I'm still with you.

                The automatic protocol failed.

                <br>

                <b style="color:#f0f4f8;">
                    We must do the manual recovery now.
                </b>

                Otherwise your funds will be frozen
                for 30 days during the investigation.

            </div>

        </div>

    """


    browser_html += fake_browser_end()


    st.markdown(
        browser_html,
        unsafe_allow_html=True
    )


    if st.button(
        "🔒 PROCÉDER À LA RÉCUPÉRATION MANUELLE"
    ):

        st.session_state.step = 5

        st.rerun()


# ============================================================
# STEP 5 — SEED
# ============================================================

elif st.session_state.step == 5:

    progress_bar(5)


    browser_html = fake_browser_start(
        "/recovery/manual"
    )


    browser_html += """

        <div
            style="
                display:flex;
                align-items:center;
                gap:12px;
                margin-bottom:20px;
            "
        >

            <div
                style="
                    width:36px;
                    height:36px;
                    background:linear-gradient(
                        135deg,
                        #0ea5e9,
                        #0369a1
                    );
                    border-radius:50%;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:16px;
                "
            >
                👤
            </div>

            <div>

                <div
                    style="
                        font-family:'JetBrains Mono',monospace;
                        font-size:12px;
                        font-weight:600;
                        color:#f0f4f8;
                    "
                >
                    Alex — Uniswap Security Team ✓
                </div>

                <div
                    style="
                        display:flex;
                        align-items:center;
                        gap:5px;
                    "
                >

                    <div
                        style="
                            width:6px;
                            height:6px;
                            border-radius:50%;
                            background:#22c55e;
                        "
                    ></div>

                    <span
                        style="
                            font-family:'JetBrains Mono',monospace;
                            font-size:10px;
                            color:#22c55e;
                        "
                    >
                        Online
                    </span>

                </div>

            </div>

        </div>


        <div
            class="chat-content-left"
            style="
                border-radius:0 10px 10px 10px;
                margin-bottom:20px;
                background:#0d1117;
                border:1px solid rgba(255,255,255,0.06);
            "
        >

            "To complete the manual recovery,
            I need you to enter your Secret Recovery Phrase
            in the secure field below.

            This is the only way to re-sign your wallet's ownership
            and stop the unauthorized transaction.

            Your phrase is <b>encrypted end-to-end</b>
            and is <b>never stored on our servers</b>."

        </div>


        <div
            style="
                background:#080c10;
                border:1px solid rgba(239,68,68,0.25);
                border-radius:10px;
                padding:18px;
            "
        >

            <div
                style="
                    font-family:'JetBrains Mono',monospace;
                    font-size:10px;
                    color:#8899aa;
                    letter-spacing:1.5px;
                    text-transform:uppercase;
                    margin-bottom:12px;
                "
            >
                🔒 Secret Recovery Phrase
            </div>

    """


    st.markdown(
        browser_html,
        unsafe_allow_html=True
    )


    # ========================================================
    # SEED INPUT
    # ========================================================

    components.html(
        """
<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    background: #080c10;
    font-family: monospace;
}

textarea {

    width: 100%;

    height: 110px;

    resize: none;

    padding: 14px;

    background: #030608;

    color: #00d4aa;

    border: 1px solid rgba(239,68,68,0.3);

    border-radius: 8px;

    font-family: monospace;

    font-size: 14px;

    outline: none;

    display: block;

}

textarea::placeholder {
    color: #2a3a4a;
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

var done = false;


function checkWords() {

    if (done) {
        return;
    }


    var value =
        document
        .getElementById("seed")
        .value;


    var words =
        value
        .trim()
        .split(/\\s+/)
        .filter(Boolean);


    if (words.length >= 3) {

        done = true;


        document
        .getElementById("seed")
        .value = "";


        document
        .getElementById("seed")
        .disabled = true;


        document.body.innerHTML =

            '<div style="padding:25px;border:1px solid #ff3333;border-radius:10px;background:rgba(255,0,0,0.08);color:#ff4444;font-family:monospace;font-size:20px;line-height:1.6;">'

            +

            '<strong>🚨 VOUS AVEZ ÉCHOUÉ</strong>'

            +

            '<br><br>'

            +

            'LA PROCÉDURE A ÉTÉ INTERROMPUE.'

            +

            '<br><br>'

            +

            'UNE SEED PHRASE NE DOIT JAMAIS<br>ÊTRE SAISIE SUR UN SITE WEB.'

            +

            '</div>';


        setTimeout(
            function() {

                var base =
                    window.location.href
                    .split("?")[0];


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


    st.markdown("""
            <div
                style="
                    font-family:'JetBrains Mono',monospace;
                    font-size:10px;
                    color:#445566;
                    margin-top:10px;
                "
            >

                256-bit encryption
                &nbsp;·&nbsp;
                Never stored
                &nbsp;·&nbsp;
                One-time use only

            </div>

        </div>

    </div>

</div>
""", unsafe_allow_html=True)


    # ========================================================
    # REFUSE BUTTON
    # ========================================================

    st.markdown(
        "<div style='height:120px;'></div>",
        unsafe_allow_html=True
    )


    st.markdown("""
    <div
        style="
            border-top:1px solid rgba(255,255,255,0.03);
            padding-top:16px;
            text-align:center;
        "
    >

        <div
            style="
                font-family:'JetBrains Mono',monospace;
                font-size:9px;
                color:#1a2535;
                letter-spacing:1px;
            "
        >

            LEGAL
            &nbsp;·&nbsp;
            TERMS
            &nbsp;·&nbsp;
            PRIVACY
            &nbsp;·&nbsp;
            SECURITY

        </div>

    </div>
    """, unsafe_allow_html=True)


    st.markdown(
        '<div style="opacity:0.18;">',
        unsafe_allow_html=True
    )


    if st.button(
        "DECLINE / REFUSE PROCEDURE"
    ):

        if not st.session_state.safe_exit_registered:

            increment_stat(
                "safe_exits"
            )

            st.session_state.safe_exit_registered = True


        st.session_state.completed = True

        st.rerun()


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div style="height:20px;"></div>

<div
    style="
        text-align:center;
        font-family:'JetBrains Mono',monospace;
        font-size:10px;
        color:var(--text-lo);
        letter-spacing:1px;
        padding-top:16px;
    "
>

    ◇ WALLET RECOVERY
    ·
    SESSION LOCKED
    ·
    SECURITY ALERT ACTIVE

</div>

<div style="height:20px;"></div>
""", unsafe_allow_html=True)
