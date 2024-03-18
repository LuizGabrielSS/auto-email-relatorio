import imaplib
import email
from email.header import decode_header
from private.email import EMAIL,PASSWORD 

from components.tratando_email import TratandoMensagemEmail,PuxandoInfo,TratandoBody
from components.classificador import Classificador
from components.telegram import EnviarRelatorio

relatorio = []

imap_url = 'imap.gmail.com'
 
# Configurações do servidor IMAP do Gmail
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

# Conectar ao servidor IMAP do Gmail
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)

# Selecionar a caixa de entrada (inbox)
mail.select('inbox')
# Procurar todos os e-mails na caixa de entrada
status, messages = mail.search(None, 'UNSEEN')

if status == 'OK':
    # Lista de IDs de e-mail
    messages_ids = messages[0].split()

    spam = 0
    
    for msg_id in messages_ids:
        # Buscar o e-mail pelo ID
        status, data = mail.fetch(msg_id, '(RFC822)')
        if status == 'OK':
            
            email_message = TratandoMensagemEmail(data,email)

            if(email_message != None):

                email_info = PuxandoInfo(email_message)
                
                body = TratandoBody(email_message)

                dados_relatorio = None

                try:

                    if(body != None):

                        dados_relatorio = Classificador(body)
                    
                    else:

                        if(email_info['subject'] != None):

                            dados_relatorio = Classificador(email_info['subject'])

                    if(dados_relatorio != None):

                        if(dados_relatorio['Categoria'] == "spam"):

                            spam = spam + 1

                        else:

                            relatorio.append({
                                "remetente":email_info['sender'],
                                "data":email_info['date_sent'],
                                "Tema_central":dados_relatorio['Tema_central'],
                                "Resumo":dados_relatorio['Produto']
                            })

                            mail.store(msg_id, '+FLAGS', '\\Seen')
                except: 

                    print('erro')
                # Imprimindo informações
                # print("Remetente:", email_info['sender'])
                # print("Assunto:", email_info['subject'])
                # print("Data de Envio:", email_info['date_sent'])
                # print("Corpo do Email:", body)
                # print("Cabeçalhos Adicionais:")
                # if(email_info['headers'] != None):
                #     for header in email_info['headers']:
                #         print(header)
                # print("ID do Email:", email_info['email_id'])
                # print("="*50)

            else:

                print(email_message)
# Fechar a conexão com o servidor IMAP
mail.logout()

relatorio_msg = "INICIO DO RELATORIO \n\n\n"

for i in relatorio:

    relatorio_msg = relatorio_msg + f"""
        Tema central:{i['Tema_central']}
        Data do envio:{i['data']}
        Remetente:{i['remetente']}
        Resumo:{i['Resumo']}
        {"="*5}
        \n
    """

relatorio_msg = relatorio_msg + "\n\n\n Numero de spams = " + str(spam)

relatorio_msg = relatorio_msg + "\n\n\n FIM DO RELATORIO"

EnviarRelatorio(relatorio_msg)