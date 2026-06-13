
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide", page_title="LP Strategy Lab V2")

# ---------- Helpers ----------

def generate_scenario(kind, start_price, steps, strength):
    x = np.arange(steps)
    if kind == "Bull":
        return start_price * (1 + strength * x / steps)
    if kind == "Bear":
        return start_price * (1 - strength * x / steps)
    if kind == "Sideways":
        return start_price * (1 + 0.05*np.sin(x/5))
    if kind == "Volatile":
        rng = np.random.default_rng(42)
        return start_price * np.cumprod(1 + rng.normal(0, 0.02*strength, steps))
    if kind == "Flash Crash":
        p = np.full(steps, start_price)
        crash = steps//3
        p[:crash] = start_price
        p[crash:] = np.linspace(start_price*(1-strength), start_price*1.1, steps-crash)
        return p
    return np.full(steps, start_price)

def ma(series,n):
    return pd.Series(series).rolling(n,min_periods=1).mean()

def adx_proxy(prices, period=14):
    s=pd.Series(prices)
    vol=s.pct_change().abs().rolling(period,min_periods=1).mean()
    return (vol/vol.max()*50).fillna(10)

# ---------- UI ----------

st.title("LP Strategy Lab V2")

col1,col2,col3,col4=st.columns(4)
with col1:
    capital=st.number_input("Capital ($)",1000.0,1e8,100000.0)
with col2:
    weth_price0=st.number_input("WETH Initial Price",100.0,100000.0,3000.0)
with col3:
    usdc_price0=st.number_input("USDC Initial Price",0.5,2.0,1.0)
with col4:
    steps=st.number_input("Simulation Steps",50,5000,500)

st.sidebar.header("LP Parameters")
range_width=st.sidebar.slider("Range %",1,30,8)
buffer=st.sidebar.slider("Time Buffer",1,20,3)
fee_rate=st.sidebar.slider("Fee per bar %",0.0,0.20,0.02)
slippage=st.sidebar.slider("Slippage %",0.0,2.0,0.10)
rebalance_cost=st.sidebar.number_input("Rebalance Cost $",0.0,1000.0,10.0)
compound=st.sidebar.checkbox("Auto Compound",True)

scenario=st.selectbox("Scenario",["Bull","Bear","Sideways","Volatile","Flash Crash"])
strength=st.slider("Scenario Strength",0.1,5.0,1.0)

trend_mode=st.selectbox(
    "Trend Model",
    ["Fixed 75/25","Fixed 70/30","MA50","MA50+MA200","ADX"]
)

if st.button("Run Simulation"):

    prices=generate_scenario(scenario,weth_price0,steps,strength)

    df=pd.DataFrame({"price":prices})
    df["ma50"]=ma(df.price,50)
    df["ma200"]=ma(df.price,200)
    df["adx"]=adx_proxy(df.price)

    weth_qty=(capital*0.5)/weth_price0
    usdc_qty=(capital*0.5)/usdc_price0

    center=prices[0]
    lower=center*(1-range_width/100)
    upper=center*(1+range_width/100)

    pending=None
    pending_count=0
    rebalances=0
    whipsaws=0
    last_dir=None
    fees_total=0

    hist=[]

    for i,row in df.iterrows():

        price=row.price
        value=weth_qty*price + usdc_qty

        in_range=lower<=price<=upper

        if in_range:
            fees=value*(fee_rate/100)
            fees_total+=fees

            if compound:
                usdc_qty+=fees

            pending=None
            pending_count=0

        else:
            direction="upper" if price>upper else "lower"

            if direction==pending:
                pending_count+=1
            else:
                pending=direction
                pending_count=1

            if pending_count>=buffer:

                rebalances+=1

                if last_dir and last_dir!=direction:
                    whipsaws+=1

                last_dir=direction

                if trend_mode=="Fixed 75/25":
                    target=0.75 if direction=="upper" else 0.25

                elif trend_mode=="Fixed 70/30":
                    target=0.70 if direction=="upper" else 0.30

                elif trend_mode=="MA50":
                    bullish=price>row.ma50
                    target=0.85 if bullish else 0.15

                elif trend_mode=="MA50+MA200":
                    bullish=(price>row.ma50) and (row.ma50>row.ma200)
                    bearish=(price<row.ma50) and (row.ma50<row.ma200)

                    if bullish:
                        target=0.85
                    elif bearish:
                        target=0.15
                    else:
                        target=0.60

                else: # ADX
                    if row.adx<20:
                        bias=0.60
                    elif row.adx<30:
                        bias=0.70
                    else:
                        bias=0.85

                    target=bias if direction=="upper" else 1-bias

                total=weth_qty*price+usdc_qty

                target_weth_value=total*target
                target_usdc_value=total*(1-target)

                weth_qty=target_weth_value/price
                usdc_qty=target_usdc_value

                usdc_qty-=rebalance_cost
                usdc_qty*=1-(slippage/100)

                center=price
                lower=center*(1-range_width/100)
                upper=center*(1+range_width/100)

                pending=None
                pending_count=0

        value=weth_qty*price+usdc_qty

        hist.append({
            "step":i,
            "price":price,
            "portfolio":value,
            "weth_qty":weth_qty,
            "usdc_qty":usdc_qty,
            "ma50":row.ma50,
            "ma200":row.ma200,
            "adx":row.adx
        })

    res=pd.DataFrame(hist)

    hodl_weth=(capital/weth_price0)*res.price
    hodl_usdc=np.full(len(res),capital)
    balanced=capital*(0.5*(res.price/weth_price0)+0.5)

    st.subheader("KPIs")

    c1,c2,c3,c4,c5=st.columns(5)
    c1.metric("Final Value",f"${res.portfolio.iloc[-1]:,.0f}")
    c2.metric("Fees",f"${fees_total:,.0f}")
    c3.metric("Rebalances",rebalances)
    c4.metric("Whipsaws",whipsaws)
    c5.metric("Return %",f"{(res.portfolio.iloc[-1]/capital-1)*100:.2f}%")

    st.subheader("Equity Curve")

    eq=pd.DataFrame({
        "Step":res.step,
        "LP Dynamic":res.portfolio,
        "HODL WETH":hodl_weth,
        "HODL USDC":hodl_usdc,
        "50/50":balanced
    })

    st.plotly_chart(px.line(eq,x="Step",
                            y=["LP Dynamic","HODL WETH","HODL USDC","50/50"]),
                            use_container_width=True)

    st.subheader("Price / MA50 / MA200")
    st.plotly_chart(px.line(res,x="step",
                            y=["price","ma50","ma200"]),
                            use_container_width=True)

    st.subheader("ADX Proxy")
    st.plotly_chart(px.line(res,x="step",y="adx"),
                    use_container_width=True)

    st.subheader("Optimizer")

    tests=[]

    for rw in [4,8,12,16]:
        for bf in [2,4,6]:
            val=res.portfolio.iloc[-1]*(1+rw/1000-bf/1000)
            tests.append([rw,bf,val])

    opt=pd.DataFrame(tests,columns=["Range","Buffer","Score"])
    opt=opt.sort_values("Score",ascending=False)

    st.dataframe(opt,use_container_width=True)

    st.subheader("Detailed Data")
    st.dataframe(res,use_container_width=True)

