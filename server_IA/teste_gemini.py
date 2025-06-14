import requests
import json

url = "http://172.17.86.223:8000/chat"

template = "Abaixo está o conteudo de um email, verifique se há possiveis reunioes ou eventos que possam ser agendados. Tarefas e atividades, entregas, trabalhos também devem ser considerados" \
"Se houver, responda com algo tipo '2025-07-21T14:00:00-03:00 Jogar bola com Miguel', se não responda com 'não há eventos agendados', nao responda nada alem disso" 
"Se houver elementos como 'outra reuniao' ou 'outro agendamento', considere que é uma reunião já agendada e deve ser criada uma nova reunião com nome tipo 'reuniao com davi 2'"
"Se voce identificar mais de um evento, responda com varios eventos separados por objeto, por exemplo: '2025-07-21T14:00:00-03:00 Jogar bola com Miguel, 2025-07-22T10:00:00-03:00 Reuniao com Davi 2'"


# emails = "Emails:\n\n1. de: Miguel, para: mim, Olá, gostaria de marcar uma reunião na próxima segunda-feira às 10h."
# emails = "Emails:\n\n1. de: Miguel, para: mim, Olá, gostaria de marcar outra reunião na próxima segunda-feira às 16h."
emails = "quarta, 18 de junho de 2025 Evento de atividade Submissão do Trabalho #2 está marcado(a) para esta data ELC133 - QUALIDADE DE SOFTWARE Trabalho 1 - Análise de Tráfego IP - 08/05 Aberto: segunda, 14 abr 2025, 00:00 Vencimento: quinta, 8 mai 2025, 23:59"

# "se for muito especifico, tipo assunto especifico semelhante e diferenca de data < 2 meses, considerar como evento semelhante e remarcar"


headers = {
    "Authorization": "Bearer sk-7aTQ9NpzV3w2uE4LmRbJxYcAq6ZHtXfG",
    "Content-Type": "application/json"
}
payload = {"prompt": f"{template}{emails}"}

response = requests.post(url, headers=headers, json=payload)
print(response.json())

# salvar json de resposta
with open("resposta.json", "w", encoding="utf-8") as f:
    json.dump(response.json(), f, indent=4, ensure_ascii=False)




# curl -X POST http://172.17.86.223:8000/chat ^
#   -H "Authorization: Bearer sk-7aTQ9NpzV3w2uE4LmRbJxYcAq6ZHtXfG" ^
#   -H "Content-Type: application/json" ^
#   -d "{\"prompt\": \"O que é CBR em IA?\"}"