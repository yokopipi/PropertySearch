# サブモジュールをインポートする
from station_search import station_search
from introduction_to_Station import introduction_to_Station
from property_search import property_search

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import streamlit as st
from streamlit_folium import st_folium 
import folium
import sqlite3

# ページの設定：広いレイアウトを使用
st.set_page_config(layout="wide")

#---------カスタムCSSの定義---------
st.markdown(
    """
    <style>
    .custom-text {
        color: black;
        font-size: 24px;
        font-weight: bold;
        background-color: lightgray;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

#---------入力欄項目内容の設定---------
### 駅近（半径1KM以内）に必要な施設
## 入力欄に表示する内容を表示するために施設タイプリストをDBから取得
# データベースに接続
conn = sqlite3.connect('Realestate_Search.db')
cursor = conn.cursor()
# SQLクエリの実行
query = "SELECT facility_code, facility_type FROM facility_type"
cursor.execute(query)
# 結果の取得
results = cursor.fetchall()
# データフレームに変換
df = pd.DataFrame(results, columns=['facility_code', 'facility_type'])

### 駅近（半径1KM以内）に必要な施設
set_layout_list = [
    "1R",
    "1K",
    "1DK",
    "1LDK",
    "2DK",
    "2LDK",
    "3DK",
    "3LDK",
    "4DK",
    "4LDK"
]

#---------サイドバー設定---------
with st.sidebar:
    #---------以下、駅検索条件---------
    st.markdown('<div class="custom-text">駅検索条件</div>', unsafe_allow_html=True)
    st.write("## よく行く場所:")  
    target_Station1 = st.text_input("目的地駅①",'大手町',key='target_Station1')
    allowable_time1 = st.number_input('目的地駅①までの許容時間（分）', min_value=0, value=30, key='allowable_time1')
    target_Station2 = st.text_input("目的地駅②",'羽田空港',key='target_Station2')
    allowable_time2 = st.number_input('目的地駅②までの許容時間（分）', min_value=0, value=30, key='allowable_time2')

    st.write("## 駅近（半径1KM以内）に必要な施設:")  
    # チェックボックスの選択状態を管理するための辞書
    selected_facilitys = {}
    # チェックボックスで施設タイプを表示
    for i, row in df.iterrows():
        facility_code = row['facility_code']
        facility_type = row['facility_type']
        selected = st.checkbox(facility_type, key=facility_code)
        selected_facilitys[facility_code] = selected

    if st.button("駅条件だけで検索"):
        # 検索実行
        station_df = station_search(target_Station1,allowable_time1,target_Station2,allowable_time2,selected_facilitys)
        st.session_state.station_df = station_df
    
    #---------以下、物件検索条件---------
    st.markdown('<div class="custom-text">物件条件</div>', unsafe_allow_html=True)
    selected_layouts = st.multiselect('希望するレイアウトを選択してください', set_layout_list)
    rental_fee_range = st.slider('希望する金額範囲を指定してください（万円）', 0, 100, (10, 20))
    building_age_range = st.slider('希望する築年数範囲を指定してください（年）', 0, 40, (0, 10))
    size_range = st.slider('希望する物件サイズ範囲を指定してください（㎡）', 10, 200, (20, 50))

    if st.button("駅と物件条件で検索"):
        # 検索実行
        station_df = station_search(target_Station1,allowable_time1,target_Station2,allowable_time2,selected_facilitys)
        st.session_state.station_df = station_df

#---------以下、駅検索結果の出力---------
if 'station_df' in st.session_state:

    st.markdown('<div class="custom-text">候補駅一覧</div>', unsafe_allow_html=True)

    # ページネーションを設定
    page_size = 10
    total_pages = (len(st.session_state.station_df) + page_size - 1) // page_size
    page_number = st.number_input('ページ番号', min_value=1, max_value=total_pages, value=1, step=1) - 1
    start_index = page_number * page_size
    end_index = min(start_index + page_size, len(st.session_state.station_df))
    displayed_df = st.session_state.station_df.iloc[start_index:end_index]

    # タイトル行の常時表示
    title_row = st.session_state.station_df.iloc[0]
    title_cols = st.columns([2, 2, 2, 2, 2, 2, 2, 2])
    title_cols[0].write('**駅名**')
    title_cols[1].write('**主要路線**')
    title_cols[2].write('**区**')
    title_cols[3].write('**①までの時間**')
    title_cols[4].write('**②までの時間**')
    title_cols[5].write('**平均賃料**')
    title_cols[6].write('**候補物件数**')


    for i, row in displayed_df.iterrows():
        index = start_index + i  # 元のデータフレームでのインデックス位置
        cols = st.columns([2, 2, 2, 2, 2, 2, 2, 2])
        cols[0].write(row['station_name'])
        cols[1].write(row['line'])
        cols[2].write(row['ward'])
        cols[3].write(row['time_to_target1'])
        cols[4].write(row['time_to_target2'])
        cols[5].write(row['average_rent'])
        cols[6].write(row['num_properties'])
        if cols[7].button("選択", key=f"select_{index}"):  # キーにインデックスを追加
            if 'selected_station' not in st.session_state:
                st.session_state.selected_station = None
            if 'last_selected_station' not in st.session_state:
                st.session_state.last_selected_station = None
            st.session_state.selected_station = row['station_name']


    #---------以下、駅指定後の物件検索結果の出力---------
    if 'selected_station' in st.session_state:
        # chatgptによる駅紹介
        st.markdown(f'<div class="custom-text">{st.session_state.selected_station} 駅の紹介</div>', unsafe_allow_html=True)

        if st.session_state.selected_station and st.session_state.selected_station != st.session_state.last_selected_station:
            st.session_state.last_selected_station = st.session_state.selected_station
            introduction_text = introduction_to_Station(st.session_state.selected_station)
            st.session_state.introduction_text = introduction_text
            st.write(introduction_text)
        elif 'introduction_text' in st.session_state:
            st.write(st.session_state.introduction_text)

        # 対象駅の物件を一覧表と地図で表示
        st.markdown(f'<div class="custom-text">{st.session_state.selected_station} 駅の物件情報</div>', unsafe_allow_html=True)
        tab_lists,tab_map = st.tabs(["一覧で表示","地図で表示",])
        df = property_search()

        # セッションステートの初期化
        if 'selected_indices' not in st.session_state:
            st.session_state.selected_indices = []

        # 選択されたインデックスをセッションステートから取得
        selected_indices = st.session_state.selected_indices

        with tab_lists:
            #---------一覧表示---------

            # タイトル行の常時表示
            title_row = df.iloc[0]
            title_cols = st.columns([0.5, 2, 1, 1, 1, 1, 1, 1, 2])
            title_cols[0].write('**選択**')
            title_cols[1].write('**物件名**')
            title_cols[2].write('**賃料**')
            title_cols[3].write('**階数**')
            title_cols[4].write('**間取り**')
            title_cols[5].write('**広さ**')
            title_cols[6].write('**築年数**')
            title_cols[7].write('**駅からの距離**')
            title_cols[8].write('**住所**')

            selected_indices = []

            # チェックボックス付きデータフレームの表示
            for i, row in df.iterrows():
                cols = st.columns([0.5, 2, 1, 1, 1, 1, 1, 1, 2])

                # セッションステートからチェックボックスの初期値を取得
                if f"cb_{i}" not in st.session_state:
                    st.session_state[f"cb_{i}"] = i in selected_indices
                
                selected = cols[0].checkbox("", key=f"cb_{i}", value=st.session_state[f"cb_{i}"])

                if selected:
                    if i not in selected_indices:
                        selected_indices.append(i)
                else:
                    if i in selected_indices:
                        selected_indices.remove(i)

                cols[1].markdown(f"**[{row['property_name']}]({row['url']})**", unsafe_allow_html=True)
                cols[2].write(row['rental_fee'])
                cols[3].write(row['floor'])
                cols[4].write(row['layout'])
                cols[5].write(row['size'])
                cols[6].write(row['building_age'])
                cols[7].write(row['distance_station'])
                cols[8].write(row['address'])

            # 選択された物件のインデックスを保存
            st.session_state.selected_indices = selected_indices

        with tab_map:
            #---------地図表示---------
            map = folium.Map(location=[35.5378631,139.5951104], zoom_start=10)
            st_folium(map, width = 1000, height = 500)

        #---------以下、選択された物件比較情報の表示---------
        if selected_indices:
            st.write("選択された物件:")

            selected_rows = df.iloc[selected_indices].copy()

            # 日本語の列名に変更
            selected_rows.columns = ['物件名', '賃料', '階数', '間取り', '広さ', '築年数', '駅からの距離', '住所', 'URL']

            # リンク付きの物件名に変更
            selected_rows['物件名'] = selected_rows.apply(lambda row: f'<a href="{row["URL"]}" target="_blank">{row["物件名"]}</a>', axis=1)

            # URLカラムを削除
            selected_rows = selected_rows.drop(columns=['URL'])

            # 行列を入れ替えて表示用のデータフレームを作成
            transposed_df = selected_rows.transpose()

            # HTMLテーブルの生成
            html_table = '<table border="1"><tbody>'
            for index, row in transposed_df.iterrows():
                html_table += f'<tr><th>{index}</th>'
                for val in row:
                    html_table += f'<td>{val}</td>'
                html_table += '</tr>'
            html_table += '</tbody></table>'

            # HTMLテーブルの表示
            st.markdown(html_table, unsafe_allow_html=True)
        else:
            st.write("選択された物件はありません。")
