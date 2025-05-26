import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("🏃‍♂️ ITRAスコア可視化＆分析アプリ")

# --- ファイルアップロード ---
uploaded_file = st.file_uploader("📂 CSVファイルをアップロード", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 アップロードされたデータ")
    st.write(df)

    # --- ITRAスコアの推移グラフ ---
    st.subheader("📈 ITRAスコアの推移")
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(pd.to_datetime(df['date']), df['itra_score'], marker='o', color='blue')
    ax1.set_title("ITRA Score Over Time", fontsize=14)
    ax1.set_xlabel("Date")
    ax1.set_ylabel("ITRA Score")
    plt.xticks(rotation=60, fontsize=8)
    st.pyplot(fig1)

    # --- 相関ヒートマップ ---
    st.subheader("📐 相関分析ヒートマップ（数値列のみ）")

    # 数値データだけを抽出（例：itra_score, distance, elevation, conditionなど）
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    corr = df[numeric_cols].corr()

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax2, fmt=".2f", vmin=-1, vmax=1)
    
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right', fontsize=8)
    ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0, fontsize=8)

    fig2.tight_layout()
    st.pyplot(fig2)

    st.markdown("💡 *ヒートマップは数値列のみを対象にしています。天気やコース状況は数値化が必要です。*")
else:
    st.info("👆 上のフォームからCSVファイルをアップロードしてください。")
