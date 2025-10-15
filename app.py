import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Equity Correlation Finder", page_icon="📈")

st.title("📊 Equity Correlation Finder (Live via Yahoo Finance)")
st.write("Enter any Indian equity symbol (e.g. **RELIANCE.NS**, **TCS.NS**, **INFY.NS**) to find the top correlated stocks.")

# ----------------------------
# DEFAULT STOCK LIST
# ----------------------------
indian_stocks = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "SBIN.NS", "ITC.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
    "LT.NS", "BAJFINANCE.NS", "AXISBANK.NS", "ASIANPAINT.NS", "MARUTI.NS",
    "SUNPHARMA.NS", "HCLTECH.NS", "ULTRACEMCO.NS", "WIPRO.NS", "NESTLEIND.NS",
    "POWERGRID.NS", "ONGC.NS", "NTPC.NS", "TITAN.NS", "TATASTEEL.NS",
    "ADANIENT.NS", "COALINDIA.NS", "BAJAJFINSV.NS", "TECHM.NS", "JSWSTEEL.NS"
]

# ----------------------------
# DATA FETCHING
# ----------------------------
@st.cache_data(show_spinner=True)
def fetch_data(symbols, start, end):
    data = yf.download(symbols, start=start, end=end, interval="1d", progress=False)["Close"]
    data = data.dropna(axis=1, how='any')
    return data

# ----------------------------
# CORRELATION COMPUTATION
# ----------------------------
@st.cache_data
def compute_correlation(data):
    returns = data.pct_change().dropna()
    corr_matrix = returns.corr()
    return corr_matrix

# ----------------------------
# INPUT SECTION
# ----------------------------
symbol = st.text_input("Enter equity symbol (e.g. RELIANCE.NS):", value="RELIANCE.NS")

if st.button("Find Correlations"):
    with st.spinner("Fetching live market data..."):
        end = datetime.today()
        start = end - timedelta(days=365)
        data = fetch_data(indian_stocks, start, end)
        corr_matrix = compute_correlation(data)
    
    if symbol not in corr_matrix.columns:
        st.error("Symbol not found! Please check your input (include .NS suffix).")
    else:
        correlations = corr_matrix[symbol].sort_values(ascending=False)
        top_pos = correlations[1:6]  # Skip self-correlation
        top_neg = correlations[-5:]

        st.success(f"✅ Found correlations for **{symbol}**")

        st.subheader("Top 5 Positively Correlated Stocks")
        st.table(top_pos)

        st.subheader("Top 5 Negatively Correlated Stocks")
        st.table(top_neg)

        # Optional visualization
        st.subheader("📉 Correlation Distribution")
        st.bar_chart(correlations)

st.caption("Data source: Yahoo Finance (updated live)")
