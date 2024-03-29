from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import EmailAddress
from hashlib import sha256
import re


class Controller:
    def __init__(self):
        self.engine = create_engine('sqlite:///emails.sqlite', echo=True)

    def save(self, email, password):
        pattern = '^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@$£€!%*?&])[A-Za-z0-9@$£€!%*?&]{8,20}$'
        if not re.match(pattern, password):
            raise ValueError('Invalid password')
        try:
            sess = Session(self.engine)
            # save the model
            new_email = EmailAddress(email=email, password=sha256(password.encode('utf-8')).hexdigest())
            sess.add(new_email)
            sess.commit()
            sess.close()

            # show a success message
            return f'The email {email} saved!'

        except Exception as error:
            raise error
