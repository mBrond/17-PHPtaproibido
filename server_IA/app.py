from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
import requests
import logging

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("server.log"),  
        logging.StreamHandler()
    ]
)

load_dotenv()

app = Flask(__name__)

# Limite de requisições em memória (adequado para simulação local)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["30 per minute"]
)
limiter.init_app(app)

# Tokens e configuração da API Gemini
AUTH_TOKEN = f"Bearer {os.getenv('AUTH_TOKEN')}"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

@app.before_request
def log_request_info():
    logging.info(f"{request.remote_addr} => {request.method} {request.path}")

@app.route("/chat", methods=["POST"])
@limiter.limit("10 per minute")
def chat():
    if request.headers.get("Authorization") != AUTH_TOKEN:
        logging.warning(f"Acesso negado para {request.remote_addr}")
        return jsonify({"error": "Token inválido"}), 401

    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    if not prompt or len(prompt) > 1000:
        return jsonify({"error": "Prompt inválido"}), 400

    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}

    try:
        r = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=10)
        r.raise_for_status()
        resposta = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"response": resposta})
    except requests.RequestException as e:
        logging.error(f"Erro na requisição Gemini: {e}")
        return jsonify({"error": "Erro ao acessar o modelo"}), 502
    except (KeyError, IndexError) as e:
        logging.error(f"Resposta malformada da API: {r.text}")
        return jsonify({"error": "Erro na resposta da API"}), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False,
        ssl_context=("certs/cert.pem", "certs/key.pem")  
    )