import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from controller import Controller
from models import Base, EmailAddress


class TestModel:
    @pytest.fixture
    def setup_db(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)
        with Session(engine) as sess:
            yield sess

    def test_email(self):
        email = EmailAddress(email='jenhil0809@highgateschool.org.uk', password='Password01')
        assert email.email == 'jenhil0809@highgateschool.org.uk'
        assert email.password == 'Password01'

    def test_database(self, setup_db):
        sess = setup_db
        emails = [EmailAddress(email='jenhil0809@highgateschool.org.uk', password='Password01'),
                  EmailAddress(email='qwerty@gmail.com', password='Password02'),
                  EmailAddress(email='new_email1@outlook.com', password='Qwerty')]
        sess.add_all(emails)
        assert sess.query(EmailAddress).count() == 3
        assert sess.query(EmailAddress).one().password == 'Password01'
        assert sess.query(EmailAddress).one().email == 'jenhil0809@highgateschool.org.uk'
        sess.close()
