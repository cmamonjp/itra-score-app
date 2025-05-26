import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import requests

st.title("🏃‍♂️ ITRA Score Transition & Growth Rate")

sample_csv_url = "https://raw.githubusercontent.com/cmamonjp/itra-score-app/main/data_itra_n30.csv"

@st.cache_data
def load_sample_csv():
    r = requests.get(sample_csv_url)
    return r.content

csv_bytes = load_sample_csv()

st.download_button(
    label="Download Sample CSV",
    data=csv_bytes,
    file_name="data_itra_n30.csv",
    mime="text/csv"
)

uploaded_file = st.file_uploader("Upload your CSV file (date, itra_score)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # 成長率の計算（前日比％）
    df['growth_rate'] = df['itra_score'].pct_change() * 100

    # NaNを含む行を削除（最初の行）
    df = df.dropna(subset=['growth_rate']).reset_index(drop=True)

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 白背景を明示的に指定
    fig.patch.set_facecolor('white')
    ax1.set_facecolor('white')

    # ITRA Scoreの折れ線グラフ
    ax1.plot(df['date'], df['itra_score'], color='#1f77b4', label='ITRA Score')
    ax1.set_xlabel('Date', color='black')
    ax1.set_ylabel('ITRA Score', color='#1f77b4')
    ax1.tick_params(axis='x', colors='black')
    ax1.tick_params(axis='y', labelcolor='#1f77b4')

    # 成長率は棒グラフで
    ax2 = ax1.twinx()
    width = pd.Timedelta(days=10)
    ax2.bar(df['date'], df['growth_rate'], width=width, alpha=0.3, color='#ff7f0e', label='Growth Rate (%)')
    ax2.set_ylabel('Growth Rate (%)', color='#ff7f0e')
    ax2.tick_params(axis='y', labelcolor='#ff7f0e')

    # 凡例をグラフ外右上に配置、背景白、文字黒に変更
    lines, labels = ax1.get_legend_handles_labels()
    bars, bar_labels = ax2.get_legend_handles_labels()
    leg = ax1.legend(lines + bars, labels + bar_labels, loc='upper left', bbox_to_anchor=(1.05, 1),
                     frameon=True, facecolor='white', edgecolor='black')
    for text in leg.get_texts():
        text.set_color('black')

    plt.title('ITRA Score Transition & Growth Rate', color='black')
    plt.tight_layout()

    st.pyplot(fig)

    # 画像ダウンロード用バッファ
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)

    st.download_button(
        label="Download Chart as PNG",
        data=buf,
        file_name="itra_score_growth.png",
        mime="image/png"
    )
