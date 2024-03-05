from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import EmailAddress
from hashlib import sha256


class Controller:
    def __init__(self):
        self.engine = create_engine('sqlite:///emails.sqlite', echo=True)

    def save(self, email, password):
        # save an email to the database
        try:
            sess = Session(self.engine)
            # save the model
            new_email = EmailAddress(email=email, password=sha256(password.encode('utf-8')))
            sess.add(new_email)
            sess.commit()

            # show a success message
            return f'The email {email} saved!'

        except Exception as error:
            raise error
