import streamlit as st
import re
import time
import random


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="KBOUR CRYPTO — Wallet Safety Training",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS — TERMINAL CYBERPUNK
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
            rgba(0, 255, 136, 0.07),
            transparent 30%
        ),
        radial-gradient(
            circle at bottom left,
            rgba(0, 150, 255, 0.05),
            transparent 30%
        ),
        #080c11;
}

/* Texte général */

p, li, label {
    color: #c9fce0 !important;
}

h1, h2, h3, h4 {
    color: #00ff88 !important;
    letter-spacing: 1px;
}

/* Header */

.header-box {
    border: 1px solid #00ff88;
    padding: 28px;
    border-radius: 12px;
    background:
        linear-gradient(
            135deg,
            rgba(0,255,136,0.08),
            rgba(0,0,0,0.35)
        );
    box-shadow:
        0 0 25px rgba(0,255,136,0.08),
        inset 0 0 20px rgba(0,255,136,0.02);
    margin-bottom: 25px;
}

.header-title {
    font-size: 38px;
    font-weight: bold;
    color: #00ff88;
    text-shadow: 0 0 12px rgba(0,255,136,0.6);
}

.header-subtitle {
    font-size: 16px;
    color: #b9dcca;
    margin-top: 8px;
}

/* Cartes */

.card {
    border: 1px solid #263a32;
    background: rgba(10, 20, 18, 0.8);
    padding: 22px;
    border-radius: 10px;
    margin: 12px 0;
}

.card:hover {
    border-color: #00ff88;
}

/* Danger */

.danger-box {
    border: 1px solid #ff3333;
    background: rgba(255, 0, 0, 0.08);
    padding: 24px;
    border-radius: 10px;
    margin: 18px 0;
    box-shadow: 0 0 20px rgba(255,0,0,0.08);
}

.danger-title {
    color: #ff4444;
    font-size: 26px;
    font-weight: bold;
}

/* Warning */

.warning-box {
    border: 1px solid #ffcc00;
    background: rgba(255, 204, 0, 0.07);
    padding: 22px;
    border-radius: 10px;
    margin: 18px 0;
}

/* Success */

.success-box {
    border: 1px solid #00ff88;
    background: rgba(0, 255, 136, 0.07);
    padding: 22px;
    border-radius: 10px;
    margin: 18px 0;
}

/* Info */

.info-box {
    border: 1px solid #00aaff;
    background: rgba(0, 150, 255, 0.07);
    padding: 22px;
    border-radius: 10px;
    margin: 18px 0;
}

/* Terminal */

.terminal {
    background: #020504;
    border: 1px solid #1d4c38;
    padding: 20px;
    border-radius: 8px;
    font-family: monospace;
    color: #00ff88;
    line-height: 1.8;
    box-shadow: inset 0 0 25px rgba(0,255,136,0.04);
}

/* Progress */

.progress-container {
    border: 1px solid #263a32;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
}

/* Boutons */

.stButton > button {
    width: 100%;
    border: 1px solid #00ff88;
    background: rgba(0, 255, 136, 0.05);
    color: #00ff88;
    font-family: 'Share Tech Mono', monospace;
    font-weight: bold;
    min-height: 48px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: rgba(0, 255, 136, 0.16);
    border-color: #ffffff;
    color: #ffffff;
    box-shadow: 0 0 15px rgba(0,255,136,0.35);
}

/* Inputs */

textarea, input {
    background-color: #0c1310 !important;
    color: #00ff88 !important;
    border: 1px solid #28563f !important;
}

/* Footer */

.footer {
    text-align: center;
    margin-top: 50px;
    padding: 20px;
    border-top: 1px solid #1b3026;
    color: #557565;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "page": "home",
    "scenario": None,
    "scenario_step": 0,
    "quiz_index": 0,
    "score": 0,
    "quiz_answers": [],
    "seed_attempt": False,
    "completed_scenarios": [],
    "training_complete": False,
    "user_name": ""
}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def reset_app():

    for key, value in DEFAULT_STATE.items():

        st.session_state[key] = value

    st.rerun()


def detect_seed_attempt(text):

    """
    Détection pédagogique.

    Cette fonction ne valide aucune seed.
    Elle détecte simplement une tentative de saisir
    un nombre de mots correspondant à une seed BIP39.

    Aucune donnée n'est sauvegardée.
    """

    if not text:
        return False

    words = re.findall(r"\b[a-zA-ZÀ-ÿ]+\b", text.strip())

    # Les longueurs standards BIP39
    valid_lengths = [12, 15, 18, 21, 24]

    if len(words) in valid_lengths:

        return True

    return False


def mark_scenario_complete(scenario):

    if scenario not in st.session_state.completed_scenarios:

        st.session_state.completed_scenarios.append(scenario)


def progress_value():

    completed = len(st.session_state.completed_scenarios)

    return completed / 3


def terminal_log(lines):

    text = ""

    for line in lines:

        text += f"> {line}<br>"

    st.markdown(
        f"""
        <div class="terminal">
        {text}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="header-box">

<div class="header-title">
🛡️ KBOUR CRYPTO // WALLET SAFETY TRAINING
</div>

<div class="header-subtitle">
SECURITY AWARENESS SIMULATOR — DON'T TRUST. VERIFY.
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# PROGRESS BAR
# ============================================================

completed = len(st.session_state.completed_scenarios)

st.markdown(
    f"""
    <div class="progress-container">

    <strong>FORMATION SECURITY PROGRESS</strong>

    <br><br>

    Scénarios validés :
    <strong>{completed}/3</strong>

    </div>
    """,
    unsafe_allow_html=True
)

st.progress(progress_value())


# ============================================================
# PAGE ACCUEIL
# ============================================================

if st.session_state.page == "home":

    st.markdown("""
    ## 🎯 OBJECTIF DE LA SIMULATION
    """)

    st.markdown("""
    <div class="card">

    Dans l'univers crypto, votre seed phrase est l'équivalent
    d'une clé maître.

    <br><br>

    <strong>Celui qui possède votre seed peut potentiellement
    contrôler vos fonds.</strong>

    <br><br>

    Cette formation va vous placer dans plusieurs situations
    réalistes utilisées par les scammers.

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### ⚠️ RÈGLE ABSOLUE

    > **Votre seed phrase ne doit jamais être communiquée à qui que ce soit.**

    Peu importe que la personne prétende être :

    - un support technique ;
    - un administrateur Telegram ;
    - un développeur ;
    - un représentant d'un protocole ;
    - un expert crypto ;
    - un ami ;
    - une IA ;
    - un service de récupération.

    **Personne n'a besoin de votre seed phrase.**
    """)

    st.markdown("---")

    st.markdown("## 🧪 CHOISISSEZ VOTRE SCÉNARIO")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="card">

        ### 🔐 SCÉNARIO 01

        <strong>FAUX WALLET RECOVERY</strong>

        <br><br>

        Un site vous propose de récupérer
        l'accès à votre wallet.

        <br><br>

        Niveau : ⚠️⚠️⚠️

        </div>
        """, unsafe_allow_html=True)

        if "recovery" in st.session_state.completed_scenarios:

            st.success("SCÉNARIO VALIDÉ")

        else:

            if st.button(
                "▶ LANCER LE SCÉNARIO 01",
                key="start_recovery"
            ):

                st.session_state.scenario = "recovery"
                st.session_state.scenario_step = 0
                st.session_state.page = "scenario"
                st.rerun()

    with col2:

        st.markdown("""
        <div class="card">

        ### 📱 SCÉNARIO 02

        <strong>LE FAUX SUPPORT TELEGRAM</strong>

        <br><br>

        Un prétendu support vous contacte
        pour vous aider.

        <br><br>

        Niveau : ⚠️⚠️⚠️⚠️

        </div>
        """, unsafe_allow_html=True)

        if "telegram" in st.session_state.completed_scenarios:

            st.success("SCÉNARIO VALIDÉ")

        else:

            if st.button(
                "▶ LANCER LE SCÉNARIO 02",
                key="start_telegram"
            ):

                st.session_state.scenario = "telegram"
                st.session_state.scenario_step = 0
                st.session_state.page = "scenario"
                st.rerun()

    with col3:

        st.markdown("""
        <div class="card">

        ### 🦊 SCÉNARIO 03

        <strong>LE FAUX SUPPORT WALLET</strong>

        <br><br>

        Une personne prétend pouvoir
        résoudre un problème technique.

        <br><br>

        Niveau : ⚠️⚠️⚠️⚠️⚠️

        </div>
        """, unsafe_allow_html=True)

        if "support" in st.session_state.completed_scenarios:

            st.success("SCÉNARIO VALIDÉ")

        else:

            if st.button(
                "▶ LANCER LE SCÉNARIO 03",
                key="start_support"
            ):

                st.session_state.scenario = "support"
                st.session_state.scenario_step = 0
                st.session_state.page = "scenario"
                st.rerun()

    st.markdown("---")

    st.markdown("""
    <div class="warning-box">

    🚨 <strong>IMPORTANT</strong>

    <br><br>

    Cette simulation ne doit jamais recevoir votre vraie seed phrase.

    Si vous avez réellement saisi votre seed phrase sur un site,
    un formulaire ou dans un message :

    <br><br>

    <strong>
    CONSIDÉREZ-LA COMME COMPROMISE.
    </strong>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# SCÉNARIO 01 — FAUX RECOVERY
# ============================================================

elif (
    st.session_state.page == "scenario"
    and st.session_state.scenario == "recovery"
):

    step = st.session_state.scenario_step

    st.markdown("## 🔐 SCÉNARIO 01 — WALLET RECOVERY")

    # STEP 0
    if step == 0:

        terminal_log([
            "INITIALIZING WALLET RECOVERY PROTOCOL...",
            "CHECKING WALLET STATUS...",
            "WARNING: ACCESS ISSUE DETECTED",
            "RECOVERY MODULE AVAILABLE"
        ])

        st.markdown("""
        <div class="warning-box">

        🚨 <strong>ALERTE WALLET</strong>

        <br><br>

        Votre wallet semble rencontrer un problème.

        <br><br>

        Un outil vous propose de restaurer automatiquement
        l'accès à vos fonds.

        </div>
        """, unsafe_allow_html=True)

        if st.button("🔓 RÉCUPÉRER MON WALLET"):

            st.session_state.scenario_step = 1
            st.rerun()

    # STEP 1
    elif step == 1:

        st.markdown("""
        <div class="danger-box">

        <div class="danger-title">
        🔐 SECRET RECOVERY PHRASE REQUIRED
        </div>

        <br>

        Pour récupérer votre wallet, veuillez entrer votre
        phrase de récupération.

        </div>
        """, unsafe_allow_html=True)

        st.error(
            "⚠️ STOP. C'est exactement le piège."
        )

        st.markdown("""
        ### 🧠 Que devez-vous faire ?

        Cette interface est volontairement conçue pour ressembler
        à un outil crédible.

        **Vous ne devez jamais entrer votre vraie seed.**

        Pour continuer la simulation, vous pouvez :

        - laisser le champ vide ;
        - écrire `JE NE DONNE JAMAIS MA SEED` ;
        - écrire `SCAM`.
        """)

        user_input = st.text_area(
            "Simulation — ne saisissez jamais votre vraie seed",
            height=120,
            placeholder="Ne saisissez aucune vraie seed phrase ici."
        )

        if st.button("▶ VALIDER LA DÉCISION"):

            if detect_seed_attempt(user_input):

                st.session_state.seed_attempt = True
                st.session_state.scenario_step = 2
                st.rerun()

            else:

                st.session_state.seed_attempt = False
                st.session_state.scenario_step = 3
                st.rerun()

    # STEP 2 — SEED TENTATIVE
    elif step == 2:

        st.markdown("""
        <div class="danger-box">

        <div class="danger-title">
        🚨 SEED PHRASE DETECTED
        </div>

        <br>

        LA SIMULATION EST ARRÊTÉE.

        </div>
        """, unsafe_allow_html=True)

        st.error("""
        Vous venez de reproduire exactement le comportement
        qu'un scammer espère obtenir.
        """)

        st.markdown("""
        ### 💀 Dans le monde réel

        Si cette phrase était votre vraie seed :

        - vos fonds pourraient être transférés ;
        - vos tokens pourraient être vendus ;
        - vos NFTs pourraient être volés ;
        - vos autorisations pourraient être exploitées.

        **La blockchain ne vous demandera pas si vous êtes sûr.**

        Le scammer non plus.
        """)

        st.markdown("""
        <div class="success-box">

        ### ✅ LEÇON

        Une seed phrase :

        <br>

        ❌ ne se saisit pas sur un site ;

        ❌ ne se communique pas à un support ;

        ❌ ne se donne pas à un admin ;

        ❌ ne se partage pas avec une IA ;

        ❌ ne se copie pas dans un formulaire web.

        <br><br>

        <strong>
        VOTRE SEED RESTE HORS LIGNE.
        </strong>

        </div>
        """, unsafe_allow_html=True)

        mark_scenario_complete("recovery")

        if st.button("▶ J'AI COMPRIS — CONTINUER"):

            st.session_state.page = "home"
            st.session_state.scenario = None
            st.rerun()

    # STEP 3 — BON COMPORTEMENT
    elif step == 3:

        st.markdown("""
        <div class="success-box">

        <h2>✅ BON RÉFLEXE</h2>

        Vous avez refusé de communiquer votre seed phrase.

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        ### 🎯 C'est exactement la bonne réaction.

        Même si le site semble :

        - professionnel ;
        - sécurisé ;
        - connu ;
        - recommandé par quelqu'un ;
        - connecté à un protocole DeFi.

        **Une seed phrase ne se communique jamais.**
        """)

        mark_scenario_complete("recovery")

        if st.button("▶ TERMINER LE SCÉNARIO"):

            st.session_state.page = "home"
            st.session_state.scenario = None
            st.rerun()


# ============================================================
# SCÉNARIO 02 — FAUX TELEGRAM
# ============================================================

elif (
    st.session_state.page == "scenario"
    and st.session_state.scenario == "telegram"
):

    step = st.session_state.scenario_step

    st.markdown("## 📱 SCÉNARIO 02 — FAUX SUPPORT TELEGRAM")

    if step == 0:

        st.markdown("""
        <div class="card">

        ### 💬 MESSAGE PRIVÉ

        <br>

        <strong>Crypto Support Official ✅</strong>

        <br><br>

        Hello sir, we detected an issue with your wallet.

        <br><br>

        We can help you recover your funds.

        <br><br>

        Please send your recovery phrase so we can verify
        your wallet ownership.

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        ### ❓ Que faites-vous ?
        """)

        choice = st.radio(
            "Choisissez votre réaction",
            [
                "Je lui envoie ma seed pour gagner du temps.",
                "Je lui demande une adresse officielle.",
                "Je bloque et signale immédiatement le compte.",
                "Je lui envoie seulement une partie de ma seed."
            ]
        )

        if st.button("▶ VALIDER MA RÉPONSE"):

            if choice == "Je bloque et signale immédiatement le compte.":

                st.session_state.scenario_step = 1

            else:

                st.session_state.scenario_step = 2

            st.rerun()

    elif step == 1:

        st.markdown("""
        <div class="success-box">

        ### ✅ EXCELLENTE RÉACTION

        Vous avez identifié un principe fondamental :

        <br><br>

        <strong>
        Un support légitime ne vous demandera jamais votre seed phrase.
        </strong>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        ### 🧠 Règle pratique

        Sur Telegram, Discord ou X :

        - un compte peut être copié ;
        - un nom peut être copié ;
        - une photo peut être copiée ;
        - un badge peut être trompeur ;
        - un profil peut être compromis.

        **Ne faites jamais confiance à un message privé inattendu.**
        """)

        mark_scenario_complete("telegram")

        if st.button("▶ TERMINER LE SCÉNARIO"):

            st.session_state.page = "home"
            st.session_state.scenario = None
            st.rerun()

    elif step == 2:

        st.markdown("""
        <div class="danger-box">

        <div class="danger-title">
        🚨 PIÈGE IDENTIFIÉ
        </div>

        <br>

        Vous venez de choisir une méthode dangereuse.

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        ### ❌ Quelques erreurs classiques

        #### « Je lui envoie seulement une partie de ma seed »

        Mauvaise idée.

        Une seed phrase est secrète dans son intégralité.

        #### « Je lui demande son adresse officielle »

        Un scammer peut vous fournir une fausse adresse.

        #### « Il semble professionnel »

        L'apparence n'est pas une preuve.

        """)

        st.markdown("""
        <div class="success-box">

        ### LA BONNE RÉACTION

        <strong>

        Ne pas répondre.<br>
        Bloquer.<br>
        Signaler.<br>
        Vérifier par les canaux officiels.

        </strong>

        </div>
        """, unsafe_allow_html=True)

        mark_scenario_complete("telegram")

        if st.button("▶ J'AI COMPRIS"):

            st.session_state.page = "home"
            st.session_state.scenario = None
            st.rerun()


# ============================================================
# SCÉNARIO 03 — FAUX SUPPORT WALLET
# ============================================================

elif (
    st.session_state.page == "scenario"
    and st.session_state.scenario == "support"
):

    step = st.session_state.scenario_step

    st.markdown("## 🦊 SCÉNARIO 03 — FAUX SUPPORT WALLET")

    if step == 0:

        st.markdown("""
        <div class="card">

        ### ⚠️ PROBLÈME DÉTECTÉ

        Votre wallet affiche une erreur lors de la connexion
        à un protocole DeFi.

        <br><br>

        Une personne vous contacte :

        <br><br>

        <em>
        "I can help you fix your wallet.
        Please connect here and sign this message."
        </em>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        ### ❓ Que faites-vous ?
        """)

        choice = st.radio(
            "Votre décision",
            [
                "Je signe immédiatement.",
                "Je demande ce que fait exactement la transaction.",
                "Je connecte un wallet contenant tous mes fonds.",
                "Je donne ma seed pour qu'il vérifie."
            ]
        )

        if st.button("▶ VALIDER MA RÉPONSE"):

            if choice == "Je demande ce que fait exactement la transaction.":

                st.session_state.scenario_step = 1

            else:

                st.session_state.scenario_step = 2

            st.rerun()

    elif step == 1:

        st.markdown("""
        <div class="success-box">

        ### ✅ BON RÉFLEXE

        Ne jamais signer aveuglément.

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        ### 🔍 Avant de signer

        Vous devez comprendre :

        - quelle fonction est appelée ;
        - quel contrat reçoit la transaction ;
        - quelles autorisations sont accordées ;
        - quels tokens sont concernés ;
        - quelles limites sont définies ;
        - si la transaction est cohérente avec votre action.

        **Signer n'est pas simplement cliquer sur OK.**
        """)

        mark_scenario_complete("support")

        if st.button("▶ TERMINER LE SCÉNARIO"):

            st.session_state.page = "home"
            st.session_state.scenario = None
            st.rerun()

    elif step == 2:

        st.markdown("""
        <div class="danger-box">

        <div class="danger-title">
        🚨 DANGER — ACTION À RISQUE
        </div>

        <br>

        Vous avez choisi une action potentiellement dangereuse.

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        ### 🧠 Ce qu'un scammer peut essayer de faire

        - vous faire signer une transaction malveillante ;
        - vous faire approuver un token ;
        - vous faire donner une autorisation illimitée ;
        - vous rediriger vers un faux site ;
        - vous convaincre de révéler votre seed.

        **Un wallet compromis peut perdre ses fonds très rapidement.**
        """)

        st.markdown("""
        <div class="success-box">

        ### RÈGLE

        <strong>

        Ne signez jamais quelque chose que vous ne comprenez pas.

        </strong>

        </div>
        """, unsafe_allow_html=True)

        mark_scenario_complete("support")

        if st.button("▶ J'AI COMPRIS"):

            st.session_state.page = "home"
            st.session_state.scenario = None
            st.rerun()


# ============================================================
# QUIZ FINAL
# ============================================================

if (
    len(st.session_state.completed_scenarios) == 3
    and st.session_state.page == "home"
    and not st.session_state.training_complete
):

    st.markdown("---")

    st.markdown("""
    <div class="success-box">

    <h2>🎓 LES 3 SCÉNARIOS SONT VALIDÉS</h2>

    Vous pouvez maintenant passer le test final.

    </div>
    """, unsafe_allow_html=True)

    if st.button("🧠 COMMENCER LE TEST FINAL"):

        st.session_state.page = "quiz"
        st.session_state.quiz_index = 0
        st.session_state.score = 0
        st.session_state.quiz_answers = []
        st.rerun()


# ============================================================
# QUESTIONS DU QUIZ
# ============================================================

QUIZ = [

    {
        "question": "Qui peut légitimement vous demander votre seed phrase ?",
        "answers": [
            "Le support officiel",
            "Un administrateur Telegram",
            "Un développeur",
            "Personne"
        ],
        "correct": "Personne"
    },

    {
        "question": "Que devez-vous faire si un site demande votre seed ?",
        "answers": [
            "Entrer seulement 12 mots",
            "Entrer une fausse seed",
            "Fermer immédiatement le site",
            "Demander confirmation sur Telegram"
        ],
        "correct": "Fermer immédiatement le site"
    },

    {
        "question": "Que signifie une transaction que vous ne comprenez pas ?",
        "answers": [
            "Elle est probablement sans danger",
            "Vous pouvez la signer quand même",
            "Vous devez vous arrêter et vérifier",
            "Le wallet la bloque automatiquement"
        ],
        "correct": "Vous devez vous arrêter et vérifier"
    },

    {
        "question": "Un message privé d'un prétendu support vous demande votre seed. Que faites-vous ?",
        "answers": [
            "Je réponds rapidement",
            "Je bloque et je signale",
            "Je donne une partie de la seed",
            "Je lui demande son mot de passe"
        ],
        "correct": "Je bloque et je signale"
    },

    {
        "question": "Quel est le meilleur endroit pour conserver une seed ?",
        "answers": [
            "Un formulaire en ligne",
            "Une conversation Telegram",
            "Un cloud non chiffré",
            "Hors ligne, de manière sécurisée"
        ],
        "correct": "Hors ligne, de manière sécurisée"
    }

]


# ============================================================
# PAGE QUIZ
# ============================================================

if st.session_state.page == "quiz":

    index = st.session_state.quiz_index

    if index < len(QUIZ):

        question = QUIZ[index]

        st.markdown(f"""
        ## 🧠 TEST FINAL

        Question {index + 1}/{len(QUIZ)}
        """)

        st.progress(index / len(QUIZ))

        st.markdown(f"""
        <div class="card">

        <h3>{question["question"]}</h3>

        </div>
        """, unsafe_allow_html=True)

        answer = st.radio(
            "Votre réponse",
            question["answers"],
            key=f"quiz_{index}"
        )

        if st.button("▶ VALIDER LA RÉPONSE"):

            st.session_state.quiz_answers.append(answer)

            if answer == question["correct"]:

                st.session_state.score += 1

            st.session_state.quiz_index += 1

            st.rerun()

    else:

        score = st.session_state.score
        total = len(QUIZ)

        st.session_state.training_complete = True

        st.markdown("""
        ## 🏆 RÉSULTAT FINAL
        """)

        st.markdown(f"""
        <div class="success-box">

        <h1>{score}/{total}</h1>

        </div>
        """, unsafe_allow_html=True)

        if score == total:

            st.markdown("""
            <div class="success-box">

            <h2>🛡️ WALLET SECURITY MASTER</h2>

            <br>

            Félicitations.

            <br><br>

            Vous avez parfaitement identifié
            les principaux pièges liés aux scams crypto.

            </div>
            """, unsafe_allow_html=True)

        elif score >= 3:

            st.markdown("""
            <div class="warning-box">

            ### ⚠️ NIVEAU ACCEPTABLE

            Vous avez compris les principes fondamentaux.

            Mais dans la crypto, une seule erreur peut coûter très cher.

            Continuez à vous former.

            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="danger-box">

            <h2>🚨 FORMATION RECOMMANDÉE</h2>

            Vous avez encore des réflexes dangereux.

            <br><br>

            Dans une vraie situation, un scammer
            ne vous laissera pas une seconde chance.

            <br><br>

            <strong>
            FORMEZ-VOUS AVANT DE METTRE VOTRE CAPITAL EN DANGER.
            </strong>

            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("""
        ### 🧠 LES 5 RÈGLES À RETENIR

        1. 🔐 **Ne partagez jamais votre seed phrase.**
        2. 🚫 **Un support légitime ne vous la demandera jamais.**
        3. 🧪 **Ne signez jamais une transaction que vous ne comprenez pas.**
        4. 🔍 **Vérifiez toujours les sites et les contrats.**
        5. 🎓 **En cas de doute : arrêtez-vous et formez-vous.**
        """)

        st.markdown("""
        <div class="terminal">

        > SECURITY STATUS: TRAINING COMPLETE<br>
        > SEED PHRASE: NEVER SHARE<br>
        > TRUST LEVEL: VERIFY EVERYTHING<br>
        > WALLET STATUS: PROTECT YOUR KEYS<br>
        > FINAL MESSAGE: NOT YOUR KEYS, NOT YOUR FUNDS

        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 RECOMMENCER LA FORMATION"):

            reset_app()


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

KBOUR CRYPTO // WALLET SAFETY TRAINING

<br><br>

Cette application est un outil pédagogique de sensibilisation
à la sécurité dans l'écosystème crypto.

<br>

Ne partagez jamais votre seed phrase.

</div>
""", unsafe_allow_html=True)
