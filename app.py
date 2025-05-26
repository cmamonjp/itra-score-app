import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.title("🏃‍♂️ ITRA Score Transition & Growth Rate")

uploaded_file = st.file_uploader("Upload your CSV file (date, itra_score)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # 成長率の計算（前日比％）
    df['growth_rate'] = df['itra_score'].pct_change() * 100
    df = df.dropna(subset=['growth_rate']).reset_index(drop=True)

    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('white')  # 背景は白

    # ITRA Scoreの折れ線グラフ
    ax1.plot(df['date'], df['itra_score'], color='#1f77b4', label='ITRA Score')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('ITRA Score', color='#1f77b4')
    ax1.tick_params(axis='y', labelcolor='#1f77b4')
    ax1.tick_params(axis='x', rotation=45)  # ラベルを45度回転して見やすく

    # y軸グリッドは消すけど、x軸はそのままにする
    ax1.grid(False, axis='y')

    # 成長率の棒グラフ（右軸）
    ax2 = ax1.twinx()
    width = pd.Timedelta(days=10)
    ax2.bar(df['date'], df['growth_rate'], width=width, alpha=0.3, color='#ff7f0e', label='Growth Rate (%)')
    ax2.set_ylabel('Growth Rate (%)', color='#ff7f0e')
    ax2.tick_params(axis='y', labelcolor='#ff7f0e')

    # 成長率側のy軸グリッドだけ表示
    ax2.grid(True, axis='y', linestyle='--', alpha=0.5)

    # 凡例をグラフ外右上に
    lines, labels = ax1.get_legend_handles_labels()
    bars, bar_labels = ax2.get_legend_handles_labels()
    ax1.legend(lines + bars, labels + bar_labels, loc='upper left', bbox_to_anchor=(1.05, 1))

    fig.autofmt_xdate()  # 日付ラベルの整形
    plt.title('ITRA Score Transition & Growth Rate')
    plt.tight_layout()

    st.pyplot(fig)

    # 画像DL用バッファ
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)

    st.download_button(
        label="Download Chart as PNG",
        data=buf,
        file_name="itra_score_growth.png",
        mime="image/png"
    )
