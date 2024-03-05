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
            return sess

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
        assert sess.query(EmailAddress).first().password == 'Password01'
        assert sess.query(EmailAddress).first().email == 'jenhil0809@highgateschool.org.uk'
        sess.close()


class NewController(Controller):
    def __init__(self):
        super().__init__()
        self.engine = create_engine('sqlite:///:memory:', echo=True)


class TestController:
    @pytest.fixture()
    def setup_controller(self):
        controller = NewController()
        Base.metadata.create_all(controller.engine)
        return controller

    def test_save(self, setup_controller):
        controller = setup_controller
        temp_email = 'bill@ms.com'
        temp_pass = 'aA&aaa2024'
        save_message = controller.save(temp_email, temp_pass)
        assert save_message == 'The email bill@ms.com saved!'

    def test_invalid_email(self, setup_controller):
        controller = setup_controller
        temp_email = 'billms.org.uk'
        temp_pass = 'A1bcabA%c!01'
        with pytest.raises(ValueError) as error:
            controller.save(temp_email, temp_pass)
        assert str(error.value) == 'Invalid email address'

    def test_invalid_password(self, setup_controller):
        controller = setup_controller
        temp_email = 'billms@uk.org.uk'
        temp_pass = 'aBc^'
        with pytest.raises(ValueError) as error:
            controller.save(temp_email, temp_pass)
        assert str(error.value) == 'Invalid password'
