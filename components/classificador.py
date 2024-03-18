import google.generativeai as genai
import json

from private.api_key_gemini import api_key

genai.configure(api_key=api_key)

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

lista_categorias_possiveis = "spam,não spam"

formato_saida = {
    "Produto":"Nome do Produto",
    "Categoria":"apresente a categoria do produto",
    "Tema_central":"resumo em ate 10 palavras sobre o que se trata o texto"
}

exemplo_saida = {
    "Produto":"jogo eletronico",
    "Categoria":"spam",
    "Tema_central":"jogo de corrida"
}

user_entry = f"""
        Você é um categorizador de produtos.
        Você deve assumir as categorias presentes na lista abaixo, não podendo colocar categorias de fora dessa listagem e dando o tema central do texto de forma resumida.

        # Lista de Categorias Válidas
        {lista_categorias_possiveis.split(",")}

        # Formato da Saída
        {json.dumps(formato_saida)}
        
        # Exemplo de Saída
        {json.dumps(exemplo_saida)}
    """

exemplo_saida_machine = {
    "Produto":"Artigo sobre a importância da segurança cibernética",
    "Categoria":"não spam",
    "Tema_central":"Segurança online, proteção de dados"
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings
                              )

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": user_entry
  },
  {
    "role": "model",
    "parts": (json.dumps(exemplo_saida_machine))
  },

])

def Classificador(Input):

    convo.send_message(Input)

    resultado = convo.last.text

    result = json.loads(resultado)

    return result