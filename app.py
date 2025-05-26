import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import lightgbm as lgb
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from datetime import datetime

st.set_page_config(layout="wide")
st.title("🏃‍♂️ ITRAスコア可視化＆予測アプリ")

# --- CSVアップロード ---
uploaded_file = st.file_uploader("📂 CSVファイルをアップロード", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['date'] = pd.to_datetime(df['date'])

    st.subheader("📊 アップロードされたデータ")
    st.dataframe(df)

    # --- ITRAスコアの推移 ---
    st.subheader("📈 ITRAスコアの推移")
    fig1, ax1 = plt.subplots(figsize=(12, 4))
    ax1.plot(df['date'], df['itra_score'], marker='o', color='blue')
    ax1.set_title("ITRA Score Over Time")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("ITRA Score")
    plt.xticks(rotation=60, fontsize=8)
    st.pyplot(fig1)

    # --- 相関分析 ---
    st.subheader("📐 相関分析")
    cols_to_use = ['itra_score', 'temp', 'time_h', 'course_condition']
    corr = df[cols_to_use].corr()
    corr_itra = corr.loc['itra_score', :].drop('itra_score')

    fig2, ax2 = plt.subplots(figsize=(6, 3))
    ax2.bar(corr_itra.index, corr_itra.values, color=['skyblue', 'salmon', 'limegreen'])
    ax2.set_ylim(-1, 1)
    ax2.set_title("ITRA Score 相関")
    st.pyplot(fig2)

    st.markdown("💡 *天気やコース状況など、数値化された項目に対して相関を表示しています。*")

    # --- 特徴量加工 ---
    df['month'] = df['date'].dt.month
    df['dayofweek'] = df['date'].dt.dayofweek
    df['days_since_start'] = (df['date'] - df['date'].min()).dt.days

    features = ['distance', 'elevation', 'temp', 'course_condition', 'month', 'dayofweek', 'days_since_start']
    target_time = 'time_h'
    target_score = 'itra_score'

    X = df[features]
    y_time = df[target_time]
    y_score = df[target_score]

    # --- 学習・予測 ---
    X_train, X_val, y_time_train, y_time_val, y_score_train, y_score_val = train_test_split(
        X, y_time, y_score, test_size=0.2, random_state=42
    )

    model_time = lgb.LGBMRegressor()
    model_time.fit(X_train, y_time_train)

    model_score = lgb.LGBMRegressor()
    model_score.fit(X_train, y_score_train)

    pred_time = model_time.predict(X_val)
    pred_score = model_score.predict(X_val)

    rmse_time = np.sqrt(mean_squared_error(y_time_val, pred_time))
    rmse_score = np.sqrt(mean_squared_error(y_score_val, pred_score))

    st.subheader("📉 モデル評価 (RMSE)")
    st.markdown(f"- `⏱ time_h`: **{rmse_time:.2f} 時間**")
    st.markdown(f"- `🎯 itra_score`: **{rmse_score:.2f} 点**")

    # --- 予測フォーム ---
    st.subheader("🔮 次のレースの予測")

    start_date = df['date'].min().date()
    with st.form("prediction_form"):
        st.write(f"📅 初回レース日: {start_date}")
        pred_date = st.date_input("📆 次のレース日を入力", value=start_date)
        distance = st.number_input("距離 (km)", value=50)
        elevation = st.number_input("累積標高 (m)", value=2500)
        temp = st.number_input("気温 (℃)", value=20)
        course_condition = st.selectbox("コース状況", options=[0, 1], format_func=lambda x: "良好" if x == 0 else "悪路")

        submitted = st.form_submit_button("予測する")

    if submitted:
        st.write("予測処理開始")
        st.write(input_data)
        st.write(f"予測タイム: {pred_time}, 予測スコア: {pred_score}")

        month = pred_date.month
        dayofweek = pred_date.weekday()
        days_since_start = (pred_date - start_date).days

        input_data = pd.DataFrame([{
            'distance': distance,
            'elevation': elevation,
            'temp': temp,
            'course_condition': course_condition,
            'month': month,
            'dayofweek': dayofweek,
            'days_since_start': days_since_start
        }])

        pred_time = model_time.predict(input_data)[0]
        pred_score = model_score.predict(input_data)[0]

        st.success(f"⏱ 予測タイム: **{pred_time:.2f} 時間**")
        st.success(f"🎯 予測ITRAスコア: **{pred_score:.0f} 点**")

else:
    st.info("👆 上のフォームからCSVファイルをアップロードしてください。")
