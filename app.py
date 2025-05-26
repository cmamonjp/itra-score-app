import streamlit as st
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🏃‍♂️ ITRA Score Growth Rate Candlestick Chart")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    required_cols = {'date', 'itra_score'}
    if not required_cols.issubset(df.columns):
        st.error(f"CSV must contain columns: {', '.join(required_cols)}")
    else:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date', 'itra_score'])  # 日付やスコアに欠損あれば削除
        df = df.sort_values('date').reset_index(drop=True)

        # 成長率計算
        df['growth_rate'] = df['itra_score'].pct_change() * 100
        df = df.dropna(subset=['growth_rate'])  # 最初のNaN行を削除

        # ローソク足用の値を作成
        open_ = df['growth_rate'].shift(1).fillna(method='bfill')
        close_ = df['growth_rate']
        high_ = np.maximum(open_, close_) + 0.1  # ±少し幅をもたせる
        low_ = np.minimum(open_, close_) - 0.1

        ohlc = pd.DataFrame({
            'Open': open_,
            'High': high_,
            'Low': low_,
            'Close': close_
        }, index=df['date'])

        # tz情報を完全に落とす
        ohlc.index = pd.to_datetime(ohlc.index).tz_localize(None)

        fig, ax = plt.subplots(figsize=(12, 6))
        mpf.plot(ohlc, type='candle', style='charles', ax=ax, tight_layout=True)
        st.pyplot(fig)

else:
    st.info("Please upload a CSV file to get started.")
