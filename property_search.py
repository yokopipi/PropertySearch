#############
#【関数名】
#物件検索（property_search）
#【処理内容】
#条件に従って物件検索を行い、結果をデータフレームに格納する。
#似たような物件が複数検索されることが想定されるので、同じマンションの同じレイアウトは集約する

#【パラメータ】
# ・対象駅：テキスト
# ・家賃（MIN）：数字
# ・家賃（MAX）：数字
# ・築年数（MIN）：数字
# ・築年数（MAX）：数字
# ・平米数（MIN）：数字
# ・平米数（MAX）：数字
# ・レイアウト：文字列のリスト
#【返り値】
# ・物件一覧：データフレーム
#############


def property_search(station_name,rental_fee_min, rental_fee_max,building_age_min,building_age_max,size_min,size_max):
    import pandas as pd
    import sqlite3
    
    # 動的SQLクエリの作成
    query = f"""
    SELECT
        p.property_name,
        p.layout,
        COUNT(*) AS hit_cnt,
        ROUND(AVG(p.rental_fee), 1) AS avg_rental_fee,
        ROUND(AVG(p.deposit), 1) AS avg_deposit,
        GROUP_CONCAT(p.floor, ', ') AS floors,
        ROUND(AVG(p.size), 1) AS avg_size,
        ROUND(AVG(p.building_age),0) AS avg_building_age,
        p.distance_station,
        p.address,
        p.url,
        p.layout_url,
        p.longitude,
        p.latitude
    FROM
        property p
    WHERE 
        p.near_station_name = '{station_name}'
        AND p.rental_fee BETWEEN {rental_fee_min} AND {rental_fee_max}
        AND p.building_age BETWEEN {building_age_min} AND {building_age_max}
        AND p.size BETWEEN {size_min} AND {size_max}
    GROUP BY 
        p.property_name,
        p.layout
    ORDER BY 
        avg_rental_fee;
    """

    # データベースへの接続とクエリの実行
    conn = sqlite3.connect('Realestate_Search.db')
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df