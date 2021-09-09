import codecs
import smtplib
import qrcode
import qrcode.image.svg
import subprocess
import csv

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from hashlib import blake2b


# Segredo para geração da chave no qr-code
SECRET = b'aoijfoaisjdfoi'

# Linha de comando para chamar o inkscape
# (se não estiver no path, adicione o cominho completo)
INKSCAPE = "inkscape"

# Nome do arquivo CSV com 3 colunas:
# nome, email, participação (palestrante, visitante, voluntário)
ENTRADA = "certificados.csv"
ENTRADA_ENCODING = "cp1252"  # cp1252 se for um csv gerado no excel

# MODELO_DO_CERTIFICADO
MODELO = "certificado.svg"

#
# Email
#

# Email de envio
ENVIA_EMAIL = False
SERVIDOR_SMTP = "smtp.gmail.com:587"  # Este e do gmail.
FROM = "SEU_EMAIL_AQUI@gmail.com"
# Senha do email. No caso do GMAIL, você precisa de uma
# senha para o aplicativo
PASS = "SENHA_DO_EMAIL"
# Esta linha será usada como o subject do email
ASSUNTO_DO_EMAIL = "Certificado de participação - PyCon Amazônia"
# Utilize a sintexe do format do Python. O parâmetro 0 é o nome do participante
CORPO_DO_EMAIL = """Caro(a) {0},

Obrigado por participar da primeira conferência de Python do Norte do Brasil.
Seu certificado está anexado a esta mensagem.

Atenciosamente,

Nilo Ney Coutinho Menezes
Organizador da PyCon Amazônia\n"""


def formata_nome(nome):
    """Converte o nome para minusculas e troca espacos por _"""
    nome = nome.lower().replace(" ", "_")
    return f"certificado - {nome}.pdf"


def gera_certificado(nome, participacao):
    # factory = qrcode.image.svg.SvgPathImage
    h = blake2b(key=SECRET, digest_size=16)
    h.update(nome.encode("utf-8"))
    h.update(participacao.encode("utf-8"))
    chave = h.hexdigest()
    img = qrcode.make(chave)  # image_factory=factory)
    img.save("qr-code.png")
    nome_out = formata_nome(nome)
    with codecs.open(MODELO, "r", "utf-8") as f:
        certificado = f.read()
    with codecs.open("w-cert.svg", "w", "utf-8") as w:
        certificado = certificado.replace("__NOME__", nome)
        certificado = certificado.replace("__PARTICIPACAO__", participacao)
        w.write(certificado)
    subprocess.call([INKSCAPE, "-A", nome_out, "w-cert.svg"])
    with open("hashes.txt", "a") as k:
        k.write("{}\t{}\t{}\n".format(nome, participacao, chave))
    return nome_out


def send_email(email_from, name_to, email_to, subject, message, file_name):
    emaillist = [email_to]
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['Reply-to'] = email_from

    msg.preamble = 'Multipart massage.\n'

    part = MIMEText(message)
    msg.attach(part)

    part = MIMEApplication(open(file_name, "rb").read())
    part.add_header('Content-Disposition', 'attachment', filename=file_name)
    msg.attach(part)

    server = smtplib.SMTP(SERVIDOR_SMTP)
    server.ehlo()
    server.starttls()
    server.login(FROM, PASS)

    server.sendmail(msg['From'], emaillist, msg.as_string())


def envia_certificado(nome, email, participacao):
    nome_pdf = gera_certificado(nome, participacao)
    if ENVIA_EMAIL:
        send_email(FROM, nome, email,
                   ASSUNTO_DO_EMAIL,
                   CORPO_DO_EMAIL.format(nome),
                   nome_pdf)


if __name__ == "__main__":
    with open(ENTRADA, newline='', encoding=ENTRADA_ENCODING) as csvfile:
        lcertificados = csv.reader(csvfile, delimiter=',')
        for linha, row in enumerate(lcertificados):
            if linha == 0:
                continue  # Pula o cabeçalho :-D
            nome, email, participacao = row
            print('#', linha)
            print("Nome        >", nome)
            print("Email       >", email)
            print("Participacao>", participacao)
            envia_certificado(nome, email, participacao)
