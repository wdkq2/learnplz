import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

app = Flask(__name__, template_folder='templates')

# OpenAI API 키를 환경 변수에서 가져옵니다.
API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

@app.route('/')
def index():
    """메인 웹페이지를 렌더링합니다."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    프론트엔드로부터 요청을 받아 OpenAI API를 호출하고 결과를 반환합니다.
    """
    if not API_KEY:
        print("🛑 오류: .env 파일에 OPENAI_API_KEY가 설정되지 않았습니다.")
        return jsonify({"error": ".env 파일에 OPENAI_API_KEY가 설정되지 않았습니다."}), 500

    data = request.json
    
    # 프론트엔드에서 받은 데이터를 기반으로 OpenAI에 보낼 payload를 구성합니다.
    payload = {
        "model": "gpt-4o",
        "messages": [{
            "role": "user",
            "content": data.get("content_parts", [])
        }],
        "max_tokens": 4096
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    try:
        print("🚀 OpenAI API에 분석을 요청합니다...")
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.
        print("✅ OpenAI API로부터 응답을 받았습니다.")
        return jsonify(response.json())
        
    except requests.exceptions.RequestException as e:
        # API 호출 실패 시 에러 메시지를 JSON 형식으로 반환합니다.
        error_message = str(e)
        if e.response:
            try:
                error_detail = e.response.json()
                error_message = error_detail.get("error", {}).get("message", "알 수 없는 오류")
            except ValueError:
                error_message = e.response.text
        
        print(f"🛑 OpenAI API 호출 실패: {error_message}")
        return jsonify({"error": f"OpenAI API 호출 실패: {error_message}"}), 500

if __name__ == '__main__':
    port = 5001
    print(f"✅ 서버를 시작합니다. http://127.0.0.1:{port} 에서 접속하세요.")
    app.run(debug=True, port=port)