# FastAPIおよびpydantic
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
# general
import datetime
# 自作のmodels, schemas, crud
# from models import ChatsModel
from schemas import Chat, Chats, ChatResponse, ChatsResponse, ChatRequest
# from crud import *

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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

# DBモデル定義
class ChatsModel(Base):
    __tablename__ = "chats" # テーブル名
    user_id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, primary_key=True, index=True)
    # user_prompt = Column(String)
    AI_objective_answer = Column(String)
    AI_personalized_answer = Column(String)

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

@app.get("/")
def get_root():
    return {"message": "Welcome to the My Log app!"}

# chatsテーブルから単一のchatデータを取得するAPI
# 仕様書には無いが、テスト用に作っておく。エンドポイントに注意。
@app.get("/chats/single/{user_id}", response_model=ChatResponse)
def get_chat(user_id: str, db_session: Session = Depends(get_db_session)):
    db_chat = db_session.query(ChatsModel).filter(ChatsModel.user_id == user_id).first()
    print()
    return ChatResponse(chat=Chat(db_chat))
    # もともとdataはresponse_modelに適合しているが、一応、明示的にresponse_modelに変換しておく。




"""# chatsテーブルから複数のchatデータを取得するAPI
@app.get("/chats/{user_id}", response_model=ChatsResponse)
def get_chats(user_id: str, db_session: Session = Depends(get_db_session)):
    db_chats = db_session.query(ChatsModel).filter(ChatsModel.user_id == user_id).all()
    return ChatsResponse(chats=db_chats)

# chatsテーブルに単一のchatデータを登録するAPI
@app.post("/chats/", response_model=ChatResponse)
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
    return ChatResponse(chat=db_chat)"""