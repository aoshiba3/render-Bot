import tweepy
import os

# 環境変数からAPIキーを取得
auth = tweepy.OAuthHandler(
    os.environ["TWITTER_API_KEY"],
    os.environ["TWITTER_API_SECRET"]
)

# 認証用URLを取得
try:
    redirect_url = auth.get_authorization_url()
    print("↓ このURLを開いてPINコードを取得してください：")
    print(redirect_url)
except tweepy.TweepError as e:
    print("⚠️ Error getting authorization URL:", e)
