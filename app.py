import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("ITRAスコア可視化")

uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(pd.to_datetime(df['date']), df['itra_score'], marker='o')
    ax.set_title("ITRA Score Progress")
    ax.set_xlabel("Date")
    ax.set_ylabel("ITRA Score")
    plt.xticks(rotation=60, fontsize=8)

    st.pyplot(fig)
