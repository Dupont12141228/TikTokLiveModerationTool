from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent
import asyncio
import argparse
import json
import os

class TikTokLiveModeration:
    """
    TikTokライブのモデレーションを管理するクラス。
    定期的なコメントの送信や、ギフトに対するメンションお礼コメントを行います。
    """
    def __init__(self, unique_id: str, access_token: str, regular_messages: list, gift_thank_you_messages: list, interval: int, send_regular_messages: bool, send_gift_thank_you: bool):
        """
        クラスの初期化を行います。

        :param unique_id: TikTokライブのユニークID
        :param access_token: TikTok APIのアクセストークン
        :param regular_messages: 定期的に送信するメッセージのリスト
        :param gift_thank_you_messages: ギフトに対するお礼コメントのリスト
        :param interval: コメント送信間隔（秒）
        :param send_regular_messages: 定期文の送信を行うかどうか
        :param send_gift_thank_you: ギフトへのお礼コメントを行うかどうか
        """
        self.client = TikTokLiveClient(unique_id=unique_id, access_token=access_token)
        self.send_regular_messages = send_regular_messages  # 定期文の送信を行うかどうか
        self.send_gift_thank_you = send_gift_thank_you  # ギフトへのお礼コメントを行うかどうか
        self.regular_messages = regular_messages  # 定期的に送信するメッセージのリスト
        self.gift_thank_you_messages = gift_thank_you_messages  # ギフトに対するお礼コメントのリスト
        self.interval = interval  # コメント送信間隔（秒）

    async def on_connect(self, event: ConnectEvent):
        """
        ライブ配信に接続したときのイベントハンドラー。

        :param event: 接続イベントの情報
        """
        print(f"Connected to @{event.unique_id} (Room ID: {self.client.room_id})")

    async def on_comment(self, event: CommentEvent):
        """
        コメントが投稿されたときのイベントハンドラー。

        :param event: コメントイベントの情報
        """
        print(f"{event.user.nickname} -> {event.comment}")

    async def on_gift(self, event: GiftEvent):
        """
        ギフトが送信されたときのイベントハンドラー。
        ギフト送信者へのお礼コメントをメンション形式で送信します。

        :param event: ギフトイベントの情報
        """
        if self.send_gift_thank_you:
            user_name = event.user.unique_id  # ギフト送信者のユーザー名
            message = self.gift_thank_you_messages[0].format(user=user_name)  # メッセージをフォーマット
            await self.client.send_message(message)  # メッセージを送信
    
    async def send_periodic_messages(self):
        """
        定期的にコメントを送信する非同期タスク。
        """
        while True:
            if self.send_regular_messages:
                for message in self.regular_messages:
                    await self.client.send_message(message)  # メッセージを送信
                    await asyncio.sleep(self.interval)  # メッセージ間の遅延（秒）

    def start(self):
        """
        モデレーション機能を開始します。
        """
        self.client.on(ConnectEvent, self.on_connect)
        self.client.on(CommentEvent, self.on_comment)
        self.client.on(GiftEvent, self.on_gift)

        # 定期的なメッセージ送信を別タスクで実行
        if self.send_regular_messages:
            asyncio.create_task(self.send_periodic_messages())

        self.client.run()

def load_settings():
    """
    settings.jsonからアクセストークンを読み込む関数。
    """
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            return json.load(f)
    return {}

def save_settings(settings):
    """
    settings.jsonにアクセストークンを保存する関数。
    """
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

if __name__ == '__main__':
    # 設定の読み込み
    settings = load_settings()

    # アクセストークンの入力
    if 'access_token' not in settings:
        access_token = input('Enter your TikTok API Access Token: ')
        settings['access_token'] = access_token
        save_settings(settings)
    else:
        access_token = settings['access_token']

    parser = argparse.ArgumentParser(description='TikTok Live Moderation Tool')
    parser.add_argument('--unique_id', type=str, required=True, help='配信者のユーザーID')
    parser.add_argument('--regular_messages', type=str, nargs='*', default=[], help='定期文リスト')
    parser.add_argument('--gift_messages', type=str, nargs='*', default=[], help='ギフトお礼コメントリスト')
    parser.add_argument('--interval', type=int, default=60, help='コメント送信間隔（秒）')
    parser.add_argument('--send_regular', type=bool, default=True, help='定期文送信のオンオフ')
    parser.add_argument('--send_thank_you', type=bool, default=True, help='ギフトお礼コメントのオンオフ')

    args = parser.parse_args()

    bot = TikTokLiveModeration(
        unique_id=args.unique_id,
        access_token=access_token,
        regular_messages=args.regular_messages,
        gift_thank_you_messages=args.gift_messages,
        interval=args.interval,
        send_regular_messages=args.send_regular,
        send_gift_thank_you=args.send_thank_you
    )
    bot.start()
