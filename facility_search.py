#############
#【関数名】
#設備検索（facility_search）
#【処理内容】
#入力された情報から駅の設備情報を検索する

#【パラメータ】
# ・対象駅：テキスト
# ・対象設備タイプ：テキストのリスト
#【返り値】
# ・設備リスト：データフレーム
#############

def facility_search():
    import pandas as pd
    import sqlite3
    
    station_name = '泉岳寺駅'
    facility_types = ['1', '2']

    # データベースに接続
    conn = sqlite3.connect('Realestate_Search.db')
    cursor = conn.cursor()
    # 動的SQLクエリの作成
    query = f"""
    select 
	    f.facility_code,
	    f.store_name,
	    f.longitude,
	    f.latitude,
	    f.distance
    FROM
	    facility f
    WHERE
	    near_station_name = '{station_name}'
	    AND f.facility_code IN ({', '.join([f"'{facility_type}'" for facility_type in facility_types])})
    """

    # データベースへの接続とクエリの実行
    conn = sqlite3.connect('Realestate_Search.db')
    df = pd.read_sql_query(query, conn)
    conn.close()


    return df