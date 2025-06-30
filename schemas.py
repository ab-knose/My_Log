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




"""summaries DBと通信するためのFastAPIスキーマ定義"""

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



"""チャットをした日付"""

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
    choice1: str
    choice2: str
    choice3: str
    choice4: str
    quiz: str
    answer: str

class QuizRequest(Quiz):
    pass

class QuizResponse(BaseModel):
    quiz: Quiz | None = None
    message: str | None = None

"""users_last_action_date DBのスキーマ定義"""
class UsersLastActionDate(BaseModel):
    user_id: str  # ユーザーIDを含む
    last_login_date: datetime.date | None = None  # 最後のログイン日
    last_quiz_answer_date: datetime.date | None = None  # 最後のクイズ回答日

class UsersLastActionDateRequest(BaseModel):
    user_id: str  # ユーザーIDを含む
    date: datetime.date  # 今日の日付を含む

class UsersLastActionDateResponse(BaseModel):
    user_id: str
    date: datetime.date

"""EF DBのスキーマ定義"""
class EF(BaseModel):
    dimension: int  # 次元を表す整数
    sub_dimension: int | None = None  # サブ次元を表す整数（オプション）
    detailed_category: str | None = None  # 詳細カテゴリを表す文字列（オプション）
    class_: int  # クラスを表す整数（'class'は予約語のためclass_とする）
    content: str  # コンテンツを表す文字列

class EFRequest(EF):
    class_: int  # クラスを表す整数（'class'は予約語のためclass_とする）

class EFResponse(BaseModel):
    ef: EF 

"""EPRs DBのスキーマ定義"""
class EPRs(BaseModel):
    user_id: str  # ユーザーIDを含む
    project_name: str  # プロジェクト名を含む
    start_date: datetime.date  # 開始日を含む
    goal1: str | None = None  # 目標1を含む（オプション）
    goal2: str | None = None  # 目標2を含む（オプション）
    goal3: str | None = None  # 目標3を含む（オプション）
    goal4: str | None = None  # 目標4を含む（オプション）
   #    goal5: str | None = None  # 目標5を含む（オプション、必要に応じて追加）

class EPRsRequest(EPRs):
    user_id: str  # ユーザーIDを含む
    start_date: datetime.date  # 開始日を含む
class EPRsResponse(BaseModel):
    epr: EPRs  # EPRsのデータを含む
    project_name: str  # プロジェクト名を含む

#EPRをアップロードするためのリクエストスキーマ
class EPRsUploadRequest(BaseModel):
    user_id: str  # ユーザーIDを含む
    project_name: str  # プロジェクト名を含む
    start_date: datetime.date  # 開始日を含む
    goal1: str | None = None  # 目標1を含む（オプション）
    goal2: str | None = None  # 目標2を含む（オプション）
    goal3: str | None = None  # 目標3を含む（オプション）
    goal4: str | None = None  # 目標4を含む（オプション）
    # goal5: str | None = None  # 目標5を含む（オプション、必要に応じて追加）

#EPRをアップロードするためのレスポンススキーマ
class EPRsUploadResponse(BaseModel):
    user_id: str  # ユーザーIDを含む
    project_name: str  # プロジェクト名を含む
    start_date: datetime.date  # 開始日を含む
    goal1: str | None = None  # 目標1を含む（オプション）
    goal2: str | None = None  # 目標2を含む（オプション）
    goal3: str | None = None  # 目標3を含む（オプション）
    goal4: str | None = None  # 目標4を含む（オプション）
    # goal5: str | None = None  # 目標5を含む（オプション、必要に応じて追加）
 

"""Bedrockと通信するためのFastAPIスキーマ定義"""
class BedrockResponse(BaseModel):
    message: str  # Bedrockからの応答メッセージを含む
    answer: str  # Bedrockからの回答内容を含む


"""Bedrockへの命令をフロントエンドから受け取るためのFastAPIスキーマ定義"""
class ChatCreateRequest(BaseModel):
    user_id: str
    date_time: datetime.datetime
    user_prompt: str

class ChatCreateResponse(BaseModel):
    AI_personalized_answer: str

