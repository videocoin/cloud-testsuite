import poplib
import email
import quopri
import re
import requests
from box import Box
import pdb

def get_password_reset_token(pop_server, test_email, password):
    pop_conn = poplib.POP3_SSL(pop_server)
    pop_conn.user(test_email)
    pop_conn.pass_(password)

    support_email = 'support@videocoin.network'
    support_subject = 'Password Recovery'
    
    count = len(pop_conn.list()[1])
    password_reset_emails = []
    for i in range(count):
        raw_email = b"\n".join(pop_conn.retr(i + 1)[1])
        parsed_email = email.message_from_bytes(raw_email)

        email_from = parsed_email['From']
        parsed_email_from = re.match(r'^.* <(.+)>$', email_from).group(1)
        subject = parsed_email['Subject']
        body = parsed_email.get_payload()
        # Read more about quoted-printable encodings here:
        # https://stackoverflow.com/questions/15621510/how-to-understand-the-equal-sign-symbol-in-imap-email-text
        # https://docs.python.org/3.7/library/quopri.html
        decoded_body = quopri.decodestring(str(body[1]))

        if parsed_email_from == support_email and subject == support_subject:
            # Having trouble with decoding using utf-8, have to use ISO-8859-1
            # https://stackoverflow.com/questions/23772144/python-unicodedecodeerror-utf8-codec-cant-decode-byte-0xc0-in-position-0-i
            password_reset_emails.append(decoded_body.decode('ISO-8859-1'))

    # bad regex, fix later
    get_reset_password_url = re.compile(r'<a href=\"(.*)\" s.*>Reset Password</a>')
    reset_password_urls = [get_reset_password_url.search(body).group(1) for body in password_reset_emails]
    redirect_urls = [requests.get(url).url for url in reset_password_urls]
    token = re.search(r'token=(.*)', redirect_urls[0]).group(1)
    return Box({'token': token})

def test_ext_works(response):
    lol = 'token'
    pdb.set_trace()
    assert True