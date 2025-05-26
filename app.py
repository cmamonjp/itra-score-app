import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.title("ITRA Score と成長率の推移グラフ")

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=['csv'])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    # 成長率（%）を計算（前回との差分÷前回値×100）
    df['growth_rate'] = df['itra_score'].pct_change() * 100

    fig, ax1 = plt.subplots(figsize=(10, 5))
    plt.style.use('dark_background')

    # ITRA Score（左軸）
    ax1.plot(df['date'], df['itra_score'], label='ITRA Score', color='#1f77b4', linewidth=2)
    ax1.set_ylabel('ITRA Score', color='#1f77b4')
    ax1.tick_params(axis='y', colors='#1f77b4')
    ax1.grid(True, linestyle='--', alpha=0.3)

    # 成長率（右軸）
    ax2 = ax1.twinx()
    ax2.bar(df['date'], df['growth_rate'], label='Growth Rate (%)', color='#d62728', alpha=0.6)
    ax2.set_ylabel('Growth Rate (%)', color='#d62728')
    ax2.tick_params(axis='y', colors='#d62728')

    # 凡例を枠外に配置
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', bbox_to_anchor=(1.05, 1))

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    plt.tight_layout()

    st.pyplot(fig)
