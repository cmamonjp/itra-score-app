import streamlit as st
import pandas as pd
import mplfinance as mpf

st.title("🏃‍♂️ ITRA Score Growth Rate Candlestick Chart")

# CSVアップロード
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # CSV読み込み
    df = pd.read_csv(uploaded_file)
    
    # 日付型に変換
    df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d')
    df.set_index('date', inplace=True)
    
    # mplfinance用のOHLCデータ作成（仮にopen/high/low/closeをITRAスコアの成長率から作る）
    # ここでは例として、前日との差分を元にcandlestick用に加工
    df['close'] = df['itra_score']
    df['open'] = df['itra_score'].shift(1)  # 前日のitra_score
    df['high'] = df[['open', 'close']].max(axis=1)
    df['low'] = df[['open', 'close']].min(axis=1)

    # NaNがある行は削除（shiftで最初のopenがNaNになるため）
    ohlc = df[['open', 'high', 'low', 'close']].dropna()
    
    # 描画
    st.write("## Candlestick Chart")
    fig, ax = mpf.plot(
        ohlc,
        type='candle',
        style='charles',
        figsize=(12,6),
        title="ITRA Score Growth Rate Candlestick Chart",
        ylabel="ITRA Score",
        tight_layout=True,
        returnfig=True,
        show_nontrading=True
    )
    
    st.pyplot(fig)
else:
    st.info("CSVファイルをアップロードしてください。")
