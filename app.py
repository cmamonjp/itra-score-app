import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    st.subheader("📐 相関分析")

    # --- 相関分析用の計算 ---
    cols_to_use = ['itra_score', 'temp', 'time_h', 'course_condition']
    corr = df[cols_to_use].corr()

    # --- ITRAスコアとの相関のみ抽出 ---
    corr_itra = corr.loc['itra_score', :].drop('itra_score')  # itra_score自身は除外

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    bars = ax2.bar(corr_itra.index, corr_itra.values, color=['skyblue', 'salmon', 'limegreen'])
    
    ax2.set_ylim(-1, 1)
    ax2.set_ylabel("Correlation with ITRA Score")
    ax2.set_title("ITRA Score vs Other Variables")
    
    plt.xticks(rotation=45, ha='right', fontsize=8)
    st.pyplot(fig2)

    st.markdown("💡 *ヒートマップは数値列のみを対象にしています。天気やコース状況は数値化が必要です。*")
else:
    st.info("👆 上のフォームからCSVファイルをアップロードしてください。")
