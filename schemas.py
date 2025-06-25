"""
FastAPIのrequest, responseのスキーマ定義を行うファイル。
"""
from pydantic import BaseModel
import datetime


""" chats DBのスキーマ定義 """
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


""" summaries DBのスキーマ定義 """
# summariesの中の単一のsummaryを表すスキーマ。
# これを直接使用することは無いが、requestやresponseに共通する一般的な性質として定義しておく。
class Summary(BaseModel):
    user_id: str
    date: datetime.date
    summary: str

# summaryをsummariesテーブルに登録するpost用のリクエストスキーマ
class SummaryRequest(Summary):
    pass  # Summaryと属性は全く同じだが、Request用のスキーマであることを明示するために定義している。

class SummaryResponse(BaseModel):
    # message: str  # Responseにメッセージを付け加えたい場合はコメントアウトを外す
    summary: Summary

class SummariesResponse(BaseModel):
    summaries: list[Summary]