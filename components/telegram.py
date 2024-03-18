import requests

from private.telegram import api_token,chat_id

def EnviarRelatorio(relatorio):

    mensagem = 'Olá, Segue o relatorio com os emails recebidos'

    url = f'https://api.telegram.org/bot{api_token}/sendMessage'

    payload = {'chat_id': chat_id, 'text': mensagem}

    requests.post(url, json=payload)

    payload = {'chat_id': chat_id, 'text': relatorio}

    requests.post(url, json=payload)