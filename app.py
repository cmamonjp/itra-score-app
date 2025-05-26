import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🏃‍♂️ ITRA Score Growth Visualization")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 必須カラムチェック
    required_cols = {'date', 'itra_score'}
    if not required_cols.issubset(df.columns):
        st.error(f"CSV must contain these columns: {', '.join(required_cols)}")
    else:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')

        # 日付範囲指定UI
        min_date = df['date'].min()
        max_date = df['date'].max()
        date_range = st.date_input("Select date range", [min_date, max_date], min_value=min_date, max_value=max_date)
        if len(date_range) == 2:
            start_date, end_date = date_range
            mask = (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))
            df = df.loc[mask]

        if len(df) < 2:
            st.warning("Not enough data in the selected date range to calculate growth rate.")
        else:
            df['growth_rate'] = df['itra_score'].pct_change() * 100

            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(df['date'], df['itra_score'], marker='o', label='ITRA Score', color='#1f77b4')
            ax.set_ylabel('ITRA Score', fontsize=12)
            ax.grid(True, which='both', axis='y', linestyle='--', alpha=0.7)
            ax.tick_params(axis='x', rotation=45)
            ax.legend(loc='upper left', fontsize=10)

            ax2 = ax.twinx()
            ax2.plot(df['date'], df['growth_rate'], marker='x', label='Growth Rate (%)', color='#2ca02c')
            ax2.set_ylabel('Growth Rate (%)', fontsize=12)
            ax2.legend(loc='upper right', fontsize=10)

            st.pyplot(fig)

            # 最初のNaNに対する説明
            if pd.isna(df['growth_rate'].iloc[0]):
                st.info("Note: The first growth rate value is undefined because there's no previous data point.")

            latest_growth = df['growth_rate'].iloc[-1]

            # フィードバック文言バリエーション
            if latest_growth > 5:
                msg = f"🔥 Awesome! Your latest growth rate is {latest_growth:.2f}%. Keep the momentum going!"
                st.success(msg)
            elif latest_growth > 0:
                msg = f"Good job! Your latest growth rate is {latest_growth:.2f}%. Keep it up!"
                st.success(msg)
            elif latest_growth < -5:
                msg = f"⚠️ Warning: Your latest growth rate is {latest_growth:.2f}%. Consider reviewing your training plan seriously."
                st.error(msg)
            elif latest_growth < 0:
                msg = f"Caution: Your latest growth rate is {latest_growth:.2f}%. Small setbacks happen; analyze and adjust."
                st.warning(msg)
            else:
                st.info("Your growth rate is stable. Maintain your current efforts!")

else:
    st.info("Please upload a CSV file to get started.")
