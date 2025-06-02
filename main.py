import os
import time
import tweepy
import openai
from flask import Flask
from threading import Thread

# Flaskアプリで常時起動
app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Bot is running on Render!"

# 環境変数読み込み
openai.api_key = os.getenv("OPENAI_API_KEY")

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Tweepy認証
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY, TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
)
api = tweepy.API(auth)

# ツイート内容生成
def generate_tweet():
    prompt = """
あなたは20代後半～50代の社会人向けに、NISAや投資、節税などの金融雑学を3行以内でわかりやすくツイートします。
では、1つ書いてください：
"""
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }]
    )
    return res.choices[0].message.content.strip()

# 実行ループ（3回・3分おき）
def run_bot():
    for i in range(3):
        try:
            tweet = generate_tweet()
            api.update_status(tweet)
            print(f"✅ ツイート[{i+1}回目]：{tweet}")
        except Exception as e:
            print("❌ ツイート失敗:", e)
        time.sleep(180)  # 3分待機

# 別スレッドでBot実行
Thread(target=run_bot).start()

# Flask起動
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
