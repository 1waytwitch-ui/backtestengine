import streamlit as st
import requests
import numpy as np
import datetime
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# ----------------------------- AUTH LOCAL -----------------------------

PASSWORD_KEY = "LP BACKTEST"
PASSWORD_VALUE = "1way"  # <-- EDIT MDP

# Récupération du mot de passe déjà stocké en localStorage
components.html("""
<script>
    const saved = localStorage.getItem("lp_password");
    if (saved) {
        window.parent.postMessage({type: "PASS", value: saved}, "*");
    }
</script>
""", height=0)

# Listener pour récupérer les messages JS
def handle_js_event():
    msg = st.session_state.get("js_event")
    if msg and msg.get("type") == "PASS":
        st.session_state[PASSWORD_KEY] = msg.get("value")

st.experimental_js_listener("message", key="js_event", on_event=handle_js_event)

# Vérification (si pas encore authentifié)
if st.session_state.get(PASSWORD_KEY) != PASSWORD_VALUE:
    st.title("🔐 Accès protégé")
    pwd = st.text_input("Entrez le mot de passe :", type="password")

    if st.button("Valider"):
        if pwd == PASSWORD_VALUE:
            st.session_state[PASSWORD_KEY] = pwd

            # On stocke dans localStorage pour les prochaines visites
            components.html(f"""
            <script>
                localStorage.setItem("lp_password", "{pwd}");
            </script>
            """, height=0)

            st.success("Mot de passe correct ✔")
            st.rerun()
        else:
            st.error("❌ Mot de passe incorrect")

    st.stop()

# ----------------------------------------------------------------------
# APP
# ----------------------------------------------------------------------

st.set_page_config(page_title="LP STRATÉGIES BACKTEST ENGINE ", layout="wide")

st.markdown("""
<style>
.stApp {background-color: #FFFFFF !important; color: #000000 !important;}
h1, h2, h3, h4 {color: #000000 !important;}
.stTextInput input,
.stNumberInput input {background-color: #F0F0F0 !important; color: #000000 !important; border: 1px solid #000000 !important;}
.stButton button {background-color: #000000 !important; color: #FFFFFF !important;}
</style>
""", unsafe_allow_html=True)

STRATEGIES = {
    "Neutre": {"ratio": (0.5, 0.5), "objectif": "Rester dans le range", "contexte": "Incertitude (attention à l'impermanent loss vente à perte ou rachat trop cher)"},
    "Coup de pouce": {"ratio": (0.2, 0.8), "objectif": "Range efficace", "contexte": "Faible volatilité(attention à inverser en fonction du marché)"},
    "Mini-doux": {"ratio": (0.1, 0.9), "objectif": "Nouveau régime prix", "contexte": "Changement de tendance (attention à inverser en fonction du marché)"},
    "Side-line Up": {"ratio": (0.95, 0.05), "objectif": "Accumulation", "contexte": "Dump"},
    "Side-line Below": {"ratio": (0.05, 0.95), "objectif": "Attente avant pump", "contexte": "Marché haussier"},
    "DCA-in": {"ratio": (1.0, 0.0), "objectif": "Entrée progressive", "contexte": "Accumulation de l'actif le plus volatile (Token A)"},
    "DCA-out": {"ratio": (0.0, 1.0), "objectif": "Sortie progressive", "contexte": "Tendance haussière revente de l'actif le plus volatile (token A contre le token B)"},
}

COINGECKO_IDS = {
    "WETH": "weth",
    "USDC": "usd-coin",
    "CBBTC": "coinbase-wrapped-btc",
    "VIRTUAL": "virtual-protocol",
    "AERO": "aerodrome-finance"
}

PAIRS = [
    ("WETH", "USDC"), ("CBBTC", "USDC"), ("WETH", "CBBTC"),
    ("VIRTUAL", "WETH"), ("AERO", "WETH")
]

@st.cache_data(ttl=3600, show_spinner=False)
def get_market_chart(asset_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{asset_id}/market_chart?vs_currency=usd&days=30&interval=daily"
        data = requests.get(url).json()
        prices = [p[1] for p in data.get("prices", [])]
        return prices if prices else [1.0] * 30
    except:
        return [1.0] * 30

def compute_volatility(prices):
    if len(prices) < 2:
        return 0.0
    returns = np.diff(prices) / prices[:-1]
    return np.std(returns) * np.sqrt(365)

def get_price_usd(token):
    try:
        res = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={COINGECKO_IDS[token]}&vs_currencies=usd"
        ).json()
        return res[COINGECKO_IDS[token]]["usd"], True
    except:
        return 0.0, False

# ---- Header --------------------------------------------------------

st.markdown("""
<style>
.deFi-banner {
    background: linear-gradient(135deg, #0a0f1f 0%, #1e2761 40%, #4b1c7d 100%);
    padding: 25px 30px;
    border-radius: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0px 4px 18px rgba(0,0,0,0.45);
    margin-bottom: 25px;
}
.deFi-title-text {
    font-size: 36px;
    font-weight: 700;
    color: white !important;
}
.deFi-telegram-box {
    display: flex;
    align-items: center;
    gap: 12px;
}
.deFi-telegram-box img {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: 2px solid rgba(255,255,255,0.4);
}
.deFi-telegram-box a {
    color: #ffffff !important;
    text-decoration: none;
    font-weight: 600;
    font-size: 18px;
}
</style>

<div class="deFi-banner">
    <div class="deFi-title-text">LP STRATÉGIES BACKTEST ENGINE</div>
    <div class="deFi-telegram-box">
        <img src="https://t.me/i/userpic/320/Pigeonchanceux.jpg">
        <a href="https://t.me/Pigeonchanceux" target="_blank">Mon Telegram</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- Main Layout ---------------------------------------------------
col1, col2 = st.columns([1.3, 1])

# ------------------- COL 1 : CONFIG -------------------
with col1:
    st.subheader("Configuration de la Pool")

    left, right = st.columns(2)
    with left:
        pair_labels = [f"{a}/{b}" for a, b in PAIRS]
        selected_pair = st.radio("Paire :", pair_labels)
    with right:
        strategy_choice = st.radio("Stratégie :", list(STRATEGIES.keys()))

    tokenA, tokenB = selected_pair.split("/")
    info = STRATEGIES[strategy_choice]
    ratioA, ratioB = info["ratio"]

    invert_market = st.checkbox("Inversion marché (bull → bear)")
    if invert_market:
        ratioA, ratioB = ratioB, ratioA

    st.write(f"Ratio : {int(ratioA*100)} / {int(ratioB*100)}")
    st.write(f"Objectif : {info['objectif']}")
    st.write(f"Contexte : {info['contexte']}")

    capital = st.number_input("Capital (USD)", value=1000, step=50)

    # Prix
    if tokenB == "USDC":
        priceA_usd, okA = get_price_usd(tokenA)
        if not okA:
            priceA_usd = st.number_input(f"Prix manuel {tokenA}", value=1.0)
        priceA = priceA_usd
    else:
        priceA_usd, okA = get_price_usd(tokenA)
        priceB_usd, okB = get_price_usd(tokenB)

        la, lb = st.columns(2)
        with la:
            if not okA:
                priceA_usd = st.number_input(f"Prix manuel {tokenA}", value=1.0)
        with lb:
            if not okB:
                priceB_usd = st.number_input(f"Prix manuel {tokenB}", value=1.0)

        priceB_usd = max(priceB_usd, 0.0000001)
        priceA = priceA_usd / priceB_usd

    range_pct = st.number_input("Range (%)", 1.0, 100.0, 20.0)

    range_low = priceA * (1 - ratioA * range_pct / 100)
    range_high = priceA * (1 + ratioB * range_pct / 100)
    if invert_market:
        range_low, range_high = range_high, range_low

    pct_low = -ratioA * range_pct
    pct_high = ratioB * range_pct

    capitalA, capitalB = capital * ratioA, capital * ratioB

# ------------------- COL 2 : backtest -------------------
with col2:
    st.subheader("Range et Prix")
    st.write(f"Prix actuel : {priceA:.6f} $")
    st.write(f"Range ($) : {range_low:.6f} ↔ {range_high:.6f}")

    st.write(f"Range (%) : {pct_low:.1f}% ⇤⇥ +{pct_high:.1f}%")

    st.write(f"Répartitions : {capitalA:.2f} USD {tokenA} ◄ ► {capitalB:.2f} USD {tokenB}")

    today = str(datetime.date.today())
    key = f"{tokenA}_prices_{today}"
    if key in st.session_state:
        pricesA = st.session_state[key]
    else:
        prices = get_market_chart(COINGECKO_IDS[tokenA])
        st.session_state[key] = prices
        pricesA = prices

    vol_30d = compute_volatility(pricesA)
    rebalances = sum((p < range_low) or (p > range_high) for p in pricesA)

    st.subheader("Analyse 30 jours")
    st.write(f"Volatilé : {vol_30d:.2%} — Hors range : {rebalances}")

    future_days = st.number_input("Jours simulés future", 1, 120, 30)
    vol_sim = vol_30d / np.sqrt(365)
    simulated = [pricesA[-1]]
    for _ in range(future_days):
        simulated.append(simulated[-1] * (1 + np.random.normal(0, vol_sim)))
    future_reb = sum((p < range_low) or (p > range_high) for p in simulated)
    st.write(f"Simulation future → Hors range : {future_reb}")

    vol_7d = compute_volatility(pricesA[-7:])
    if vol_7d > 0.8:
        suggestion = "Neutre"
    elif vol_7d > 0.4:
        suggestion = "Coup de pouce"
    else:
        suggestion = "Mini-doux"

    st.subheader("Analyse stratégie")
    st.write(f"Vol 7j : {vol_7d:.2%} — Suggestion : {suggestion}")

# ------------------- AUTOMATION -------------------
st.write("---")
st.header("Réglages Automation")

st.subheader("Range future")
range_percent = st.slider("Range total (%)", 1.0, 90.0, 20.0)

ratio_low, ratio_high = 20, 80
low_offset_pct = -range_percent * ratio_low / 100
high_offset_pct = range_percent * ratio_high / 100

final_low = priceA * (1 + low_offset_pct/100)
final_high = priceA * (1 + high_offset_pct/100)
if invert_market:
    final_low, final_high = final_high, final_low

st.write(f"Range : {final_low:.6f} – {final_high:.6f}")

st.subheader("Trigger d’anticipation")
t1, t2 = st.columns(2)
with t1:
    trig_low = st.slider("Trigger Low (%)", 0, 100, 10)
with t2:
    trig_high = st.slider("Trigger High (%)", 0, 100, 90)

rw = final_high - final_low
trigger_low_price = final_low + (trig_low/100)*rw
trigger_high_price = final_low + (trig_high/100)*rw

st.write(f"Trigger Low : {trigger_low_price:.6f}")
st.write(f"Trigger High : {trigger_high_price:.6f}")

st.subheader("Time-buffer")
vola = vol_30d * 100
if vola < 1:
    recomand = "6 à 12 minutes"
elif vola < 3:
    recomand = "18 à 48 minutes"
else:
    recomand = "60 et plus minutes"
st.write(f"Recommandation avec la volatilité actuelle : {recomand}")

# ------------------- REBALANCE AVANCÉE -------------------
st.subheader("Rebalance avancée (futur range)")

col_b1, col_b2 = st.columns(2)

with col_b1:
    st.markdown("**Marché Baissier**")
    rb_low_bear = priceA * (1 - 0.04)
    rb_high_bear = priceA * (1 + 0.16)
    st.write(f"Range Low : {rb_low_bear:.6f} (-4%)")
    st.write(f"Range High : {rb_high_bear:.6f} (+16%)")

with col_b2:
    st.markdown("**Marché Haussier**")
    rb_low_bull = priceA * (1 - 0.16)
    rb_high_bull = priceA * (1 + 0.04)
    st.write(f"Range Low : {rb_low_bull:.6f} (-16%)")
    st.write(f"Range High : {rb_high_bull:.6f} (+4%)")
