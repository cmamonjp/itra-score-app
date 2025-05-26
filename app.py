import streamlit as st
import pandas as pd
import mplfinance as mpf

st.title("🏃‍♂️ ITRA Score Growth Rate Candlestick Chart")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=['date'])
    df.set_index('date', inplace=True)
    df['growth_rate'] = df['itra_score'].pct_change() * 100
    df['growth_rate'].fillna(0, inplace=True)

    ohlc = pd.DataFrame(index=df.index)
    ohlc['open'] = df['growth_rate'].shift(1).fillna(0)
    ohlc['close'] = df['growth_rate']
    ohlc['high'] = ohlc[['open', 'close']].max(axis=1)
    ohlc['low'] = ohlc[['open', 'close']].min(axis=1)

    try:
        mpf.plot(
            ohlc,
            type='candle',
            style='charles',
            title="Growth Rate Candlestick Chart",
            ylabel='Growth Rate (%)',
            tight_layout=True,
            show_nontrading=True
            # figsizeをいったん外して様子見る
        )
    except Exception as e:
        st.error(f"Plot error: {e}")
