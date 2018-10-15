

import easyimap

login = 'Bar.RasBari@gmail.com'
password = 'dehzyp-ceQryj-kujty2'

imapper = easyimap.connect('imap.gmail.com', login, password)

while True :
    for mail_id in imapper.listids(limit=1):
        mail = imapper.mail(mail_id)
        print(mail.message_id)


