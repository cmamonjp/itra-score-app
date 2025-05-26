import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.style.use('dark_background')

# CSV読み込み（パスは適宜変更）
df = pd.read_csv('path/to/your/data.csv')

# date列を日時型に変換
df['date'] = pd.to_datetime(df['date'])

# ソート（必須）
df = df.sort_values('date').reset_index(drop=True)

variables = ['growth_rate', 'distance', 'elevation', 'temp', 'time_h']
color_map = {
    'growth_rate': '#d62728',
    'distance': '#ff7f0e',
    'elevation': '#2ca02c',
    'temp': '#9467bd',
    'time_h': '#8c564b'
}

for var in variables:
    fig, ax1 = plt.subplots(figsize=(10, 4))

    ax1.plot(df['date'], df['itra_score'], label='ITRA Score', color='#1f77b4', linewidth=2)
    ax1.set_ylabel('ITRA Score', color='#1f77b4')
    ax1.tick_params(axis='y', colors='#1f77b4')
    ax1.grid(True, linestyle='--', alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(df['date'], df[var], label=var.capitalize(), color=color_map[var], linewidth=2)
    ax2.set_ylabel(var.capitalize(), color=color_map[var])
    ax2.tick_params(axis='y', colors=color_map[var])

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', bbox_to_anchor=(1.05, 1))

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    plt.tight_layout()

    st.pyplot(fig)
