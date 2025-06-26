"""
DBモデルからschemaへの変換といった、汎用的な処理を記述する。
"""

from models import *
from schemas import *

# ChatsModelモデルからChatスキーマへの変換
def convert_chat_model_to_chat_schema(chat_model: ChatsModel) -> Chat:
    return Chat(
        user_id=chat_model.user_id,
        date_time=chat_model.date_time,
        user_prompt=chat_model.user_prompt,
        AI_objective_answer=chat_model.AI_objective_answer,
        AI_personalized_answer=chat_model.AI_personalized_answer
    )

# ChatスキーマからChatsModelモデルへの変換
def convert_chat_schema_to_chat_model(chat_schema: Chat) -> ChatsModel:
    return ChatsModel(
        user_id=chat_schema.user_id,
        date_time=chat_schema.date_time,
        user_prompt=chat_schema.user_prompt,
        AI_objective_answer=chat_schema.AI_objective_answer,
        AI_personalized_answer=chat_schema.AI_personalized_answer
    )

# SummariesModelモデルからSummaryスキーマへの変換
def convert_summary_model_to_summary_schema(summary_model: SummariesModel) -> Summary:
    return Summary(
        user_id=summary_model.user_id,
        date=summary_model.date,
        summary=summary_model.summary
    )

# SummaryスキーマからSummariesModelモデルへの変換
def convert_summary_schema_to_summary_model(summary_schema: Summary) -> SummariesModel:
    return SummariesModel(
        user_id=summary_schema.user_id,
        date=summary_schema.date,
        summary=summary_schema.summary
    )