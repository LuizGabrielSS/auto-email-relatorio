from email.header import decode_header

def TratandoMensagemEmail(data,email):

    try:
        # Obter o conteúdo do e-mail
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

    except:
        email_message = None
        # print('erro no email')
    
    return email_message

def PuxandoInfo(email_message):

    try:

        sender = email_message['From']

    except:

        sender = None

        # print("Erro com o sender")

    try:

        date_sent = email_message['Date']

    except:

        date_sent = None

        # print("Erro com o date_sent")

    try:

        headers = email_message.items()

    except:

        headers = None

        # print("Erro com o headers")

    try:

        email_id = email_message.items()

    except:

        email_id = None

        # print("Erro com o email_id")

    try:

        subject = email_message['Subject']

        if subject:
            subject = decode_header(subject)[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()

    except:

        subject = None

        # print("Erro com o subject")

    return({
        'sender':sender,
        'date_sent':date_sent,
        'subject':subject,
        'email_id':email_id,
        'headers':headers
    })

def TratandoBody(email_message):

    try:
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if "attachment" not in content_disposition:
                    body += part.get_payload(decode=True).decode()
        else:
            body = email_message.get_payload(decode=True).decode()

    except Exception as e:

        body = None

        # print('erro no body')

        # print(e)

        # print('erro no body')

    return body