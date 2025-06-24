"""
FastAPIのrequest, responseのスキーマ定義を行うファイル。
"""
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
import datetime

# DB_chatsのレスポンススキーマ定義
class ChatsResponse(BaseModel):
    user_id: str
    date_time: datetime.datetime
    AI_objective_answer: str
    AI_personalized_answer: str