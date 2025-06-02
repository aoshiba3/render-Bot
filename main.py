import os
import random
import time
from datetime import datetime
from threading import Thread
from flask import Flask
from openai import OpenAI
import tweepy

# Flaskセットアップ
app = Flask(__name__)
@app.route("/")
def index():
    return "✅ Bot is running on Render!"

# OpenAI API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Tweepy API
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET")
)
api = tweepy.API(auth)

# ツイート生成
def generate_tweet():
    prompt = """あなたは20代後半～50代前半の社会人向けに..."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# ファクトチェック
def fact_check(tweet):
    check_prompt = f"""以下の文章に...:\n{tweet}"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": check_prompt}]
    )
    return response.choices[0].message.content.strip()

# 自動ツイート処理（3分おきに3回）
def post_test_tweets():
    for i in range(3):
        print(f"🌀 {i+1}回目のツイート生成中…")
        tweet = generate_tweet()
        print("📝 生成結果:\n", tweet)

        check = fact_check(tweet)
        print("🔍 ファクトチェック結果:", check)

        if "OK" in check:
            try:
                api.update_status(tweet)
                print("✅ ツイート成功！")
            except Exception as e:
                print("❌ ツイート送信エラー:", e)
        else:
            print("⚠️ NG判定。スキップ")

        if i < 2:
            print("⏳ 3分待機中...")
            time.sleep(180)

# Flaskサーバー起動用スレッド
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# 並列実行
Thread(target=run_flask).start()
Thread(target=post_test_tweets).start()
