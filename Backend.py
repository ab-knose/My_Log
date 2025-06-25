from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import datetime

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# DB接続設定
#DATABASE_URL要修正
DATABASE_URL = "mysql+pymysql://admin:Digitaldev1@group1-chats.c7c4ksi06r6a.ap-southeast-2.rds.amazonaws.com:3306/group1"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

# DB_chatsのモデル定義
class ChatsModel(Base):
    __tablename__ = "chats" # テーブル名
    user_id = Column(Integer, primary_key=True, index=True) # 主キー
    date_time = Column(DateTime, primary_key=True, index=True) # 日時
    # user_prompt = Column(String)
    AI_objective_answer = Column(String)
    AI_personalized_answer = Column(String)

# DB_summariesのモデル定義
class SummariesModel(Base):
    __tablename__ = "summaries" # テーブル名
    user_id = Column(Integer, primary_key=True, index=True) # 主キー
    date = Column(DateTime.date, primary_key=True, index=True) # 日時
    summary = Column(String)

# DB_chatsのレスポンススキーマ定義
class ChatsResponse(BaseModel):
    user_id: str
    date_time: datetime.datetime
    AI_objective_answer: str
    AI_personalized_answer: str

# DB_summariesのレスポンススキーマ定義
class SummariesResponse(BaseModel):
    user_id: str
    date: datetime.date
    summary: str


# DB test
@app.get("/chats/{user_id}", response_model=ChatsResponse)
# user_id = user001をブラウザやポストマンで入力すること。
def get_chat(user_id: str, db_session: Session = Depends(get_db_session)):
    data = db_session.query(ChatsModel).filter(ChatsModel.user_id == user_id).first()
    return data

# post_chat
@app.post("/chats", response_model=ChatsResponse)
def post_chat(chat: ChatsResponse, db_session: Session = Depends(get_db_session)):
    db_chat = ChatsModel(chat)
    db_session.add(db_chat)
    db_session.commit()
    db_session.refresh(db_chat)
    return db_chat

# get_summaries
@app.get("/chats/summaries", response_model=list[SummariesModel])
def get_summaries(db_session: Session = Depends(get_db_session)):
    data = db_session.query(SummariesModel).all()
    return data

# post_summaries
@app.post("/chats/summaries", response_model=SummariesResponse)
def post_summary(summary: SummariesResponse, db_session: Session = Depends(get_db_session)):
    db_summary = SummariesModel(summary)
    db_session.add(db_summary)
    db_session.commit()
    db_session.refresh(db_summary)
    return db_summary

