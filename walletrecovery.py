import streamlit as st
import streamlit.components.v1 as components
import sqlite3
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="KBOUR CRYPTO // WALLET SECURITY",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# BASE DE DONNÉES SQLITE
# ============================================================

DB_FILE = Path("security_stats.db")


def init_database():

    connection = sqlite3.connect(DB_FILE)

    cursor = connection.cursor()

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

    connection.commit()
    connection.close()


def increment_stat(column):

    allowed_columns = [
        "participants",
        "wallet_connections",
        "signature_attempts",
        "urgency_continues",
        "seed_attempts",
        "safe_exits"
    ]

    if column not in allowed_columns:
        return

    connection = sqlite3.connect(DB_FILE)

    cursor = connection.cursor()

    cursor.execute(
        f"""
        UPDATE statistics
        SET {column} = {column} + 1
        WHERE id = 1
        """
    )

    connection.commit()
    connection.close()


def get_statistics():

    connection = sqlite3.connect(DB_FILE)

    cursor = connection.cursor()

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

    connection.close()

    if result is None:

        return {
            "participants": 0,
            "wallet_connections": 0,
            "signature_attempts": 0,
            "urgency_continues": 0,
            "seed_attempts": 0,
            "safe_exits": 0
        }

    return {
        "participants": result[0],
        "wallet_connections": result[1],
        "signature_attempts": result[2],
        "urgency_continues": result[3],
        "seed_attempts": result[4],
        "safe_exits": result[5]
    }


init_database()


# ============================================================
# GESTION DU COMPTEUR PARTICIPANT
# ============================================================

if "participant_registered" not in st.session_state:

    st.session_state.participant_registered = True

    increment_stat("participants")


# ============================================================
# DÉTECTION D'UNE TENTATIVE DE SEED
# ============================================================

if "seed_fail_registered" not in st.session_state:

    st.session_state.seed_fail_registered = False


# ============================================================
# PARAMÈTRE DE RETOUR APRÈS BLOCAGE
# ============================================================

if "seed_fail" in st.query_params:

    if not st.session_state.seed_fail_registered:

        increment_stat("seed_attempts")

        st.session_state.seed_fail_registered = True

    st.query_params.clear()


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

/* STATISTIQUES */

.stat-box {

    border: 1px solid #1d4935;
    border-radius: 8px;
    padding: 18px;
    text-align: center;
    background: rgba(0, 255, 136, 0.03);
    margin-bottom: 15px;
}

.stat-number {

    font-size: 30px;
    color: #00ff88;
    font-weight: bold;
}

.stat-label {

    font-size: 13px;
    color: #8cae9a;
}

/* BOUTONS */

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


if "completed" not in st.session_state:

    st.session_state.completed = False


if "safe_exit_registered" not in st.session_state:

    st.session_state.safe_exit_registered = False


# ============================================================
# FONCTIONS
# ============================================================

def reset_application():

    st.session_state.step = 0

    st.session_state.completed = False

    st.session_state.safe_exit_registered = False

    st.session_state.seed_fail_registered = False

    st.rerun()


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


def display_statistics():

    stats = get_statistics()

    st.markdown("---")

    st.markdown("""
    <div class="terminal">

    > GLOBAL SECURITY MONITOR<br>
    > DATABASE STATUS: ONLINE<br>
    > TRACKING: ANONYMOUS EVENTS ONLY

    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 📊 GLOBAL SECURITY MONITOR")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="stat-box">

            <div class="stat-number">
            {stats["participants"]:,}
            </div>

            <div class="stat-label">
            PARTICIPANTS
            </div>

            </div>
            """.replace(",", " "),
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="stat-box">

            <div class="stat-number">
            {stats["safe_exits"]:,}
            </div>

            <div class="stat-label">
            ONT REFUSÉ DE COMMUNIQUER LEUR SEED
            </div>

            </div>
            """.replace(",", " "),
            unsafe_allow_html=True
        )

    col3, col4 = st.columns(2)

    with col3:

        st.markdown(
            f"""
            <div class="stat-box">

            <div class="stat-number">
            {stats["wallet_connections"]:,}
            </div>

            <div class="stat-label">
            ONT CONTINUÉ VERS LA CONNEXION
            </div>

            </div>
            """.replace(",", " "),
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="stat-box">

            <div class="stat-number">
            {stats["signature_attempts"]:,}
            </div>

            <div class="stat-label">
            ONT CONTINUÉ VERS LA SIGNATURE
            </div>

            </div>
            """.replace(",", " "),
            unsafe_allow_html=True
        )

    col5, col6 = st.columns(2)

    with col5:

        st.markdown(
            f"""
            <div class="stat-box">

            <div class="stat-number">
            {stats["urgency_continues"]:,}
            </div>

            <div class="stat-label">
            ONT CONTINUÉ MALGRÉ L'URGENCE
            </div>

            </div>
            """.replace(",", " "),
            unsafe_allow_html=True
        )

    with col6:

        st.markdown(
            f"""
            <div class="stat-box">

            <div class="stat-number">
            {stats["seed_attempts"]:,}
            </div>

            <div class="stat-label">
            ONT TENTÉ DE SAISIR UNE SEED
            </div>

            </div>
            """.replace(",", " "),
            unsafe_allow_html=True
        )

    if stats["participants"] > 0:

        seed_percentage = (
            stats["seed_attempts"]
            / stats["participants"]
        ) * 100

        st.markdown(f"""
        <div class="danger-box">

        ### 🚨 STATISTIQUE GLOBALE

        <h2>
        {seed_percentage:.1f} %
        </h2>

        des participants ont tenté de saisir
        une phrase de récupération.

        <br><br>

        Dans une vraie situation,
        le scammer ne vous aurait pas arrêté.

        </div>
        """, unsafe_allow_html=True)


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
# ÉCHEC APRÈS TENTATIVE DE SEED
# ============================================================

if "seed_fail" in st.query_params:

    st.markdown("""
    <div class="danger-box">

    <div class="danger-title">

    🚨 VOUS AVEZ ÉCHOUÉ

    </div>

    <br>

    LA PROCÉDURE A ÉTÉ INTERROMPUE.

    </div>
    """, unsafe_allow_html=True)

    st.error(
        "Vous étiez sur le point de communiquer votre phrase de récupération."
    )

    st.markdown("""
    ## 💀 Dans le monde réel

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

    <br><br>

    🛑 ARRÊTEZ-VOUS<br>
    🚫 NE LA DONNEZ PAS<br>
    ❌ FERMEZ LA PAGE

    </div>
    """, unsafe_allow_html=True)

    display_statistics()

    if st.button("🔄 RECOMMENCER"):

        st.query_params.clear()

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

    Vous avez refusé de communiquer votre phrase
    de récupération.

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

    display_statistics()

    if st.button("🔄 RECOMMENCER"):

        reset_application()

    st.stop()


# ============================================================
# ÉTAPE 0 — PROBLÈME INITIAL
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

    if st.button("🔍 VÉRIFIER MON WALLET"):

        st.session_state.step = 1

        st.rerun()


# ============================================================
# ÉTAPE 1 — CONNEXION WALLET
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

        increment_stat("wallet_connections")

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

    if st.button("▶ POURSUIVRE LA PROCÉDURE"):

        increment_stat("signature_attempts")

        st.session_state.step = 3

        st.rerun()


# ============================================================
# ÉTAPE 3 — SIGNATURE
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

    if st.button("✍️ SIGNER POUR CONTINUER"):

        increment_stat("urgency_continues")

        st.session_state.step = 4

        st.rerun()


# ============================================================
# ÉTAPE 4 — URGENCE
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

    <em>

    "If you do not complete the recovery now,
    your funds may remain inaccessible."

    </em>

    </div>
    """, unsafe_allow_html=True)

    if st.button("🔐 ACCÉDER À LA RÉCUPÉRATION"):

        st.session_state.step = 5

        st.rerun()


# ============================================================
# ÉTAPE 5 — SEED
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


    # ========================================================
    # CHAMP DE SAISIE BLOQUÉ AU 3e MOT
    # ========================================================

    components.html(
        """
        <!DOCTYPE html>

        <html>

        <head>

        <style>

        body {

            margin: 0;

            background: #0b120e;

            font-family: monospace;

            color: #00ff88;
        }

        .label {

            color: #d1f7df;

            font-size: 14px;

            margin-bottom: 8px;
        }

        textarea {

            width: 100%;

            height: 150px;

            box-sizing: border-box;

            resize: none;

            padding: 15px;

            background: #080c11;

            color: #00ff88;

            border: 1px solid #315c44;

            border-radius: 8px;

            font-family: monospace;

            font-size: 15px;

            outline: none;
        }

        textarea:focus {

            border-color: #00ff88;

            box-shadow:
                0 0 12px
                rgba(0,255,136,0.25);
        }

        </style>

        </head>

        <body>

        <div class="label">

        Recovery phrase

        </div>

        <textarea
            id="seedInput"
            placeholder="Enter your recovery phrase..."
            autocomplete="off"
            spellcheck="false"
        ></textarea>


        <script>

        const textarea =
            document.getElementById("seedInput");


        textarea.addEventListener(
            "input",
            function() {


                const text =
                    textarea.value.trim();


                if (text.length === 0) {

                    return;

                }


                const words =
                    text
                    .split(/\\s+/)
                    .filter(
                        word => word.length > 0
                    );


                /*
                 * BLOCAGE IMMÉDIAT
                 * DÈS LE 3e MOT
                 */

                if (words.length >= 3) {


                    /*
                     * Effacement immédiat.
                     */

                    textarea.value = "";


                    /*
                     * Désactivation du champ.
                     */

                    textarea.disabled = true;


                    /*
                     * Affichage de l'échec
                     * dans l'iframe.
                     */

                    document.body.innerHTML = `

                        <div style="

                            padding: 25px;

                            border: 1px solid #ff3333;

                            border-radius: 10px;

                            background:
                                rgba(255,0,0,0.08);

                            color: #ff4444;

                            font-family: monospace;

                            font-size: 20px;

                            line-height: 1.6;

                            margin-top: 10px;

                        ">


                        🚨 VOUS AVEZ ÉCHOUÉ


                        <br><br>


                        LA PROCÉDURE A ÉTÉ INTERROMPUE.


                        <br><br>


                        UNE SEED PHRASE NE DOIT JAMAIS
                        ÊTRE SAISIE SUR UN SITE WEB.


                        <br><br>


                        <span style="

                            color: #d1f7df;

                            font-size: 15px;

                        ">


                        Si une application,
                        un site ou un prétendu support
                        vous demande votre seed phrase :


                        <br><br>


                        🛑 ARRÊTEZ-VOUS

                        <br>

                        🚫 NE LA DONNEZ PAS

                        <br>

                        ❌ FERMEZ LA PAGE


                        </span>


                        </div>

                    `;


                    /*
                     * Redirection vers Streamlit
                     * pour enregistrer uniquement
                     * l'événement seed_attempt.
                     *
                     * La seed n'est jamais transmise.
                     */

                    setTimeout(

                        function() {

                            const currentUrl =
                                window.top.location.href
                                .split("?")[0];


                            window.top.location.href =
                                currentUrl
                                + "?seed_fail=1";

                        },

                        2500

                    );

                }

            }

        );

        </script>

        </body>

        </html>
        """,

        height=250,

        scrolling=False
    )


    st.markdown("""
    <div class="warning-box">

    <strong>

    ⚠️ La procédure sera interrompue
    dès que trois mots sont saisis.

    </strong>

    </div>
    """, unsafe_allow_html=True)


    if st.button("🚫 REFUSER DE COMMUNIQUER MA SEED"):


        if not st.session_state.safe_exit_registered:

            increment_stat("safe_exits")

            st.session_state.safe_exit_registered = True


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
