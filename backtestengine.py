# ----------------- SECTION IL / LP -----------------
st.markdown("<h2 style='background-color:#FFA500;color:white;padding:10px;border-radius:8px;'>Interactive Impermanent Loss (IL)</h2>", unsafe_allow_html=True)

row1_col1, row1_col2, row1_col3 = st.columns([1,1,1])
with row1_col1:
    P_deposit = st.number_input("Prix dépôt (P_deposit)", value=3000.0, format="%.6f")
with row1_col2:
    P_now = st.number_input("Prix actuel (P_now)", value=3000.0, format="%.6f")
with row1_col3:
    v_deposit = st.number_input("Valeur dépôt (USD)", value=500.0, format="%.2f")

row2_col1, row2_col2 = st.columns([1,1])
with row2_col1:
    P_lower = st.number_input("Prix lower (P_lower)", value=2800.0, format="%.6f")
with row2_col2:
    P_upper = st.number_input("Prix upper (P_upper)", value=3500.0, format="%.6f")

# FONCTIONS LP / HODL
def compute_L(P, P_l, P_u, V):
    sqrtP = np.sqrt(P)
    sqrtPl = np.sqrt(P_l)
    sqrtPu = np.sqrt(P_u)
    A = (1 / sqrtP - 1 / sqrtPu)
    B = (sqrtP - sqrtPl)
    return V / (P * A + B)

def tokens_from_L(L, P, P_l, P_u):
    sqrtP = np.sqrt(P)
    sqrtPl = np.sqrt(P_l)
    sqrtPu = np.sqrt(P_u)
    x = L * (1 / sqrtP - 1 / sqrtPu)
    y = L * (sqrtP - sqrtPl)
    return x, y

def normalize_L(L, x0, y0, P, V):
    factor = V / (x0 * P + y0)
    return L * factor, x0 * factor, y0 * factor

def x_of_P(P, L, P_upper):
    P_arr = np.asarray(P, float)
    sqrtP = np.sqrt(P_arr)
    x = L * (1 / sqrtP - 1 / np.sqrt(P_upper))
    if isinstance(x, np.ndarray):
        return np.where(x < 0, 0, x)
    return max(x, 0.0)

def y_of_P(P, L, P_lower):
    P_arr = np.asarray(P, float)
    sqrtP = np.sqrt(P_arr)
    y = L * (sqrtP - np.sqrt(P_lower))
    if isinstance(y, np.ndarray):
        return np.where(y < 0, 0, y)
    return max(y, 0.0)

def V_LP(P, L, P_lower, P_upper):
    P_arr = np.asarray(P, float)
    return x_of_P(P_arr, L, P_upper) * P_arr + y_of_P(P_arr, L, P_lower)

def V_HODL(P, x0, y0):
    return x0 * P + y0

# CALCUL
L_raw = compute_L(P_deposit, P_lower, P_upper, v_deposit)
x0_raw, y0_raw = tokens_from_L(L_raw, P_deposit, P_lower, P_upper)
L, x0, y0 = normalize_L(L_raw, x0_raw, y0_raw, P_deposit, v_deposit)

prices = np.linspace(P_lower*0.8, P_upper*1.3, 400)
LP_values = V_LP(prices, L, P_lower, P_upper)
HODL_values = V_HODL(prices, x0, y0)
IL_curve = (LP_values / HODL_values - 1) * 100

fig = go.Figure()
fig.add_trace(go.Scatter(x=prices, y=IL_curve, mode="lines", name="IL (%)", line=dict(color="red", width=3)))
fig.update_layout(height=350, title="Impermanent Loss (%) — Courbe exacte", xaxis_title="Prix", yaxis_title="IL (%)")
st.plotly_chart(fig, use_container_width=True)

IL_now = (V_LP(P_now, L, P_lower, P_upper) / V_HODL(P_now, x0, y0) - 1) * 100
LP_now = V_LP(P_now, L, P_lower, P_upper)
HODL_now = V_HODL(P_now, x0, y0)

row_metrics = st.columns(4)
row_metrics[0].metric("IL now", f"{IL_now:.2f} %")
row_metrics[1].metric("LP now", f"${LP_now:,.2f}")
row_metrics[2].metric("HODL now", f"${HODL_now:,.2f}")
row_metrics[3].metric("Liquidité dépôt", f"${L:,.2f}")
