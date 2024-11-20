import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Snowflakeの接続情報を設定
user = 'Fujii_Kotaro'
password = 'Fujimitu13'
account = 'ELNQWKZ.MY89942'
database = 'SMOOTHIES'
schema = 'PUBLIC'
warehouse = 'COMPUTE_WH'

# グローバル変数として接続を保持
if 'engine' not in st.session_state:
    try:
        # 接続文字列を作成
        connection_string = f'snowflake://{user}:{password}@{account}.snowflakecomputing.com/{database}/{schema}?warehouse={warehouse}'
        st.session_state.engine = create_engine(connection_string)
        st.success("接続が成功しました。")
    except Exception as e:
        st.error(f"接続の確立中にエラーが発生しました: {e}")

# アプリのタイトルを表示
st.title("個人情報検索アプリ")

# ユーザーに氏名を入力してもらう
name_input = st.text_input("氏名を入力してください:")

if name_input:
    # SQLAlchemyを使い、ハンドラーから提供された接続を使用してデータを取得
    query = "SELECT * FROM SMOOTHIES.PUBLIC.DUMMY WHERE NAME = :name"

    try:
        # データを取得
        df = pd.read_sql(query, st.session_state.engine, params={"name":name_input})

        if not df.empty:
            個人情報の表示
            st.write("個人情報:")
            st.dataframe(df)
        else:
            st.error("該当する氏名が見つかりませんでした。")
    except Exception as e:
        st.error(f"データの取得中にエラーが発生しました: {e}")

# アプリの説明
st.write("氏名を入力すると、対応する個人情報が表示されます。")
