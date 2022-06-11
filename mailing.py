__author__ = 'Dinmukhamed Stamaliev'

import logging
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.settings import MAIL, SMTP


def _parse_to_addrs_string_to_list(send_to: str) -> list:
    """
    Фунция парсит почты из строки, преобразует в список и возвращает, если по
    какой то причине происходит ошибка то фунция возврощает пустой массив.
    """
    try:
        to_addrs = list(map(lambda m: m.strip(), send_to.split(',')))
    except Exception as e:
        logging.info(f'send_email_file xls function error: {e}')
        print(f'send_email_file xls function error: {e}')

        return []
    else:
        return to_addrs


def _create_mime_msg(subject, text):
    msg = MIMEMultipart()
    msg['From'] = MAIL.get('username')
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    return msg


def _send_mail(to_addrs, msg):
    with smtplib.SMTP(host=SMTP.get('host'), port=SMTP.get('port')) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        if MAIL.get('password'):
            smtp.login(MAIL.get('username'), MAIL.get('password'))
        smtp.sendmail(from_addr=MAIL.get('username'),
                      to_addrs=to_addrs, msg=msg.as_string())


def send_email_file(file_attachment, file_name,
                    subject, send_to: str, text=''):

    try:
        to_addrs = _parse_to_addrs_string_to_list(send_to)
        msg = _create_mime_msg(subject, send_to)
        attachedfile = MIMEApplication(file_attachment)
        attachedfile.add_header(
            'Content-Disposition', f'attachment; filename="{file_name}.xlsx"',
        )
        msg.attach(attachedfile)

        _send_mail(to_addrs, msg)
    except Exception as e:
        logging.info(f'send_email_file xls function error: {e}')
        print(f'send_email_file xls function error: {e}')