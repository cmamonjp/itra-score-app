import streamlit as st
import pandas as pd
import numpy as np
import mplfinance as mpf

st.set_page_config(layout="wide")
st.title("🏃‍♂️ ITRA Score Growth Rate Candlestick Chart")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    required_cols = {'date', 'itra_score'}
    if not required_cols.issubset(df.columns):
        st.error(f"CSV must contain columns: {', '.join(required_cols)}")
    else:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)

        # 成長率計算
        df['growth_rate'] = df['itra_score'].pct_change() * 100

        # ろうそくチャート用のOHLCを成長率の差分から作る
        # 「Open」は前日の成長率、「Close」は当日の成長率
        # 「High」と「Low」はOpen, Close周辺に小さな振れ幅を付与（±1%）で代用

        o = df['growth_rate'].shift(1)  # 前日
        c = df['growth_rate']           # 当日

        # NaNを埋める（先頭はNaNになるので0に）
        o.fillna(0, inplace=True)
        c.fillna(0, inplace=True)

        high = np.maximum(o, c) + 1
        low = np.minimum(o, c) - 1

        ohlc = pd.DataFrame({
            'Open': o,
            'High': high,
            'Low': low,
            'Close': c
        }, index=df['date'])

        # mplfinanceで表示
        mpf.plot(ohlc, type='candle', style='charles',
                 title="Growth Rate Candlestick Chart",
                 ylabel='Growth Rate (%)',
                 figsize=(12,6),
                 tight_layout=True)

else:
    st.info("Please upload a CSV file to get started.")
