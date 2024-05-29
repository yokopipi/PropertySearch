def property_search():
    import pandas as pd
    
    # 空のデータフレームを定義するための列名
    columns = ['property_name', 'rental_fee', 'floor','layout','size', 'building_age','distance_station','address','url']

    # 空のデータフレームを作成
    df = pd.DataFrame(columns=columns)

    # 追加するサンプルデータ
    sample_data = [
        ["グレイシアパーク仲町台 ", '150,000', '4','2LDK','72㎡','5年','10分','都筑区新栄町15-1','https://suumo.jp/chintai/jnc_000088903472/?bc=100380612216'],
        ["●●山荘", '150,000', '4','2LDK','72㎡','5年','10分','都筑区新栄町15-1','https://suumo.jp/chintai/jnc_000088903472/?bc=100380612216'],
        ["ハイツ仲町台", '150,000', '4','2LDK','72㎡','5年','10分','都筑区新栄町15-1','https://suumo.jp/chintai/jnc_000088903472/?bc=100380612216'],
        ["ライオンズマンション仲町台", '150,000', '4','2LDK','72㎡','5年','10分','都筑区新栄町15-1','https://suumo.jp/chintai/jnc_000088903472/?bc=100380612216'],
        ["スターダスト仲町台", '150,000', '4','2LDK','72㎡','5年','10分','都筑区新栄町15-1','https://suumo.jp/chintai/jnc_000088903472/?bc=100380612216'],
        ["ジョジョの奇妙な仲町台", '150,000', '4','2LDK','72㎡','5年','10分','都筑区新栄町15-1','https://suumo.jp/chintai/jnc_000088903472/?bc=100380612216'],
        ["オープンハウス仲町台", '150,000', '4','2LDK','72㎡','5年','10分','都筑区新栄町15-1','https://suumo.jp/chintai/jnc_000088903472/?bc=100380612216'],
        ["サンクレスト仲町台", '150,000', '4','2LDK','72㎡','5年','10分','都筑区新栄町15-1','https://suumo.jp/chintai/jnc_000088903472/?bc=100380612216'],
        ["グットハウス仲町台", '150,000', '4','2LDK','72㎡','5年','10分','都筑区新栄町15-1','https://suumo.jp/chintai/jnc_000088903472/?bc=100380612216'],
    ]

    # サンプルデータをデータフレームに追加
    df = pd.DataFrame(sample_data, columns=columns)

    return df