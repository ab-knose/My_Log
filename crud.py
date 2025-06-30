"""
crud操作APIを記述するファイル。
Backend For Frontendの考え方に基づき、
main.pyの大きなAPIから、crud.pyの小さなAPIを呼び出す形にする。
ただし、開発初期の段階では、構造の単純化を優先して、main.pyに直接記述しよう。
ある程度小さなAPIができたら、crud.pyに分離することを検討する。
"""
# FastAPIおよびpydantic
from fastapi import FastAPI, HTTPException, Depends
# SQLAlchemy
from sqlalchemy.orm import sessionmaker, Session
# 自作のdb
from db import get_db_session

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
from utils import *
from app_base import app

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
    return get_chats_internal(user_id, start_date, end_date, db_session=db_session)


def get_chats_internal(user_id: str, start_date: datetime.date, end_date: datetime.date, db_session: Session) -> ChatsResponse:
    """
    内部関数: chatsテーブルから複数のchatデータを取得する。
    これは、他のAPIからも利用されるため、共通の処理として定義している。
    """
    db_chats = db_session.query(ChatsModel).filter(
        ChatsModel.user_id == user_id,
        ChatsModel.date_time >= datetime.datetime.combine(start_date, datetime.time.min),
        ChatsModel.date_time <= datetime.datetime.combine(end_date, datetime.time.max)
    ).all()
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


# chatsテーブルからすべてのchatデータを削除するAPI
"""※危険！使う時は全員の同意を得てからにせよ。"""
@app.delete("/chats", response_model=ChatsResponse)
def delete_all_chats(db_session: Session = Depends(get_db_session)):
    db_chats = db_session.query(ChatsModel).all()
    chats = list(map(convert_chat_model_to_chat_schema, db_chats))  # db_chatsの各要素をChatスキーマに変換
    db_session.query(ChatsModel).delete()  # 全てのchatデータを削除
    db_session.commit()  # 変更をコミット
    return ChatsResponse(chats=chats)


# summariesテーブルから単一のsummaryデータを取得するAPI
# 仕様書には無いが、テスト用に作っておく。エンドポイントに注意。
@app.get("/summaries/single/{user_id}", response_model=SummaryResponse)
def get_summary(user_id: str, db_session: Session = Depends(get_db_session)):
    db_summary = db_session.query(SummariesModel).filter(SummariesModel.user_id == user_id).first()
    return SummaryResponse(summary=convert_summary_model_to_summary_schema(db_summary))  # db_summaryをSummaryスキーマに変換して返す

# summariesテーブルから複数のsummaryデータを取得するAPI
@app.get("/summaries/{user_id}/{start_date}_{end_date}", response_model=SummariesResponse)
def get_summaries(user_id: str, start_date: datetime.date, end_date: datetime.date, db_session: Session = Depends(get_db_session)):
    return get_summaries_internal(user_id, start_date, end_date, db_session=db_session)

def get_summaries_internal(user_id: str, start_date: datetime.date, end_date: datetime.date, db_session: Session = Depends(get_db_session)):
    """
    内部関数: summariesテーブルから複数のsummaryデータを取得する。
    これは、他のAPIからも利用されるため、共通の処理として定義している。
    """
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

def put_summary_internal(summary_request: SummaryRequest, db_session: Session = Depends(get_db_session)):
    """
    内部関数: summariesテーブルに単一のsummaryデータを登録する。
    これは、他のAPIからも利用されるため、共通の処理として定義している。
    """
    db_summary = db_session.query(SummariesModel).filter(
        SummariesModel.user_id == summary_request.user_id,
        SummariesModel.date == summary_request.date
    ).first()
    if db_summary:  # 既に存在する場合は更新
        db_summary = convert_summary_schema_to_summary_model(summary_request)  # SummaryRequestをSummariesModelに変換して、db_summaryを更新する。
        db_session.commit()
        db_session.refresh(db_summary)
        return convert_summary_model_to_summary_schema(db_summary)  # 登録したdb_summaryをSummaryスキーマに変換して返す
    else:  # 無ければ新規作成
        db_summary = convert_summary_schema_to_summary_model(summary_request)  # SummaryRequestをSummariesModelに変換。
        db_session.add(db_summary)
        db_session.commit()
        db_session.refresh(db_summary)
        return convert_summary_model_to_summary_schema(db_summary)  # 登録したdb_summaryをSummaryスキーマに変換して返す

# summariesテーブルからすべてのsummaryデータを削除するAPI
"""※危険！使う時は全員の同意を得てからにせよ。"""
@app.delete("/summaries", response_model=SummariesResponse)
def delete_all_summaries(db_session: Session = Depends(get_db_session)):
    db_summaries = db_session.query(SummariesModel).all()
    summaries = list(map(convert_summary_model_to_summary_schema, db_summaries))  # db_summariesの各要素をSummaryスキーマに変換
    db_session.query(SummariesModel).delete()  # 全てのsummaryデータを削除
    db_session.commit()  # 変更をコミット
    return SummariesResponse(summaries=summaries)


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