"""
FastAPIのrequest, responseのスキーマ定義を行うファイル。
"""
from pydantic import BaseModel
import datetime


""" chats DBと通信するためのFastAPIスキーマ定義 """

# chatsの中の単一のchatを表すスキーマ。
# これを直接使用することは無いが、requestやresponseに共通する一般的な性質として定義しておく。
class Chat(BaseModel):
    user_id: str
    date_time: datetime.datetime
    user_prompt: str
    user_prompt: str
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



# summariesの中の単一のsummaryを表すスキーマ。
# これを直接使用することは無いが、requestやresponseに共通する一般的な性質として定義しておく。
class Summary(BaseModel):
    user_id: str
    date: datetime.date
    summary: str

# summaryをsummariesテーブルに登録するpost用のリクエストスキーマ
class SummaryRequest(Summary):
    pass  # Summaryと属性は全く同じだが、Request用のスキーマであることを明示するために定義している。

# summaryをsummariesテーブルから取得するget用のレスポンススキーマ
class SummaryResponse(BaseModel):
    # message: str  # Responseにメッセージを付け加えたい場合はコメントアウトを外す
    summary: Summary

# 複数のsummaryをsummariesテーブルから取得するget用のレスポンススキーマ
class SummariesResponse(BaseModel):
    summaries: list[Summary]


#ラベルを付けた日を取得するためのリクエストスキーマ
class LabeledDatesRequest(BaseModel):
    user_id: str
    month: int

# ラベルを付けた日を取得するためのレスポンススキーマ
class LabeledDatesResponse(BaseModel):
    labeled_dates: list[datetime.date]

""" quizzes DBのスキーマ定義 """
class Quiz(BaseModel):
    id: int
    quiz: str
    answer: str
    choice1: str
    choice2: str
    choice3: str
    choice4: str

class QuizRequest(Quiz):
    pass

class QuizResponse(BaseModel):
    quiz: Quiz | None = None
    message: str | None = None

"""Bedrockと通信するためのFastAPIスキーマ定義"""
class BedrockResponse(BaseModel):
    message: str  # Bedrockからの応答メッセージを含む
    answer: str  # Bedrockからの回答内容を含む

class BedrockRequest(BaseModel):
    user_id: str  # ユーザーIDを含む
    date_time: datetime.datetime  # 日時を含む
    user_prompt: str  # ユーザーからのプロンプトを含む


"""Bedrockへの命令をフロントエンドから受け取るためのFastAPIスキーマ定義"""
class ChatCreateRequest(BaseModel):
    user_id: str
    date_time: datetime.datetime
    user_prompt: str

class ChatCreateResponse(BaseModel):
    AI_personalized_answer: str

