import json
import urllib.request

def lambda_handler(event, context):
    try:
        # リクエストボディを取得
        body = json.loads(event['body'])
        message = body.get('message', '')
        conversation_history = body.get('conversationHistory', [])

        # ユーザーの入力（今回は単発メッセージのみ送信）
        user_input = message

        # あなたのFastAPIサーバーのURL（/generate 付き！）
        url = "https://1519-2400-2411-620-1700-a9d8-da47-b2ad-11c6.ngrok-free.app/generate"

        # FastAPIに送るデータ（POST形式）
        payload = json.dumps({
            "prompt": user_input,
            "max_new_tokens": 512,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.9
        }).encode("utf-8")

        # HTTPリクエスト作成
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        # リクエスト実行・応答取得
        with urllib.request.urlopen(req) as res:
            res_body = res.read().decode("utf-8")
            response_data = json.loads(res_body)
            assistant_response = response_data.get("generated_text", "")

        # 会話履歴に応答を追加
        conversation_history.append({"role": "user", "content": message})
        conversation_history.append({"role": "assistant", "content": assistant_response})

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
                "conversationHistory": conversation_history
            })
        }

    except Exception as error:
        print("Error:", str(error))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }
