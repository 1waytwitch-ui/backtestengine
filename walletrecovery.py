from pathlib import Path

code = r'''# -*- coding: utf-8 -*-
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
# CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-main:#080c10;
    --bg-panel:#0d1318;
    --bg-card:#111820;
    --accent:#00d4aa;
    --accent-dim:rgba(0,212,170,.10);
    --border:rgba(0,212,170,.18);
    --border-soft:rgba(255,255,255,.06);
    --text-hi:#f0f4f8;
    --text-mid:#8899aa;
    --text-lo:#445566;
    --red:#ef4444;
    --green:#22c55e;
    --yellow:#f59e0b;
    --font-mono:'JetBrains Mono','Courier New',monospace;
    --font-ui:'Inter',sans-serif;
}

#MainMenu, footer { visibility:hidden !important; }
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
[data-testid="stToolbar"],
[data-testid="stHeader"] { display:none !important; }

.block-container {
    padding-top:72px !important;
    padding-bottom:60px !important;
    width:100% !important;
    max-width:780px !important;
}

html, body, [data-testid="stAppViewContainer"] {
    background:var(--bg-main) !important;
    color:var(--text-hi);
    font-family:var(--font-ui);
}

.nav-bar {
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:58px;
    z-index:99999;
    background:rgba(6,10,14,.98);
    backdrop-filter:blur(16px);
    border-bottom:1px solid rgba(239,68,68,.25);
    display:flex;
    align-items:center;
    padding:0 28px;
    box-sizing:border-box;
}

.nav-brand {
    display:flex;
    align-items:center;
    gap:10px;
}

.nav-glyph {
    width:28px;
    height:28px;
    border:2px solid var(--red);
    border-radius:6px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:14px;
}

.nav-title {
    font-family:var(--font-mono);
    font-size:13px;
    font-weight:600;
    color:var(--text-hi);
    letter-spacing:2px;
}

.nav-subtitle {
    font-family:var(--font-mono);
    font-size:10px;
    color:var(--text-mid);
    letter-spacing:1px;
}

.status-dot {
    width:7px;
    height:7px;
    border-radius:50%;
    background:var(--red);
    display:inline-block;
    margin-right:5px;
    animation:pulse-red 1.2s infinite;
}

@keyframes pulse-red {
    0%,100% { opacity:1; box-shadow:0 0 0 0 rgba(239,68,68,.5); }
    50% { opacity:.8; box-shadow:0 0 0 5px rgba(239,68,68,0); }
}

.sec-head {
    display:flex;
    align-items:center;
    gap:10px;
    margin:28px 0 14px;
    padding-bottom:8px;
    border-bottom:1px solid var(--border);
}

.sec-head-icon {
    width:24px;
    height:24px;
    background:var(--accent-dim);
    border:1px solid var(--border);
    border-radius:5px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:11px;
}

.sec-head-label {
    font-family:var(--font-mono);
    font-size:11px;
    font-weight:600;
    letter-spacing:2px;
    text-transform:uppercase;
}

.m-card,
.m-card-wide,
.step-card,
.stat-card {
    background:var(--bg-card);
    border:1px solid var(--border-soft);
    border-radius:10px;
}

.m-card { padding:16px 18px; margin:8px 0; }
.m-card-wide { padding:18px 20px; margin:8px 0; }

.term-block {
    background:#030608;
    border:1px solid rgba(0,212,170,.12);
    border-radius:10px;
    padding:20px;
    font-family:var(--font-mono);
    font-size:12px;
    line-height:1.7;
    color:var(--accent);
    margin:12px 0;
}

.fake-browser {
    width:100%;
    max-width:100%;
    box-sizing:border-box;
    border-radius:12px;
    overflow:hidden;
    border:1px solid rgba(255,255,255,.08);
    box-shadow:0 20px 60px rgba(0,0,0,.5);
    margin:16px 0;
}

.fake-browser-bar {
    width:100%;
    min-width:0;
    box-sizing:border-box;
    background:#1a1f2e;
    padding:10px 12px;
    display:flex;
    align-items:center;
    gap:10px;
    border-bottom:1px solid rgba(255,255,255,.06);
}

.fake-dots {
    display:flex;
    gap:6px;
    flex-shrink:0;
}

.dot {
    width:12px;
    height:12px;
    border-radius:50%;
}

.dot-r { background:#ff5f57; }
.dot-y { background:#febc2e; }
.dot-g { background:#28c840; }

.fake-url-bar {
    min-width:0;
    flex:1;
    overflow:hidden;
    background:#0d1117;
    border:1px solid rgba(255,255,255,.08);
    border-radius:6px;
    padding:5px 10px;
    font-family:var(--font-mono);
    font-size:11px;
    color:#8899aa;
    display:flex;
    align-items:center;
    gap:6px;
}

.fake-url-text,
.fake-url-host {
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}

.fake-url-host {
    color:#f0f4f8;
    font-weight:600;
}

.fake-browser-content {
    width:100%;
    max-width:100%;
    box-sizing:border-box;
    background:#0d1117;
    padding:24px 28px;
    overflow:hidden;
}

.chat-wrap {
    display:flex;
    flex-direction:column;
    gap:12px;
    margin:16px 0;
}

.chat-bubble-left,
.chat-bubble-right {
    display:flex;
    gap:10px;
    align-items:flex-start;
    max-width:85%;
}

.chat-bubble-right {
    align-self:flex-end;
    flex-direction:row-reverse;
}

.chat-avatar {
    width:32px;
    height:32px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    flex-shrink:0;
}

.avatar-support { background:linear-gradient(135deg,#0ea5e9,#0369a1); }
.avatar-user { background:linear-gradient(135deg,#374151,#1f2937); }

.chat-content-left,
.chat-content-right {
    padding:12px 16px;
    font-size:13px;
    line-height:1.7;
}

.chat-content-left {
    background:#111820;
    border:1px solid var(--border-soft);
    border-radius:0 10px 10px 10px;
    color:#b0bec5;
}

.chat-content-right {
    background:#1a2535;
    border:1px solid rgba(14,165,233,.2);
    border-radius:10px 0 10px 10px;
    color:#f0f4f8;
}

.chat-name {
    font-family:var(--font-mono);
    font-size:10px;
    color:var(--text-mid);
    letter-spacing:1px;
    margin-bottom:4px;
}

.chat-typing {
    display:flex;
    gap:4px;
    align-items:center;
    padding:10px 16px;
    background:#111820;
    border:1px solid var(--border-soft);
    border-radius:0 10px 10px 10px;
    width:70px;
}

.typing-dot {
    width:6px;
    height:6px;
    border-radius:50%;
    background:#8899aa;
    animation:typing 1.2s infinite;
}

.typing-dot:nth-child(2) { animation-delay:.2s; }
.typing-dot:nth-child(3) { animation-delay:.4s; }

@keyframes typing {
    0%,100% { opacity:.3; transform:translateY(0); }
    50% { opacity:1; transform:translateY(-3px); }
}

.d-card,
.s-card,
.w-card,
.abs-rule {
    border-radius:10px;
    padding:20px 22px;
    margin:14px 0;
}

.d-card {
    background:rgba(239,68,68,.07);
    border:1px solid rgba(239,68,68,.35);
}

.s-card {
    background:rgba(34,197,94,.07);
    border:1px solid rgba(34,197,94,.3);
}

.w-card {
    background:rgba(245,158,11,.06);
    border:1px solid rgba(245,158,11,.28);
}

.d-card-title,
.s-card-title,
.w-card-title {
    font-family:var(--font-mono);
    font-weight:700;
    letter-spacing:1px;
}

.d-card-title { color:var(--red); }
.s-card-title { color:var(--green); }
.w-card-title { color:var(--yellow); }

.progress-bar-wrap { margin:16px 0 24px; }
.progress-bar-track {
    height:3px;
    background:var(--border-soft);
    border-radius:2px;
}
.progress-bar-fill {
    height:3px;
    background:var(--red);
    border-radius:2px;
    box-shadow:0 0 8px rgba(239,68,68,.5);
}
.progress-label {
    font-family:var(--font-mono);
    font-size:10px;
    color:var(--text-lo);
    letter-spacing:1px;
    margin-top:6px;
    text-align:right;
}

.rule-item {
    display:flex;
    align-items:flex-start;
    gap:12px;
    padding:16px 0;
    border-bottom:1px solid var(--border-soft);
    font-size:13px;
    color:#b0bec5;
    line-height:1.6;
}

.rule-num {
    min-width:28px;
    height:28px;
    border-radius:6px;
    background:rgba(239,68,68,.1);
    border:1px solid rgba(239,68,68,.25);
    display:flex;
    align-items:center;
    justify-content:center;
    font-family:var(--font-mono);
    font-size:11px;
    font-weight:700;
    color:var(--red);
}

.stat-card {
    padding:20px;
    text-align:center;
    margin-bottom:10px;
}

.stat-num {
    font-family:var(--font-mono);
    font-size:30px;
    font-weight:700;
}

.stat-lbl {
    font-family:var(--font-mono);
    font-size:10px;
    color:var(--text-mid);
    letter-spacing:1.5px;
    text-transform:uppercase;
    margin-top:8px;
}

.stButton > button {
    background:var(--red) !important;
    color:#fff !important;
    border:none !important;
    border-radius:8px !important;
    font-family:var(--font-mono) !important;
    font-size:12px !important;
    font-weight:700 !important;
    letter-spacing:1px !important;
    padding:12px 20px !important;
    text-transform:uppercase !important;
    width:100% !important;
}

.btn-success > button {
    background:transparent !important;
    color:var(--green) !important;
    border:1px solid rgba(34,197,94,.4) !important;
}

.btn-neutral > button {
    background:#1a2535 !important;
    color:#8899aa !important;
    border:1px solid var(--border-soft) !important;
}

.btn-accent > button {
    background:var(--accent) !important;
    color:#030a07 !important;
}

.v2-divider {
    height:1px;
    background:linear-gradient(90deg,var(--border),transparent);
    margin:28px 0;
}

@media (max-width:600px) {
    .block-container {
        padding-left:12px !important;
        padding-right:12px !important;
    }

    .nav-bar {
        padding:0 12px;
    }

    .fake-browser-content {
        padding:18px 14px;
    }

    .fake-browser-bar {
        padding:8px;
    }

    .fake-url-bar {
        font-size:9px;
    }

    .dot {
        width:8px;
        height:8px;
    }

    .chat-bubble-left,
    .chat-bubble-right {
        max-width:95%;
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
# SESSION STATE
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
    st.session_state.participant_registered = True
    increment_stat("participants")

# =========================================================
# SEED FAILURE CALLBACK
# =========================================================
if "seed_fail" in st.query_params:

    if not st.session_state.seed_fail_registered:
        increment_stat("seed_attempts")
        st.session_state.seed_fail_registered = True

    st.query_params.clear()
    st.session_state.outcome = "fail"
    st.session_state.step = 99
    st.rerun()

# =========================================================
# HELPERS
# =========================================================
def reset_app():
    st.session_state.step = 0
    st.session_state.completed = False
    st.session_state.outcome = None
    st.session_state.safe_exit_registered = False
    st.session_state.seed_fail_registered = False
    st.session_state.chat_step = 0
    st.rerun()

def sec(icon, label, color="var(--accent)"):
    st.markdown(
        f"""
        <div class="sec-head">
            <div class="sec-head-icon" style="color:{color};">{icon}</div>
            <div class="sec-head-label" style="color:{color};">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def progress_bar(step, total=5):
    pct = min(step / total * 100, 100)
    st.markdown(
        f"""
        <div class="progress-bar-wrap">
            <div class="progress-bar-track">
                <div class="progress-bar-fill" style="width:{pct:.0f}%;"></div>
            </div>
            <div class="progress-label">ÉTAPE {step} / {total}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# PEDAGOGY
# =========================================================
def show_pedagogy(outcome):
    stats = get_statistics()

    if outcome == "fail":
        st.markdown("""
        <div class="d-card" style="text-align:center;padding:36px;">
            <div style="font-size:48px;">💀</div>
            <div class="d-card-title" style="font-size:22px;text-align:center;">
                VOUS AVEZ ÉTÉ SCAMMÉ
            </div>
            <div style="font-size:14px;color:#b0bec5;line-height:1.8;margin-top:12px;">
                Vous avez tenté de saisir votre phrase de récupération.<br>
                <span style="color:#ef4444;font-weight:600;">
                    Dans une situation réelle, votre wallet pourrait être compromis immédiatement.
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="s-card" style="text-align:center;padding:36px;">
            <div style="font-size:48px;">🛡️</div>
            <div class="s-card-title" style="font-size:22px;text-align:center;">
                VOUS AVEZ RÉSISTÉ
            </div>
            <div style="font-size:14px;color:#b0bec5;line-height:1.8;margin-top:12px;">
                Vous avez refusé de communiquer votre phrase de récupération.<br>
                <span style="color:#22c55e;font-weight:600;">
                    C'est la seule décision correcte.
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    sec("◈", "Ce qui vient de se passer", "#ef4444")

    st.markdown("""
    <div class="m-card-wide">
        <div style="font-size:13px;color:#b0bec5;line-height:2;">
            Vous venez de traverser une simulation de
            <b style="color:#f0f4f8;">phishing DeFi</b>.<br><br>
            <span style="color:#ef4444;">1.</span> Fausse alerte de sécurité<br>
            <span style="color:#ef4444;">2.</span> Fausse connexion wallet<br>
            <span style="color:#ef4444;">3.</span> Faux support<br>
            <span style="color:#ef4444;">4.</span> Demande de signature<br>
            <span style="color:#ef4444;">5.</span> Pression d'urgence<br>
            <span style="color:#ef4444;">6.</span> Demande de seed phrase
        </div>
    </div>
    """, unsafe_allow_html=True)

    sec("🛡", "Les règles à ne jamais oublier", "#22c55e")

    rules = [
        (
            "Votre seed phrase = votre wallet",
            "Quiconque possède votre seed phrase possède votre wallet. Aucun support légitime n'a besoin de la connaître."
        ),
        (
            "L'urgence est une arme",
            "Les scammers créent une pression artificielle pour vous empêcher de réfléchir."
        ),
        (
            "Un support légitime ne demande jamais votre seed",
            "Ne communiquez jamais votre phrase de récupération, même à une personne prétendant être un employé officiel."
        ),
        (
            "Vérifiez toujours l'URL",
            "Un faux domaine peut ressembler presque parfaitement au vrai."
        ),
        (
            "Une signature peut être dangereuse",
            "Lisez toujours ce que vous signez et vérifiez les autorisations accordées."
        ),
        (
            "Formez-vous avant de manipuler des fonds",
            "Un scammer ne vous donnera pas une seconde chance avec votre argent."
        ),
    ]

    for i, (title, description) in enumerate(rules, 1):
        st.markdown(
            f"""
            <div class="rule-item">
                <div class="rule-num">{i}</div>
                <div>
                    <b style="color:#f0f4f8;">{title}</b><br>
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    sec("◉", "Statistiques globales")

    st.markdown("""
    <div class="m-card-wide">
        <div style="font-size:12px;color:var(--text-mid);line-height:1.7;">
            Ces chiffres sont collectés de manière
            <b style="color:#f0f4f8;">100% anonyme</b>.<br>
            Aucune donnée personnelle et aucune seed phrase ne sont stockées.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    metrics = [
        ("PARTICIPANTS", stats["participants"], "var(--accent)"),
        ("ONT REFUSÉ LA SEED", stats["safe_exits"], "#22c55e"),
        ("ONT CONNECTÉ LEUR WALLET", stats["wallet_connections"], "#f59e0b"),
        ("ONT SIGNÉ", stats["signature_attempts"], "#f59e0b"),
        ("ONT CONTINUÉ SOUS PRESSION", stats["urgency_continues"], "#ef4444"),
        ("ONT TENTÉ LA SEED", stats["seed_attempts"], "#ef4444"),
    ]

    for i, (label, value, color) in enumerate(metrics):
        with c1 if i % 2 == 0 else c2:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-num" style="color:{color};">
                        {value:,}
                    </div>
                    <div class="stat-lbl">{label}</div>
                </div>
                """.replace(",", "\u202f"),
                unsafe_allow_html=True,
            )

    if stats["participants"] > 0:
        percentage = stats["seed_attempts"] / stats["participants"] * 100

        st.markdown(
            f"""
            <div class="d-card" style="text-align:center;">
                <div class="d-card-title">
                    🚨 STATISTIQUE QUI DOIT VOUS MARQUER
                </div>
                <div style="
                    font-family:var(--font-mono);
                    font-size:42px;
                    font-weight:700;
                    color:#ef4444;
                    margin:14px 0;
                ">
                    {percentage:.1f}%
                </div>
                <div style="font-size:13px;color:#b0bec5;line-height:1.8;">
                    des participants ont tenté de saisir leur seed phrase.<br>
                    <span style="color:#f0f4f8;font-weight:600;">
                        Un vrai scammer ne les aurait pas arrêtés.
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='v2-divider'></div>", unsafe_allow_html=True)

    st.markdown('<div class="btn-accent">', unsafe_allow_html=True)
    if st.button("◈ RECOMMENCER LA SIMULATION"):
        reset_app()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
        text-align:center;
        font-family:var(--font-mono);
        font-size:10px;
        color:var(--text-lo);
        letter-spacing:1px;
        border-top:1px solid var(--border-soft);
        padding-top:20px;
        margin-top:40px;
    ">
        ◈ KBOUR CRYPTO · WALLET SECURITY AWARENESS
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# ROUTING
# =========================================================
if st.session_state.step == 99 or st.session_state.outcome == "fail":
    show_pedagogy("fail")
    st.stop()

if st.session_state.completed:
    show_pedagogy("success")
    st.stop()

# =========================================================
# STEP 0 — FAUSSE ALERTE
# =========================================================
if st.session_state.step == 0:

    st.markdown("""
    <div class="fake-browser">
        <div class="fake-browser-bar">
            <div class="fake-dots">
                <div class="dot dot-r"></div>
                <div class="dot dot-y"></div>
                <div class="dot dot-g"></div>
            </div>
            <div class="fake-url-bar">
                <span>🔒</span>
                <span class="fake-url-text">https://</span>
                <span class="fake-url-host">
                    uniswap-security.protocol-verify.com
                </span>
            </div>
        </div>

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
                ">🦄</div>

                <div>
                    <div style="
                        font-family:var(--font-mono);
                        font-size:14px;
                        font-weight:700;
                        color:#f0f4f8;
                    ">
                        Uniswap Protocol
                    </div>
                    <div style="
                        font-family:var(--font-mono);
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
                    font-family:var(--font-mono);
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
                    on your wallet address.<br>
                    Your funds may be at risk.
                </div>
            </div>

            <div style="
                font-size:12px;
                color:#8899aa;
                line-height:1.6;
            ">
                This alert was triggered by our Smart Contract Security Monitor v4.2.<br>
                Reference:
                <span style="
                    color:#00d4aa;
                    font-family:var(--font-mono);
                ">
                    SC-2024-A39F2
                </span>
            </div>

        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔍 VÉRIFIER MON WALLET"):
        st.session_state.step = 1
        st.rerun()

# =========================================================
# STEP 1 — CONNEXION
# =========================================================
elif st.session_state.step == 1:

    progress_bar(1)

    st.markdown("""
    <div class="fake-browser">
        <div class="fake-browser-bar">
            <div class="fake-dots">
                <div class="dot dot-r"></div>
                <div class="dot dot-y"></div>
                <div class="dot dot-g"></div>
            </div>

            <div class="fake-url-bar">
                <span>🔒</span>
                <span class="fake-url-text">https://</span>
                <span class="fake-url-host">
                    uniswap-security.protocol-verify.com
                </span>
                <span style="color:#8899aa;">
                    /wallet/connect
                </span>
            </div>
        </div>

        <div class="fake-browser-content">

            <div style="
                font-family:var(--font-mono);
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
                    border:1px solid rgba(14,165,233,.2);
                    border-radius:8px;
                    padding:14px 16px;
                    display:flex;
                    align-items:center;
                    gap:12px;
                ">
                    <div style="font-size:22px;">🐇</div>
                    <div>
                        <div style="
                            font-family:var(--font-mono);
                            font-size:12px;
                            font-weight:600;
                            color:#f0f4f8;
                        ">
                            RABBY WALLET
                        </div>
                        <div style="
                            font-family:var(--font-mono);
                            font-size:10px;
                            color:#8899aa;
                        ">
                            Browser Extension
                        </div>
                    </div>
                </div>

                <div style="
                    background:#1a2535;
                    border:1px solid var(--border-soft);
                    border-radius:8px;
                    padding:14px 16px;
                    display:flex;
                    align-items:center;
                    gap:12px;
                ">
                    <div style="font-size:22px;">🔵</div>
                    <div>
                        <div style="
                            font-family:var(--font-mono);
                            font-size:12px;
                            font-weight:600;
                            color:#f0f4f8;
                        ">
                            Coinbase Wallet
                        </div>
                        <div style="
                            font-family:var(--font-mono);
                            font-size:10px;
                            color:#8899aa;
                        ">
                            Mobile & Extension
                        </div>
                    </div>
                </div>

                <div style="
                    background:#1a2535;
                    border:1px solid var(--border-soft);
                    border-radius:8px;
                    padding:14px 16px;
                    display:flex;
                    align-items:center;
                    gap:12px;
                ">
                    <div style="font-size:22px;">◈</div>
                    <div>
                        <div style="
                            font-family:var(--font-mono);
                            font-size:12px;
                            font-weight:600;
                            color:#f0f4f8;
                        ">
                            WalletConnect
                        </div>
                        <div style="
                            font-family:var(--font-mono);
                            font-size:10px;
                            color:#8899aa;
                        ">
                            All wallets via QR code
                        </div>
                    </div>
                </div>

            </div>

        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🐇 CONNECTER RABBY WALLET"):
        increment_stat("wallet_connections")
        st.session_state.step = 2
        st.rerun()

# =========================================================
# STEP 2 — SUPPORT
# =========================================================
elif st.session_state.step == 2:

    progress_bar(2)

    chat_step = st.session_state.chat_step

    st.markdown("""
    <div class="fake-browser">
        <div class="fake-browser-bar">
            <div class="fake-dots">
                <div class="dot dot-r"></div>
                <div class="dot dot-y"></div>
                <div class="dot dot-g"></div>
            </div>

            <div class="fake-url-bar">
                <span>🔒</span>
                <span class="fake-url-text">https://</span>
                <span class="fake-url-host">
                    uniswap-security.protocol-verify.com
                </span>
                <span style="color:#8899aa;">
                    /support/live
                </span>
            </div>
        </div>

        <div class="fake-browser-content">

            <div style="
                display:flex;
                align-items:center;
                gap:10px;
                padding-bottom:14px;
                border-bottom:1px solid rgba(255,255,255,.06);
            ">
                <div class="chat-avatar avatar-support">👤</div>
                <div>
                    <div style="
                        font-family:var(--font-mono);
                        font-size:12px;
                        font-weight:600;
                        color:#f0f4f8;
                    ">
                        Alex — Uniswap Security Team
                    </div>
                    <div style="
                        font-family:var(--font-mono);
                        font-size:10px;
                        color:#22c55e;
                    ">
                        ● Online
                    </div>
                </div>
            </div>
    """, unsafe_allow_html=True)

    messages = [
        "Hi, I'm Alex from Uniswap's Security Team. I've been assigned to your case. We detected unauthorized access attempts on your wallet. Don't worry — I'm here to help you secure your funds.",
        "I can see your wallet is connected. Our system shows your liquidity positions are at risk. We need to run a verification protocol to protect your assets.",
        "This is urgent. We have a limited window to secure your wallet before the unauthorized transaction goes through. Please follow my instructions carefully.",
    ]

    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)

    for i in range(min(chat_step + 1, len(messages))):

        st.markdown(
            f"""
            <div class="chat-bubble-left">
                <div class="chat-avatar avatar-support">👤</div>
                <div>
                    <div class="chat-name">
                        Alex · Uniswap Security
                    </div>
                    <div class="chat-content-left">
                        {messages[i]}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if i == 0 and chat_step >= 1:
            st.markdown("""
            <div class="chat-bubble-right">
                <div class="chat-avatar avatar-user">MOI</div>
                <div>
                    <div class="chat-name">Moi</div>
                    <div class="chat-content-right">
                        Ok, qu'est-ce que je dois faire ?
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if i == 1 and chat_step >= 2:
            st.markdown("""
            <div class="chat-bubble-right">
                <div class="chat-avatar avatar-user">MOI</div>
                <div>
                    <div class="chat-name">Moi</div>
                    <div class="chat-content-right">
                        Mes positions sont vraiment en danger ?
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div></div></div>", unsafe_allow_html=True)

    if chat_step < len(messages) - 1:

        c1, c2 = st.columns(2)

        with c1:
            if st.button("▶ RÉPONDRE AU SUPPORT"):
                st.session_state.chat_step += 1
                st.rerun()

        with c2:
            st.markdown('<div class="btn-neutral">', unsafe_allow_html=True)
            if st.button("⟳ ATTENDRE LA RÉPONSE"):
                st.session_state.chat_step += 1
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    else:

        if st.button("▶ POURSUIVRE LA PROCÉDURE"):
            increment_stat("signature_attempts")
            st.session_state.step = 3
            st.rerun()

# =========================================================
# STEP 3 — SIGNATURE
# =========================================================
elif st.session_state.step == 3:

    progress_bar(3)

    st.markdown("""
    <div class="fake-browser">
        <div class="fake-browser-bar">
            <div class="fake-dots">
                <div class="dot dot-r"></div>
                <div class="dot dot-y"></div>
                <div class="dot dot-g"></div>
            </div>

            <div class="fake-url-bar">
                <span>🔒</span>
                <span class="fake-url-text">https://</span>
                <span class="fake-url-host">
                    uniswap-security.protocol-verify.com
                </span>
                <span style="color:#8899aa;">
                    /auth/sign
                </span>
            </div>
        </div>

        <div class="fake-browser-content">

            <div style="
                font-family:var(--font-mono);
                font-size:12px;
                color:#8899aa;
                margin-bottom:16px;
            ">
                RABBY WALLET · SIGNATURE REQUEST
            </div>

            <div style="
                background:#0d1117;
                border:1px solid rgba(255,255,255,.08);
                border-radius:8px;
                padding:16px;
            ">
                <div style="
                    font-family:var(--font-mono);
                    font-size:10px;
                    color:#8899aa;
                    margin-bottom:8px;
                ">
                    MESSAGE
                </div>

                <div style="
                    font-family:var(--font-mono);
                    font-size:11px;
                    color:#b0bec5;
                    line-height:1.7;
                    word-break:break-word;
                ">
                    Uniswap Security Protocol v4.2<br>
                    Action: wallet_verification<br>
                    Timestamp: 1735123456<br>
                    Nonce: 0x7f3a9b2c<br>
                    <span style="color:#ef4444;">
                        setApprovalForAll(...)
                    </span>
                </div>
            </div>

            <div style="
                background:rgba(245,158,11,.07);
                border:1px solid rgba(245,158,11,.25);
                border-radius:6px;
                padding:10px 14px;
                margin-top:16px;
                font-family:var(--font-mono);
                font-size:11px;
                color:#f59e0b;
            ">
                ⚠ This action requires your authorization
            </div>

        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✅ SIGNER ET CONTINUER"):
        increment_stat("urgency_continues")
        st.session_state.step = 4
        st.rerun()

# =========================================================
# STEP 4 — URGENCE
# =========================================================
elif st.session_state.step == 4:

    progress_bar(4)

    st.markdown("""
    <div class="fake-browser">
        <div class="fake-browser-bar">
            <div class="fake-dots">
                <div class="dot dot-r"></div>
                <div class="dot dot-y"></div>
                <div class="dot dot-g"></div>
            </div>

            <div class="fake-url-bar">
                <span>🔒</span>
                <span class="fake-url-text">https://</span>
                <span class="fake-url-host">
                    uniswap-security.protocol-verify.com
                </span>
                <span style="color:#8899aa;">
                    /recovery/urgent
                </span>
            </div>
        </div>

        <div class="fake-browser-content">

            <div style="
                background:rgba(239,68,68,.08);
                border:1px solid rgba(239,68,68,.35);
                border-radius:8px;
                padding:20px;
                text-align:center;
            ">
                <div style="font-size:32px;">🚨</div>

                <div style="
                    font-family:var(--font-mono);
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
                    Our system could not complete the automatic wallet recovery.<br>
                    <b style="color:#f0f4f8;">
                        Manual verification is now required.
                    </b>
                </div>

                <div style="
                    font-family:var(--font-mono);
                    font-size:22px;
                    font-weight:700;
                    color:#ef4444;
                    margin-top:16px;
                ">
                    11:47
                </div>
            </div>

            <div style="
                background:#111820;
                border:1px solid var(--border-soft);
                border-radius:8px;
                padding:16px;
                margin-top:16px;
                font-size:13px;
                color:#b0bec5;
                line-height:1.7;
            ">
                <b style="color:#f0f4f8;">
                    Alex · Uniswap Security
                </b><br><br>
                The automatic protocol failed. We need to do the manual recovery now.
                Follow the next step to complete the process.
            </div>

        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔐 PROCÉDER À LA RÉCUPÉRATION MANUELLE"):
        st.session_state.step = 5
        st.rerun()

# =========================================================
# STEP 5 — SEED
# =========================================================
elif st.session_state.step == 5:

    progress_bar(5)

    st.markdown("""
    <div class="fake-browser">
        <div class="fake-browser-bar">
            <div class="fake-dots">
                <div class="dot dot-r"></div>
                <div class="dot dot-y"></div>
                <div class="dot dot-g"></div>
            </div>

            <div class="fake-url-bar">
                <span>🔒</span>
                <span class="fake-url-text">https://</span>
                <span class="fake-url-host">
                    uniswap-security.protocol-verify.com
                </span>
                <span style="color:#8899aa;">
                    /recovery/manual
                </span>
            </div>
        </div>

        <div class="fake-browser-content">

            <div style="
                display:flex;
                align-items:center;
                gap:12px;
                margin-bottom:20px;
            ">
                <div class="chat-avatar avatar-support">👤</div>

                <div>
                    <div style="
                        font-family:var(--font-mono);
                        font-size:12px;
                        font-weight:600;
                        color:#f0f4f8;
                    ">
                        Alex — Uniswap Security Team
                    </div>

                    <div style="
                        font-family:var(--font-mono);
                        font-size:10px;
                        color:#22c55e;
                    ">
                        ● Online
                    </div>
                </div>
            </div>

            <div class="chat-content-left" style="
                background:#0d1117;
                margin-bottom:16px;
            ">
                "To complete the manual recovery, enter your Secret Recovery Phrase below."
            </div>

            <div style="
                background:#080c10;
                border:1px solid rgba(239,68,68,.2);
                border-radius:8px;
                padding:16px;
            ">

                <div style="
                    font-family:var(--font-mono);
                    font-size:10px;
                    color:#8899aa;
                    letter-spacing:1.5px;
                    text-transform:uppercase;
                    margin-bottom:10px;
                ">
                    SECRET RECOVERY PHRASE
                </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # IMPORTANT:
    # Le champ est isolé dans une iframe.
    # Rien n'est envoyé à Streamlit.
    # Dès le 3e mot, le champ est vidé et bloqué.
    # =====================================================
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * {
            box-sizing:border-box;
            margin:0;
            padding:0;
        }

        html, body {
            width:100%;
            min-width:0;
            background:#080c10;
            overflow:hidden;
        }

        textarea {
            width:100%;
            height:110px;
            resize:none;
            padding:14px;
            background:#030608;
            color:#00d4aa;
            border:1px solid rgba(239,68,68,.3);
            border-radius:8px;
            font-family:'Courier New',monospace;
            font-size:14px;
            outline:none;
            display:block;
        }

        textarea::placeholder {
            color:#445566;
        }

        .blocked {
            width:100%;
            min-height:110px;
            background:rgba(239,68,68,.07);
            border:1px solid rgba(239,68,68,.35);
            border-radius:8px;
            padding:18px;
            color:#ef4444;
            font-family:'Courier New',monospace;
            font-size:12px;
            line-height:1.8;
        }
    </style>
    </head>

    <body>

    <textarea
        id="seed"
        placeholder="Enter your 12 or 24-word secret recovery phrase..."
        autocomplete="off"
        autocorrect="off"
        autocapitalize="off"
        spellcheck="false">
    </textarea>

    <script>
    const field = document.getElementById("seed");

    field.addEventListener("input", function () {

        const words = this.value
            .trim()
            .split(/\\s+/)
            .filter(Boolean);

        if (words.length >= 3) {

            this.value = "";
            this.disabled = true;

            document.body.innerHTML = `
                <div class="blocked">
                    🚨 TENTATIVE DÉTECTÉE — PROCÉDURE INTERROMPUE
                    <br><br>
                    <span style="color:#f0f4f8;">
                        Vous avez tenté de saisir une phrase de récupération.
                        <br>
                        Dans une situation réelle, votre wallet pourrait être compromis.
                        <br><br>
                    </span>
                    <span style="font-weight:700;">
                        UNE SEED PHRASE NE SE SAISIT JAMAIS EN LIGNE.
                    </span>
                </div>
            `;

            setTimeout(function () {
                window.top.location.href =
                    window.top.location.href.split("?")[0] +
                    "?seed_fail=1";
            }, 1800);
        }
    });
    </script>

    </body>
    </html>
    """, height=150, scrolling=False)

    st.markdown("""
            </div>

            <div style="
                font-family:var(--font-mono);
                font-size:10px;
                color:#8899aa;
                margin-top:10px;
                line-height:1.6;
            ">
                🔒 This field is monitored for security awareness purposes.
            </div>

        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown('<div class="btn-success">', unsafe_allow_html=True)

        if st.button("🛡️ NON — JE REFUSE DE DONNER MA SEED PHRASE"):

            if not st.session_state.safe_exit_registered:
                increment_stat("safe_exits")
                st.session_state.safe_exit_registered = True

            st.session_state.completed = True
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style="
            font-family:var(--font-mono);
            font-size:10px;
            color:var(--text-lo);
            text-align:center;
            padding:14px 0;
        ">
            ← SEULE BONNE DÉCISION
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div style="
    height:40px;
"></div>

<div style="
    text-align:center;
    font-family:var(--font-mono);
    font-size:10px;
    color:var(--text-lo);
    letter-spacing:1px;
    padding-top:16px;
">
    ◈ WALLET RECOVERY · SESSION LOCKED · WARNING AUTO ALERT
</div>
""", unsafe_allow_html=True)
