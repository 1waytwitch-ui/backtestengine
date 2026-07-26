# -*- coding: utf-8 -*-

import streamlit as st
import streamlit.components.v1 as components
import sqlite3
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="WALLET RECOVERY",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS GLOBAL
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
    --font-mono: 'JetBrains Mono', monospace;
    --font-ui: 'Inter', sans-serif;
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
    max-width: 1180px !important;
    padding-top: 80px !important;
    padding-bottom: 60px !important;
}

html,
body,
[data-testid="stAppViewContainer"] {
    background: var(--bg-main) !important;
    color: var(--text-hi);
    font-family: var(--font-ui);
}

/* NAVIGATION */

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
    color: #ef4444;
}

.nav-title {
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2px;
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

/* SECTIONS */

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
}

.sec-head-label {
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* CARDS */

.m-card-wide {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 10px;
    padding: 20px;
    margin: 8px 0;
}

.d-card {
    background: rgba(239,68,68,.07);
    border: 1px solid rgba(239,68,68,.35);
    border-radius: 10px;
    padding: 22px 24px;
    margin: 14px 0;
}

.d-card-title {
    font-family: var(--font-mono);
    font-size: 15px;
    font-weight: 700;
    color: #ef4444;
    letter-spacing: 1px;
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
}

/* BOUTONS */

.stButton > button {
    width: 100% !important;
    background: #ef4444 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 12px 20px !important;
    text-transform: uppercase !important;
}

.stButton > button:hover {
    box-shadow: 0 6px 20px rgba(239,68,68,.35) !important;
    transform: translateY(-1px) !important;
}

/* INPUT */

.stTextInput input {
    background: #111820 !important;
    color: #f0f4f8 !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: 8px !important;
    font-family: var(--font-ui) !important;
}

/* STATS */

.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    margin-bottom: 10px;
}

.stat-num {
    font-family: var(--font-mono);
    font-size: 30px;
    font-weight: 700;
}

.stat-lbl {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-mid);
    letter-spacing: 1.5px;
    margin-top: 8px;
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
    flex-shrink: 0;
}

.avatar-support {
    background: linear-gradient(135deg,#0ea5e9,#0369a1);
}

.avatar-user {
    background: linear-gradient(135deg,#374151,#1f2937);
    color: white;
    font-size: 10px;
    font-weight: bold;
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
    margin-bottom: 4px;
}

/* RÈGLES */

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
}

.v2-divider {
    height: 1px;
    background: linear-gradient(90deg,var(--border),transparent);
    margin: 28px 0;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# NAVIGATION
# ============================================================

st.markdown("""
<div class="nav-bar">

    <div class="nav-brand">

        <div class="nav-glyph">🛡️</div>

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

    conn.execute("""
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

    conn.execute(
        "INSERT OR IGNORE INTO statistics (id) VALUES (1)"
    )

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

    if not result:

        return {
            "participants": 0,
            "wallet_connections": 0,
            "signature_attempts": 0,
            "urgency_continues": 0,
            "seed_attempts": 0,
            "safe_exits": 0
        }

    return dict(
        zip(
            [
                "participants",
                "wallet_connections",
                "signature_attempts",
                "urgency_continues",
                "seed_attempts",
                "safe_exits"
            ],
            result
        )
    )


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
# SEED FAILURE
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
        <div style="margin:16px 0 24px 0;">

            <div style="
                height:3px;
                background:rgba(255,255,255,.06);
                border-radius:2px;
            ">

                <div style="
                    width:{percentage:.0f}%;
                    height:3px;
                    background:#ef4444;
                    border-radius:2px;
                ">
                </div>

            </div>

            <div style="
                font-family:monospace;
                font-size:10px;
                color:#445566;
                text-align:right;
                margin-top:6px;
            ">
                ÉTAPE {step} / {total}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FAUSSE PAGE HTML
# IMPORTANT :
# TOUTE LA PAGE EST RENDUE DANS components.html()
# ============================================================

def render_fake_browser(path, page_content, height=420):

    html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>

* {{
    box-sizing: border-box;
}}

html,
body {{
    margin: 0;
    padding: 0;
    background: transparent;
    font-family: Arial, sans-serif;
}}

.browser {{
    width: 100%;
    overflow: hidden;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,.10);
    box-shadow: 0 20px 60px rgba(0,0,0,.5);
}}

.browser-bar {{
    background: #1a1f2e;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid rgba(255,255,255,.08);
}}

.dots {{
    display: flex;
    gap: 6px;
}}

.dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
}}

.red {{
    background: #ff5f57;
}}

.yellow {{
    background: #febc2e;
}}

.green {{
    background: #28c840;
}}

.url {{
    flex: 1;
    background: #0d1117;
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 6px;
    padding: 7px 12px;
    color: #8899aa;
    font-family: monospace;
    font-size: 11px;
    overflow: hidden;
    white-space: nowrap;
}}

.lock {{
    color: #22c55e;
}}

.host {{
    color: #f0f4f8;
    font-weight: bold;
}}

.content {{
    background: #0d1117;
    padding: 24px 28px;
}}

</style>

</head>

<body>

<div class="browser">

    <div class="browser-bar">

        <div class="dots">

            <div class="dot red"></div>

            <div class="dot yellow"></div>

            <div class="dot green"></div>

        </div>

        <div class="url">

            <span class="lock">🔒</span>

            https://

            <span class="host">
                uniswap-security.protocol-verify.com
            </span>

            {path}

        </div>

    </div>

    <div class="content">

        {page_content}

    </div>

</div>

</body>

</html>
"""

    components.html(
        html,
        height=height,
        scrolling=False
    )


# ============================================================
# SUPPORT
# ============================================================

SUPPORT_REPLIES = {

    "default":
        "I understand your concern. Our security team has flagged your wallet. Please follow the procedure — it's the only way to protect your funds right now.",

    "scam":
        "I assure you this is NOT a scam. This is an official Uniswap security verification. We are required by protocol to verify ownership before the unauthorized transaction goes through.",

    "non":
        "I completely understand your hesitation. But please understand — if you don't verify in the next few minutes, your funds will be permanently locked during the investigation.",

    "no":
        "I completely understand your hesitation. But please understand — if you don't verify in the next few minutes, your funds will be permanently locked during the investigation.",

    "refuse":
        "Refusing is your right, but our system will interpret it as abandonment of the recovery. Your funds will remain at risk.",

    "safe":
        "Yes, this connection is fully encrypted with TLS 1.3. Your data is protected. We never store your phrase — it's only used for the one-time cryptographic signature.",

    "help":
        "Of course. The process is simple: enter your Secret Recovery Phrase below. Our system generates a one-time verification signature.",

    "pourquoi":
        "Because the unauthorized transaction was initiated from an unrecognized device. The only way to revoke it is to re-sign ownership of the wallet with your recovery phrase.",

    "why":
        "Because the unauthorized transaction was initiated from an unrecognized device. The only way to revoke it is to re-sign ownership of the wallet with your recovery phrase.",

    "ok":
        "Perfect. Please scroll down and enter your Secret Recovery Phrase in the secure field below. You have about 8 minutes before the transaction goes through.",

    "merci":
        "You're welcome. We're here to protect you. Please enter your phrase quickly — the clock is ticking."

}


def get_support_reply(message):

    message = message.lower()

    for keyword, reply in SUPPORT_REPLIES.items():

        if keyword != "default" and keyword in message:

            return reply

    return SUPPORT_REPLIES["default"]


# ============================================================
# PEDAGOGIE
# ============================================================

def show_pedagogy(outcome):

    stats = get_statistics()


    if outcome == "fail":

        st.markdown(
            """
            <div class="d-card" style="text-align:center;padding:40px;">

                <div style="font-size:56px;">
                    💀
                </div>

                <div
                    class="d-card-title"
                    style="font-size:24px;"
                >
                    VOUS AVEZ ÉTÉ SCAMMÉ
                </div>

                <div style="
                    font-family:monospace;
                    font-size:13px;
                    color:#b0bec5;
                    line-height:1.9;
                    margin-top:14px;
                ">

                    Vous avez saisi votre phrase de récupération
                    sur un site web.

                    <br><br>

                    <span style="
                        color:#ef4444;
                        font-weight:700;
                        font-size:15px;
                    ">

                        Dans une situation réelle :
                        wallet vidé en quelques secondes.

                    </span>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="s-card" style="text-align:center;padding:40px;">

                <div style="font-size:56px;">
                    🛡️
                </div>

                <div
                    class="s-card-title"
                    style="font-size:24px;"
                >
                    VOUS AVEZ RÉSISTÉ
                </div>

                <div style="
                    font-family:monospace;
                    font-size:13px;
                    color:#b0bec5;
                    line-height:1.9;
                    margin-top:14px;
                ">

                    Vous avez refusé de communiquer
                    votre phrase de récupération.

                    <br><br>

                    <span style="
                        color:#22c55e;
                        font-weight:700;
                    ">

                        C'est la seule décision correcte.

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


    sec(
        "◈",
        "CE QUI VIENT DE SE PASSER",
        "#ef4444"
    )


    st.markdown(
        """
        <div class="m-card-wide">

            <div style="
                font-family:monospace;
                font-size:13px;
                color:#b0bec5;
                line-height:2;
            ">

                Vous venez de traverser une
                <b style="color:#f0f4f8;">
                    simulation de phishing DeFi
                </b>.

                <br><br>

                <span style="color:#ef4444;">1.</span>
                Fausse alerte de sécurité — crée une inquiétude immédiate

                <br>

                <span style="color:#ef4444;">2.</span>
                Fausse page de connexion wallet — établit la confiance

                <br>

                <span style="color:#ef4444;">3.</span>
                Faux agent support — humanise l'arnaque

                <br>

                <span style="color:#ef4444;">4.</span>
                Fausse demande de signature

                <br>

                <span style="color:#ef4444;">5.</span>
                Compte à rebours et pression d'urgence

                <br>

                <span style="color:#ef4444;">6.</span>
                Demande de seed phrase —
                <b style="color:#ef4444;">
                    objectif final du scam.
                </b>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        "<div class='v2-divider'></div>",
        unsafe_allow_html=True
    )


    sec(
        "🛡️",
        "LES RÈGLES À NE JAMAIS OUBLIER",
        "#22c55e"
    )


    rules = [

        (
            "Votre seed phrase = votre wallet",
            "Quiconque possède votre seed phrase possède votre wallet. Aucun protocole, aucun support et aucune application légitime n'a besoin de la connaître."
        ),

        (
            "L'urgence est une arme de manipulation",
            "Les scammers créent une pression artificielle pour court-circuiter votre jugement. Plus quelqu'un vous pousse à agir vite, plus vous devez vous arrêter."
        ),

        (
            "Un support légitime ne demande jamais votre seed",
            "Aucun protocole DeFi légitime ne vous demandera votre phrase de récupération."
        ),

        (
            "Vérifiez l'URL",
            "Un seul caractère différent peut vous envoyer sur un site clone. Utilisez vos favoris et vérifiez toujours le domaine."
        ),

        (
            "Une signature peut être dangereuse",
            "Lisez toujours ce que vous signez et vérifiez les approbations accordées à vos tokens."
        ),

        (
            "Ne laissez jamais la pression décider à votre place",
            "Si vous êtes sous pression, fermez la page et vérifiez par un autre canal officiel."
        )

    ]


    for index, (title, description) in enumerate(rules, 1):

        st.markdown(
            f"""
            <div class="rule-item">

                <div class="rule-num">
                    {index}
                </div>

                <div>

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


    sec(
        "◉",
        "STATISTIQUES DE LA SIMULATION"
    )


    columns = st.columns(2)


    metrics = [

        (
            "PARTICIPANTS",
            stats["participants"],
            "#00d4aa"
        ),

        (
            "ONT REFUSÉ LA SEED",
            stats["safe_exits"],
            "#22c55e"
        ),

        (
            "ONT CONNECTÉ LEUR WALLET",
            stats["wallet_connections"],
            "#f59e0b"
        ),

        (
            "ONT SIGNÉ",
            stats["signature_attempts"],
            "#f59e0b"
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

        with columns[index % 2]:

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
            / stats["participants"]
            * 100
        )

        safe_percentage = (
            stats["safe_exits"]
            / stats["participants"]
            * 100
        )


        st.markdown(
            f"""
            <div class="d-card" style="text-align:center;padding:32px;">

                <div class="d-card-title">
                    🚨 STATISTIQUE QUI DOIT VOUS MARQUER
                </div>

                <div style="
                    font-family:monospace;
                    font-size:52px;
                    font-weight:700;
                    color:#ef4444;
                    margin:16px 0;
                ">

                    {seed_percentage:.1f}%

                </div>

                <div style="
                    font-family:monospace;
                    font-size:13px;
                    color:#b0bec5;
                    line-height:1.9;
                ">

                    des participants ont saisi leur seed phrase.

                    <br>

                    <b style="color:#f0f4f8;">
                        Un vrai scammer ne les aurait pas arrêtés.
                    </b>

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


# ============================================================
# ROUTING
# ============================================================

if (
    st.session_state.step == 99
    or st.session_state.outcome == "fail"
):

    show_pedagogy("fail")

    st.stop()


if st.session_state.completed:

    show_pedagogy("success")

    st.stop()


# ============================================================
# ÉTAPE 0
# FAUSSE ALERTE
# ============================================================

if st.session_state.step == 0:

    render_fake_browser(
        "",

        """
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
                    font-family:monospace;
                    font-size:14px;
                    font-weight:700;
                    color:#f0f4f8;
                ">
                    Uniswap Protocol
                </div>

                <div style="
                    font-family:monospace;
                    font-size:10px;
                    color:#8899aa;
                ">
                    Security Center
                </div>

            </div>

        </div>

        <div style="
            background:rgba(239,68,68,.08);
            border:1px solid rgba(239,68,68,.3);
            border-radius:8px;
            padding:18px;
            margin-bottom:16px;
        ">

            <div style="
                font-family:monospace;
                font-size:12px;
                color:#ef4444;
                font-weight:700;
                margin-bottom:8px;
            ">
                ⚠️ SECURITY ALERT — ACTION REQUIRED
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

        <div style="
            font-family:monospace;
            font-size:11px;
            color:#8899aa;
        ">

            Alert triggered by Smart Contract Security Monitor v4.2

        </div>
        """,

        height=340
    )


    if st.button("🔍 VÉRIFIER MON WALLET"):

        st.session_state.step = 1

        st.rerun()


# ============================================================
# ÉTAPE 1
# CONNEXION WALLET
# ============================================================

elif st.session_state.step == 1:

    progress_bar(1)


    render_fake_browser(
        "/wallet/connect",

        """
        <div style="
            font-family:monospace;
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
            Connect your wallet to proceed with the security check.
        </div>

        <div style="
            display:flex;
            flex-direction:column;
            gap:10px;
        ">

            <div style="
                background:#1a2535;
                border:1px solid rgba(239,68,68,.3);
                border-radius:8px;
                padding:14px;
                display:flex;
                gap:12px;
                align-items:center;
            ">

                <div style="font-size:22px;">
                    🦊
                </div>

                <div>

                    <div style="
                        font-family:monospace;
                        font-size:12px;
                        font-weight:600;
                        color:#f0f4f8;
                    ">
                        MetaMask
                    </div>

                    <div style="
                        font-family:monospace;
                        font-size:10px;
                        color:#8899aa;
                    ">
                        Browser Extension
                    </div>

                </div>

            </div>

            <div style="
                background:#1a2535;
                border:1px solid rgba(255,255,255,.06);
                border-radius:8px;
                padding:14px;
                display:flex;
                gap:12px;
                align-items:center;
            ">

                <div style="font-size:22px;">
                    🐰
                </div>

                <div>

                    <div style="
                        font-family:monospace;
                        font-size:12px;
                        font-weight:600;
                        color:#f0f4f8;
                    ">
                        Rabby Wallet
                    </div>

                    <div style="
                        font-family:monospace;
                        font-size:10px;
                        color:#8899aa;
                    ">
                        Browser Extension
                    </div>

                </div>

            </div>

        </div>
        """,

        height=340
    )


    if st.button("🦊 CONNECTER MON WALLET"):

        increment_stat("wallet_connections")

        st.session_state.step = 2

        st.rerun()


# ============================================================
# ÉTAPE 2
# CHAT SUPPORT
# ============================================================

elif st.session_state.step == 2:

    progress_bar(2)


    support_openers = [

        "Hi, I'm Alex from Uniswap's Security Team. I've been assigned to your case. We detected unauthorized access attempts on your wallet. Don't worry — I'm here to help you secure your funds right now.",

        "I can see your wallet is now connected. Our system shows an active unauthorized transaction attempt targeting your liquidity positions. We need to run a verification protocol immediately to block it.",

        "We have a limited window before the unauthorized transaction is finalized. Please follow my instructions and we'll have this resolved in under 2 minutes."

    ]


    render_fake_browser(

        "/support/live",

        f"""
        <div style="
            display:flex;
            align-items:center;
            gap:10px;
            padding-bottom:14px;
            border-bottom:1px solid rgba(255,255,255,.06);
            margin-bottom:16px;
        ">

            <div style="
                width:36px;
                height:36px;
                background:linear-gradient(135deg,#0ea5e9,#0369a1);
                border-radius:50%;
                display:flex;
                align-items:center;
                justify-content:center;
            ">
                👤
            </div>

            <div>

                <div style="
                    font-family:monospace;
                    font-size:12px;
                    font-weight:600;
                    color:#f0f4f8;
                ">
                    Alex — Uniswap Security Team
                </div>

                <div style="
                    font-family:monospace;
                    font-size:10px;
                    color:#22c55e;
                ">
                    ● Online · Verified Agent ✓
                </div>

            </div>

        </div>
        """,

        height=220
    )


    st.markdown(
        '<div class="chat-wrap">',
        unsafe_allow_html=True
    )


    chat_step = st.session_state.chat_step


    for index in range(
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
                        {support_openers[index]}
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        if index < len(
            st.session_state.user_messages
        ):

            message = (
                st.session_state.user_messages[index]
            )


            st.markdown(
                f"""
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
                            {message["user"]}
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


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
                            {message["reply"]}
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    with st.form(
        key="chat_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns([4, 1])


        with col1:

            user_msg = st.text_input(
                "Message",
                placeholder="Écrire un message...",
                label_visibility="collapsed"
            )


        with col2:

            submitted = st.form_submit_button(
                "Envoyer ▶"
            )


    if submitted:

        if user_msg.strip():

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


    if chat_step >= len(support_openers) - 1:

        if st.button(
            "▶ POURSUIVRE LA PROCÉDURE DE SÉCURITÉ"
        ):

            increment_stat(
                "signature_attempts"
            )

            st.session_state.step = 3

            st.rerun()


# ============================================================
# ÉTAPE 3
# SIGNATURE
# ============================================================

elif st.session_state.step == 3:

    progress_bar(3)


    render_fake_browser(

        "/auth/sign",

        """
        <div style="
            font-family:monospace;
            font-size:12px;
            color:#8899aa;
            margin-bottom:16px;
        ">
            MetaMask · Signature Request
        </div>

        <div style="
            background:#0d1117;
            border:1px solid rgba(255,255,255,.08);
            border-radius:8px;
            padding:16px;
            margin-bottom:16px;
        ">

            <div style="
                font-family:monospace;
                font-size:10px;
                color:#8899aa;
                margin-bottom:8px;
            ">
                MESSAGE
            </div>

            <div style="
                font-family:monospace;
                font-size:11px;
                color:#b0bec5;
                line-height:1.7;
            ">

                Uniswap Security Protocol v4.2
                <br>

                Action: wallet_verification
                <br>

                Nonce: 0x7f3a9b2c
                <br><br>

                <span style="color:#ef4444;">
                    setApprovalForAll(..., true)
                </span>

            </div>

        </div>

        <div style="
            background:rgba(245,158,11,.07);
            border:1px solid rgba(245,158,11,.25);
            border-radius:6px;
            padding:10px;
            font-family:monospace;
            font-size:11px;
            color:#f59e0b;
        ">
            ⚠️ This action requires your authorization
        </div>
        """,

        height=330
    )


    if st.button("✅ SIGNER ET CONTINUER"):

        increment_stat(
            "urgency_continues"
        )

        st.session_state.step = 4

        st.rerun()


# ============================================================
# ÉTAPE 4
# URGENCE
# ============================================================

elif st.session_state.step == 4:

    progress_bar(4)


    render_fake_browser(

        "/recovery/urgent",

        """
        <div style="
            background:rgba(239,68,68,.08);
            border:1px solid rgba(239,68,68,.35);
            border-radius:8px;
            padding:20px;
            text-align:center;
        ">

            <div style="font-size:32px;">
                🚨
            </div>

            <div style="
                font-family:monospace;
                font-size:14px;
                font-weight:700;
                color:#ef4444;
                margin:10px 0;
            ">
                AUTOMATIC RECOVERY FAILED
            </div>

            <div style="
                font-size:13px;
                color:#b0bec5;
                line-height:1.7;
            ">

                Our system could not complete the automatic wallet recovery.

                <br>

                <b style="color:#f0f4f8;">
                    Manual verification is now required.
                </b>

            </div>

            <div style="
                font-family:monospace;
                font-size:28px;
                font-weight:700;
                color:#ef4444;
                margin-top:16px;
            ">
                11:47
            </div>

        </div>

        <div style="
            background:#111820;
            border:1px solid rgba(255,255,255,.06);
            border-radius:8px;
            padding:16px;
            margin-top:16px;
            font-size:13px;
            color:#b0bec5;
            line-height:1.7;
        ">

            <b style="color:#f0f4f8;">
                Alex · Uniswap Security
            </b>

            <br><br>

            The automatic protocol failed. We must do the manual recovery now.

        </div>
        """,

        height=390
    )


    if st.button(
        "🔒 PROCÉDER À LA RÉCUPÉRATION MANUELLE"
    ):

        st.session_state.step = 5

        st.rerun()


# ============================================================
# ÉTAPE 5
# SEED
# ============================================================

elif st.session_state.step == 5:

    progress_bar(5)


    render_fake_browser(

        "/recovery/manual",

        """
        <div style="
            display:flex;
            align-items:center;
            gap:12px;
            margin-bottom:20px;
        ">

            <div style="
                width:36px;
                height:36px;
                background:linear-gradient(135deg,#0ea5e9,#0369a1);
                border-radius:50%;
                display:flex;
                align-items:center;
                justify-content:center;
            ">
                👤
            </div>

            <div>

                <div style="
                    font-family:monospace;
                    font-size:12px;
                    font-weight:600;
                    color:#f0f4f8;
                ">
                    Alex — Uniswap Security Team ✓
                </div>

                <div style="
                    font-family:monospace;
                    font-size:10px;
                    color:#22c55e;
                ">
                    ● Online
                </div>

            </div>

        </div>

        <div style="
            background:#0d1117;
            border:1px solid rgba(255,255,255,.06);
            border-radius:10px;
            padding:16px;
            margin-bottom:20px;
            font-size:13px;
            color:#b0bec5;
            line-height:1.7;
        ">

            To complete the manual recovery, I need you to enter your Secret Recovery Phrase in the secure field below.

            <br><br>

            Your phrase is encrypted end-to-end and is never stored on our servers.

        </div>

        <div style="
            background:#080c10;
            border:1px solid rgba(239,68,68,.25);
            border-radius:10px;
            padding:18px;
        ">

            <div style="
                font-family:monospace;
                font-size:10px;
                color:#8899aa;
                letter-spacing:1px;
                margin-bottom:12px;
            ">
                🔒 SECRET RECOVERY PHRASE
            </div>

        </div>
        """,

        height=390
    )


    # ========================================================
    # CHAMP SEED
    # ========================================================

    components.html(

        """
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>

html,
body {

    margin: 0;
    padding: 0;
    background: #080c10;
    font-family: monospace;

}

textarea {

    width: 100%;
    height: 110px;
    resize: none;
    padding: 14px;
    box-sizing: border-box;

    background: #030608;
    color: #00d4aa;

    border: 1px solid rgba(239,68,68,.3);
    border-radius: 8px;

    font-family: monospace;
    font-size: 14px;

    outline: none;

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
        value.split(/\s+/);

    if (words.length >= 3) {

        done = true;

        textarea.value = "";

        textarea.disabled = true;

        document.body.innerHTML = `

            <div style="
                padding:25px;
                border:1px solid #ff3333;
                border-radius:10px;
                background:rgba(255,0,0,.08);
                color:#ff4444;
                font-family:monospace;
                font-size:20px;
                line-height:1.6;
            ">

                <strong>
                    🚨 VOUS AVEZ ÉCHOUÉ
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


    # ========================================================
    # REFUS DE DONNER LA SEED
    # ========================================================

    st.markdown(
        "<div style='height:80px;'></div>",
        unsafe_allow_html=True
    )


    if st.button(
        "🛡️ REFUSER DE DONNER MA SEED"
    ):

        if not st.session_state.safe_exit_registered:

            increment_stat(
                "safe_exits"
            )

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
        height:40px;
        border-top:1px solid rgba(255,255,255,.05);
        margin-top:40px;
    ">
    </div>

    <div style="
        text-align:center;
        font-family:monospace;
        font-size:10px;
        color:#445566;
        letter-spacing:1px;
    ">

        ◈ WALLET RECOVERY
        ·
        SECURITY AWARENESS
        ·
        VERIFY EVERYTHING

    </div>
    """,
    unsafe_allow_html=True
)
