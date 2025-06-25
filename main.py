# FastAPIおよびpydantic
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
# general
import datetime
# 自作のmodels, schemas, crud
from models import *
from schemas import *
# from crud import *


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


@app.get("/")
def get_root():
    return {"message": "Welcome to the My Log app!"}

# chatsテーブルから単一のchatデータを取得するAPI
# 仕様書には無いが、テスト用に作っておく。エンドポイントに注意。
@app.get("/chats/single/{user_id}", response_model=ChatResponse)
def get_chat(user_id: str, db_session: Session = Depends(get_db_session)):
    db_chat = db_session.query(ChatsModel).filter(ChatsModel.user_id == user_id).first()
    print()
    chat = Chat(
        user_id=db_chat.user_id,
        date_time=db_chat.date_time,
        AI_objective_answer=db_chat.AI_objective_answer,
        AI_personalized_answer=db_chat.AI_personalized_answer
    )
    return ChatResponse(chat=chat)
    # もともとdataはresponse_modelに適合しているが、一応、明示的にresponse_modelに変換しておく。

# chatsテーブルから複数のchatデータを取得するAPI
@app.get("/chats/{user_id}", response_model=ChatsResponse)
def get_chats(user_id: str, db_session: Session = Depends(get_db_session)):
    db_chats = db_session.query(ChatsModel).filter(ChatsModel.user_id == user_id).all()
    chats = [Chat(
        user_id=db_chats[i].user_id,
        date_time=db_chats[i].date_time,
        AI_objective_answer=db_chats[i].AI_objective_answer,
        AI_personalized_answer=db_chats[i].AI_personalized_answer
    ) for i in range(len(db_chats))]  # db_chatsの各要素をChatスキーマに変換

    return ChatsResponse(chats=chats)

# chatsテーブルに単一のchatデータを登録するAPI
@app.post("/chats", response_model=ChatResponse)
def create_chat(chat_request: ChatRequest, db_session: Session = Depends(get_db_session)):
    db_chat = ChatsModel(
        user_id=chat_request.user_id,
        date_time=chat_request.date_time,
        AI_objective_answer=chat_request.AI_objective_answer,
        AI_personalized_answer=chat_request.AI_personalized_answer
    )  # chats DBに登録するためのインスタンス。chat_requestから必要な属性を取り出して設定する。
    db_session.add(db_chat)
    db_session.commit()
    db_session.refresh(db_chat)
    return ChatResponse(chat=chat_request)

# get_summaries
@app.get("/summaries/single/{user_id}", response_model=SummaryResponse)
def get_summaries(user_id: str, db_session: Session = Depends(get_db_session)):
    db_summary = db_session.query(SummariesModel).filter(SummariesModel.user_id == user_id).first()
    summary = Summary(
        user_id=db_summary.user_id,
        date=db_summary.date,
        summary=db_summary.summary
    )
    return SummaryResponse(summary=summary)

# post_summaries
@app.post("/summaries", response_model=SummariesResponse)
def post_summary(summary: SummariesResponse, db_session: Session = Depends(get_db_session)):
    db_summary = SummariesModel(summary)
    db_session.add(db_summary)
    db_session.commit()
    db_session.refresh(db_summary)
    return db_summary

# get_labeled_dates
@app.get("/chats/labeled_dates/{user_id}", response_model=list[datetime.date])
def get_labeled_dates(user_id: str, db_session: Session = Depends(get_db_session)):
    db_chats = db_session.query(ChatsModel).filter(ChatsModel.user_id == user_id).all()
    # 日付だけを抽出し、重複をなくす
    labeled_dates = list({chat.date_time.date() for chat in db_chats})
    labeled_dates.sort()
    return labeled_dates
