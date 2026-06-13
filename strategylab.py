
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="LP Strategy Lab", layout="wide")

st.title("LP Strategy Lab - WETH/USDC Dynamic Range Rebalancing")

st.sidebar.header("Paramètres")

capital = st.sidebar.number_input("Capital initial ($)", 1000.0, 10000000.0, 100000.0)
range_width = st.sidebar.slider("Largeur de Range (%)", 1.0, 30.0, 8.0)
buffer_bars = st.sidebar.slider("Time Buffer (nombre de points)", 1, 20, 3)
pool_fee = st.sidebar.number_input("Fees LP (%) par point in-range", 0.0, 1.0, 0.02)
slippage = st.sidebar.number_input("Slippage (%)", 0.0, 5.0, 0.10)
rebalance_cost = st.sidebar.number_input("Coût fixe rebalance ($)", 0.0, 1000.0, 10.0)
auto_compound = st.sidebar.checkbox("Auto Compound", value=False)

st.markdown("### Saisie manuelle des prix")
rows = st.number_input("Nombre de points", 10, 500, 50)

default_df = pd.DataFrame({
    "Step": list(range(rows)),
    "Price": np.linspace(3000, 3500, rows)
})

prices_df = st.data_editor(default_df, use_container_width=True)

if st.button("Lancer Backtest"):

    prices = prices_df["Price"].astype(float).tolist()

    center_price = prices[0]
    lower = center_price * (1 - range_width/100)
    upper = center_price * (1 + range_width/100)

    weth_ratio = 0.5
    usdc_ratio = 0.5

    portfolio = capital
    fees_earned = 0
    rebal_count = 0
    whipsaws = 0

    pending_trigger = None
    trigger_count = 0
    last_direction = None

    history = []

    for i, price in enumerate(prices):

        in_range = lower <= price <= upper

        if in_range:

            fee = portfolio * (pool_fee / 100)
            fees_earned += fee

            if auto_compound:
                portfolio += fee

            pending_trigger = None
            trigger_count = 0

        else:

            direction = "upper" if price > upper else "lower"

            if pending_trigger == direction:
                trigger_count += 1
            else:
                pending_trigger = direction
                trigger_count = 1

            if trigger_count >= buffer_bars:

                rebal_count += 1

                if last_direction and last_direction != direction:
                    whipsaws += 1

                last_direction = direction

                distance = abs(price - center_price) / center_price * 100

                if distance < 5:
                    strong_ratio = 0.60
                elif distance < 10:
                    strong_ratio = 0.70
                else:
                    strong_ratio = 0.85

                if direction == "upper":
                    weth_ratio = strong_ratio
                    usdc_ratio = 1 - strong_ratio
                else:
                    weth_ratio = 1 - strong_ratio
                    usdc_ratio = strong_ratio

                portfolio -= rebalance_cost
                portfolio *= (1 - slippage/100)

                center_price = price
                lower = center_price * (1 - range_width/100)
                upper = center_price * (1 + range_width/100)

                pending_trigger = None
                trigger_count = 0

        price_perf = (price / prices[0])

        synthetic_value = (
            portfolio *
            (weth_ratio * price_perf + usdc_ratio)
        )

        history.append({
            "Step": i,
            "Price": price,
            "Portfolio": synthetic_value,
            "WETH_Ratio": weth_ratio,
            "USDC_Ratio": usdc_ratio,
            "Lower": lower,
            "Upper": upper
        })

    result = pd.DataFrame(history)

    hodl_eth = capital * (result["Price"] / result["Price"].iloc[0])
    hodl_5050 = capital * (0.5 * result["Price"] / result["Price"].iloc[0] + 0.5)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Portfolio Final", f"${result['Portfolio'].iloc[-1]:,.2f}")
    c2.metric("Fees", f"${fees_earned:,.2f}")
    c3.metric("Rebalances", rebal_count)
    c4.metric("Whipsaws", whipsaws)

    equity = pd.DataFrame({
        "Step": result["Step"],
        "LP Dynamic": result["Portfolio"],
        "HODL ETH": hodl_eth,
        "50/50": hodl_5050
    })

    st.subheader("Equity Curve")

    fig = px.line(
        equity,
        x="Step",
        y=["LP Dynamic", "HODL ETH", "50/50"]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Prix et Ranges")

    fig2 = px.line(
        result,
        x="Step",
        y=["Price", "Lower", "Upper"]
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Allocation")

    alloc = result[["Step","WETH_Ratio","USDC_Ratio"]]

    fig3 = px.area(
        alloc,
        x="Step",
        y=["WETH_Ratio","USDC_Ratio"]
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Résultats détaillés")
    st.dataframe(result, use_container_width=True)

st.caption("Prototype professionnel mono-fichier Streamlit pour tester une stratégie Directional Dynamic Range Rebalancing.")
