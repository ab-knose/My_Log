# FastAPIおよびpydantic
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
# general
import datetime
# 自作のmodels, schemas, crud
from models import ChatsModel
from schemas import ChatsResponse
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

@app.get("/")
def get_root():
    return {"message": "Welcome to the My Log app!"}

# chastsテーブルからuser_idを指定してchatデータを取得するAPI
# user_id = user001をブラウザやポストマンで入力してテストせよ。
@app.get("/chats/{user_id}", response_model=ChatsResponse)
def get_chat(user_id: str, db_session: Session = Depends(get_db_session)):
    data = db_session.query(ChatsModel).filter(ChatsModel.user_id == user_id).first()
    return data
    # return ChatsResponse(data)
    # もともとdataはresponse_modelに適合しているが、一応、明示的にresponse_modelに変換しておく。