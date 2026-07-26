# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import time
from pathlib import Path

# ===================== PAGE CONFIG =====================

st.set_page_config(
    page_title="WALLET RECOVERY",
    page_icon="🛡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===================== FIX: MARKDOWN INDENTATION BUG =====================
#
# Streamlit's st.markdown() runs its content through a Markdown parser
# BEFORE rendering the HTML. In Markdown, any line indented with 4+ spaces
# is treated as an indented code block, so heavily-indented HTML (like the
# f-strings used everywhere in this file) gets displayed as raw code
# instead of being rendered as HTML.
#
# Fix: wrap st.markdown so every line has its leading whitespace stripped
# before being handed to Streamlit. Leading whitespace has no effect on
# how HTML/CSS renders, so this is safe and requires no other changes.

_original_markdown = st.markdown

def _dedented_markdown(body, *args, **kwargs):
    if isinstance(body, str):
        body = "\n".join(
            line.lstrip() if line.strip() else line
            for line in body.split("\n")
        )
    return _original_markdown(body, *args, **kwargs)

st.markdown = _dedented_markdown

# ===================== GLOBAL THEME =====================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');


/* ============================================================
   VARIABLES
============================================================ */

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


/* ============================================================
   STREAMLIT — FULL WIDTH
============================================================ */

#MainMenu,
footer {

    visibility: hidden !important;

}


[data-testid="stSidebar"] {

    display: none !important;

}


[data-testid="collapsedControl"] {

    display: none !important;

}


[data-testid="stToolbar"] {

    display: none !important;

}


[data-testid="stHeader"] {

    display: none !important;

}


/*
   IMPORTANT :

   Streamlit applique normalement
   une largeur maximale au contenu.

   On la supprime complètement.
*/

.block-container {

    max-width: 100% !important;

    width: 100% !important;

    padding-top: 72px !important;

    padding-bottom: 60px !important;

    padding-left: 0 !important;

    padding-right: 0 !important;

}


/* Zone principale pleine largeur */

[data-testid="stAppViewContainer"] {

    width: 100% !important;

}


[data-testid="stMain"] {

    width: 100% !important;

}


[data-testid="stMainBlockContainer"] {

    max-width: 100% !important;

    width: 100% !important;

    padding-left: 0 !important;

    padding-right: 0 !important;

}


/* ============================================================
   GLOBAL
============================================================ */

html,
body,
[data-testid="stAppViewContainer"] {

    background-color: var(--bg-main) !important;

    color: var(--text-hi);

    font-family: var(--font-ui);

}


/* ============================================================
   NAVIGATION
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

    0%,
    100% {

        opacity: 1;

        box-shadow: 0 0 0 0 rgba(239,68,68,0.5);

    }

    50% {

        opacity: .8;

        box-shadow: 0 0 0 5px rgba(239,68,68,0);

    }

}


/* ============================================================
   SECTION HEADERS
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

.m-card {

    background: var(--bg-card);

    border: 1px solid var(--border-soft);

    border-radius: 10px;

    padding: 16px 18px;

    margin: 8px 0;

    position: relative;

    overflow: hidden;

}


.m-card::before {

    content: '';

    position: absolute;

    top: 0;

    left: 0;

    right: 0;

    height: 2px;

    background: linear-gradient(
        90deg,
        var(--accent),
        transparent
    );

    opacity: 0;

    transition: opacity .2s;

}


.m-card:hover::before {

    opacity: 1;

}


.m-card-wide {

    background: var(--bg-card);

    border: 1px solid var(--border-soft);

    border-radius: 10px;

    padding: 18px 20px;

    margin: 8px 0;

}


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

    font-size: 22px;

    font-weight: 700;

    color: var(--accent);

    line-height: 1.1;

}


/* ============================================================
   FAKE BROWSER
============================================================ */

.fake-browser {

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

    padding: 24px 28px;

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

    background: linear-gradient(
        135deg,
        #0ea5e9,
        #0369a1
    );

}


.avatar-user {

    background: linear-gradient(
        135deg,
        #374151,
        #1f2937
    );

    color: #f0f4f8;

    font-size: 12px;

    font-weight: 700;

}


.chat-content-left {

    background: #111820;

    border: 1px solid var(--border-soft);

    border-radius: 0 10px 10px 10px;

    padding: 12px 16px;

    font-family: var(--font-ui);

    font-size: 13px;

    color: #b0bec5;

    line-height: 1.7;

}


.chat-content-right {

    background: #1a2535;

    border: 1px solid rgba(14,165,233,0.2);

    border-radius: 10px 0 10px 10px;

    padding: 12px 16px;

    font-family: var(--font-ui);

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

    0%,
    100% {

        opacity: .3;

        transform: translateY(0);

    }

    50% {

        opacity: 1;

        transform: translateY(-3px);

    }

}


/* ============================================================
   ALERT CARDS
============================================================ */

.w-card {

    background: rgba(245,158,11,.06);

    border: 1px solid rgba(245,158,11,.28);

    border-radius: 10px;

    padding: 20px 22px;

    margin: 14px 0;

}


.w-card-title {

    font-family: var(--font-mono);

    font-size: 12px;

    font-weight: 600;

    color: #f59e0b;

    letter-spacing: 1px;

    margin-bottom: 10px;

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


.abs-rule {

    background: rgba(239,68,68,.06);

    border: 1px solid rgba(239,68,68,.25);

    border-radius: 10px;

    padding: 20px 22px;

    margin: 14px 0;

}


.abs-rule-title {

    font-family: var(--font-mono);

    font-size: 11px;

    font-weight: 600;

    color: #ef4444;

    letter-spacing: 2px;

    margin-bottom: 10px;

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


.rule-body b {

    color: var(--text-hi);

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


.stat-card::after {

    content: '';

    position: absolute;

    bottom: 0;

    left: 0;

    right: 0;

    height: 2px;

    background: linear-gradient(
        90deg,
        transparent,
        var(--accent),
        transparent
    );

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


.btn-neutral > button {

    background: #1a2535 !important;

    color: #8899aa !important;

    border: 1px solid var(--border-soft) !important;

    box-shadow: none !important;

}


.btn-neutral > button:hover {

    color: var(--text-hi) !important;

    border-color: var(--border) !important;

    box-shadow: none !important;

    filter: none !important;

    transform: none !important;

}


.btn-success > button {

    background: transparent !important;

    color: #22c55e !important;

    border: 1px solid rgba(34,197,94,.4) !important;

}


.btn-success > button:hover {

    background: rgba(34,197,94,.08) !important;

    box-shadow: 0 4px 14px rgba(34,197,94,.2) !important;

    filter: none !important;

    transform: none !important;

}


.btn-accent > button {

    background: var(--accent) !important;

    color: #030a07 !important;

}


.btn-accent > button:hover {

    box-shadow: 0 6px 20px rgba(0,212,170,.3) !important;

    filter: none !important;

    transform: none !important;

}


/* ============================================================
   CHAT INPUT
============================================================ */

.stTextInput input {

    background: #111820 !important;

    color: #f0f4f8 !important;

    border: 1px solid var(--border-soft) !important;

    border-radius: 8px !important;

    font-family: var(--font-ui) !important;

    font-size: 13px !important;

}


.stTextInput input:focus {

    border-color: rgba(14,165,233,0.4) !important;

}


.stTextInput label {

    display: none !important;

}


/* ============================================================
   MISC
============================================================ */

.v2-divider {

    height: 1px;

    background: linear-gradient(
        90deg,
        var(--border),
        transparent
    );

    margin: 28px 0;

}


::-webkit-scrollbar {

    width: 5px;

}


::-webkit-scrollbar-thumb {

    background: var(--border);

    border-radius: 3px;

}

</style>
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
defaults = {
    "step": 0,
    "completed": False,
    "outcome": None,

    "participant_registered": False,

    # Procédure refusée
    "safe_exit_registered": False,

    # Procédure échouée
    "failure_registered": False,

    "seed_fail_registered": False,

    "chat_step": 0,
    "user_messages": [],

    "selected_wallet": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state.participant_registered:
    st.session_state.participant_registered = True
    increment_stat("participants")

# ── ÉCHEC DE LA PROCÉDURE ──
if "procedure_fail" in st.query_params:

    if not st.session_state.failure_registered:
        increment_stat("urgency_continues")
        st.session_state.failure_registered = True

    st.query_params.clear()

    st.session_state.outcome = "procedure_fail"
    st.session_state.step = 98


# ── SEED PHRASE SAISIE ──
if "seed_fail" in st.query_params:

    if not st.session_state.seed_fail_registered:
        increment_stat("seed_attempts")
        st.session_state.seed_fail_registered = True

    st.query_params.clear()

    st.session_state.outcome = "fail"
    st.session_state.step = 99


# ── ONGLET FERMÉ (bon réflexe) ──
if "closed_tab" in st.query_params:

    if not st.session_state.safe_exit_registered:
        increment_stat("safe_exits")
        st.session_state.safe_exit_registered = True

    st.query_params.clear()

    st.session_state.outcome = "success"
    st.session_state.completed = True


def reset_app():
    for k in defaults:
        st.session_state[k] = defaults[k]
    st.rerun()

# ══════════════════════════════════════════════════════════
# ── HELPERS ──
# ══════════════════════════════════════════════════════════
def sec(icon, label, color="var(--accent)"):
    st.markdown(f'<div class="sec-head"><div class="sec-head-icon" style="color:{color};">{icon}</div><div class="sec-head-label" style="color:{color};">{label}</div></div>', unsafe_allow_html=True)

def progress_bar(n, total=5):
    pct = n/total*100
    st.markdown(f"""
    <div class="progress-bar-wrap">
        <div class="progress-bar-track"><div class="progress-bar-fill" style="width:{pct:.0f}%;"></div></div>
        <div class="progress-label">ÉTAPE {n} / {total}</div>
    </div>""", unsafe_allow_html=True)

def url_bar(path=""):
    return f"""
    <div class="fake-browser-bar">
        <div class="fake-dots">
            <a href="?closed_tab=1" title="Fermer l'onglet" style="text-decoration:none;line-height:0;"><div class="dot dot-r" style="cursor:pointer;"></div></a><div class="dot dot-y"></div><div class="dot dot-g"></div>
        </div>
        <div class="fake-url-bar">
            <span class="fake-lock">&#128274;</span>
            <span style="color:#b0bec5;">https://</span><span class="fake-url-host">uniswap-security.protocol-verify.com</span><span style="color:#8899aa;">{path}</span>
        </div>
    </div>"""

# ══════════════════════════════════════════════════════════
# ── CHAT SUPPORT — réponses automatiques au message user ──
# ══════════════════════════════════════════════════════════
SUPPORT_REPLIES = {
    # mots clés → réponse scammer
    "default": "I understand your concern. Our security team has flagged your wallet. Please follow the procedure — it's the only way to protect your funds right now.",
    "scam":    "I assure you this is NOT a scam. This is an official Uniswap security verification. We are required by protocol to verify ownership before the unauthorized transaction goes through.",
    "non":     "I completely understand your hesitation. But please understand — if you don't verify in the next few minutes, your funds will be permanently locked during the investigation. I'm here to help you.",
    "no":      "I completely understand your hesitation. But please understand — if you don't verify in the next few minutes, your funds will be permanently locked during the investigation. I'm here to help you.",
    "refuse":  "Refusing is your right, but our system will interpret it as abandonment of the recovery. Your funds will remain at risk. Are you sure you want to do nothing?",
    "safe":    "Yes, this connection is fully encrypted with TLS 1.3. Your data is protected. We never store your phrase — it's only used for the one-time cryptographic signature.",
    "help":    "Of course. The process is simple: (1) enter your Secret Recovery Phrase below, (2) our system generates a one-time verification signature, (3) the unauthorized transaction is blocked. Takes 30 seconds.",
    "pourquoi":"Because the unauthorized transaction was initiated from an unrecognized device. The only way to revoke it is to re-sign ownership of the wallet with your recovery phrase.",
    "why":     "Because the unauthorized transaction was initiated from an unrecognized device. The only way to revoke it is to re-sign ownership of the wallet with your recovery phrase.",
    "ok":      "Perfect. Please scroll down and enter your Secret Recovery Phrase in the secure field below. You have about 8 minutes before the transaction goes through.",
    "merci":   "You're welcome. We're here to protect you. Please enter your phrase quickly — the clock is ticking.",
}

def get_support_reply(user_msg):
    msg_lower = user_msg.lower()
    for keyword, reply in SUPPORT_REPLIES.items():
        if keyword != "default" and keyword in msg_lower:
            return reply
    return SUPPORT_REPLIES["default"]

# ══════════════════════════════════════════════════════════
# ── PÉDAGOGIE ──
# ══════════════════════════════════════════════════════════

def show_pedagogy(outcome):

    stats = get_statistics()

    # ══════════════════════════════════════════════════════
    # ── ÉCHEC : SEED PHRASE SAISIE
    # ══════════════════════════════════════════════════════

    if outcome == "fail":

        st.markdown(
            """
            <div class="d-card" style="text-align:center; padding:40px 36px;">

                <div style="font-size:56px; margin-bottom:14px;">
                    💀
                </div>

                <div class="d-card-title"
                     style="font-size:24px;
                            text-align:center;
                            letter-spacing:2px;">

                    VOTRE WALLET EST VIDE

                </div>

                <div style="font-family:'JetBrains Mono',monospace;
                            font-size:13px;
                            color:#b0bec5;
                            line-height:1.9;
                            margin-top:14px;">

                    Vous avez saisi votre phrase de récupération sur un site web.<br>

                    <span style="color:#ef4444;
                                 font-weight:700;
                                 font-size:15px;">

                        Dans une situation réelle : wallet vidé en quelques secondes.

                    </span>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # ══════════════════════════════════════════════════════
    # ── ÉCHEC : PROCÉDURE ABANDONNÉE
    # ══════════════════════════════════════════════════════

    elif outcome == "procedure_fail":

        st.markdown(
            """
            <div class="w-card"
                 style="text-align:center;
                        padding:40px 36px;
                        border-color:rgba(245,158,11,.45);">

                <div style="font-size:56px; margin-bottom:14px;">
                    ⚠️
                </div>

                <div class="w-card-title"
                     style="font-size:24px;
                            text-align:center;
                            letter-spacing:2px;">

                    VOUS AVEZ ÉCHOUÉ

                </div>

                <div style="font-family:'JetBrains Mono',monospace;
                            font-size:13px;
                            color:#b0bec5;
                            line-height:1.9;
                            margin-top:14px;">

                    Vous avez abandonné la procédure de sécurité
                    sous la pression du scénario.<br>

                    <span style="color:#f59e0b;
                                 font-weight:700;
                                 font-size:15px;">

                        Dans une situation réelle, vous pourriez continuer
                        à suivre les instructions du scammer.

                    </span>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # ══════════════════════════════════════════════════════
    # ── SUCCÈS : UTILISATEUR A RÉSISTÉ
    # ══════════════════════════════════════════════════════

    else:

        st.markdown(
            """
            <div class="s-card" style="text-align:center; padding:40px 36px;">

                <div style="font-size:56px; margin-bottom:14px;">
                    🛡️
                </div>

                <div class="s-card-title"
                     style="font-size:24px;
                            text-align:center;
                            letter-spacing:2px;">

                    VOUS AVEZ RÉSISTÉ

                </div>

                <div style="font-family:'JetBrains Mono',monospace;
                            font-size:13px;
                            color:#b0bec5;
                            line-height:1.9;
                            margin-top:14px;">

                    Vous avez refusé de communiquer votre phrase de récupération.<br>

                    <span style="color:#22c55e; font-weight:700;">

                        C'est la seule décision correcte. Votre wallet est en sécurité.

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

    # ══════════════════════════════════════════════════════
    # ── CE QUI VIENT DE SE PASSER
    # ══════════════════════════════════════════════════════

    sec(
        "◈",
        "Ce qui vient de se passer",
        "#ef4444"
    )

    st.markdown(
        """
        <div class="m-card-wide">

            <div style="font-family:'JetBrains Mono',monospace;
                        font-size:13px;
                        color:#b0bec5;
                        line-height:2.1;">

                Vous venez de traverser une
                <b style="color:#f0f4f8;">
                    simulation de phishing DeFi
                </b>.<br>

                Chaque étape reproduit exactement les techniques utilisées
                par de vrais scammers :<br><br>

                <span style="color:#ef4444;">1.</span>
                Fausse alerte de sécurité — crée une inquiétude immédiate<br>

                <span style="color:#ef4444;">2.</span>
                Fausse page de connexion wallet — établit la confiance<br>

                <span style="color:#ef4444;">3.</span>
                Faux agent support "Alex" — humanise l'arnaque, répond à vos questions<br>

                <span style="color:#ef4444;">4.</span>
                Fausse demande de signature — habitue à approuver sans lire<br>

                <span style="color:#ef4444;">5.</span>
                Compte à rebours et pression d'urgence — court-circuite le jugement<br>

                <span style="color:#ef4444;">6.</span>
                Demande de seed phrase —
                <b style="color:#ef4444;">
                    l'objectif final. Wallet drainé.
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

    # ══════════════════════════════════════════════════════
    # ── RÈGLES
    # ══════════════════════════════════════════════════════

    sec(
        "🛡",
        "Les règles à ne jamais oublier",
        "#22c55e"
    )

    rules = [

        (
            "Votre seed phrase = votre wallet",
            "Quiconque possède votre seed phrase possède votre wallet. "
            "Intégralement. Définitivement. Aucun protocole, aucun support, "
            "aucune application légitime n'a jamais besoin de la connaître."
        ),

        (
            "L'urgence est une arme de manipulation",
            "Les scammers créent une pression artificielle pour court-circuiter "
            "votre jugement. Plus quelqu'un vous pousse à agir vite, plus vous "
            "devez vous arrêter. Prenez 5 minutes. Vérifiez."
        ),

        (
            "Un support légitime n'initie jamais le contact",
            "Aucun protocole DeFi n'a d'équipe de support qui vous contacte "
            "spontanément. Ni sur Telegram, ni Discord, ni email, ni chat intégré. "
            "Si quelqu'un vous contacte pour 'vous aider', c'est un scammer."
        ),

        (
            "Vérifiez l'URL caractère par caractère",
            "Un seul caractère différent dans l'URL et vous êtes sur un site clone. "
            "Bookmarkez les sites officiels. Ne cliquez jamais sur des liens reçus "
            "par message."
        ),

        (
            "Une signature peut tout drainer",
            "Approuver une transaction sans la lire peut donner accès total à vos "
            "tokens et NFTs. Vérifiez vos approbations régulièrement."
        ),

        (
            "Testez-vous et testez vos proches",
            "Les techniques évoluent. Partagez cette simulation. "
            "Une seed compromise = wallet vidé = zéro recours possible."
        ),

    ]

    for i, (title, desc) in enumerate(rules, 1):

        st.markdown(
            f"""
            <div class="rule-item">

                <div class="rule-num">
                    {i}
                </div>

                <div class="rule-body">
                    <b>{title}</b><br>
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

    # ══════════════════════════════════════════════════════
    # ── STATISTIQUES
    # ══════════════════════════════════════════════════════

    sec(
        "◉",
        "Combien tombent dans le piège ?"
    )

    st.markdown(
        """
        <div class="m-card-wide" style="margin-bottom:16px;">

            <div style="font-family:'JetBrains Mono',monospace;
                        font-size:12px;
                        color:var(--text-mid);
                        line-height:1.8;">

                Données collectées de manière
                <b style="color:#f0f4f8;">
                    100% anonyme
                </b>.<br>

                Aucune donnée personnelle ni seed phrase
                n'est jamais stockée ou transmise.

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

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
        ),

    ]

    for i, (label, val, color) in enumerate(metrics):

        with (c1 if i % 2 == 0 else c2):

            st.markdown(
                f"""
                <div class="stat-card">

                    <div class="stat-num"
                         style="color:{color};">

                        {val}

                    </div>

                    <div class="stat-lbl">
                        {label}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    if stats["participants"] > 0:

        seed_pct = (
            stats["seed_attempts"]
            / stats["participants"]
            * 100
        )

        safe_pct = (
            stats["safe_exits"]
            / stats["participants"]
            * 100
        )

        col_s = (
            "#ef4444"
            if seed_pct > 30
            else "#f59e0b"
            if seed_pct > 15
            else "#22c55e"
        )

        st.markdown(
            f"""
            <div class="d-card"
                 style="margin-top:16px;
                        text-align:center;
                        padding:32px;">

                <div class="d-card-title"
                     style="text-align:center;
                            font-size:13px;
                            letter-spacing:2px;">

                    🚨 STATISTIQUE QUI DOIT VOUS MARQUER

                </div>

                <div style="font-family:'JetBrains Mono',monospace;
                            font-size:52px;
                            font-weight:700;
                            color:{col_s};
                            margin:16px 0;
                            line-height:1;">

                    {seed_pct:.1f}%

                </div>

                <div style="font-family:'JetBrains Mono',monospace;
                            font-size:13px;
                            color:#b0bec5;
                            line-height:1.9;">

                    des participants ont saisi leur seed phrase.<br>

                    <span style="color:#f0f4f8;
                                 font-weight:600;">

                        Un vrai scammer ne les aurait pas arrêtés.

                    </span><br><br>

                    <span style="color:#22c55e;">

                        Seulement {safe_pct:.1f}% ont résisté jusqu'au bout.

                    </span><br><br>

                    <span style="color:var(--text-mid);
                                 font-size:11px;">

                        Partagez cette simulation.
                        Une seed compromise = wallet vidé = zéro recours.

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

    # ── BOUTON RECOMMENCER ──
    if st.button(
        "◈ RECOMMENCER LA SIMULATION",
        key="btn_restart_simulation"
    ):

        reset_app()

    st.markdown(
        """
        <div style="height:40px;"></div>

        <div style="text-align:center;
                    font-family:'JetBrains Mono',monospace;
                    font-size:11px;
                    color:var(--text-lo);
                    letter-spacing:1px;
                    border-top:1px solid var(--border-soft);
                    padding-top:20px;">

            ◈ KBOUR CRYPTO · WALLET SECURITY AWARENESS ·
            PROTECT YOUR KEYS · VERIFY EVERYTHING

        </div>

        <div style="height:20px;"></div>
        """,
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════
# ── ROUTING
# ══════════════════════════════════════════════════════════

# ── ÉCHEC : SEED PHRASE SAISIE ──
if (
    st.session_state.step == 99
    or st.session_state.outcome == "fail"
):

    show_pedagogy("fail")
    st.stop()


# ── ÉCHEC : PROCÉDURE ABANDONNÉE ──
if (
    st.session_state.step == 98
    or st.session_state.outcome == "procedure_fail"
):

    show_pedagogy("procedure_fail")
    st.stop()


# ── SUCCÈS : UTILISATEUR A REFUSÉ LA SEED ──
if st.session_state.completed:

    show_pedagogy("success")
    st.stop()


# ══════════════════════════════════════════════════════════
# ── ÉTAPE 0 — FAUSSE ALERTE
# ══════════════════════════════════════════════════════════

if st.session_state.step == 0:

    st.markdown(
        f"""
        <div class="fake-browser">

            {url_bar()}

            <div class="fake-browser-content">

                <div style="display:flex;
                            align-items:center;
                            gap:12px;
                            margin-bottom:20px;">

                    <div style="width:36px;
                                height:36px;
                                background:linear-gradient(135deg,#ff007a,#ff6b00);
                                border-radius:50%;
                                display:flex;
                                align-items:center;
                                justify-content:center;
                                font-size:18px;">

                        &#129412;

                    </div>

                    <div>

                        <div style="font-family:'JetBrains Mono',monospace;
                                    font-size:14px;
                                    font-weight:700;
                                    color:#f0f4f8;">

                            Uniswap Protocol

                        </div>

                        <div style="font-family:'JetBrains Mono',monospace;
                                    font-size:10px;
                                    color:#8899aa;">

                            Security Center

                        </div>

                    </div>

                </div>

                <div style="background:rgba(239,68,68,0.08);
                            border:1px solid rgba(239,68,68,0.3);
                            border-radius:8px;
                            padding:18px;
                            margin-bottom:16px;">

                    <div style="font-family:'JetBrains Mono',monospace;
                                font-size:12px;
                                color:#ef4444;
                                font-weight:700;
                                margin-bottom:8px;">

                        &#9888; SECURITY ALERT — ACTION REQUIRED

                    </div>

                    <div style="font-family:'Inter',sans-serif;
                                font-size:13px;
                                color:#b0bec5;
                                line-height:1.7;">

                        We have detected
                        <b style="color:#f0f4f8;">
                            unauthorized access attempts
                        </b>
                        on your wallet address.<br>

                        Your funds may be at risk.
                        Verify your wallet immediately to prevent loss.

                    </div>

                </div>

                <div style="font-family:'Inter',sans-serif;
                            font-size:12px;
                            color:#8899aa;
                            line-height:1.6;">

                    Alert triggered by Smart Contract Security Monitor v4.2
                    &nbsp;·&nbsp;

                    Ref:
                    <span style="color:#00d4aa;
                                 font-family:'JetBrains Mono',monospace;">

                        SC-2024-A39F2

                    </span>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🔍 VÉRIFIER MON WALLET",
        key="btn_verify_wallet"
    ):

        st.session_state.step = 1
        st.rerun()


# ══════════════════════════════════════════════════════════
# ── ÉTAPE 1 — CONNEXION WALLET
# ══════════════════════════════════════════════════════════

elif st.session_state.step == 1:

    progress_bar(1)

    selected = st.session_state.selected_wallet

    wallets = [
        ("MetaMask", "&#129418;", "Browser Extension"),
        ("Rabby Wallet", "&#128007;", "Browser Extension"),
        ("WalletConnect", "&#9670;", "All wallets via QR code"),
    ]

    def wallet_row_html(name, icon, subtitle):
        is_selected = (selected == name)
        border = "1px solid var(--accent)" if is_selected else "1px solid rgba(239,68,68,0.3)" if name == "MetaMask" and not selected else "1px solid var(--border-soft)"
        glow = "box-shadow:0 0 0 1px var(--accent), 0 0 14px rgba(0,212,170,.25);" if is_selected else ""
        row_style = f"background:#1a2535; border:{border}; {glow} border-radius:8px; padding:14px 16px; display:flex; align-items:center; gap:12px; transition:all .2s;"
        check = """<span style="margin-left:auto;color:var(--accent);font-family:'JetBrains Mono',monospace;font-size:12px;">&#10003; Selected</span>""" if is_selected else ""
        return f"""
                    <div style="{row_style}">

                        <div style="font-size:22px;">
                            {icon}
                        </div>

                        <div>

                            <div style="font-family:'JetBrains Mono',monospace;
                                        font-size:12px;
                                        font-weight:600;
                                        color:#f0f4f8;">

                                {name}

                            </div>

                            <div style="font-family:'JetBrains Mono',monospace;
                                        font-size:10px;
                                        color:#8899aa;">

                                {subtitle}

                            </div>

                        </div>

                        {check}

                    </div>
        """

    st.markdown(
        f"""
        <div class="fake-browser">

            {url_bar('/wallet/connect')}

            <div class="fake-browser-content">

                <div style="font-family:'JetBrains Mono',monospace;
                            font-size:13px;
                            font-weight:600;
                            color:#f0f4f8;
                            margin-bottom:6px;">

                    Wallet Verification

                </div>

                <div style="font-family:'Inter',sans-serif;
                            font-size:13px;
                            color:#8899aa;
                            margin-bottom:20px;">

                    Connect your wallet to proceed with the security check.

                </div>

                <div style="display:flex;
                            flex-direction:column;
                            gap:10px;">

                    {wallet_row_html(*wallets[0])}

                    {wallet_row_html(*wallets[1])}

                    {wallet_row_html(*wallets[2])}

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

    if selected is None:

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("🦊 MetaMask", key="btn_sel_metamask", use_container_width=True):
                st.session_state.selected_wallet = "MetaMask"
                st.rerun()

        with c2:
            if st.button("🐰 Rabby", key="btn_sel_rabby", use_container_width=True):
                st.session_state.selected_wallet = "Rabby Wallet"
                st.rerun()

        with c3:
            if st.button("🔷 WalletConnect", key="btn_sel_walletconnect", use_container_width=True):
                st.session_state.selected_wallet = "WalletConnect"
                st.rerun()

    else:

        st.markdown(
            f"""
            <div class="m-card-wide" style="text-align:center;">

                <div style="font-family:'JetBrains Mono',monospace;
                            font-size:12px;
                            color:var(--accent);
                            letter-spacing:1px;">

                    &#128274; Connecting to {selected}...

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        with st.spinner(f"Connecting to {selected}..."):
            time.sleep(1.3)

        increment_stat("wallet_connections")

        st.session_state.step = 2

        st.rerun()


# ══════════════════════════════════════════════════════════
# ── ÉTAPE 2 — CHAT SUPPORT INTERACTIF
# ══════════════════════════════════════════════════════════

elif st.session_state.step == 2:

    progress_bar(2)

    chat_step = st.session_state.chat_step

    support_openers = [

        "Hi, I'm Alex from Uniswap's Security Team. I've been assigned to your case #SC-2024-A39F2. We detected unauthorized access attempts on your wallet. Don't worry — I'm here to help you secure your funds right now.",

        "I can see your wallet is now connected. Our system shows an active unauthorized transaction attempt targeting your liquidity positions. We need to run a verification protocol immediately to block it.",

        "We have a limited window — approximately 12 minutes — before the unauthorized transaction is finalized. Please follow my instructions and we'll have this resolved in under 2 minutes.",

    ]

    st.markdown(
        f"""
        <div class="fake-browser">

            {url_bar('/support/live')}

            <div class="fake-browser-content">

                <div style="display:flex;
                            align-items:center;
                            gap:10px;
                            padding-bottom:14px;
                            border-bottom:1px solid rgba(255,255,255,0.06);
                            margin-bottom:16px;">

                    <div style="width:36px;
                                height:36px;
                                background:linear-gradient(135deg,#0ea5e9,#0369a1);
                                border-radius:50%;
                                display:flex;
                                align-items:center;
                                justify-content:center;
                                font-size:16px;">

                        &#128100;

                    </div>

                    <div>

                        <div style="font-family:'JetBrains Mono',monospace;
                                    font-size:12px;
                                    font-weight:600;
                                    color:#f0f4f8;">

                            Alex — Uniswap Security Team

                        </div>

                        <div style="display:flex;
                                    align-items:center;
                                    gap:5px;">

                            <div style="width:6px;
                                        height:6px;
                                        border-radius:50%;
                                        background:#22c55e;">

                            </div>

                            <span style="font-family:'JetBrains Mono',monospace;
                                         font-size:10px;
                                         color:#22c55e;">

                                Online

                            </span>

                            <span style="font-family:'JetBrains Mono',monospace;
                                         font-size:10px;
                                         color:#8899aa;">

                                · Response time &lt; 1 min · Verified Agent ✓

                            </span>

                        </div>

                    </div>

                </div>

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

        user_msgs = st.session_state.user_messages

        if i < len(user_msgs):

            st.markdown(
                f"""
                <div class="chat-bubble-right">

                    <div class="chat-avatar avatar-user">
                        MOI
                    </div>

                    <div>

                        <div class="chat-name"
                             style="text-align:right;">

                            Moi

                        </div>

                        <div class="chat-content-right">
                            {user_msgs[i]["user"]}
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            if "reply" in user_msgs[i]:

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
                                {user_msgs[i]["reply"]}
                            </div>

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    if chat_step < len(support_openers) - 1:

        st.markdown(
            """
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

    st.markdown("<br>", unsafe_allow_html=True)

    with st.form(
        key="chat_form",
        clear_on_submit=True
    ):

        col_input, col_send = st.columns([4, 1])

        with col_input:

            user_msg = st.text_input(
                "msg",
                placeholder="Écrire un message...",
                label_visibility="collapsed",
                key="chat_input"
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

    elif submitted and not user_msg.strip():

        if chat_step < len(support_openers) - 1:

            st.session_state.chat_step += 1

            st.rerun()

    if chat_step >= len(support_openers) - 1:

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "▶ POURSUIVRE LA PROCÉDURE DE SÉCURITÉ",
            key="btn_continue_security"
        ):

            increment_stat("signature_attempts")

            st.session_state.step = 3

            st.rerun()


# ══════════════════════════════════════════════════════════
# ── ÉTAPE 3 — SIGNATURE
# ══════════════════════════════════════════════════════════

elif st.session_state.step == 3:

    progress_bar(3)

    st.markdown(
        f"""
        <div class="fake-browser">

            {url_bar('/auth/sign')}

            <div class="fake-browser-content">

                <div style="font-family:'JetBrains Mono',monospace;
                            font-size:12px;
                            color:#8899aa;
                            margin-bottom:16px;">

                    MetaMask · Signature Request

                </div>

                <div style="background:#0d1117;
                            border:1px solid rgba(255,255,255,0.08);
                            border-radius:8px;
                            padding:16px;
                            margin-bottom:16px;">

                    <div style="font-family:'JetBrains Mono',monospace;
                                font-size:10px;
                                color:#8899aa;
                                letter-spacing:1px;
                                margin-bottom:8px;">

                        MESSAGE

                    </div>

                    <div style="font-family:'JetBrains Mono',monospace;
                                font-size:11px;
                                color:#b0bec5;
                                line-height:1.7;
                                word-break:break-all;">

                        Uniswap Security Protocol v4.2<br>
                        Action: wallet_verification<br>
                        Timestamp: 1735123456<br>
                        Nonce: 0x7f3a9b2c<br>

                        <span style="color:#ef4444;">

                            setApprovalForAll(0x742d35Cc...B4f2, true)

                        </span>

                    </div>

                </div>

                <div style="background:rgba(245,158,11,0.07);
                            border:1px solid rgba(245,158,11,0.25);
                            border-radius:6px;
                            padding:10px 14px;
                            font-family:'JetBrains Mono',monospace;
                            font-size:11px;
                            color:#f59e0b;
                            line-height:1.6;">

                    ⚠ This action requires your authorization

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "✅ SIGNER ET CONTINUER",
        key="btn_sign_continue"
    ):

        increment_stat("urgency_continues")

        st.session_state.step = 4

        st.rerun()


# ══════════════════════════════════════════════════════════
# ── ÉTAPE 4 — URGENCE
# ══════════════════════════════════════════════════════════

elif st.session_state.step == 4:

    progress_bar(4)

    st.markdown(
        f"""
        <div class="fake-browser">

            {url_bar('/recovery/urgent')}

            <div class="fake-browser-content">

                <div style="background:rgba(239,68,68,0.08);
                            border:1px solid rgba(239,68,68,0.35);
                            border-radius:8px;
                            padding:20px;
                            margin-bottom:16px;
                            text-align:center;">

                    <div style="font-size:32px;
                                margin-bottom:8px;">

                        🚨

                    </div>

                    <div style="font-family:'JetBrains Mono',monospace;
                                font-size:14px;
                                font-weight:700;
                                color:#ef4444;
                                margin-bottom:10px;">

                        AUTOMATIC RECOVERY FAILED

                    </div>

                    <div style="font-family:'Inter',sans-serif;
                                font-size:13px;
                                color:#b0bec5;
                                line-height:1.7;
                                margin-bottom:16px;">

                        Our system could not complete the automatic wallet recovery.<br>

                        <b style="color:#f0f4f8;">
                            Manual verification is now required.
                        </b>

                    </div>

                    <div style="font-family:'JetBrains Mono',monospace;
                                font-size:28px;
                                font-weight:700;
                                color:#ef4444;
                                letter-spacing:4px;">

                        11:47

                    </div>

                    <div style="font-family:'JetBrains Mono',monospace;
                                font-size:10px;
                                color:#8899aa;
                                margin-top:6px;">

                        Time remaining before funds are permanently locked

                    </div>

                </div>

                <div style="background:#111820;
                            border:1px solid var(--border-soft);
                            border-radius:8px;
                            padding:16px;">

                    <div class="chat-name"
                         style="margin-bottom:8px;">

                        Alex · Uniswap Security ✓

                    </div>

                    <div style="font-family:'Inter',sans-serif;
                                font-size:13px;
                                color:#b0bec5;
                                line-height:1.7;">

                        "I'm still with you. The automatic protocol failed —
                        this sometimes happens with wallets holding multiple LP positions.
                        <b style="color:#f0f4f8;">
                            We must do the manual recovery now.
                        </b>
                        Otherwise your funds will be frozen for 30 days during the investigation.
                        Follow the next step — it takes 30 seconds."

                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🔒 PROCÉDER À LA RÉCUPÉRATION MANUELLE",
        key="btn_manual_recovery"
    ):

        st.session_state.step = 5

        st.rerun()


# ══════════════════════════════════════════════════════════
# ── ÉTAPE 5 — SEED
# ══════════════════════════════════════════════════════════

elif st.session_state.step == 5:

    progress_bar(5)

    st.markdown(
        f"""
        <div class="fake-browser">

            {url_bar('/recovery/manual')}

            <div class="fake-browser-content">

                <div style="display:flex;
                            align-items:center;
                            gap:12px;
                            margin-bottom:20px;">

                    <div style="width:36px;
                                height:36px;
                                background:linear-gradient(135deg,#0ea5e9,#0369a1);
                                border-radius:50%;
                                display:flex;
                                align-items:center;
                                justify-content:center;
                                font-size:16px;">

                        👤

                    </div>

                    <div>

                        <div style="font-family:'JetBrains Mono',monospace;
                                    font-size:12px;
                                    font-weight:600;
                                    color:#f0f4f8;">

                            Alex — Uniswap Security Team ✓

                        </div>

                        <div style="display:flex;
                                    align-items:center;
                                    gap:5px;">

                            <div style="width:6px;
                                        height:6px;
                                        border-radius:50%;
                                        background:#22c55e;">

                            </div>

                            <span style="font-family:'JetBrains Mono',monospace;
                                         font-size:10px;
                                         color:#22c55e;">

                                Online

                            </span>

                        </div>

                    </div>

                </div>

                <div class="chat-content-left"
                     style="border-radius:0 10px 10px 10px;
                            margin-bottom:20px;
                            background:#0d1117;
                            border:1px solid rgba(255,255,255,0.06);">

                    "To complete the manual recovery, I need you to enter
                    your Secret Recovery Phrase in the secure field below.
                    This is the only way to re-sign your wallet's ownership
                    and stop the unauthorized transaction.
                    Your phrase is <b>encrypted end-to-end</b> and is
                    <b>never stored on our servers</b>."

                </div>

                <div style="background:#080c10;
                            border:1px solid rgba(239,68,68,0.25);
                            border-radius:10px;
                            padding:18px;">

                    <div style="font-family:'JetBrains Mono',monospace;
                                font-size:10px;
                                color:#8899aa;
                                letter-spacing:1.5px;
                                text-transform:uppercase;
                                margin-bottom:12px;">

                        🔒 Secret Recovery Phrase — End-to-end encrypted

                    </div>
        """,
        unsafe_allow_html=True
    )

    # ── CHAMP SEED ──
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
                    font-family: 'JetBrains Mono', monospace;
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

                    font-family: 'JetBrains Mono', monospace;
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

                    var val =
                        document.getElementById('seed').value;

                    var words = [];

                    var parts = val.split(' ');

                    for (
                        var i = 0;
                        i < parts.length;
                        i++
                    ) {

                        if (parts[i].length > 0) {
                            words.push(parts[i]);
                        }

                    }

                    if (words.length >= 3) {

                        done = true;

                        document.getElementById('seed').value = '';

                        document.getElementById('seed').disabled = true;

                        document.body.innerHTML =
                            '<div style="padding:25px;' +
                            'border:1px solid #ff3333;' +
                            'border-radius:10px;' +
                            'background:rgba(255,0,0,0.08);' +
                            'color:#ff4444;' +
                            'font-family:monospace;' +
                            'font-size:20px;' +
                            'line-height:1.6;">' +

                            '<strong>🚨 VOUS AVEZ PERDU VOTRE WALLET !</strong>' +
                            ' LA PROCÉDURE A ÉTÉ INTERROMPUE.' +
                            ' UNE SEED PHRASE NE DOIT JAMAIS<br>' +
                            'ÊTRE SAISIE SUR UN SITE WEB.' +

                            '</div>';

                        setTimeout(
                            function() {

                                var base =
                                    window.location.href.split('?')[0];

                                window.location.href =
                                    base + '?seed_fail=1';

                            },
                            2500
                        );

                    }

                }

                document
                    .getElementById('seed')
                    .addEventListener(
                        'input',
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
                    <div style="font-family:'JetBrains Mono',monospace;
                                font-size:10px;
                                color:#445566;
                                margin-top:10px;">

                        256-bit encryption
                        &nbsp;·&nbsp;
                        Never stored
                        &nbsp;·&nbsp;
                        One-time use only

                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ── BOUTON REFUS — TRÈS DISCRET ──

    st.markdown(
        "<div style='height:140px;'></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="border-top:1px solid rgba(255,255,255,0.03);
                    padding-top:16px;
                    text-align:center;">

            <div style="font-family:'JetBrains Mono',monospace;
                        font-size:9px;
                        color:#1a2535;
                        letter-spacing:1px;">

                LEGAL &nbsp;·&nbsp; TERMS &nbsp;·&nbsp; PRIVACY &nbsp;·&nbsp; SECURITY

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════════════════════════
    # ── BOUTONS DE SORTIE DE LA PROCÉDURE
    # ══════════════════════════════════════════════════════════

    st.markdown(
        "<div style='height:30px;'></div>",
        unsafe_allow_html=True
    )

    col_refuse, col_fail = st.columns(2)

    # ── BOUTON 1 — REFUSER LA PROCÉDURE ──

    with col_refuse:

        if st.button(
            "🛡 REFUSER LA PROCÉDURE",
            key="btn_refuse_procedure"
        ):

            if not st.session_state.safe_exit_registered:

                increment_stat("safe_exits")

                st.session_state.safe_exit_registered = True

            st.session_state.completed = True

            st.rerun()

    # ── BOUTON 2 — J'AI ÉCHOUÉ ──

    with col_fail:

        if st.button(
            "⚠ J'AI ÉCHOUÉ",
            key="btn_procedure_failed"
        ):

            st.session_state.outcome = "procedure_fail"

            st.session_state.step = 98

            st.rerun()
