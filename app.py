import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

st.title("🏃‍♂️ ITRA Score Progress & Growth Rate Visualization")

uploaded_file = st.file_uploader("📂 Upload your CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    st.subheader("📊 Uploaded Data")
    st.dataframe(df)

    df['itra_growth_rate'] = df['itra_score'].pct_change() * 100
    df['itra_growth_rate'] = df['itra_growth_rate'].fillna(0)

    fig, ax1 = plt.subplots(figsize=(12, 5))

    # ITRA Score line plot
    ax1.plot(df['date'], df['itra_score'], marker='o', color='blue', label='ITRA Score')
    ax1.set_xlabel("Date")
    ax1.set_ylabel("ITRA Score", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # ITRA Score Y-axis ticks: from min to max with step 5 (adjust if needed)
    min_score = int(df['itra_score'].min() // 5 * 5)
    max_score = int((df['itra_score'].max() + 4) // 5 * 5)
    ax1.set_ylim(min_score, max_score)
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(5))

    # Growth rate bar plot with secondary y-axis
    ax2 = ax1.twinx()
    ax2.bar(df['date'], df['itra_growth_rate'], alpha=0.3, color='orange', label='Growth Rate (%)')
    ax2.set_ylabel("Growth Rate (%)", color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    # Growth rate Y-axis range fixed to -10% to 10%
    ax2.set_ylim(-10, 10)
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax2.yaxis.set_minor_locator(ticker.MultipleLocator(1))

    plt.title("ITRA Score Progress and Growth Rate Over Time")
    plt.xticks(rotation=45)

    lines, labels = ax1.get_legend_handles_labels()
    bars, bar_labels = ax2.get_legend_handles_labels()
    ax1.legend(lines + bars, labels + bar_labels, loc='upper left')

    st.pyplot(fig)

else:
    st.info("👆 Please upload a CSV file to get started.")
