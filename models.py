"""
DBモデル定義を行うファイル。
chats DB やsummary DBといったテーブルを# pythonプログラムに読み込む際に必要な型定義を記述する。
"""
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# chats DBのモデル定義
class ChatsModel(Base):
    __tablename__ = "chats" # テーブル名
    user_id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, primary_key=True, index=True)
    user_prompt = Column(String)
    AI_objective_answer = Column(String)
    AI_personalized_answer = Column(String)


# summaries DBのモデル定義
class SummariesModel(Base):
    __tablename__ = "summaries" # テーブル名
    user_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, primary_key=True, index=True)
    summary = Column(String)

# quizzes DBのモデル定義
class QuizzesModel(Base):
    __tablename__ = "quizzes"  # テーブル名
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quiz = Column(String)
    answer = Column(String)
    choice1 = Column(String, primary_key=True, index=True)
    choice2 = Column(String, primary_key=True, index=True)
    choice3 = Column(String, primary_key=True, index=True)
    choice4 = Column(String, primary_key=True, index=True)

# users_last_action_date DBのモデル定義
class UsersLastActionDateModel(Base):
    __tablename__ = "users_last_action_date"  # テーブル名
    user_id = Column(String, nullable=False, primary_key=True, index=True)
    last_login_date = Column(Date)
    last_quiz_answer_date = Column(Date)
   
# EF DBのモデル定義
class EFModel(Base):
    __tablename__ = "EF"  # テーブル名
    dimension = Column(Integer, nullable=False)
    sub_dimension = Column(Integer)
    detailed_category = Column(String)
    class_ = Column(Integer, name = "class",nullable=False)  # 'class'は予約語のためclass_
    content = Column(String, primary_key=True, index=True)

#EPRs DBのモデル定義
class  EPRsModel(Base):
    __tablename__ = "EPRs"  # テーブル名
    user_id = Column(String, nullable=False, primary_key=True, index=True)
    project_name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False, primary_key=True, index=True)
    goal1 = Column(String)
    goal2 = Column(String)
    goal3 = Column(String)
    goal4 = Column(String)


    