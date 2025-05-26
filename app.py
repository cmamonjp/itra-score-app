import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from io import BytesIO
import base64

st.title("🏃‍♂️ ITRA Score Transition & Growth Rate with Trend Analysis")

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください（日付, itra_score列のみ必須）", type="csv")

def create_plot(df):
    # 欠損値・異常値の削除
    df = df.dropna(subset=['itra_score'])
    df = df[df['itra_score'] >= 0]  # ITRAスコアは負にならないはず

    if len(df) < 3:
        st.error("データが少なすぎます。3行以上の有効データが必要です。")
        return None

    # 日付をdatetime変換・ソート
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date']).sort_values('date').reset_index(drop=True)

    # 成長率計算（前回比％）
    df['growth_rate'] = df['itra_score'].pct_change() * 100

    # 移動平均（3点移動平均）
    df['itra_sma'] = df['itra_score'].rolling(window=3).mean()

    # 線形回帰トレンド
    x = np.arange(len(df)).reshape(-1,1)
    y = df['itra_score'].values.reshape(-1,1)
    model = LinearRegression()
    model.fit(x, y)
    trend = model.predict(x).flatten()

    # プロット準備
    fig, ax1 = plt.subplots(figsize=(12,6))
    plt.style.use('dark_background')

    # ITRAスコア折れ線＋移動平均
    ax1.plot(df['date'], df['itra_score'], label='ITRA Score', color='#1f77b4', linewidth=2)
    ax1.plot(df['date'], df['itra_sma'], label='3-Point Moving Avg', color='#ff7f0e', linestyle='--', linewidth=2)
    ax1.plot(df['date'], trend, label='Trend Line (Linear Reg)', color='#2ca02c', linewidth=2)

    ax1.set_ylabel('ITRA Score', color='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.tick_params(axis='x', colors='white')
    ax1.grid(True, linestyle='--', alpha=0.3)

    # 成長率の棒グラフ（二軸）
    ax2 = ax1.twinx()
    ax2.bar(df['date'], df['growth_rate'], width=5, alpha=0.5, color='#d62728', label='Growth Rate (%)')
    ax2.set_ylabel('Growth Rate (%)', color='#d62728')
    ax2.tick_params(axis='y', colors='#d62728')

    # 凡例を枠外右側に表示
    lines_labels = [ax1.get_legend_handles_labels(), ax2.get_legend_handles_labels()]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    ax1.legend(lines, labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

    plt.title("ITRA Score Transition and Growth Rate with Trend Analysis", color='white', fontsize=16)
    plt.tight_layout(rect=[0,0,0.85,1])  # 凡例のスペース確保

    return fig

def get_image_download_link(fig, filename="itra_score_plot.png"):
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches='tight')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="{filename}">⬇️ 画像をダウンロード</a>'
    return href

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        required_cols = {'date','itra_score'}
        if not required_cols.issubset(df.columns):
            st.error("CSVに必要な列がありません。'date'と'itra_score'列が必須です。")
        else:
            fig = create_plot(df)
            if fig:
                st.pyplot(fig)
                st.markdown(get_image_download_link(fig), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"ファイル処理中にエラーが発生しました: {e}")
else:
    st.info("上のアップローダーからCSVファイルを選択してください。")

