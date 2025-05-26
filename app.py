import streamlit as st
import pandas as pd
import numpy as np
import mplfinance as mpf

st.title("🏃‍♂️ ITRA Score Growth Rate Candlestick Chart")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=['date'])

    # 日付をインデックスに設定
    df.set_index('date', inplace=True)

    # 成長率 = (今回のスコア / 前回のスコア - 1) * 100 (%)
    df['growth_rate'] = df['itra_score'].pct_change() * 100

    # NaN（最初の行）を0に置換
    df['growth_rate'].fillna(0, inplace=True)

    # ローソクチャート用のOHLCデータ作成  
    # ここでは単純に成長率を元にしたダミーOHLCを作る
    ohlc = pd.DataFrame(index=df.index)
    ohlc['open'] = df['growth_rate'].shift(1).fillna(0)
    ohlc['close'] = df['growth_rate']
    ohlc['high'] = ohlc[['open', 'close']].max(axis=1)
    ohlc['low'] = ohlc[['open', 'close']].min(axis=1)

    # mplfinanceはvolumeカラムなくても動く
    # プロット
    try:
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
    except Exception as e:
        st.error(f"Plot error: {e}")

