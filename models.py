"""
DBモデル定義を行うファイル。
chats DB やsummary DBといったテーブルを# pythonプログラムに読み込む際に必要な型定義を記述する。
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

"""
2025/06/24現在、chatsテーブルにはuser_promptは存在しないため、コメントアウトした。
後ほどchatsテーブルとともに修正すべし。
"""
class ChatsModel(Base):
    __tablename__ = "chats" # テーブル名
    user_id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, primary_key=True, index=True)
    # user_prompt = Column(String)
    AI_objective_answer = Column(String)
    AI_personalized_answer = Column(String)
