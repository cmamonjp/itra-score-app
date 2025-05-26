import streamlit as st
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt

st.title("🏃‍♂️ ITRA Score Growth Rate Candlestick Chart")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['date'] = pd.to_datetime(df['date'])
    
    # 元データ確認
    st.write("Raw data preview:", df.head())
    st.write("Total rows:", len(df))
    
    # 成長率計算
    df['growth_rate'] = df['itra_score'].pct_change() * 100
    st.write("After pct_change, growth_rate preview:", df['growth_rate'].head())
    
    # NaNの数も確認
    st.write("NaN count in growth_rate:", df['growth_rate'].isna().sum())
    
    # NaN削除前の行数を記録
    before_drop = len(df)
    
    # NaN削除
    df = df.dropna(subset=['growth_rate'])
    after_drop = len(df)
    st.write(f"Rows before dropna: {before_drop}, after dropna: {after_drop}")
    
    if after_drop == 0:
        st.error("成長率計算後、データが全て消えてしまいました。入力データを確認してください。")
        st.stop()
    
    # open/close作成
    open_ = df['growth_rate'].shift(1)
    close_ = df['growth_rate']
    
    # fillnaはbfillじゃなくてffillにしてみる
    open_ = open_.replace([np.inf, -np.inf], np.nan).fillna(method='ffill')
    close_ = close_.replace([np.inf, -np.inf], np.nan).fillna(method='ffill')
    
    # もう一回NaN確認
    st.write("NaN in open_ after fillna:", open_.isna().sum())
    st.write("NaN in close_ after fillna:", close_.isna().sum())
    
    # Nanが残ってたらエラーで止める
    if open_.isna().sum() > 0 or close_.isna().sum() > 0:
        st.error("openまたはcloseにNaNが残っています。入力データを確認してください。")
        st.stop()
    
    high_ = np.maximum(open_, close_) + 0.1
    low_ = np.minimum(open_, close_) - 0.1
    
    ohlc = pd.DataFrame({
        'Open': open_,
        'High': high_,
        'Low': low_,
        'Close': close_
    }, index=df['date'])
    
    # ohlcのNaN/Inf除去
    ohlc = ohlc.replace([np.inf, -np.inf], np.nan).dropna()
    st.write(f"OHLC data rows after dropna: {len(ohlc)}")
    
    if len(ohlc) == 0:
        st.error("OHLCデータが空になりました。入力データを見直してください。")
        st.stop()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
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
    st.pyplot(fig)
