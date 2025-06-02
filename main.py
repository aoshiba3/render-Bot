import os
import time
from flask import Flask
import tweepy
from threading import Thread

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Test Bot is running on Render!"

# 環境変数チェック（ログに明示）
def validate_env():
    keys = [
        "TWITTER_API_KEY",
        "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_SECRET"
    ]
    missing = [key for key in keys if not os.getenv(key)]
    if missing:
        print("❌ 以下の環境変数が未設定です:", ", ".join(missing))
        return False
    return True

# ツイート処理
def post_test_tweets():
    if not validate_env():
        print("❌ 実行停止：環境変数エラー")
        return

    try:
        auth = tweepy.OAuth1UserHandler(
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_SECRET"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_SECRET")
        )
        api = tweepy.API(auth)
    except Exception as e:
        print("❌ 認証エラー:", e)
        return

    for i in range(3):
        print(f"🌀 {i+1}回目のツイート中…")
        try:
            api.update_status("hello, world")
            print("✅ ツイート成功！")
        except Exception as e:
            print("❌ ツイート送信エラー:", e)
        if i < 2:
            print("⏳ 1分待機中...")
            time.sleep(60)

# スレッドでツイート実行
Thread(target=post_test_tweets).start()

# Flask起動
app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
