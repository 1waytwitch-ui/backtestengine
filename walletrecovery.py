# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import sqlite3
from pathlib import Path

# =========================================================
# CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="WALLET RECOVERY",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================================================
# CSS GLOBAL
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #080c10;
    --panel: #0d1318;
    --card: #111820;
    --text: #f0f4f8;
    --muted: #8899aa;
    --dim: #445566;
    --green: #00d4aa;
    --red: #ef4444;
    --orange: #f59e0b;
    --success: #22c55e;
    --border: rgba(255,255,255,.08);
}

#MainMenu, footer,
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
[data-testid="stToolbar"],
[data-testid="stHeader"] {
    display: none !important;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: Inter, sans-serif;
}

.block-container {
    max-width: 820px !important;
    padding: 82px 18px 60px !important;
}

.nav-bar {
    position: fixed;
    z-index: 9999;
    top: 0;
    left: 0;
    width: 100%;
    min-height: 58px;
    padding: 8px 18px;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    background: rgba(6,10,14,.98);
    border-bottom: 1px solid rgba(239,68,68,.25);
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.nav-glyph {
    width: 30px;
    height: 30px;
    border: 2px solid var(--red);
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.nav-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
}

.nav-subtitle {
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    letter-spacing: .7px;
    margin-top: 2px;
}

.status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    margin-right: 5px;
    border-radius: 50%;
    background: var(--red);
}

.fake-browser {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 12px;
    background: #0d1117;
    box-shadow: 0 18px 50px rgba(0,0,0,.40);
}

.fake-browser-bar {
    width: 100%;
    box-sizing: border-box;
    min-height: 52px;
    padding: 10px 12px;
    display: flex;
    align-items: center;
    gap: 10px;
    background: #1a1f2e;
    border-bottom: 1px solid rgba(255,255,255,.07);
}

.fake-dots {
    display: flex;
    gap: 6px;
    flex-shrink: 0;
}

.dot {
    width: 11px;
    height: 11px;
    border-radius: 50%;
}

.dot-r { background: #ff5f57; }
.dot-y { background: #febc2e; }
.dot-g { background: #28c840; }

.fake-url-bar {
    min-width: 0;
    flex: 1;
    overflow: hidden;
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 7px 10px;
    border-radius: 7px;
    background: #0d1117;
    border: 1px solid rgba(255,255,255,.08);
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    white-space: nowrap;
}

.fake-url-text {
    color: #8899aa;
    flex-shrink: 0;
}

.fake-url-host {
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    color: #f0f4f8;
    font-weight: 600;
}

.fake-browser-content {
    width: 100%;
    box-sizing: border-box;
    padding: clamp(16px, 4vw, 30px);
    background: #0d1117;
}

.sec-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 28px 0 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(0,212,170,.18);
}

.sec-head-icon {
    width: 25px;
    height: 25px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0,212,170,.10);
    border: 1px solid rgba(0,212,170,.20);
}

.sec-head-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
}

.card {
    padding: 20px;
    margin: 12px 0;
    border-radius: 10px;
    background: var(--card);
    border: 1px solid var(--border);
}

.danger-card {
    padding: 28px 20px;
    margin: 14px 0;
    border-radius: 10px;
    text-align: center;
    background: rgba(239,68,68,.07);
    border: 1px solid rgba(239,68,68,.35);
}

.success-card {
    padding: 28px 20px;
    margin: 14px 0;
    border-radius: 10px;
    text-align: center;
    background: rgba(34,197,94,.07);
    border: 1px solid rgba(34,197,94,.30);
}

.step-card {
    position: relative;
    overflow: hidden;
    padding: 24px;
    margin: 14px 0;
    border-radius: 12px;
    background: var(--card);
    border: 1px solid var(--border);
}

.step-card:before {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    width: 3px;
    background: var(--red);
}

.progress-wrap {
    margin: 10px 0 24px;
}

.progress-track {
    height: 3px;
    border-radius: 3px;
    background: rgba(255,255,255,.08);
}

.progress-fill {
    height: 3px;
    border-radius: 3px;
    background: var(--red);
    box-shadow: 0 0 8px rgba(239,68,68,.5);
}

.progress-label {
    margin-top: 6px;
    text-align: right;
    color: var(--dim);
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
}

.chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.chat-left, .chat-right {
    display: flex;
    gap: 10px;
    max-width: 88%;
}

.chat-right {
    align-self: flex-end;
    flex-direction: row-reverse;
}

.avatar {
    width: 32px;
    height: 32px;
    flex: 0 0 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.avatar-support { background: linear-gradient(135deg,#0ea5e9,#0369a1); }
.avatar-user { background: #273244; font-size: 11px; }

.chat-bubble {
    padding: 12px 15px;
    border-radius: 0 10px 10px 10px;
    color: #b0bec5;
    background: #111820;
    border: 1px solid var(--border);
    line-height: 1.65;
    font-size: 13px;
}

.chat-right .chat-bubble {
    border-radius: 10px 0 10px 10px;
    color: var(--text);
    background: #1a2535;
}

.chat-name {
    margin-bottom: 4px;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
}

.stat-card {
    padding: 18px 10px;
    margin-bottom: 10px;
    text-align: center;
    border-radius: 10px;
    background: var(--card);
    border: 1px solid var(--border);
}

.stat-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 28px;
    font-weight: 700;
}

.stat-label {
    margin-top: 7px;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    letter-spacing: 1px;
}

.rule {
    display: flex;
    gap: 12px;
    padding: 15px 0;
    border-bottom: 1px solid rgba(255,255,255,.06);
    color: #b0bec5;
    line-height: 1.6;
    font-size: 13px;
}

.rule:last-child { border-bottom: 0; }

.rule-num {
    min-width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    color: var(--red);
    background: rgba(239,68,68,.10);
    border: 1px solid rgba(239,68,68,.25);
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
}

button {
    min-height: 44px !important;
}

.stButton > button {
    width: 100%;
    border: 0 !important;
    border-radius: 8px !important;
    background: var(--red) !important;
    color: white !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: .8px !important;
}

.stButton > button:hover {
    filter: brightness(1.08);
    box-shadow: 0 6px 20px rgba(239,68,68,.30);
}

@media (max-width: 600px) {
    .block-container {
        padding-left: 10px !important;
        padding-right: 10px !important;
    }

    .nav-title { font-size: 11px; }
    .nav-subtitle { font-size: 8px; }

    .fake-browser-bar {
        padding: 8px;
        gap: 7px;
    }

    .dot {
        width: 9px;
        height: 9px;
    }

    .fake-url-bar {
        font-size: 8px;
        padding: 6px 7px;
    }

    .chat-left, .chat-right {
        max-width: 96%;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# NAVIGATION
# =========================================================
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

# =========================================================
# DATABASE
# =========================================================
DB_FILE = Path("security_stats.db")

STAT_COLUMNS = [
    "participants",
    "wallet_connections",
    "signature_attempts",
    "urgency_continues",
    "seed_attempts",
    "safe_exits",
]

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
    conn.execute("INSERT OR IGNORE INTO statistics (id) VALUES (1)")
    conn.commit()
    conn.close()

def increment_stat(column):
    if column not in STAT_COLUMNS:
        return
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        f"UPDATE statistics SET {column} = {column} + 1 WHERE id = 1"
    )
    conn.commit()
    conn.close()

def get_statistics():
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute("""
        SELECT participants,
               wallet_connections,
               signature_attempts,
               urgency_continues,
               seed_attempts,
               safe_exits
        FROM statistics
        WHERE id = 1
    """).fetchone()
    conn.close()

    if not row:
        return {key: 0 for key in STAT_COLUMNS}

    return dict(zip(STAT_COLUMNS, row))

init_database()

# =========================================================
# SESSION
# =========================================================
defaults = {
    "step": 0,
    "completed": False,
    "outcome": None,
    "participant_registered": False,
    "safe_exit_registered": False,
    "seed_fail_registered": False,
    "chat_step": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

if not st.session_state.participant_registered:
    increment_stat("participants")
    st.session_state.participant_registered = True

# =========================================================
# SEED FAIL CALLBACK VIA QUERY PARAMETER
# =========================================================
if "seed_fail" in st.query_params:
    if not st.session_state.seed_fail_registered:
        increment_stat("seed_attempts")
        st.session_state.seed_fail_registered = True

    st.query_params.clear()
    st.session_state.outcome = "fail"
    st.session_state.step = 99

# =========================================================
# HELPERS
# =========================================================
def section_header(icon, title, color="#00d4aa"):
    st.markdown(
        f"""
        <div class="sec-head">
            <div class="sec-head-icon" style="color:{color};">{icon}</div>
            <div class="sec-head-label" style="color:{color};">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def progress(step, total=5):
    pct = min(100, max(0, step / total * 100))
    st.markdown(
        f"""
        <div class="progress-wrap">
            <div class="progress-track">
                <div class="progress-fill" style="width:{pct:.0f}%;"></div>
            </div>
            <div class="progress-label">ÉTAPE {step} / {total}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def reset_app():
    st.session_state.step = 0
    st.session_state.completed = False
    st.session_state.outcome = None
    st.session_state.safe_exit_registered = False
    st.session_state.seed_fail_registered = False
    st.session_state.chat_step = 0
    st.rerun()

def browser_header(path=""):
    return f"""
    <div class="fake-browser-bar">
        <div class="fake-dots">
            <div class="dot dot-r"></div>
            <div class="dot dot-y"></div>
            <div class="dot dot-g"></div>
        </div>

        <div class="fake-url-bar">
            <span>🔒</span>
            <span class="fake-url-text">https://</span>
            <span class="fake-url-host">uniswap-security.protocol-verify.com</span>
            <span style="color:#8899aa; overflow:hidden; text-overflow:ellipsis;">
                {path}
            </span>
        </div>
    </div>
    """

def show_pedagogy(outcome):
    stats = get_statistics()

    if outcome == "fail":
        st.markdown("""
        <div class="danger-card">
            <div style="font-size:48px;">💀</div>
            <h2 style="color:#ef4444; font-family:'JetBrains Mono',monospace;">
                VOUS AVEZ ÉTÉ SCAMMÉ
            </h2>
            <p style="color:#b0bec5; line-height:1.8;">
                Vous avez tenté de communiquer votre phrase de récupération.
                <br>
                <b style="color:#ef4444;">
                    Dans une situation réelle, votre wallet pourrait être vidé très rapidement.
                </b>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-card">
            <div style="font-size:48px;">🛡️</div>
            <h2 style="color:#22c55e; font-family:'JetBrains Mono',monospace;">
                VOUS AVEZ RÉSISTÉ
            </h2>
            <p style="color:#b0bec5; line-height:1.8;">
                Vous avez refusé de communiquer votre phrase de récupération.
                <br>
                <b style="color:#22c55e;">
                    C'est la seule décision correcte.
                </b>
            </p>
        </div>
        """, unsafe_allow_html=True)

    section_header("◈", "CE QUI VIENT DE SE PASSER", "#ef4444")

    st.markdown("""
    <div class="card">
        <div style="color:#b0bec5; line-height:2;">
            Vous venez de traverser une simulation de
            <b style="color:#f0f4f8;">phishing DeFi</b>.
            Chaque étape reproduit une technique couramment utilisée par des scammers :
            <br><br>
            <span style="color:#ef4444;">1.</span>
            Fausse alerte de sécurité
            <br>
            <span style="color:#ef4444;">2.</span>
            Fausse connexion wallet
            <br>
            <span style="color:#ef4444;">3.</span>
            Faux support
            <br>
            <span style="color:#ef4444;">4.</span>
            Demande de signature
            <br>
            <span style="color:#ef4444;">5.</span>
            Pression et urgence
            <br>
            <span style="color:#ef4444;">6.</span>
            Demande de phrase de récupération
        </div>
    </div>
    """, unsafe_allow_html=True)

    section_header("🛡", "RÈGLES ABSOLUES", "#22c55e")

    rules = [
        (
            "Votre seed phrase = votre wallet",
            "Quiconque possède votre phrase de récupération peut potentiellement contrôler les fonds associés. Aucun support légitime n'a besoin de la connaître."
        ),
        (
            "L'urgence est une arme",
            "Un scammer veut vous empêcher de réfléchir. Plus la pression est forte, plus vous devez vous arrêter et vérifier."
        ),
        (
            "Un support légitime ne demande jamais votre seed",
            "Ne communiquez jamais votre phrase de récupération à un support, un protocole ou une personne qui vous contacte."
        ),
        (
            "Vérifiez toujours l'URL",
            "Un site peut imiter parfaitement une interface connue tout en utilisant un domaine frauduleux."
        ),
        (
            "Lisez chaque signature",
            "Une signature ou une approbation peut avoir des conséquences importantes. Ne signez jamais automatiquement."
        ),
        (
            "Formez-vous avant de manipuler des fonds",
            "La sécurité ne repose pas sur la chance. Comprenez ce que vous signez et ne laissez jamais la pression décider à votre place."
        ),
    ]

    for i, (title, text) in enumerate(rules, 1):
        st.markdown(
            f"""
            <div class="rule">
                <div class="rule-num">{i}</div>
                <div>
                    <b style="color:#f0f4f8;">{title}</b>
                    <br>
                    {text}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    section_header("◉", "STATISTIQUES ANONYMES")

    st.markdown("""
    <div class="card">
        <div style="color:#8899aa; font-size:12px; line-height:1.7;">
            Ces chiffres sont collectés de manière <b style="color:#f0f4f8;">anonyme</b>.
            <br>
            Aucune seed phrase n'est stockée ou transmise par l'application.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    metrics = [
        ("PARTICIPANTS", stats["participants"], "#00d4aa"),
        ("REFUS DE LA SEED", stats["safe_exits"], "#22c55e"),
        ("CONNEXIONS WALLET", stats["wallet_connections"], "#f59e0b"),
        ("TENTATIVES DE SIGNATURE", stats["signature_attempts"], "#f59e0b"),
        ("ONT SUIVI L'URGENCE", stats["urgency_continues"], "#ef4444"),
        ("TENTATIVES DE SEED", stats["seed_attempts"], "#ef4444"),
    ]

    for i, (label, value, color) in enumerate(metrics):
        with c1 if i % 2 == 0 else c2:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-num" style="color:{color};">{value:,}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """.replace(",", "\u202f"),
                unsafe_allow_html=True,
            )

    if stats["participants"] > 0:
        pct = stats["seed_attempts"] / stats["participants"] * 100

        st.markdown(
            f"""
            <div class="danger-card">
                <div style="color:#ef4444; font-family:'JetBrains Mono',monospace; font-weight:700;">
                    🚨 STATISTIQUE À RETENIR
                </div>
                <div style="font-size:42px; font-weight:700; color:#ef4444; margin:12px 0;">
                    {pct:.1f}%
                </div>
                <div style="color:#b0bec5; line-height:1.8;">
                    des participants ont tenté de saisir leur phrase de récupération.
                    <br><br>
                    <b style="color:#f0f4f8;">
                        Un vrai scammer, lui, ne vous aurait pas arrêté.
                    </b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("◈ RECOMMENCER LA SIMULATION"):
        reset_app()

# =========================================================
# ROUTING FINAL
# =========================================================
if st.session_state.step == 99 or st.session_state.outcome == "fail":
    show_pedagogy("fail")
    st.stop()

if st.session_state.completed:
    show_pedagogy("success")
    st.stop()

# =========================================================
# ÉTAPE 0 — FAUSSE ALERTE
# =========================================================
if st.session_state.step == 0:

    st.markdown(
        """
        <div class="fake-browser">
        """ + browser_header() + """
            <div class="fake-browser-content">

                <div style="display:flex; align-items:center; gap:12px; margin-bottom:20px;">
                    <div style="
                        width:38px;
                        height:38px;
                        border-radius:50%;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        background:linear-gradient(135deg,#ff007a,#ff6b00);
                        font-size:19px;
                    ">🦄</div>

                    <div>
                        <div style="
                            color:#f0f4f8;
                            font-family:'JetBrains Mono',monospace;
                            font-size:14px;
                            font-weight:700;
                        ">Uniswap Protocol</div>

                        <div style="
                            color:#8899aa;
                            font-family:'JetBrains Mono',monospace;
                            font-size:10px;
                        ">Security Center</div>
                    </div>
                </div>

                <div style="
                    padding:18px;
                    border-radius:8px;
                    background:rgba(239,68,68,.08);
                    border:1px solid rgba(239,68,68,.30);
                ">
                    <div style="
                        color:#ef4444;
                        font-family:'JetBrains Mono',monospace;
                        font-size:12px;
                        font-weight:700;
                        margin-bottom:8px;
                    ">⚠ SECURITY ALERT — ACTION REQUIRED</div>

                    <div style="
                        color:#b0bec5;
                        font-size:13px;
                        line-height:1.7;
                    ">
                        We have detected
                        <b style="color:#f0f4f8;">unauthorized access attempts</b>
                        on your wallet address.
                        <br>
                        Your funds may be at risk.
                        Verify your wallet immediately to prevent loss.
                    </div>
                </div>

                <div style="
                    color:#8899aa;
                    font-size:12px;
                    line-height:1.7;
                    margin-top:16px;
                ">
                    Smart Contract Security Monitor v4.2
                    <br>
                    Reference:
                    <span style="color:#00d4aa; font-family:'JetBrains Mono',monospace;">
                        SC-2024-A39F2
                    </span>
                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🔍 VÉRIFIER MON WALLET"):
        st.session_state.step = 1
        st.rerun()

# =========================================================
# ÉTAPE 1 — CONNEXION WALLET
# =========================================================
elif st.session_state.step == 1:

    progress(1)

    st.markdown(
        """
        <div class="fake-browser">
        """ + browser_header("/wallet/connect") + """
            <div class="fake-browser-content">

                <div style="
                    color:#f0f4f8;
                    font-family:'JetBrains Mono',monospace;
                    font-size:13px;
                    font-weight:700;
                    margin-bottom:6px;
                ">Wallet Verification</div>

                <div style="
                    color:#8899aa;
                    font-size:13px;
                    margin-bottom:20px;
                ">Connect your wallet to proceed with the security check.</div>

                <div style="display:flex; flex-direction:column; gap:10px;">

                    <div style="
                        padding:14px 16px;
                        display:flex;
                        align-items:center;
                        gap:12px;
                        border-radius:8px;
                        background:#1a2535;
                        border:1px solid rgba(14,165,233,.20);
                    ">
                        <div style="font-size:22px;">🐇</div>
                        <div>
                            <div style="
                                color:#f0f4f8;
                                font-family:'JetBrains Mono',monospace;
                                font-size:12px;
                                font-weight:700;
                            ">RABBY WALLET</div>
                            <div style="
                                color:#8899aa;
                                font-family:'JetBrains Mono',monospace;
                                font-size:10px;
                            ">Browser Extension</div>
                        </div>
                    </div>

                    <div style="
                        padding:14px 16px;
                        display:flex;
                        align-items:center;
                        gap:12px;
                        border-radius:8px;
                        background:#1a2535;
                        border:1px solid rgba(255,255,255,.06);
                    ">
                        <div style="font-size:22px;">🔵</div>
                        <div>
                            <div style="
                                color:#f0f4f8;
                                font-family:'JetBrains Mono',monospace;
                                font-size:12px;
                                font-weight:700;
                            ">Coinbase Wallet</div>
                            <div style="
                                color:#8899aa;
                                font-family:'JetBrains Mono',monospace;
                                font-size:10px;
                            ">Mobile & Extension</div>
                        </div>
                    </div>

                    <div style="
                        padding:14px 16px;
                        display:flex;
                        align-items:center;
                        gap:12px;
                        border-radius:8px;
                        background:#1a2535;
                        border:1px solid rgba(255,255,255,.06);
                    ">
                        <div style="font-size:22px;">◈</div>
                        <div>
                            <div style="
                                color:#f0f4f8;
                                font-family:'JetBrains Mono',monospace;
                                font-size:12px;
                                font-weight:700;
                            ">WalletConnect</div>
                            <div style="
                                color:#8899aa;
                                font-family:'JetBrains Mono',monospace;
                                font-size:10px;
                            ">All wallets via QR code</div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🐇 CONNECTER RABBY WALLET"):
        increment_stat("wallet_connections")
        st.session_state.step = 2
        st.rerun()

# =========================================================
# ÉTAPE 2 — SUPPORT
# =========================================================
elif st.session_state.step == 2:

    progress(2)

    messages = [
        "Hi, I'm Alex from Uniswap's Security Team. I've been assigned to your case. We detected unauthorized access attempts on your wallet. Don't worry — I'm here to help you secure your funds.",
        "I can see your wallet is connected. Our system shows your liquidity positions are at risk. We need to run a verification protocol to protect your assets.",
        "This is urgent. We have a 15-minute window to secure your wallet before the unauthorized transaction goes through. Please follow my instructions carefully.",
    ]

    st.markdown(
        """
        <div class="fake-browser">
        """ + browser_header("/support/live") + """
            <div class="fake-browser-content">

                <div style="
                    display:flex;
                    align-items:center;
                    gap:10px;
                    padding-bottom:14px;
                    margin-bottom:16px;
                    border-bottom:1px solid rgba(255,255,255,.06);
                ">
                    <div class="avatar avatar-support">👤</div>
                    <div>
                        <div style="
                            color:#f0f4f8;
                            font-family:'JetBrains Mono',monospace;
                            font-size:12px;
                            font-weight:700;
                        ">Alex — Uniswap Security Team</div>
                        <div style="color:#22c55e; font-size:10px;">● Online</div>
                    </div>
                </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)

    for i in range(min(st.session_state.chat_step + 1, len(messages))):
        st.markdown(
            f"""
            <div class="chat-left">
                <div class="avatar avatar-support">👤</div>
                <div>
                    <div class="chat-name">Alex · Uniswap Security</div>
                    <div class="chat-bubble">{messages[i]}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if i == 0 and st.session_state.chat_step >= 1:
            st.markdown("""
            <div class="chat-right">
                <div class="avatar avatar-user">MOI</div>
                <div>
                    <div class="chat-name" style="text-align:right;">Moi</div>
                    <div class="chat-bubble">Ok, qu'est-ce que je dois faire ?</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if i == 1 and st.session_state.chat_step >= 2:
            st.markdown("""
            <div class="chat-right">
                <div class="avatar avatar-user">MOI</div>
                <div>
                    <div class="chat-name" style="text-align:right;">Moi</div>
                    <div class="chat-bubble">Mes positions sont vraiment en danger ?</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div></div></div>", unsafe_allow_html=True)

    if st.session_state.chat_step < len(messages) - 1:
        c1, c2 = st.columns(2)

        with c1:
            if st.button("▶ RÉPONDRE AU SUPPORT"):
                st.session_state.chat_step += 1
                st.rerun()

        with c2:
            if st.button("⟳ ATTENDRE LA RÉPONSE"):
                st.session_state.chat_step += 1
                st.rerun()
    else:
        if st.button("▶ POURSUIVRE LA PROCÉDURE DE SÉCURITÉ"):
            increment_stat("signature_attempts")
            st.session_state.step = 3
            st.rerun()

# =========================================================
# ÉTAPE 3 — SIGNATURE
# =========================================================
elif st.session_state.step == 3:

    progress(3)

    st.markdown(
        """
        <div class="fake-browser">
        """ + browser_header("/auth/sign") + """
            <div class="fake-browser-content">

                <div style="
                    color:#8899aa;
                    font-family:'JetBrains Mono',monospace;
                    font-size:12px;
                    margin-bottom:16px;
                ">RABBY WALLET · Signature Request</div>

                <div style="
                    padding:16px;
                    margin-bottom:16px;
                    border-radius:8px;
                    background:#0d1117;
                    border:1px solid rgba(255,255,255,.08);
                ">
                    <div style="
                        color:#8899aa;
                        font-family:'JetBrains Mono',monospace;
                        font-size:10px;
                        letter-spacing:1px;
                        margin-bottom:8px;
                    ">MESSAGE</div>

                    <div style="
                        color:#b0bec5;
                        font-family:'JetBrains Mono',monospace;
                        font-size:11px;
                        line-height:1.7;
                        word-break:break-word;
                    ">
                        Uniswap Security Protocol v4.2<br>
                        Action: wallet_verification<br>
                        Timestamp: 1735123456<br>
                        Nonce: 0x7f3a9b2c<br>
                        <span style="color:#ef4444;">
                            setApprovalForAll(0x742d35Cc...B4f2, true)
                        </span>
                    </div>
                </div>

                <div style="
                    padding:10px 14px;
                    border-radius:6px;
                    color:#f59e0b;
                    background:rgba(245,158,11,.07);
                    border:1px solid rgba(245,158,11,.25);
                    font-family:'JetBrains Mono',monospace;
                    font-size:11px;
                ">
                    ⚠ This action requires your authorization
                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("✅ SIGNER ET CONTINUER"):
        increment_stat("urgency_continues")
        st.session_state.step = 4
        st.rerun()

# =========================================================
# ÉTAPE 4 — URGENCE
# =========================================================
elif st.session_state.step == 4:

    progress(4)

    st.markdown(
        """
        <div class="fake-browser">
        """ + browser_header("/recovery/urgent") + """
            <div class="fake-browser-content">

                <div style="
                    padding:20px;
                    margin-bottom:16px;
                    text-align:center;
                    border-radius:8px;
                    background:rgba(239,68,68,.08);
                    border:1px solid rgba(239,68,68,.35);
                ">
                    <div style="font-size:32px;">🚨</div>

                    <div style="
                        color:#ef4444;
                        font-family:'JetBrains Mono',monospace;
                        font-size:14px;
                        font-weight:700;
                        margin:10px 0;
                    ">AUTOMATIC RECOVERY FAILED</div>

                    <div style="
                        color:#b0bec5;
                        font-size:13px;
                        line-height:1.7;
                    ">
                        Our system could not complete the automatic wallet recovery.
                        <br>
                        <b style="color:#f0f4f8;">Manual verification is now required.</b>
                    </div>

                    <div style="
                        margin-top:16px;
                        color:#ef4444;
                        font-family:'JetBrains Mono',monospace;
                        font-size:22px;
                        font-weight:700;
                    ">11:47</div>

                    <div style="
                        margin-top:4px;
                        color:#8899aa;
                        font-family:'JetBrains Mono',monospace;
                        font-size:10px;
                    ">Time remaining before funds are locked</div>
                </div>

                <div style="
                    padding:16px;
                    border-radius:8px;
                    background:#111820;
                    border:1px solid rgba(255,255,255,.06);
                    color:#b0bec5;
                    font-size:13px;
                    line-height:1.7;
                ">
                    <b style="color:#f0f4f8;">Alex · Uniswap Security</b>
                    <br><br>
                    "The automatic protocol failed. We need to do the manual recovery now. Follow the next step and this will be resolved."
                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🔐 PROCÉDER À LA RÉCUPÉRATION MANUELLE"):
        st.session_state.step = 5
        st.rerun()

# =========================================================
# ÉTAPE 5 — PHRASE DE RÉCUPÉRATION
# =========================================================
elif st.session_state.step == 5:

    progress(5)

    st.markdown(
        """
        <div class="fake-browser">
        """ + browser_header("/recovery/manual") + """
            <div class="fake-browser-content">

                <div style="
                    display:flex;
                    align-items:center;
                    gap:12px;
                    margin-bottom:20px;
                ">
                    <div class="avatar avatar-support">👤</div>
                    <div>
                        <div style="
                            color:#f0f4f8;
                            font-family:'JetBrains Mono',monospace;
                            font-size:12px;
                            font-weight:700;
                        ">Alex — Uniswap Security Team</div>
                        <div style="color:#22c55e; font-size:10px;">● Online</div>
                    </div>
                </div>

                <div style="
                    padding:14px 16px;
                    margin-bottom:16px;
                    border-radius:0 10px 10px 10px;
                    background:#0d1117;
                    border:1px solid rgba(255,255,255,.06);
                    color:#b0bec5;
                    font-size:13px;
                    line-height:1.7;
                ">
                    "To complete the manual recovery, enter your Secret Recovery Phrase below."
                </div>

                <div style="
                    padding:16px;
                    border-radius:8px;
                    background:#080c10;
                    border:1px solid rgba(239,68,68,.20);
                ">
                    <div style="
                        color:#8899aa;
                        font-family:'JetBrains Mono',monospace;
                        font-size:10px;
                        letter-spacing:1.5px;
                        margin-bottom:10px;
                    ">SECRET RECOVERY PHRASE</div>
        """,
        unsafe_allow_html=True,
    )

    # IMPORTANT :
    # La phrase reste uniquement dans l'iframe.
    # Elle n'est jamais envoyée à Streamlit et n'est jamais stockée.
    components.html(
        """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        * { box-sizing:border-box; }

        html, body {
            margin:0;
            padding:0;
            background:#080c10;
            font-family:'JetBrains Mono','Courier New',monospace;
        }

        textarea {
            width:100%;
            height:110px;
            resize:none;
            padding:14px;
            border-radius:8px;
            outline:none;
            background:#030608;
            color:#00d4aa;
            border:1px solid rgba(239,68,68,.30);
            font-family:'JetBrains Mono','Courier New',monospace;
            font-size:14px;
        }

        textarea::placeholder {
            color:#445566;
        }

        textarea:focus {
            border-color:rgba(239,68,68,.65);
            box-shadow:0 0 0 2px rgba(239,68,68,.08);
        }

        .blocked {
            padding:20px;
            border-radius:8px;
            color:#ef4444;
            background:rgba(239,68,68,.07);
            border:1px solid rgba(239,68,68,.35);
            font-size:13px;
            line-height:1.8;
        }
        </style>
        </head>

        <body>

        <textarea
            id="seed"
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
            spellcheck="false"
            placeholder="Enter your 12 or 24-word secret recovery phrase..."
        ></textarea>

        <script>
        const input = document.getElementById("seed");

        input.addEventListener("input", function () {
            const words = this.value
                .trim()
                .split(/[\\s]+/)
                .filter(Boolean);

            // Blocage immédiat dès le troisième mot.
            if (words.length >= 3) {
                this.value = "";
                this.disabled = true;

                document.body.innerHTML = `
                    <div class="blocked">
                        🚨 TENTATIVE DÉTECTÉE — PROCÉDURE INTERROMPUE
                        <br><br>
                        <span style="color:#f0f4f8;font-size:12px;">
                            Vous venez de tenter de communiquer une phrase de récupération.
                            <br>
                            Dans une situation réelle, vos fonds pourraient être compromis.
                            <br><br>
                            <b style="color:#ef4444;">
                                UNE PHRASE DE RÉCUPÉRATION NE SE SAISIT JAMAIS SUR UN SITE WEB.
                            </b>
                        </span>
                    </div>
                `;

                setTimeout(function () {
                    const base = window.top.location.href.split("?")[0];
                    window.top.location.href = base + "?seed_fail=1";
                }, 1800);
            }
        });
        </script>

        </body>
        </html>
        """,
        height=150,
        scrolling=False,
    )

    st.markdown(
        """
                </div>

                <div style="
                    margin-top:10px;
                    color:#8899aa;
                    font-family:'JetBrains Mono',monospace;
                    font-size:10px;
                    line-height:1.6;
                ">
                    🔒 No recovery phrase is stored by this application.
                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])

    with c1:
        if st.button("🛡️ NON — JE REFUSE DE DONNER MA SEED PHRASE"):
            if not st.session_state.safe_exit_registered:
                increment_stat("safe_exits")
                st.session_state.safe_exit_registered = True

            st.session_state.completed = True
            st.rerun()

    with c2:
        st.markdown("""
        <div style="
            padding:14px 0;
            text-align:center;
            color:#445566;
            font-family:'JetBrains Mono',monospace;
            font-size:10px;
        ">
            ← SEULE BONNE DÉCISION
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div style="height:40px;"></div>

<div style="
    padding-top:16px;
    text-align:center;
    color:#445566;
    border-top:1px solid rgba(255,255,255,.06);
    font-family:'JetBrains Mono',monospace;
    font-size:10px;
    letter-spacing:1px;
">
    ◈ WALLET RECOVERY · SESSION LOCKED · WARNING AUTO ALERT
</div>
""", unsafe_allow_html=True)
