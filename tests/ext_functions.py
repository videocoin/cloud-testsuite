import poplib
import email
import quopri
import re
import requests
from box import Box

import utils

def get_password_reset_body(pop_server, test_email, test_email_password, new_password):
    pop_conn = poplib.POP3_SSL(pop_server)
    pop_conn.user(test_email)
    pop_conn.pass_(test_email_password)
    test_environment = utils.load_yaml('common.yaml')['variables']['environment']

    support_email = test_environment['support_email']
    support_subject = test_environment['support_subject']
    
    email_count = len(pop_conn.list()[1])
    while email_count > 0:
        raw_email = b"\n".join(pop_conn.retr(email_count)[1])
        parsed_email = email.message_from_bytes(raw_email)

        email_from = parsed_email['From']
        parsed_email_from = re.match(r'^.* <(.+)>$', email_from).group(1)
        subject = parsed_email['Subject']
        
        if parsed_email_from == support_email and subject == support_subject:
            body = parsed_email.get_payload()
            # Read more about quoted-printable encodings here:
            # https://stackoverflow.com/questions/15621510/how-to-understand-the-equal-sign-symbol-in-imap-email-text
            # https://docs.python.org/3.7/library/quopri.html
            decoded_body = quopri.decodestring(str(body[1]))

            # Having trouble with decoding using utf-8, have to use ISO-8859-1
            # https://stackoverflow.com/questions/23772144/python-unicodedecodeerror-utf8-codec-cant-decode-byte-0xc0-in-position-0-i
            password_reset_email = decoded_body.decode('ISO-8859-1')
            break
            
        email_count -= 1

    # bad regex, fix later
    reset_password_url = re.search(r'<a href=\"(.*)\" s.*>Reset Password</a>', password_reset_email).group(1)
    redirect_url = requests.get(reset_password_url).url
    token = re.search(r'token=(.*)', redirect_url).group(1)

    pop_conn.quit()
    return Box({
        'token': token, 
        'password': new_password,
        'confirm_password': new_password})
