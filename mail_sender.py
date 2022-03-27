from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from smtplib import SMTP_SSL
from mimetypes import guess_type
from email.mime.text import MIMEText
from os import getenv, listdir
from os.path import isfile, exists, basename
from email.mime.multipart import MIMEMultipart


def send_email(email, subject, text, attachments):
    addr_from = getenv("FROM")
    msg = MIMEMultipart()
    msg["From"] = addr_from
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(text, "plain"))
    process_attachments(msg, attachments)
    server = SMTP_SSL(getenv("HOST"), getenv("PORT"))
    server.login(addr_from, getenv("PASSWORD"))
    server.send_message(msg)
    server.quit()


def process_attachments(msg, attachments):
    for f in attachments:
        if isfile(f):
            attach_file(msg, f)
        elif exists(f):
            for file in listdir(f):
                attach_file(msg, f + "/" + file)


def attach_file(msg, f):
    attach_types = {"text": MIMEText, "image": MIMEImage, "audio": MIMEAudio}
    ctype, encoding = guess_type(f)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split('/', 1)
    with open(f, mode="rb" if maintype != "text" else "r") as fp:
        if maintype in attach_types:
            file = attach_types[maintype](fp.read(), _subtype=subtype)
        else:
            file = MIMEBase(maintype, subtype)
            file.set_payload(fp.read())
            encoders.encode_base64(file)
    file.add_header("Content-Disposition", "attachment", filename=basename(f))
    msg.attach(file)
