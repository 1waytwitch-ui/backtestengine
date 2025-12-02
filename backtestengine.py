import streamlit as st
import numpy as np

st.set_page_config(page_title="Trading App", layout="wide")

# ------------------------------------------------------------------------------------
# FONCTIONS UTILITAIRES
# ------------------------------------------------------------------------------------

def compute_low_high_range(range_percent, ratio_low=20, ratio_high=80):
    """
    Retourne les offsets low/high basés sur un range total.
    Exemple : range 20%, ratio 20/80 → -4% +16%
    """
    low_offset = -(range_percent * (ratio_low / 100))
    high_offset = range_percent * (ratio_high / 100)
    return low_offset, high_offset


def suggest_time_buffer(volatility):
    """
    Suggestion simplifiée :
    - faible volatilité -> buffer long
    - forte volatilité -> buffer court
    """
    if volatility < 1:
        return "Long (30–60 min)"
    elif volatility < 3:
        return "Moyen (10–30 min)"
    else:
        return "Court (1–10 min)"


def compute_trigger_offset(range_percent, trigger_low_ratio, trigger_high_ratio):
    """
    Calcul du déclenchement anticipé.
    Ex : trigger_low_ratio=10 → déclenche 10% avant la fin du range low
    """
    trigger_low = -(range_percent * (trigger_low_ratio / 100))
    trigger_high = range_percent * (trigger_high_ratio / 100)
    return trigger_low, trigger_high


# ------------------------------------------------------------------------------------
# INTERFACE
# ------------------------------------------------------------------------------------

tab1, tab2 = st.tabs(["Dashboard", "Automation"])

# ------------------------------------------------------------------------------------
# ONGLET DASHBOARD
# ------------------------------------------------------------------------------------
with tab1:
    st.title("Dashboard Général")
    st.write("Contenu original conservé ici…")
    st.info("Tu peux coller ton vrai code dashboard et je l’intégrerai.")

# ------------------------------------------------------------------------------------
# ONGLET AUTOMATION
# ------------------------------------------------------------------------------------
with tab2:
    st.title("Paramètres d’Automation")

    st.subheader("Réglage du Range")
    range_percent = st.slider(
        "Range total (%)",
        min_value=1.0,
        max_value=50.0,
        value=20.0,
        step=0.5
    )

    col1, col2 = st.columns(2)

    with col1:
        ratio_low = st.number_input("Ratio bas (%)", value=20)
    with col2:
        ratio_high = st.number_input("Ratio haut (%)", value=80)

    low_offset, high_offset = compute_low_high_range(range_percent, ratio_low, ratio_high)

    st.write(f"**Range Low : {low_offset:.2f}%**")
    st.write(f"**Range High : {high_offset:.2f}%**")

    st.divider()

    # --------------------------------------------------------------------------
    # TIME BUFFER (suggestion automatique)
    # --------------------------------------------------------------------------
    st.subheader("Suggestion du Time Buffer en fonction de la volatilité")
    volatility = st.slider(
        "Volatilité (écart-type %)",
        min_value=0.1,
        max_value=10.0,
        value=2.0,
        step=0.1
    )

    buffer_suggestion = suggest_time_buffer(volatility)
    st.success(f"**Time buffer suggéré : {buffer_suggestion}**")

    st.divider()

    # --------------------------------------------------------------------------
    # TRIGGER ANTICIPÉ
    # --------------------------------------------------------------------------
    st.subheader("Trigger d’anticipation")

    col3, col4 = st.columns(2)

    with col3:
        trigger_low_ratio = st.number_input(
            "Trigger anticipation bas (%)",
            min_value=0,
            max_value=100,
            value=10
        )
    with col4:
        trigger_high_ratio = st.number_input(
            "Trigger anticipation haut (%)",
            min_value=0,
            max_value=100,
            value=90
        )

    trigger_low, trigger_high = compute_trigger_offset(
        range_percent, trigger_low_ratio, trigger_high_ratio
    )

    st.write(f"**Trigger Low anticipé : {trigger_low:.2f}%**")
    st.write(f"**Trigger High anticipé : {trigger_high:.2f}%**")

    st.info(
        "Exemple : 10/90 → déclenche 10% avant la fin du range low ou high."
    )

    st.divider()

    st.header("Récapitulatif Automation")
    st.json({
        "Range total (%)": range_percent,
        "Range Low (%)": low_offset,
        "Range High (%)": high_offset,
        "Volatilité (%)": volatility,
        "Time Buffer recommandé": buffer_suggestion,
        "Trigger anticipation bas (%)": trigger_low,
        "Trigger anticipation haut (%)": trigger_high
    })
