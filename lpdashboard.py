import math
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="LP Recovery Simulator", layout="wide")

# ----------------------------------------------------------------------
# Fonctions de calcul — mécanique Uniswap v3 (liquidité concentrée)
# ----------------------------------------------------------------------

def lp_amounts(price, L, p_lower, p_upper):
    """Retourne (montant ETH, montant USDC) détenus par la position à un prix donné."""
    sqrt_p = math.sqrt(price)
    sqrt_pa = math.sqrt(p_lower)
    sqrt_pb = math.sqrt(p_upper)

    if price <= p_lower:
        x = L * (1 / sqrt_pa - 1 / sqrt_pb)   # tout en ETH
        y = 0.0
    elif price >= p_upper:
        x = 0.0
        y = L * (sqrt_pb - sqrt_pa)            # tout en USDC
    else:
        x = L * (1 / sqrt_p - 1 / sqrt_pb)
        y = L * (sqrt_p - sqrt_pa)
    return x, y


def lp_value(price, L, p_lower, p_upper):
    x, y = lp_amounts(price, L, p_lower, p_upper)
    return x * price + y


def compute_liquidity(deposit_usd, entry_price, p_lower, p_upper):
    """Déduit L à partir du montant déposé à l'entrée (doit être dans la range)."""
    sqrt_p0 = math.sqrt(entry_price)
    sqrt_pa = math.sqrt(p_lower)
    sqrt_pb = math.sqrt(p_upper)
    denom = (1 / sqrt_p0 - 1 / sqrt_pb) * entry_price + (sqrt_p0 - sqrt_pa)
    return deposit_usd / denom


# ----------------------------------------------------------------------
# UI — Section "Your position"
# ----------------------------------------------------------------------

st.title("LP DASHBOARD")


st.markdown(
    "Ta position de liquidité concentrée ETH/USDC est sortie de sa range. "
    "Cet outil montre la perte impermanente déjà verrouillée, le temps "
    "nécessaire pour la récupérer via les frais, et ce qui arrive à ton "
    "capital selon quatre façons de jouer la suite."
)

st.header("Ta position")
st.caption("Position LP concentrée ETH / USDC. Modifie n'importe quelle valeur.")

col1, col2, col3 = st.columns(3)
with col1:
    deposit = st.number_input("Montant déposé ($)", min_value=0.0, value=10_000.0, step=100.0)
    entry_price = st.number_input("Prix d'entrée (ETH, $)", min_value=0.01, value=2200.0, step=10.0)
with col2:
    current_price = st.number_input("Prix actuel (ETH, $)", min_value=0.01, value=1700.0, step=10.0)
    range_width_pct = st.slider("Largeur de range (±%)", min_value=1, max_value=80, value=15)
with col3:
    fee_apr = st.number_input("APR de frais quand dans la range (%)", min_value=0.0, value=20.0, step=1.0)
    target_price = st.number_input("Si l'ETH revient à ($)", min_value=0.01, value=2000.0, step=10.0)

col4, col5 = st.columns(2)
with col4:
    btc_price = st.number_input("Prix actuel du BTC ($)", min_value=0.01, value=60000.0, step=100.0)
with col5:
    btc_rel_strength = st.slider(
        "Force relative du BTC", min_value=0.0, max_value=2.0, value=0.85, step=0.05,
        help="1.0 = le BTC suit exactement l'ETH · <1 = le BTC est à la traîne · >1 = le BTC dépasse l'ETH",
    )

# Range de la position
p_lower = entry_price * (1 - range_width_pct / 100)
p_upper = entry_price * (1 + range_width_pct / 100)
out_of_range = current_price <= p_lower or current_price >= p_upper

L = compute_liquidity(deposit, entry_price, p_lower, p_upper)
x0, y0 = lp_amounts(entry_price, L, p_lower, p_upper)          # avoirs à l'entrée
x_now, y_now = lp_amounts(current_price, L, p_lower, p_upper)  # avoirs actuels

lp_value_now = x_now * current_price + y_now
hodl_value_now = x0 * current_price + y0  # aurait valu si on avait juste détenu x0/y0
il_dollar = lp_value_now - hodl_value_now
il_pct = (il_dollar / hodl_value_now * 100) if hodl_value_now else 0.0

daily_fee = lp_value_now * (fee_apr / 100) / 365
recoup_days = abs(il_dollar) / daily_fee if daily_fee > 0 else float("inf")

st.divider()

status_col, il_col, recoup_col = st.columns(3)
with status_col:
    st.metric("Statut de la position", "Hors range" if out_of_range else "Dans la range")
    st.caption(f"Range : ${p_lower:,.0f} — ${p_upper:,.0f}")
with il_col:
    st.metric("Perte impermanente verrouillée", f"${il_dollar:,.0f}", f"{il_pct:,.1f}%")
with recoup_col:
    if math.isfinite(recoup_days):
        st.metric("Temps de récupération par les frais", f"{recoup_days:,.0f} jours")
    else:
        st.metric("Temps de récupération par les frais", "—")
    st.caption("Valable une fois *revenu* dans la range — hors range, la position ne génère aucun frais.")

st.caption(f"Répartition actuelle : {x_now:,.4f} ETH (${x_now*current_price:,.0f}) · {y_now:,.0f} USDC")

# ----------------------------------------------------------------------
# Comparaison des 4 stratégies
# ----------------------------------------------------------------------

st.header("Où atterrit ton argent")
st.caption("Valeur du portefeuille selon le chemin de prix de l'ETH — pour chacune des 4 stratégies.")

price_range = np.linspace(current_price * 0.3, current_price * 2.5, 200)

# 1. Rester dans le LP
stay_lp = [lp_value(p, L, p_lower, p_upper) for p in price_range]

# 2. Retirer et détenir de l'ETH spot (tout converti en ETH au prix actuel)
eth_equiv_now = lp_value_now / current_price
hold_eth = [eth_equiv_now * p for p in price_range]

# 3. Moitié -> BTC
half_usd = lp_value_now / 2
eth_half_amount = half_usd / current_price
btc_amount = half_usd / btc_price
half_btc = [
    eth_half_amount * p + btc_amount * (btc_price * (1 + btc_rel_strength * (p / current_price - 1)))
    for p in price_range
]

# 4. Sortie totale en stables
exit_stables = [lp_value_now for _ in price_range]

strategies = {
    "Rester dans le LP": stay_lp,
    "Détenir ETH spot": hold_eth,
    "Moitié → BTC": half_btc,
    "Sortir en stables": exit_stables,
}

selected = st.multiselect(
    "Stratégies à afficher", list(strategies.keys()), default=list(strategies.keys())
)

fig = go.Figure()
for name in selected:
    fig.add_trace(go.Scatter(x=price_range, y=strategies[name], mode="lines", name=name))

fig.add_vline(x=current_price, line_dash="dot", line_color="gray",
              annotation_text="prix actuel", annotation_position="top")
fig.add_vline(x=target_price, line_dash="dot", line_color="orange",
              annotation_text="prix cible", annotation_position="top")

fig.update_layout(
    xaxis_title="Prix ETH ($)",
    yaxis_title="Valeur du portefeuille ($)",
    height=480,
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
)
st.plotly_chart(fig, use_container_width=True)

# Valeurs au prix cible
st.subheader(f"Valeurs si l'ETH atteint ${target_price:,.0f}")
target_cols = st.columns(len(strategies))
for col, (name, values) in zip(target_cols, strategies.items()):
    val_at_target = np.interp(target_price, price_range, values)
    col.metric(name, f"${val_at_target:,.0f}")

# ----------------------------------------------------------------------
# Option E — Extraire son ETH, emprunter, redéployer
# ----------------------------------------------------------------------

st.header("Option E · jeu avancé")
st.caption(
    "Au lieu de vendre, dépose ton ETH en collatéral (ex. sur Aave), emprunte des "
    "stablecoins contre, et redéploie ce capital. Tu gardes 100% de l'upside ETH — "
    "mais tu prends un risque de liquidation si le prix continue de baisser."
)

colA, colB, colC = st.columns(3)
with colA:
    eth_collateral = st.number_input(
        "ETH en collatéral (Ξ)", min_value=0.0, value=float(round(eth_equiv_now, 4)), step=0.01
    )
    ltv = st.slider("LTV d'emprunt (%)", min_value=1, max_value=90, value=50) / 100
with colB:
    liq_threshold = st.slider("Seuil de liquidation (%)", min_value=1, max_value=95, value=80) / 100
    borrow_apr = st.number_input("APR d'emprunt (%)", min_value=0.0, value=6.0, step=0.5)
with colC:
    deploy_apy = st.number_input("APY du capital redéployé (%)", min_value=0.0, value=12.0, step=0.5)
    horizon_months = st.slider("Horizon (mois)", min_value=1, max_value=36, value=12)

borrowable = eth_collateral * current_price * ltv
t = horizon_months / 12
debt_owed = borrowable * (1 + borrow_apr / 100 * t)
deployed_value = borrowable * (1 + deploy_apy / 100 * t)

liquidation_price = (borrowable / (eth_collateral * liq_threshold)) if eth_collateral > 0 else float("nan")
health_factor = (
    (eth_collateral * current_price * liq_threshold) / borrowable if borrowable > 0 else float("inf")
)
price_buffer_pct = (
    (current_price - liquidation_price) / current_price * 100 if current_price else float("nan")
)

net_equity_target = eth_collateral * target_price - debt_owed + deployed_value
edge_vs_hold = deployed_value - debt_owed  # == net_equity_target - (eth_collateral*target_price)

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Tu peux emprunter", f"${borrowable:,.0f}")
m2.metric("Prix de liquidation", f"${liquidation_price:,.0f}")
m3.metric("Health factor", f"{health_factor:,.2f}", help="1.0 = liquidation")

m4, m5, m6 = st.columns(3)
m4.metric("Marge de prix avant liquidation", f"{price_buffer_pct:,.1f}%")
m5.metric(f"Équité nette si ETH → ${target_price:,.0f}", f"${net_equity_target:,.0f}")
m6.metric("Avantage vs. simplement détenir de l'ETH", f"${edge_vs_hold:,.0f}")

if health_factor < 1.1 and math.isfinite(health_factor):
    st.warning("Health factor proche ou sous 1.0 — risque de liquidation élevé avec ces paramètres.")
