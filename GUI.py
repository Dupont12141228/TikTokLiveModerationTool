import tkinter as tk
from tkinter import ttk
import json
from TikTokLiveModeration import TikTokLiveModeration  # TikTokLiveModerationクラスをインポート

# 設定ファイルのパス
SETTINGS_FILE = "settings.json"

class TikTokLiveModerationGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TikTok Live Moderation Tool")
        self.geometry("500x700")  # サイズを調整

        # ユーザーIDの入力欄
        self.label_id = tk.Label(self, text="配信者のユーザーID:")
        self.label_id.pack(pady=5)
        self.entry_id = tk.Entry(self)
        self.entry_id.pack(pady=5)

        # アクセストークンの入力欄
        self.label_token = tk.Label(self, text="アクセストークン:")
        self.label_token.pack(pady=5)
        self.entry_token = tk.Entry(self)
        self.entry_token.pack(pady=5)

        # 定期文の入力欄
        self.label_regular_messages = tk.Label(self, text="定期文 (1行ずつ入力):")
        self.label_regular_messages.pack(pady=5)
        self.text_regular_messages = tk.Text(self, height=5)
        self.text_regular_messages.pack(pady=5)

        # 定期文の送信間隔の入力欄
        self.label_interval = tk.Label(self, text="定期文送信間隔 (秒):")
        self.label_interval.pack(pady=5)
        self.entry_interval = tk.Entry(self)
        self.entry_interval.pack(pady=5)

        # 定期文のオンオフチェックボックス
        self.var_send_regular = tk.BooleanVar(value=True)
        self.checkbox_send_regular = tk.Checkbutton(self, text="定期文を送信", variable=self.var_send_regular)
        self.checkbox_send_regular.pack(pady=5)

        # 定期文無効メッセージ
        self.label_regular_disable = tk.Label(self, text="チェックを外すと定期文機能は無効になります。")
        self.label_regular_disable.pack(pady=5)

        # ギフトお礼コメントの入力欄
        self.label_gift_messages = tk.Label(self, text="ギフトお礼コメント (1行ずつ入力):")
        self.label_gift_messages.pack(pady=5)
        self.text_gift_messages = tk.Text(self, height=5)
        self.text_gift_messages.pack(pady=5)

        # ギフトお礼コメントのオンオフチェックボックス
        self.var_send_gift = tk.BooleanVar(value=True)
        self.checkbox_send_gift = tk.Checkbutton(self, text="ギフトお礼コメントを送信", variable=self.var_send_gift)
        self.checkbox_send_gift.pack(pady=5)

        # ギフトお礼コメント無効メッセージ
        self.label_gift_disable = tk.Label(self, text="チェックを外すとギフトお礼コメント機能は無効になります。")
        self.label_gift_disable.pack(pady=5)

        # 実行ボタン
        self.button_run = tk.Button(self, text="開始", command=self.start_mod)
        self.button_run.pack(pady=20)

        # 設定の読み込み
        self.load_settings()

    def start_mod(self):
        unique_id = self.entry_id.get()
        token = self.entry_token.get()  # アクセストークンの取得
        regular_messages = self.text_regular_messages.get("1.0", tk.END).splitlines()
        gift_messages = self.text_gift_messages.get("1.0", tk.END).splitlines()
        interval = int(self.entry_interval.get())  # 入力値を秒に変換

        SEND_REGULAR_MESSAGES = self.var_send_regular.get()
        SEND_GIFT_THANK_YOU_MESSAGES = self.var_send_gift.get()

        # TikTokLiveModeration のインスタンスを作成し、設定を渡して実行
        bot = TikTokLiveModeration(
            unique_id=unique_id,
            regular_messages=regular_messages,
            gift_thank_you_messages=gift_messages,
            interval=interval,
            send_regular_messages=SEND_REGULAR_MESSAGES,
            send_gift_thank_you=SEND_GIFT_THANK_YOU_MESSAGES
        )
        bot.access_token = token  # アクセストークンを設定
        bot.start()

        # 設定の保存
        self.save_settings()

    def save_settings(self):
        settings = {
            "unique_id": self.entry_id.get(),
            "token": self.entry_token.get(),  # アクセストークンを保存
            "regular_messages": self.text_regular_messages.get("1.0", tk.END).splitlines(),
            "gift_messages": self.text_gift_messages.get("1.0", tk.END).splitlines(),
            "interval": int(self.entry_interval.get()),
            "send_regular": self.var_send_regular.get(),
            "send_thank_you": self.var_send_gift.get()
        }
        with open(SETTINGS_FILE, "w") as file:
            json.dump(settings, file)

    def load_settings(self):
        try:
            with open(SETTINGS_FILE, "r") as file:
                settings = json.load(file)
                self.entry_id.insert(0, settings.get("unique_id", ""))
                self.entry_token.insert(0, settings.get("token", ""))  # アクセストークンの読み込み
                self.text_regular_messages.insert("1.0", "\n".join(settings.get("regular_messages", [])))
                self.text_gift_messages.insert("1.0", "\n".join(settings.get("gift_messages", [])))
                self.entry_interval.insert(0, str(settings.get("interval", 60)))
                self.var_send_regular.set(settings.get("send_regular", True))
                self.var_send_gift.set(settings.get("send_thank_you", True))
        except FileNotFoundError:
            pass  # 設定ファイルがない場合は何もしない

if __name__ == "__main__":
    app = TikTokLiveModerationGUI()
    app.mainloop()
