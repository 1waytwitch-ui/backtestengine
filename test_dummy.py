import streamlit as st
import time
import requests
import numpy as np
from datetime import datetime

@st.cache_resource(ttl=30)
def test_cache():
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"⚡ FONCTION EXÉCUTÉE à {timestamp}")
    return timestamp

@st.cache_resource(ttl=30)
def test_cache_btc():
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"⚡ FONCTION test_cache_btc EXÉCUTÉE à {timestamp}")
    print(f"Récupération des données BTC depuis CoinGecko...")
    prices = get_market_chart("coinbase-wrapped-btc")


    return timestamp


def get_market_chart(asset_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{asset_id}/market_chart?vs_currency=usd&days=30&interval=daily"
        data = requests.get(url).json()
        prices = [p[1] for p in data.get("prices", [])]
        prices = np.array(prices)
        prices = prices[~np.isnan(prices)]
        prices = prices[prices > 0]
        return prices.tolist() if len(prices) > 0 else [1.0] * 30
    except:
        return [1.0] * 30

# Test du cache classique
# st.title("Test du cache")   

# Test du cache BTC from COinGecko
st.title("Test du cache BTC from CoinGecko")   


# Afficher le résultat
# result = test_cache()
result = test_cache_btc() 

st.write(f"Timestamp du cache : {result}")
st.write(f"Heure actuelle : {datetime.now().strftime('%H:%M:%S')}")

# Bouton pour forcer un refresh
if st.button("Rafraîchir la page"):
    st.rerun()
