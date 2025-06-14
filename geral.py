from flask import Flask, jsonify, request
import requests
import teste_gemini

app = Flask(__name__)
url_ia = 'http://192.168.66.241:8000/chat'
url_calendario = 'http://192.168.66.170/8080/api/events'

def enviar_calendario(summary, startDateTime endDateTime):
    dados = {"summary": summary, "endDateTime":endDateTime, "startDateTime":startDateTime}

    payload = {
        "summary": "MIGUEL",
        "location": "Remoto",
        "description": "Este evento foi criado a partir de uma requisição POST.",
        "startDateTime": "2025-07-20T14:00:00-03:00",
        "endDateTime": "2025-07-20T15:00:00-03:00"
    }

    try:
        resposta = requests.post(url_calendario, json=payload)
        return jsonify({"status":"enviado", "resposta": resposta.json()}), resposta.status_code
    except Exception as e:
        print(e)
        return jsonify({"erro": str(e)}), 500

def enviar_ia():
    teste_gemini.mainIA()


@app.route('/recebendo_emails', methods=['POST'])
def recebendo_emails():
    conteudo = request.get_json()

    titulo = conteudo.get('subject')
    remetente = conteudo.get('from')
    corpo = conteudo.get('text')
    destinatario = conteudo.get('to')
    dia = conteudo.get('date')

    print(titulo)
    print(remetente)
    print(corpo)

    if not corpo:
        return jsonify({"erro": "Campo 'corpo' é obrigatório."}), 400
    
    enviar_ia()

    return jsonify({
        "mensagem": "JSON recebido com sucesso",
        "titulo": titulo,
        "remetente": remetente,
        "corpo": corpo,
        "destinatario": destinatario,
        "data": dia
    })


app.run(host="0.0.0.0", port=5000, debug=True)