import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.title("ITRA Score & Growth Rate Chart")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['date'])

    # 日付をインデックスにセット
    df.set_index('date', inplace=True)

    # 成長率を計算（前日比 %）
    df['growth_rate'] = df['itra_score'].pct_change() * 100

    fig, ax1 = plt.subplots(figsize=(12,6))

    # ITRAスコアの折れ線
    color_score = '#1f77b4'  # 青系
    ax1.set_xlabel('Date')
    ax1.set_ylabel('ITRA Score', color=color_score)
    ax1.plot(df.index, df['itra_score'], color=color_score, label='ITRA Score', linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color_score)

    # 右軸：成長率
    ax2 = ax1.twinx()
    color_growth = '#ff7f0e'  # オレンジ系
    ax2.set_ylabel('Growth Rate (%)', color=color_growth)
    ax2.plot(df.index, df['growth_rate'], color=color_growth, label='Growth Rate (%)', linewidth=2, linestyle='--')
    ax2.tick_params(axis='y', labelcolor=color_growth)

    # 凡例を枠外右上に表示
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    plt.title("ITRA Score and Growth Rate Over Time")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    # 画像バッファ用意
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    st.pyplot(fig)

    st.download_button(
        label="Download Chart as PNG",
        data=buf,
        file_name="itra_growth_chart.png",
        mime="image/png"
    )
