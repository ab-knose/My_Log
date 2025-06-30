import boto3
import json

SENDER_MAIL = "ayokita@abeam.com"
RECIPIENT_MAIL = "ayokita@abeam.com"
REGION = "ap-southeast-2"
SUBJECT =  "MyLogで会話を始めよう"
BODY = "ここ一週間会話ができていないようです。MyLogを開いて今日一日を振り返ってみましょう"

def send_email(source, to, subject, body):
    client = boto3.client('ses', region_name=REGION)

    response = client.send_email(
        Source=source,
        Destination={
            'ToAddresses': [
                to,
            ]
        },
        Message={
            'Subject': {
                'Data': subject,
            },
            'Body': {
                'Text': {
                    'Data': body,
                },
            }
        }
    )
    
    return response

def lambda_handler(event, context):
    send_email_to = send_email(SENDER_MAIL, RECIPIENT_MAIL, SUBJECT, BODY)
    print("Send ResponseMetadata:" + json.dumps(send_email_to, ensure_ascii=False))
    return {'send_email': 'success'}