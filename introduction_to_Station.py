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

    # OpenAI APIキーの設定
    'openai.api_key = ''


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"駅名: {station_name}\nこの駅の簡単な紹介文を1000文字程度で教えてください。"}
        ],
        max_tokens=1000
    )
    return response.choices[0].message['content'].strip()