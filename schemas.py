"""
FastAPIのrequest, responseのスキーマ定義を行うファイル。
"""
from pydantic import BaseModel
import datetime

# DB_chatsのレスポンススキーマ
# chatsの中の単一のchatを表すスキーマ。
# これを直接使用することは無いが、requestやresponseに共通する一般的な性質として定義しておく。
class Chat(BaseModel):
    user_id: str
    date_time: datetime.datetime
    # user_prompt = Column(String)
    AI_objective_answer: str
    AI_personalized_answer: str

# chatをchatsテーブルに登録するpost用のリクエストスキーマ
class ChatRequest(Chat):
    pass  # Chatと属性は全く同じだが、Request用のスキーマであることを明示するために定義している。

# chatをchatsテーブルから取得するget用のレスポンススキーマ
class ChatResponse(BaseModel):
    # message: str  # Responseにメッセージを付け加えたい場合はコメントアウトを外す
    chat: Chat

# 複数のchatをchatsテーブルから取得するget用のレスポンススキーマ
class ChatsResponse(BaseModel):
    # message: str  # Responseにメッセージを付け加えたい場合はコメントアウトを外す
    chats: list[Chat]