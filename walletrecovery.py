import streamlit as st
import re


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="KBOUR CRYPTO // SECURITY",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Share Tech Mono', monospace;
}

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(0, 255, 136, 0.06),
            transparent 35%
        ),
        #080c11;
}

h1, h2, h3, h4 {
    color: #00ff88 !important;
}

p, li, label {
    color: #d1f7df !important;
}

/* HEADER */

.header {
    border: 1px solid #00ff88;
    border-radius: 10px;
    padding: 25px;
    margin-bottom: 25px;
    background: rgba(0, 255, 136, 0.04);
    box-shadow: 0 0 25px rgba(0, 255, 136, 0.08);
}

.header-title {
    color: #00ff88;
    font-size: 32px;
    font-weight: bold;
    text-shadow: 0 0 10px rgba(0,255,136,0.6);
}

.header-subtitle {
    color: #8cae9a;
    margin-top: 8px;
}

/* TERMINAL */

.terminal {
    background: #020504;
    border: 1px solid #1d4935;
    border-radius: 8px;
    padding: 20px;
    color: #00ff88;
    line-height: 1.8;
    font-family: monospace;
    margin: 20px 0;
}

/* CARDS */

.card {
    border: 1px solid #263a32;
    border-radius: 10px;
    padding: 22px;
    background: rgba(10, 20, 18, 0.8);
    margin: 15px 0;
}

/* WARNING */

.warning-box {
    border: 1px solid #ffcc00;
    border-radius: 10px;
    padding: 22px;
    background: rgba(255, 204, 0, 0.06);
    margin: 20px 0;
}

/* DANGER */

.danger-box {
    border: 1px solid #ff3333;
    border-radius: 10px;
    padding: 25px;
    background: rgba(255, 0, 0, 0.08);
    margin: 20px 0;
    box-shadow: 0 0 25px rgba(255, 0, 0, 0.08);
}

.danger-title {
    color: #ff4444;
    font-size: 27px;
    font-weight: bold;
}

/* SUCCESS */

.success-box {
    border: 1px solid #00ff88;
    border-radius: 10px;
    padding: 25px;
    background: rgba(0, 255, 136, 0.07);
    margin: 20px 0;
}

/* BUTTONS */

.stButton > button {
    width: 100%;
    min-height: 48px;
    background: rgba(0, 255, 136, 0.04);
    color: #00ff88;
    border: 1px solid #00ff88;
    font-family: 'Share Tech Mono', monospace;
    font-weight: bold;
    transition: 0.2s;
}

.stButton > button:hover {
    background: rgba(0, 255, 136, 0.15);
    color: white;
    border-color: white;
    box-shadow: 0 0 15px rgba(0,255,136,0.35);
}

/* INPUTS */

textarea,
input {
    background-color: #0b120e !important;
    color: #00ff88 !important;
    border: 1px solid #315c44 !important;
}

/* FOOTER */

.footer {
    text-align: center;
    margin-top: 50px;
    padding: 20px;
    color: #4f6c59;
    border-top: 1px solid #1b3026;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "step" not in st.session_state:
    st.session_state.step = 0

if "failed" not in st.session_state:
    st.session_state.failed = False

if "completed" not in st.session_state:
    st.session_state.completed = False

if "seed_attempt" not in st.session_state:
    st.session_state.seed_attempt = False


# ============================================================
# FONCTIONS
# ============================================================

def reset_application():

    st.session_state.step = 0
    st.session_state.failed = False
    st.session_state.completed = False
    st.session_state.seed_attempt = False

    st.rerun()


def contains_seed_length(text):

    """
    Détecte uniquement le nombre de mots saisis.

    Aucune seed n'est validée.
    Aucun mot n'est conservé.
    Le texte n'est jamais stocké.
    """

    if not text:
        return False

    words = re.findall(
        r"\b[a-zA-ZÀ-ÿ]+\b",
        text.strip()
    )

    return len(words) in [12, 15, 18, 21, 24]


def terminal(lines):

    output = ""

    for line in lines:
        output += f"> {line}<br>"

    st.markdown(
        f"""
        <div class="terminal">
        {output}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="header">

<div class="header-title">
🛡️ KBOUR CRYPTO // WALLET SECURITY
</div>

<div class="header-subtitle">
SECURITY AWARENESS PROTOCOL // VERIFY EVERYTHING
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# ÉCHEC IMMÉDIAT
# ============================================================

if st.session_state.failed:

    st.markdown("""
    <div class="danger-box">

    <div class="danger-title">
    🚨 VOUS AVEZ ÉCHOUÉ
    </div>

    <br>

    VOTRE PHRASE DE RÉCUPÉRATION NE DOIT JAMAIS ÊTRE SAISIE ICI.

    </div>
    """, unsafe_allow_html=True)

    st.error(
        "La procédure a été interrompue immédiatement."
    )

    st.markdown("""
    ## 💀 Ce qui aurait pu se passer dans le monde réel

    Si cette phrase avait été votre véritable seed phrase :

    - vos cryptomonnaies auraient pu être transférées ;
    - vos tokens auraient pu être vendus ;
    - vos NFTs auraient pu être volés ;
    - vos autorisations auraient pu être exploitées ;
    - vos fonds auraient pu être définitivement perdus.

    **Un scammer ne vous préviendra pas avant de vider votre wallet.**
    """)

    st.markdown("""
    <div class="warning-box">

    ### ⚠️ RÈGLE ABSOLUE

    <strong>
    Une seed phrase ne se saisit jamais dans un site web,
    une application, un formulaire, un chat ou un support.
    </strong>

    <br><br>

    Si quelqu'un vous demande votre seed phrase :

    <br>

    🛑 ARRÊTEZ-VOUS<br>
    🚫 NE LA DONNEZ PAS<br>
    ❌ FERMEZ LA PAGE<br>
    🔒 CONSIDÉREZ LA DEMANDE COMME FRAUDULEUSE

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ## 🎓 Vous devez vous former avant d'exposer votre capital

    Dans la crypto, une erreur peut être irréversible.

    Les scammers, eux, connaissent parfaitement les erreurs
    qu'ils cherchent à provoquer.

    **Ne mettez jamais de capital en jeu avec des connaissances
    insuffisantes en sécurité.**
    """)

    if st.button("🔄 RECOMMENCER"):

        reset_application()

    st.stop()


# ============================================================
# SUCCÈS FINAL
# ============================================================

if st.session_state.completed:

    st.markdown("""
    <div class="success-box">

    <h2>🛡️ VOUS AVEZ RÉUSSI</h2>

    <br>

    Vous avez identifié les différentes étapes
    d'une attaque classique visant un utilisateur crypto.

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ## 🔐 Les règles à retenir

    ### 1️⃣ Votre seed phrase est secrète

    Elle ne doit jamais être communiquée.

    ### 2️⃣ Un support ne demande jamais votre seed

    Ni sur Telegram, ni sur Discord, ni par email,
    ni sur un site.

    ### 3️⃣ Un wallet connecté n'est pas forcément sécurisé

    Vérifiez toujours le site et le contrat.

    ### 4️⃣ Une signature peut être dangereuse

    Ne signez jamais ce que vous ne comprenez pas.

    ### 5️⃣ Les scammers jouent sur l'urgence

    Plus quelqu'un vous pousse à agir vite,
    plus vous devez vous arrêter.

    """)

    st.markdown("""
    <div class="terminal">

    > SECURITY PROTOCOL COMPLETE<br>
    > SEED PHRASE: NEVER SHARE<br>
    > SIGNATURES: VERIFY<br>
    > CONTRACTS: INSPECT<br>
    > URGENCY: SUSPICIOUS<br>
    > CAPITAL: PROTECT IT

    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 RECOMMENCER"):

        reset_application()

    st.stop()


# ============================================================
# ÉTAPE 0 — LE PROBLÈME INITIAL
# ============================================================

if st.session_state.step == 0:

    terminal([
        "WALLET SECURITY MONITOR",
        "STATUS: WARNING",
        "UNUSUAL ACTIVITY DETECTED",
        "ACTION REQUIRED"
    ])

    st.markdown("""
    <div class="warning-box">

    ### ⚠️ ACTIVITÉ INHABITUELLE DÉTECTÉE

    Une activité inhabituelle semble avoir été détectée
    sur votre wallet.

    <br><br>

    Une procédure de vérification est disponible.

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### Que souhaitez-vous faire ?
    """)

    if st.button("🔍 VÉRIFIER MON WALLET"):

        st.session_state.step = 1
        st.rerun()


# ============================================================
# ÉTAPE 1 — FAUX SITE / CONNEXION
# ============================================================

elif st.session_state.step == 1:

    terminal([
        "SECURITY CHECK INITIALIZED",
        "WALLET CONNECTION REQUIRED",
        "CONNECT WALLET TO CONTINUE"
    ])

    st.markdown("""
    <div class="card">

    ### 🔗 WALLET VERIFICATION

    Pour analyser le problème détecté,
    votre wallet doit être connecté.

    <br><br>

    Cette étape permet de vérifier votre adresse
    et l'état de vos actifs.

    </div>
    """, unsafe_allow_html=True)

    st.warning(
        "⚠️ Vérifiez toujours le domaine d'un site avant de connecter votre wallet."
    )

    if st.button("🦊 CONNECTER MON WALLET"):

        st.session_state.step = 2
        st.rerun()


# ============================================================
# ÉTAPE 2 — FAUX SUPPORT
# ============================================================

elif st.session_state.step == 2:

    terminal([
        "WALLET CONNECTED",
        "ADDRESS DETECTED",
        "SUPPORT CHANNEL AVAILABLE"
    ])

    st.markdown("""
    <div class="card">

    ### 💬 SUPPORT TECHNIQUE

    Un agent vous contacte :

    <br><br>

    <em>
    "Hello. We detected an issue with your wallet.
    We can help you recover your assets."
    </em>

    <br><br>

    <em>
    "Please follow the recovery procedure."
    </em>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### Le support vous propose de poursuivre la procédure.
    """)

    if st.button("▶ POURSUIVRE LA PROCÉDURE"):

        st.session_state.step = 3
        st.rerun()


# ============================================================
# ÉTAPE 3 — FAUSSE SIGNATURE
# ============================================================

elif st.session_state.step == 3:

    terminal([
        "RECOVERY MODULE INITIALIZED",
        "AUTHENTICATION REQUIRED",
        "SIGNATURE REQUEST GENERATED"
    ])

    st.markdown("""
    <div class="warning-box">

    ### ✍️ SIGNATURE REQUISE

    Une signature de wallet est nécessaire
    pour confirmer que vous êtes bien le propriétaire
    de l'adresse.

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### Que faites-vous ?
    """)

    choice = st.radio(
        "Sélectionnez une action",
        [
            "Je signe immédiatement.",
            "Je vérifie exactement ce que je signe.",
            "Je ferme la page.",
            "Je demande au support de signer à ma place."
        ]
    )

    if st.button("▶ CONTINUER"):

        if choice in [
            "Je vérifie exactement ce que je signe.",
            "Je ferme la page."
        ]:

            st.session_state.step = 4

        else:

            st.session_state.step = 4

        st.rerun()


# ============================================================
# ÉTAPE 4 — PRESSION / URGENCE
# ============================================================

elif st.session_state.step == 4:

    terminal([
        "AUTHENTICATION FAILED",
        "RECOVERY INCOMPLETE",
        "MANUAL VERIFICATION REQUIRED"
    ])

    st.markdown("""
    <div class="danger-box">

    ### 🚨 ACTION URGENTE REQUISE

    Votre wallet ne peut pas être restauré automatiquement.

    <br><br>

    Le support vous informe :

    <br>

    <em>
    "If you do not complete the recovery now,
    your funds may remain inaccessible."
    </em>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### Le support vous demande maintenant votre phrase de récupération.
    """)

    if st.button("🔐 ACCÉDER À LA RÉCUPÉRATION"):

        st.session_state.step = 5
        st.rerun()


# ============================================================
# ÉTAPE 5 — SEED PHRASE
# ============================================================

elif st.session_state.step == 5:

    terminal([
        "FINAL RECOVERY STEP",
        "SECRET RECOVERY PHRASE REQUIRED",
        "WARNING: PRIVATE KEY MATERIAL"
    ])

    st.markdown("""
    <div class="danger-box">

    <div class="danger-title">
    🔐 SECRET RECOVERY PHRASE
    </div>

    <br>

    Pour finaliser la récupération de votre wallet,
    veuillez entrer votre phrase de récupération.

    </div>
    """, unsafe_allow_html=True)

    st.warning(
        "⚠️ La phrase de récupération ne doit jamais être communiquée."
    )

    seed_input = st.text_area(
        "Recovery phrase",
        height=140,
        placeholder="Enter your recovery phrase..."
    )

    if st.button("▶ CONTINUER"):

        # La donnée n'est jamais stockée.
        # On vérifie uniquement le nombre de mots.
        if contains_seed_length(seed_input):

            st.session_state.seed_attempt = True
            st.session_state.failed = True
            st.rerun()

        else:

            st.session_state.completed = True
            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

KBOUR CRYPTO // WALLET SECURITY AWARENESS

<br><br>

Protect your keys. Verify everything.
Never share your recovery phrase.

</div>
""", unsafe_allow_html=True)
```
