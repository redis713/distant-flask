import smtplib
import imaplib
import ssl
from email.message import EmailMessage
from email.utils import formatdate
from datetime import datetime, timezone
import html2text
from config import Config

#from Demos.OpenEncryptedFileRaw import dst_dir

HOST = Config.HOST
USERNAME = Config.USERNAME
PASSWORD = Config.PASSWORD


def html_to_text(html):
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0
    h.ignore_emphasis = True

    return h.handle(html)


def save_to_sent(msg):
    imap = imaplib.IMAP4_SSL(HOST)
    imap.login(USERNAME, PASSWORD)

    date = datetime.now(timezone.utc)

    imap.append("Sent", "\\Seen", imaplib.Time2Internaldate(date), msg.as_bytes())
    #imap.append("Sent", "\\Seen", None, msg.as_bytes())

    #Проверка
    status, data = imap.select("Sent")
    print("SELECT:", status, data)

    imap.logout()

def send_email(to_email, name, login, password, date_from, date_to):
    smtp_port = 587

    msg = EmailMessage()
    msg["Subject"] = "Дистанционное обучение"
    msg["From"] = "Информационная система <" + USERNAME + ">"
    msg["To"] = to_email
    msg["Date"] = formatdate(localtime=True)


    with open("templates/email_template.html", encoding="utf-8") as f:
        template = f.read()

    html = template.format(
        name=name,
        login=login,
        password=password,
        date_from=date_from,
        date_to=date_to
    )

    text = html_to_text(html)

    #html = text.replace("\n", "<br>")

    msg.set_content(text)
    msg.add_alternative(html, subtype="html")

    context = ssl.create_default_context()

    with smtplib.SMTP(HOST, smtp_port) as server:
        server.starttls(context=context)
        server.login(USERNAME, PASSWORD)
        server.send_message(msg)

    save_to_sent(msg)


#Пример отправки
#send_email('rdskbtmn@yandex.ru', 'Евгений Оооооооооааааа', 'fewepkkef_rj234', 'fksfkewkfke192189421', '19.03.1989', '31.01.2008')

'''
imap = imaplib.IMAP4_SSL(HOST)
imap.login(USERNAME, PASSWORD)

status, folders = imap.list()
for f in folders:
    print(f.decode())

imap.logout()
'''