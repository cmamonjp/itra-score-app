import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏃‍♂️ ITRA Score & Growth Rate Chart")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['date'])
    df = df.sort_values('date')
    df['growth_rate'] = df['itra_score'].pct_change() * 100

    fig, ax1 = plt.subplots(figsize=(12,6))
    
    # ITRAスコア（折れ線） - 青よりも濃いネイビー
    ax1.plot(df['date'], df['itra_score'], color='#003366', marker='o', label='ITRA Score')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('ITRA Score', color='#003366')
    ax1.tick_params(axis='y', labelcolor='#003366')
    ax1.grid(True, which='both', axis='y', linestyle='--', alpha=0.3)
    
    ax2 = ax1.twinx()
    # 成長率（棒グラフ） - はっきり見えるオレンジより強めの赤橙
    ax2.bar(df['date'], df['growth_rate'], color='#FF4500', alpha=0.7, label='Growth Rate (%)')
    ax2.set_ylabel('Growth Rate (%)', color='#FF4500')
    ax2.tick_params(axis='y', labelcolor='#FF4500')

    plt.title('ITRA Score & Growth Rate Over Time')
    fig.tight_layout()

    # 凡例を右枠外に配置
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    st.pyplot(fig)

else:
    st.info("Please upload a CSV file containing 'date' and 'itra_score' columns.")
