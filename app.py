import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏃‍♂️ ITRAスコア成長率可視化アプリ")

uploaded_file = st.file_uploader("📂 CSVファイルをアップロード", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    st.subheader("📊 アップロードされたデータ")
    st.dataframe(df)

    # ITRAスコア推移プロット
    st.subheader("📈 ITRAスコア推移")
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df['date'], df['itra_score'], marker='o')
    ax.set_xlabel("日付")
    ax.set_ylabel("ITRAスコア")
    ax.set_title("ITRAスコアの推移")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # 成長率計算（前回比%）
    df['itra_growth_rate'] = df['itra_score'].pct_change() * 100  # %変化率
    df['itra_growth_rate'] = df['itra_growth_rate'].fillna(0)

    st.subheader("📉 ITRAスコア成長率（前回比）")
    fig2, ax2 = plt.subplots(figsize=(12, 3))
    ax2.bar(df['date'], df['itra_growth_rate'], color='skyblue')
    ax2.set_xlabel("日付")
    ax2.set_ylabel("成長率 (%)")
    ax2.set_title("ITRAスコア成長率の推移（前回比）")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    st.markdown("💡 成長率がプラスならパフォーマンス向上、マイナスなら低下を意味します。")

else:
    st.info("👆 まずはCSVファイルをアップロードしてください。")
