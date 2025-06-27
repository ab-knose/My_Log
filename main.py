# FastAPIおよびpydantic
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
# Bedrock
import boto3
from dotenv import load_dotenv
# general
import datetime
import random
import os
import json
# 自作のmodels, schemas, crud, utils
import random
# 自作のmodels, schemas, crud, utils
from models import *
from schemas import *
# from crud import *
from utils import *




"""DBの設定"""
# データベースのURLを設定
# [要対応？]DATABASE_URL が研修で指定されている形式と違うらしい？
DATABASE_URL = "mysql+pymysql://admin:Digitaldev1@group1-chats.c7c4ksi06r6a.ap-southeast-2.rds.amazonaws.com:3306/group1"

# SQLAlchemyのエンジンとセッションを作成
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


"""FastAPIの準備"""
# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# CORSミドルウェアの設定
# これにより、フロントエンドアプリケーション（例：Vue.jsやReactなど）からのリクエストを許可する。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # または ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""API定義"""
@app.get("/")
def get_root():
    return {"message": "Welcome to the My Log app!"}

# chatsテーブルから単一のchatデータを取得するAPI
# 仕様書には無いが、テスト用に作っておく。エンドポイントに注意。
@app.get("/chats/single/{user_id}", response_model=ChatResponse)
def get_chat(user_id: str, db_session: Session = Depends(get_db_session)):
    db_chat = db_session.query(ChatsModel).filter(ChatsModel.user_id == user_id).first()
    return ChatResponse(chat=convert_chat_model_to_chat_schema(db_chat))  # 登録したdb_chatをChatスキーマに変換して返す

# chatsテーブルから複数のchatデータを取得するAPI
@app.get("/chats/{user_id}/{start_date}_{end_date}", response_model=ChatsResponse)
def get_chats(user_id: str, start_date: datetime.date, end_date: datetime.date, db_session: Session = Depends(get_db_session)):
    db_chats = db_session.query(ChatsModel).filter(
        ChatsModel.user_id == user_id,
        ChatsModel.date_time >= datetime.datetime.combine(start_date, datetime.time.min),
        ChatsModel.date_time <= datetime.datetime.combine(end_date, datetime.time.max)
    ).all()
    chats = list(map(convert_chat_model_to_chat_schema, db_chats))  # db_chatsの各要素をChatスキーマに変換

    return ChatsResponse(chats=chats)


# chatsテーブルからすべてのchatデータを削除するAPI
"""※危険！使う時は全員の同意を得てからにせよ。"""
@app.delete("/chats", response_model=ChatsResponse)
def delete_all_chats(db_session: Session = Depends(get_db_session)):
    db_chats = db_session.query(ChatsModel).all()
    chats = list(map(convert_chat_model_to_chat_schema, db_chats))  # db_chatsの各要素をChatスキーマに変換

    db_session.query(ChatsModel).delete()  # 全てのchatデータを削除
    db_session.commit()  # 変更をコミット
    chats = list(map(convert_chat_model_to_chat_schema, db_chats))  # db_chatsの各要素をChatスキーマに変換

    return ChatsResponse(chats=chats)


# chatsテーブルに単一のchatデータを登録するAPI
@app.post("/chats", response_model=ChatResponse)
def post_chat(chat_request: ChatRequest, db_session: Session = Depends(get_db_session)):
    db_chat = convert_chat_schema_to_chat_model(chat_request)  # ChatRequestをChatsModelに変換
    db_chat = convert_chat_schema_to_chat_model(chat_request)  # ChatRequestをChatsModelに変換
    db_session.add(db_chat)
    db_session.commit()
    db_session.refresh(db_chat)
    return ChatResponse(chat=chat_request)



# summariesテーブルから単一のsummaryデータを取得するAPI
# 仕様書には無いが、テスト用に作っておく。エンドポイントに注意。
@app.get("/summaries/single/{user_id}", response_model=SummaryResponse)
def get_summary(user_id: str, db_session: Session = Depends(get_db_session)):


    db_summary = db_session.query(SummariesModel).filter(SummariesModel.user_id == user_id).first()
    return SummaryResponse(summary=convert_summary_model_to_summary_schema(db_summary))  # db_summaryをSummaryスキーマに変換して返す

# summariesテーブルから複数のsummaryデータを取得するAPI
@app.get("/summaries/{user_id}/{start_date}_{end_date}", response_model=SummariesResponse)
def get_summaries(user_id: str, start_date: datetime.date, end_date: datetime.date, db_session: Session = Depends(get_db_session)):
    db_summaries = db_session.query(SummariesModel).filter(
        SummariesModel.user_id == user_id,
        SummariesModel.date >= start_date,
        SummariesModel.date <= end_date
    ).all()
    summaries = list(map(convert_summary_model_to_summary_schema, db_summaries))  # db_summariesの各要素をSummaryスキーマに変換
    return SummariesResponse(summaries=summaries)



# summariesテーブルに単一のsummaryデータを登録するAPI
@app.post("/summaries", response_model=SummaryResponse)
def post_summary(summary_request: SummaryRequest, db_session: Session = Depends(get_db_session)):
    db_summary = convert_summary_schema_to_summary_model(summary_request)  # SummaryRequestをSummariesModelに変換
    db_session.add(db_summary)
    db_session.commit()
    db_session.refresh(db_summary)
    return SummaryResponse(summary=convert_summary_model_to_summary_schema(db_summary))  # 登録したdb_summaryをSummaryスキーマに変換して返す


#EFの内容をEF DBから取得する。	
@app.get("/ef", response_model=list[EF])
def get_ef(db_session: Session = Depends(get_db_session)):
    db_efs = db_session.query(EFModel).all()
    # EFModelの各要素をEFスキーマに変換
    efs = [EF(
        dimension=ef.dimension,
        sub_dimension=ef.sub_dimension,
        detailed_category=ef.detailed_category,
        class_=ef.class_,
        content=ef.content
    ) for ef in db_efs]
    return efs

# EPRsテーブルからEPRの内容を取得するAPI
@app.get("/epr", response_model=list[EPRs])	
def get_eprs(db_session: Session = Depends(get_db_session)):
    db_eprs = db_session.query(EPRsModel).all()
    # EPRsModelの各要素をEPRスキーマに変換
    eprs = [EPRs(
        user_id=epr.user_id,
        project_name=epr.project_name,
        start_date=epr.start_date,
        goal1=epr.goal1,
        goal2=epr.goal2,
        goal3=epr.goal3,
        goal4=epr.goal4,
    ) for epr in db_eprs]
    return eprs																		

# chatsテーブルから特定のユーザーのラベル付けされた日付を取得するAPI

@app.get("/chats/labeled_dates/{user_id}", response_model=list[datetime.date])
def get_labeled_dates(user_id: str, db_session: Session = Depends(get_db_session)):
    db_chats = db_session.query(ChatsModel).filter(ChatsModel.user_id == user_id).all()
    # 日付だけを抽出し、重複をなくす
    labeled_dates = list({chat.date_time.date() for chat in db_chats})
    labeled_dates.sort()
    return labeled_dates

# EFからランダムにクイズを選択し取得するAPI
@app.get("/quizzes/random/{user_id}", response_model=QuizResponse)
def get_random_quiz(user_id: str, db_session: Session = Depends(get_db_session)):
    import hashlib
    import datetime

#teを更新するAPI
    today = datetime.date.today()
    today = datetime.date.today().strftime("%Y-%m-%d")

    # 既に今日クイズに回答しているか確認
    answered = db_session.query(UsersLastActionDateModel).filter(
        UsersLastActionDateModel.user_id == user_id,
        UsersLastActionDateModel.last_quiz_answer_date == today
    ).first()
    if answered:
        # 422エラーではなく、200で既に回答済みを返す
        return QuizResponse(quiz=None, message="Already answered today's quiz")

    quizzes = db_session.query(QuizzesModel).all()
    if not quizzes:
        # 404エラーではなく、200でクイズ無しを返す
        return QuizResponse(quiz=None, message="No quizzes found")

    quiz_count = len(quizzes)
    # user_idと日付で決定
    hash_input = f"{user_id}_{today}".encode()
    hash_value = int(hashlib.sha256(hash_input).hexdigest(), 16)
    quiz_index = hash_value % quiz_count

    quiz = quizzes[quiz_index]
    quiz_schema = Quiz(
        id=quiz.id,
        choice1=quiz.choice1,
        choice2=quiz.choice2,
        choice3=quiz.choice3,
        choice4=quiz.choice4,
        quiz=quiz.quiz,
        answer=quiz.answer,
    )
    return QuizResponse(quiz=quiz_schema, message="OK")


#クイズに答えた場合users_last_action_dateのlast_quiz_answer_dateを更新するAPI
@app.put("/quiz/last_answerdate/{user_id}", response_model=UsersLastActionDateResponse)	
def update_last_quiz_answer_date(user_id: str, db_session: Session = Depends(get_db_session)):
    today = datetime.date.today().strftime("%Y-%m-%d")
    user = db_session.query(UsersLastActionDateModel).filter(UsersLastActionDateModel.user_id == user_id).first()
    if user:
        user.last_quiz_answer_date = today
        db_session.commit()
        return UsersLastActionDateResponse(user_id=user_id, date=today)
    else:
        # ユーザーがいない場合は新規作成する場合など、適宜対応
        user = UsersLastActionDateModel(user_id=user_id, last_quiz_answer_date=today)
        db_session.add(user)
        db_session.commit()
        return UsersLastActionDateResponse(user_id=user_id, date=today)


# チャットの返信を生成し、chats DBに登録した後、フロントエンドにAI_personalized API
@app.post("/create_reply", response_model=ChatCreateResponse)
def create_reply(chat_create_request: ChatCreateRequest, db_session: Session = Depends(get_db_session)):

    AI_objective_answer = create_objective_reply(chat_create_request)
    AI_personalized_answer=AI_objective_answer
    post_chat(
        ChatRequest(
            user_id=chat_create_request.user_id,
            date_time=chat_create_request.date_time,
            user_prompt=chat_create_request.user_prompt,
            AI_objective_answer=AI_objective_answer,
            AI_personalized_answer=AI_personalized_answer
        ),
        db_session=db_session
    ).chat.AI_personalized_answer  # chats DBに登録したAI_personalized_answerを再取得。

    return ChatCreateResponse(AI_personalized_answer=AI_personalized_answer)


@app.post("/create_reply/objective", response_model= str)
def create_objective_reply(chat_create_request: ChatCreateRequest, db_session: Session = Depends(get_db_session)):
    # return stub()

    load_dotenv()  # .envファイルから環境変数を読み込む
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")  # 環境変数からアクセスキーを取得
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")  # 環境変数からシークレットキーを取得
    client = boto3.client(
        'bedrock-runtime',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name="us-east-1"
    )

    # [要変更] EFの内容は別の関数で持ってくるようにする。
    EF = "1. 日々行動する。2. 他者に配慮する。3. 目標を持つ。4. 自分の感情を理解する。5. 自分の行動を振り返る。6. 他者と協力する。7. 自分の価値観を持つ。8. 健康的な生活を送る。9. 学び続ける。10. 社会に貢献する。"
    initial_prompt = f"""
        ユーザーとチャットをしてもらいます。
        会話の中で、もし以下の[基準]に関連する内容があれば、ユーザーにそれを教えて褒めてください。
        回答は短文で、あくまで、ユーザーとの気軽なチャットであることを忘れないでください。
        もしも、[基準]に関連する内容が見つからなかった場合は、ユーザーの入力を受け入れ、自然な会話を続けてください。
        [基準]：{EF}[基準ここまで]
    """

    # initial_prompt + 会話の履歴 をBedrockに与えるためのリスト
    messages = []
    messages.append({
        "role": "user",
        "content": initial_prompt
    })
    messages.append({
        "role": "user",
        "content": chat_create_request.user_prompt
    })

    body = json.dumps(  # JSON形式でリクエストボディを作成
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": messages
        }
    )

    # AIへリクエストを送信
    response = client.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0", # Claude 3.5 Sonnet
        body=body
    )
    response_body = json.loads(response.get('body').read())  # JSON形式でレスポンスを取得
    AI_answer = response_body["content"][0]["text"]  # JSONから必要な部分を抽出

    return AI_answer

def stub() -> str:
    # これはcreate_objective_replyのスタブ関数です。
    ls = [
        "ハチは地球上で最も重要な生物と呼ばれています。",
        "富士山は日本で最も高い山で、標高は3,776メートルです。",
        "タコには3つの心臓があります。",
        "シロクマの肌は実は黒色です。",
        "カタツムリの歯の数は1万本以上あります。",
        "バナナはベリー類に分類されます。",
        "キリンの首には人間と同じ数の骨（7個）があります。",
        "オウムは自分の名前を認識できることがあります。",
        "地球上で最も古い木は約5,000歳です。",
        "カメレオンは舌を体の2倍以上の長さまで伸ばせます。"
    ]
    return ls[random.randint(0, len(ls) - 1)]
