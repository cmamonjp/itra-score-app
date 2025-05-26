import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import lightgbm as lgb
import numpy as np

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

    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error
    
    # 日付加工
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['dayofweek'] = df['date'].dt.dayofweek
    df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
    
    features = ['distance', 'elevation', 'temp', 'course_condition', 'month', 'dayofweek', 'days_since_start']
    target_time = 'time_h'
    target_score = 'itra_score'
    
    X = df[features]
    y_time = df[target_time]
    y_score = df[target_score]
    
    # 同時に分割
    X_train, X_val, y_time_train, y_time_val, y_score_train, y_score_val = train_test_split(X, y_time, y_score, test_size=0.2, random_state=42)
    
    # モデル学習
    model_time = lgb.LGBMRegressor()
    model_time.fit(X_train, y_time_train)
    
    model_score = lgb.LGBMRegressor()
    model_score.fit(X_train, y_score_train)
    
    # 予測と評価
    pred_time = model_time.predict(X_val)
    pred_score = model_score.predict(X_val)

    # squared=False が使えないなら自分でsqrt取る
    rmse_time = np.sqrt(mean_squared_error(y_time_val, pred_time))
    rmse_score = np.sqrt(mean_squared_error(y_score_val, pred_score))
    
    st.write("time_h RMSE:", rmse_time)
    st.write("itra_score RMSE:", rmse_score)

else:
    st.info("👆 上のフォームからCSVファイルをアップロードしてください。")
