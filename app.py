import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏃‍♂️ ITRA Score & Growth Rate Chart")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # CSV読み込み
    df = pd.read_csv(uploaded_file, parse_dates=['date'])
    
    # 日付昇順にソート
    df = df.sort_values('date')
    
    # 成長率（前回比％）計算
    df['growth_rate'] = df['itra_score'].pct_change() * 100
    
    fig, ax1 = plt.subplots(figsize=(12,6))
    
    # 折れ線：ITRAスコア
    ax1.plot(df['date'], df['itra_score'], color='blue', marker='o', label='ITRA Score')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('ITRA Score', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    # 2軸目を作成
    ax2 = ax1.twinx()
    # 棒グラフ：成長率
    ax2.bar(df['date'], df['growth_rate'], color='orange', alpha=0.5, label='Growth Rate (%)')
    ax2.set_ylabel('Growth Rate (%)', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')
    
    # タイトルと凡例
    plt.title('ITRA Score & Growth Rate Over Time')
    fig.tight_layout()
    
    # 凡例をまとめて表示
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
    
    st.pyplot(fig)
else:
    st.info("Please upload a CSV file containing 'date' and 'itra_score' columns.")
