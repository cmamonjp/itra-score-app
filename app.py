import streamlit as st
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt

st.title("🏃‍♂️ ITRA Score Growth Rate Candlestick Chart")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # CSV読み込み
    df = pd.read_csv(uploaded_file)

    # 日付カラムが 'date' ならdatetime化（名前が違ったら適宜変更）
    df['date'] = pd.to_datetime(df['date'])

    # 'itra_score'がある前提で成長率計算
    df['growth_rate'] = df['itra_score'].pct_change() * 100

    # growth_rateにNaNがあれば除去（先頭行など）
    df = df.dropna(subset=['growth_rate'])

    # open, closeの計算
    open_ = df['growth_rate'].shift(1).fillna(method='bfill')
    close_ = df['growth_rate']

    # InfやNaNがあれば補正
    open_ = open_.replace([np.inf, -np.inf], np.nan).fillna(method='bfill')
    close_ = close_.replace([np.inf, -np.inf], np.nan).fillna(method='bfill')

    # 高値・安値を上下0.1ずつオフセットして設定
    high_ = np.maximum(open_, close_) + 0.1
    low_ = np.minimum(open_, close_) - 0.1

    # OHLCデータフレーム作成
    ohlc = pd.DataFrame({
        'Open': open_,
        'High': high_,
        'Low': low_,
        'Close': close_
    }, index=df['date'])

    # ohlcにNaNやInfがあれば除去
    ohlc = ohlc.replace([np.inf, -np.inf], np.nan).dropna()

    # プロット用のFigureとAxesを準備
    fig, ax = plt.subplots(figsize=(12, 6))

    # mplfinanceでローソク足描画
    mpf.plot(
        ohlc,
        type='candle',
        style='charles',
        ax=ax,
        tight_layout=True,
        title="Growth Rate Candlestick Chart",
        ylabel='Growth Rate (%)',
        show_nontrading=True
    )

    # Streamlitで表示
    st.pyplot(fig)
