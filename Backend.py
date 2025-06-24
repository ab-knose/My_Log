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
DATABASE_URL = r"mysql+pymysql://admin:Digitaldev1@group1-chats.c7c4ksi06r6a.ap-southeast-2.rds.amazonaws.com:3306/group1"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

# DBモデル定義
class ChatsModel(Base):
    __tablename__ = "chats" # テーブル名
    user_id = Column(Integer, primary_key=True, index=True) # 主キー
    datetime = Column(DateTime)
    user_prompt = Column(String)
    AI_objective_answer = Column(String)
    AI_personalized_answer = Column(String)

# DB_chatsのリクエストスキーマ定義
class ChatsRequest(BaseModel):
    user_id: str
    date_time: datetime.datetime

# DB_chatsのレスポンススキーマ定義
class ChatsResponse(BaseModel):
    chats: list[str]


# DB test
@app.get("/chats/{user_id}", response_model=ChatsResponse)
def get_chat(user_id: str, db_session: Session = Depends(get_db_session)):
    data = db_session.query(ChatsModel).filter(ChatsModel.user_id == user_id).all()
    # itemが見つからない場合は404エラーを返す
    if data is None:
        print("data is None")
        raise HTTPException(status_code=404, detail="data not found")
    return ChatsResponse(chats=data)

@app.get("/chats", response_model=ChatsResponse)
def get_chats(db_session: Session = Depends(get_db_session)):
    data = db_session.query(ChatsModel).filter(ChatsModel.user_id).all()
    # itemが見つからない場合は404エラーを返す
    if data is None:
        raise HTTPException(status_code=404, detail="data not found")
    return ChatsResponse(chats=data)

@app.post("/chats", response_model=ChatsResponse)
def get_chats(user_id: str, db_session: Session = Depends(get_db_session)):
    data = db_session.query(ChatsModel).filter(ChatsModel.user_id == user_id).all()
    # itemが見つからない場合は404エラーを返す
    if data is None:
        raise HTTPException(status_code=404, detail="data not found")
    return ChatsResponse(chats=data)