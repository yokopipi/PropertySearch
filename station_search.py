#############
#【関数名】
#駅検索（station_search）
#【処理内容】
#入力された情報から駅を検索する

#【パラメータ】
# ・地点①の駅：テキスト
# ・地点①までの許容時間：テキスト
# ・地点②の駅：テキスト
# ・地点②までの許容時間：テキスト
# ・必要な設備場情報：設備タイプ（facility_type)の数値リスト
#【返り値】
# ・駅リスト：データフレーム
#############

def station_search(target_Station1,allowable_time1,target_Station2,allowable_time2,selected_facilitys):
    import pandas as pd
    import sqlite3
    
    # データベースに接続
    conn = sqlite3.connect('Realestate_Search.db')
    cursor = conn.cursor()
    # 動的SQLクエリの作成
    query = f"""
    SELECT
        st.station_name,
        st.line,
        st.ward,
        st.address,
        MAX(CASE WHEN tt.station_name_to = '{target_Station1}' THEN tt.travel_time END) AS time_to_target1,
        MAX(CASE WHEN tt.station_name_to = '{target_Station2}' THEN tt.travel_time END) AS time_to_target2,
        10000 AS average_rent,
        50 AS num_properties,
        st.longitude,
        st.latitude
    FROM 
        station st
    JOIN 
        travel_time tt ON st.station_name = tt.station_name_from
    WHERE 
        st.Facility1 IS NOT NULL AND st.Facility1 != ''
        AND (tt.station_name_to = '{target_Station1}' OR tt.station_name_to = '{target_Station2}')
        AND ((tt.station_name_to = '{target_Station1}' AND tt.travel_time <= {allowable_time1}) OR (tt.station_name_to = '{target_Station2}' AND tt.travel_time <= {allowable_time2}))
    GROUP BY
        st.station_code
    """

    # クエリの実行
    cursor.execute(query)

    # 結果の取得
    results = cursor.fetchall()
    # データベース接続を閉じる
    conn.close()

    # 空のデータフレームを定義するための列名
    columns = ['station_name', 'line', 'ward','address','time_to_target1', 'time_to_target2','average_rent','num_properties','longitude','latitude']

    # 空のデータフレームを作成
    df = pd.DataFrame(columns=columns)

    # 結果をデータフレームに変換
    df = pd.DataFrame(results, columns=columns)
    df = df.dropna(subset=['time_to_target1', 'time_to_target2'])

    return df