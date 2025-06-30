# FastAPIおよびpydantic
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

# Bedrock
import boto3
from dotenv import load_dotenv
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
from crud import *
from utils import *
from db import get_db_session
from app_base import app
from mangum import Mangum

from ses import *




"""Bedrockの設定"""
load_dotenv()  # .envファイルから環境変数を読み込む
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")  # 環境変数からアクセスキーを取得
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")  # 環境変数からシークレットキーを取得
client = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="us-east-1"
)




"""大きなAPI定義"""


# EPRsテーブルに初回のEPRの内容を登録するAPI	
@app.post("/epr", response_model=EPRsResponse)
def post_epr(epr_request: EPRsRequest, db_session: Session = Depends(get_db_session)):	
    # EPRsModelに変換
    db_epr = EPRsModel(
        user_id=epr_request.user_id,
        project_name=epr_request.project_name,
        start_date=epr_request.start_date,
        goal1=epr_request.goal1,
        goal2=epr_request.goal2,
        goal3=epr_request.goal3,
        goal4=epr_request.goal4,
    )
    db_session.add(db_epr)
    db_session.commit()
    db_session.refresh(db_epr)
    return EPRsResponse(
        epr=EPRs(
            user_id=db_epr.user_id,
            project_name=db_epr.project_name,
            start_date=db_epr.start_date,
            goal1=db_epr.goal1,
            goal2=db_epr.goal2,
            goal3=db_epr.goal3,
            goal4=db_epr.goal4
            )
        )
											

# EPRsの内容を更新するAPI
@app.put("/epr", response_model=EPRsResponse)
def update_epr(eprs_upload_request:EPRsUploadRequest,  db_session: Session = Depends(get_db_session)):
    # EPRsModelに変換
    db_epr = db_session.query(EPRsModel).filter(
        EPRsModel.user_id == eprs_upload_request.user_id,
        EPRsModel.project_name == eprs_upload_request.project_name,
        EPRsModel.start_date == eprs_upload_request.start_date,
        EPRsModel.goal1 == eprs_upload_request.goal1,
        EPRsModel.goal2 == eprs_upload_request.goal2,
        EPRsModel.goal3 == eprs_upload_request.goal3,
        EPRsModel.goal4 == eprs_upload_request.goal4
    ).first()

    if not db_epr:
        raise HTTPException(status_code=404, detail="EPR not found")

    # 更新
    db_epr.project_name = eprs_upload_request.project_name
    db_epr.goal1 = eprs_upload_request.goal1
    db_epr.goal2 = eprs_upload_request.goal2
    db_epr.goal3 = eprs_upload_request.goal3
    db_epr.goal4 = eprs_upload_request.goal4

    db_session.commit()
    db_session.refresh(db_epr)

    return EPRsResponse(epr=EPRs(
        user_id=db_epr.user_id,
        project_name=db_epr.project_name,
        start_date=db_epr.start_date,
        goal1=db_epr.goal1,
        goal2=db_epr.goal2,
        goal3=db_epr.goal3,
        goal4=db_epr.goal4
    ))


# チャットの返信を生成し、chats DBに登録した後、フロントエンドにAI_personalized API
@app.post("/create_reply", response_model=ChatCreateResponse)
def create_reply(chat_create_request: ChatCreateRequest, db_session: Session = Depends(get_db_session)):
    AI_objective_answer = create_objective_reply(chat_create_request, db_session=db_session)  # AIの客観的な回答を生成
    AI_personalized_answer=AI_objective_answer
    post_chat(
        ChatRequest(
            user_id=chat_create_request.user_id,
            date_time=chat_create_request.date_time,
            user_prompt=chat_create_request.user_prompt,
            AI_objective_answer=AI_objective_answer,
            AI_personalized_answer=AI_personalized_answer
        ),
        db_session=db_session
    ).chat.AI_personalized_answer  # chats DBに登録したAI_personalized_answerを再取得。

    return ChatCreateResponse(AI_personalized_answer=AI_personalized_answer)


@app.post("/create_reply/objective", response_model= str)
def create_objective_reply(chat_create_request: ChatCreateRequest, db_session: Session = Depends(get_db_session)):
    # return stub()

    # [要変更] EFの内容は別の関数で持ってくるようにする。
    EF = "1. 日々行動する。2. 他者に配慮する。3. 目標を持つ。4. 自分の感情を理解する。5. 自分の行動を振り返る。6. 他者と協力する。7. 自分の価値観を持つ。8. 健康的な生活を送る。9. 学び続ける。10. 社会に貢献する。"
    initial_prompt = f"""
        ユーザーとチャットをしてもらいます。
        会話の中で、もし以下の[基準]に関連する内容があれば、ユーザーにそれを教えて褒めてください。
        [注意]
        ・あくまで、ユーザーとの気軽なチャットであることを忘れないでください。
        ・回答は50字程度の短文としてください。
        ・もしも、[基準]に関連する内容が見つからなかった場合は、ユーザーの入力を受け入れ、自然な会話を続けてください。
        [注意ここまで]
        [基準]：{EF}[基準ここまで]
    """

    # initial_prompt + 会話の履歴 をBedrockに与えるためのリスト
    messages = []
    messages.append({
        "role": "user",
        "content": initial_prompt
    })  # Bedrockへの指示を最初に追加

    # 当日のユーザーのチャット履歴を取得
    today = chat_create_request.date_time.date()
    chats = get_chats_internal(user_id=chat_create_request.user_id, start_date=today, end_date=today, db_session=db_session).chats

    for chat in chats: # ユーザーとAIの応答を交互に追加
        messages.append({
            "role": "user",
            "content": chat.user_prompt
        })
        messages.append({
            "role": "assistant",
            "content": chat.AI_objective_answer
        })

    messages.append({
        "role": "user",
        "content": chat_create_request.user_prompt
    })  # ユーザーの入力を追加

    AI_objective_answer = communicate_with_bedrock(client=client,
        messages=messages,
        db_session=db_session
    )
    return AI_objective_answer


def communicate_with_bedrock(client: boto3.client, messages: list[dict], db_session: Session = Depends(get_db_session)) -> str:
    # return stub()
    body = json.dumps(  # JSON形式でリクエストボディを作成
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": messages
        }
    )

    # AIへリクエストを送信
    response = client.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0", # Claude 3.5 Sonnet
        body=body
    )
    response_body = json.loads(response.get('body').read())  # JSON形式でレスポンスを取得
    AI_answer = response_body["content"][0]["text"]  # JSONから必要な部分を抽出

    return AI_answer

def stub() -> str:
    # これはcreate_objective_replyのスタブ関数です。
    ls = [
        "ハチは地球上で最も重要な生物と呼ばれています。",
        "富士山は日本で最も高い山で、標高は3,776メートルです。",
        "タコには3つの心臓があります。",
        "シロクマの肌は実は黒色です。",
        "カタツムリの歯の数は1万本以上あります。",
        "バナナはベリー類に分類されます。",
        "キリンの首には人間と同じ数の骨（7個）があります。",
        "オウムは自分の名前を認識できることがあります。",
        "地球上で最も古い木は約5,000歳です。",
        "カメレオンは舌を体の2倍以上の長さまで伸ばせます。"
    ]
    return ls[random.randint(0, len(ls) - 1)]



@app.post("/create_summary/{user_id}/{start_date}_{end_date}", response_model=str)
def create_objective_summary(user_id: str, start_date: datetime.date, end_date: datetime.date, db_session: Session = Depends(get_db_session)):
    chats = get_chats_internal(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        db_session=db_session
    )

    initial_prompt = f"""
        ユーザーとチャットをしてもらいます。
        会話の中で、もし以下の[基準]に関連する内容があれば、ユーザーにそれを教えて褒めてください。
        [注意]
        ・あくまで、ユーザーとの気軽なチャットであることを忘れないでください。
        ・回答は50字程度の短文としてください。
        ・もしも、[基準]に関連する内容が見つからなかった場合は、ユーザーの入力を受け入れ、自然な会話を続けてください。
        [注意ここまで]
        [基準]：{EF}[基準ここまで]
    """

    # initial_prompt + 会話の履歴 をBedrockに与えるためのリスト
    messages = []
    messages.append({
        "role": "user",
        "content": initial_prompt
    })  # Bedrockへの指示を最初に追加


    for chat in chats: # ユーザーとAIの応答を交互に追加
        messages.append({
            "role": "user",
            "content": chat.user_prompt
        })
        messages.append({
            "role": "assistant",
            "content": chat.AI_objective_answer
        })

    messages.append({
        "role": "user",
        "content": chat_create_request.user_prompt
    })  # ユーザーの入力を追加

    AI_objective_answer = communicate_with_bedrock(client=client,
        messages=messages,
        db_session=db_session
    )
    return AI_objective_answer

handler = Mangum(app)  # AWS LambdaでFastAPIを使用するためのハンドラー
