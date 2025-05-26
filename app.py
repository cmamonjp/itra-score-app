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
        # 日付処理（タイムゾーン付きの可能性も排除）
        df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
        df = df.sort_values('date').reset_index(drop=True)

        # 成長率計算
        df['growth_rate'] = df['itra_score'].pct_change() * 100

        # 成長率の前日値（Open）、当日値（Close）
        o = df['growth_rate'].shift(1).fillna(0)
        c = df['growth_rate'].fillna(0)

        # High, LowはOpen, Closeの上下に±1%の振れ幅
        high = np.maximum(o, c) + 1
        low = np.minimum(o, c) - 1

        ohlc = pd.DataFrame({
            'Open': o,
            'High': high,
            'Low': low,
            'Close': c
        }, index=df['date'])

        # タイムゾーン情報を削除（mplfinanceの要件）
        ohlc.index = ohlc.index.tz_localize(None)

        # mplfinanceでろうそくチャート表示
        mpf.plot(
            ohlc,
            type='candle',
            style='charles',
            title="Growth Rate Candlestick Chart",
            ylabel='Growth Rate (%)',
            figsize=(12, 6),
            tight_layout=True,
            show_nontrading=True
        )

else:
    st.info("Please upload a CSV file to get started.")
