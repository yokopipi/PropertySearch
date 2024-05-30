#############
#【関数名】
#駅紹介（introduction_to_Station）
#【処理内容】
#指定された駅の情報をChatGTPに問い合わせて、結果を返す。

#【パラメータ】
# ・対象駅：テキスト
#【返り値】
# ・紹介文：テキスト
#############



def introduction_to_Station(station_name):

    import openai
    import os
    from dotenv import load_dotenv

    # .envファイルから環境変数を読み込む
    load_dotenv()

    # OpenAI APIキーの設定
    openai.api_key = os.getenv('OPENAI_API_KEY')


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたはこの駅の住民です。"},
            {"role": "user", "content": f"駅名: {station_name}\nこの駅の簡単な紹介文を800文字程度で教えてください。以下の形式で回答してください。\n【駅前の特徴】\n【駅としての魅力】\n【利用者特性】"}
        ],
        max_tokens=1200
    )
    return response.choices[0].message['content'].strip()