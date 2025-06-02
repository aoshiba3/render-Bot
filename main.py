import os
import time
from flask import Flask
import tweepy
from threading import Thread

# Flaskアプリ（Renderでの起動確認用）
app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Bot is running (Test Mode)!"

# Tweepy認証
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET")
)
api = tweepy.API(auth)

# テストツイートを3回、1分間隔で送信
def post_test_tweets():
    for i in range(3):
        try:
            text = f"hello, world! ({i+1}/3)"
            print(f"📝 {text}")
            api.update_status(text)
            print("✅ ツイート送信成功")
        except Exception as e:
            print("❌ ツイート送信失敗:", e)

        if i < 2:
            print("⏳ 1分待機中…")
            time.sleep(60)

# Flaskサーバーと投稿処理を並行実行
if __name__ == "__main__":
    def run_flask():
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
    Thread(target=run_flask).start()
    post_test_tweets()
