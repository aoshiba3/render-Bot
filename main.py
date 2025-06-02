import os
import random
import time
from datetime import datetime
from flask import Flask
from openai import OpenAI
import tweepy

# Flaskで起動確認用ルートを用意
app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Bot is running on Render!"

# OpenAIクライアントの初期化（v1.0形式）
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Tweepy認証
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET")
)
api = tweepy.API(auth)

# ツイート生成関数
def generate_tweet():
    prompt = """
あなたは20代後半～50代前半の社会人向けに、日常で役立つ金融系の雑学をつぶやくTwitterアカウントです。
内容は3行以内で簡潔に、ひとくちメモのような口調で書いてください。
話題の例：NISA、iDeCo、税金、投資信託、金利、円安、インフレ、家計管理、貯蓄術、節税

ツイート例：
「NISAって投資だけの制度だと思ってない？  
実は節税効果の方がめちゃくちゃ大きい制度です。  
特に非課税の効果は想像以上ですよ。」

では、今の時間帯に合った金融雑学を1つ書いてください：
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# ファクトチェック関数
def fact_check(tweet):
    check_prompt = f"""
以下の文章に金融・経済・税制・投資に関する事実誤認が含まれていないか確認してください。
問題がなければ「OK」とだけ返答してください。
不正確な内容があれば「NG: ○○が不正確です」と返答してください。

文章：
{tweet}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": check_prompt}]
    )
    return response.choices[0].message.content.strip()

# テスト用のツイート投稿処理（3回、3分おき）
def post_test_tweets():
    for i in range(3):
        print(f"\n🌀 {i+1}回目のツイート生成中…")
        tweet = generate_tweet()
        print(f"📝 生成結果:\n{tweet}")

        check = fact_check(tweet)
        print(f"🔍 ファクトチェック結果: {check}")

        if "OK" in check:
            try:
                api.update_status(tweet)
                print("✅ ツイート成功！")
            except Exception as e:
                print("❌ ツイート送信エラー:", e)
        else:
            print("⚠️ NG判定。ツイートスキップ")

        if i < 2:
            print("⏳ 3分待機中...")
            time.sleep(180)

# デプロイ時に即時実行
if __name__ == "__main__":
    from threading import Thread

    # Flaskサーバーを別スレッドで起動
    def run_flask():
        app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

    Thread(target=run_flask).start()

    # メイン処理（3回ツイート）
    post_test_tweets()
