# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Snowflake接続情報を辞書として指定
connection_parameters = {
    "account": "ELNQWKZ-MY89942",  # 例: "your_account"
    "user": "Fujii_Kotaro",        # あなたのユーザー名
    "password": "Fujimitu13", # あなたのパスワード
    "role": "SYSADMIN",        # optional, 役割
    "warehouse": "COMPUTE_WH", # 使用するウェアハウス
    "database": "SMOOTHIES", # 使用するデータベース
    "schema": "PUBLIC"     # 使用するスキーマ
}

# Snowflakeセッションの作成
session = Session.builder.configs(connection_parameters).create()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# ユーザーからの入力を受け取る
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

# Snowflakeセッションからデータを取得
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# ユーザーに果物の選択を促す
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe.to_pandas()['FRUIT_NAME'].tolist(),  # Snowpark DataFrameをPandas DataFrameに変換してリストを取得
    max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # 選択した果物をカンマ区切りの文字列にする

    # SQL文をパラメータ化
    my_insert_stmt = "INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES (:1, :2)"  # 正しい列名を使用

    # 注文を送信するボタン
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        try:
            # SQLを実行
            session.sql(my_insert_stmt, [ingredients_string, name_on_order]).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
        except Exception as e:
            # エラーが発生した場合の処理
            st.error(f'Error: {e}', icon="❌")
            st.write("SQL Statement:", my_insert_stmt)
