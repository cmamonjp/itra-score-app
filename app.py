import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import requests

st.title("🏃‍♂️ ITRA Score Transition & Growth Rate")

sample_csv_url = "https://raw.githubusercontent.com/cmamonjp/itra-score-app/main/data_itra_n30.csv"

@st.cache_data
def load_sample_csv():
    try:
        r = requests.get(sample_csv_url)
        r.raise_for_status()
        return r.content
    except requests.RequestException:
        st.error("Failed to download the sample CSV. Please check your internet connection.")
        return None

csv_bytes = load_sample_csv()

if csv_bytes:
    st.download_button(
        label="Download Sample CSV",
        data=csv_bytes,
        file_name="data_itra_n30.csv",
        mime="text/csv"
    )

 # サンプルCSVのプレビュー表示
        df_sample = pd.read_csv(io.BytesIO(csv_bytes), parse_dates=["date"])
        st.write("### Sample CSV Preview")
        st.dataframe(df_sample.head(10))

uploaded_file = st.file_uploader("Upload your CSV file (date, itra_score)", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, parse_dates=["date"])
        if not {'date', 'itra_score'}.issubset(df.columns):
            st.error("The CSV file must contain both 'date' and 'itra_score' columns.")
        else:
            df = df.sort_values("date").reset_index(drop=True)

            df['growth_rate'] = df['itra_score'].pct_change() * 100
            df = df.dropna(subset=['growth_rate']).reset_index(drop=True)

            fig, ax1 = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('white')
            ax1.set_facecolor('white')

            ax1.plot(df['date'], df['itra_score'], color='#1f77b4', label='ITRA Score')
            ax1.set_xlabel('Date', color='black')
            ax1.set_ylabel('ITRA Score', color='#1f77b4')
            ax1.tick_params(axis='x', colors='black')
            ax1.tick_params(axis='y', labelcolor='#1f77b4')

            ax2 = ax1.twinx()
            width = pd.Timedelta(days=10)
            ax2.bar(df['date'], df['growth_rate'], width=width, alpha=0.3, color='#ff7f0e', label='Growth Rate (%)')
            ax2.set_ylabel('Growth Rate (%)', color='#ff7f0e')
            ax2.tick_params(axis='y', labelcolor='#ff7f0e')

            lines, labels = ax1.get_legend_handles_labels()
            bars, bar_labels = ax2.get_legend_handles_labels()
            leg = ax1.legend(lines + bars, labels + bar_labels, loc='upper left', bbox_to_anchor=(1.05, 1),
                             frameon=True, facecolor='white', edgecolor='black')
            for text in leg.get_texts():
                text.set_color('black')

            plt.title('ITRA Score Transition & Growth Rate', color='black')
            plt.tight_layout()

            st.pyplot(fig)

            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches='tight', facecolor=fig.get_facecolor())
            buf.seek(0)

            st.download_button(
                label="Download Chart as PNG",
                data=buf,
                file_name="itra_score_growth.png",
                mime="image/png"
            )

    except Exception as e:
        st.error(f"Error loading or processing file: {e}")
