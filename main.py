import os
import time
from flask import Flask
import tweepy

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Bot is running on Render!"

# Tweepy 認証（OAuth1.0a）
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET")
)
api = tweepy.API(auth)

# テストツイート（3回、1分おき）
def post_test_tweets():
    for i in range(3):
        text = f"hello, world {i+1}"
        try:
            api.update_status(text)
            print(f"✅ ツイート成功: {text}")
        except Exception as e:
            print(f"❌ ツイート送信エラー: {e}")
        if i < 2:
            time.sleep(60)

# 起動時処理
if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))).start()
    post_test_tweets()
