import unittest
from web_app import db, create_app
from web_app.models import User, BaseModel


class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://stockbuddy_dev:^stockbuddy**@localhost/stockbuddy_test_db"
        self.app.config["TESTING"] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_username(self):
        user = User(
                username="John1",
                email="john@gmail.com",
                password ="123",
                first_name="John", 
                last_name="Doe",
                )
        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)