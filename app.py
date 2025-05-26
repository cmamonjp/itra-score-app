import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏃‍♂️ ITRA Score Growth Rate Visualization")

uploaded_file = st.file_uploader("📂 Upload your CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    st.subheader("📊 Uploaded Data")
    st.dataframe(df)

    # Plot ITRA score over time
    st.subheader("📈 ITRA Score Over Time")
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df['date'], df['itra_score'], marker='o')
    ax.set_xlabel("Date")
    ax.set_ylabel("ITRA Score")
    ax.set_title("ITRA Score Progression")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Calculate growth rate (percentage change from previous score)
    df['itra_growth_rate'] = df['itra_score'].pct_change() * 100  # percentage
    df['itra_growth_rate'] = df['itra_growth_rate'].fillna(0)

    st.subheader("📉 ITRA Score Growth Rate (Compared to Previous)")
    fig2, ax2 = plt.subplots(figsize=(12, 3))
    ax2.bar(df['date'], df['itra_growth_rate'], color='skyblue')
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Growth Rate (%)")
    ax2.set_title("ITRA Score Growth Rate Over Time")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    st.markdown("💡 A positive growth rate means improvement, while a negative one means performance decline.")

else:
    st.info("👆 Please upload a CSV file to get started.")
