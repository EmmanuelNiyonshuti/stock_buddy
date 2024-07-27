from datetime import datetime
import unittest
from web_app import db, create_app
from web_app.models import BaseModel

class TestModel(BaseModel):
    __tablename__ = "test_basemodel"
    name = db.Column(db.String(50))

class TestBaseModel(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.app = create_app()
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://stockbuddy_dev:^stockbuddy**@localhost/stockbuddy_test_db"
        self.app.config["TESTING"] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_attrs(self):
        """Test model attributes."""
        model = TestModel(name="Test")
        self.assertIsNotNone(model.id)
        self.assertIsNotNone(model.created_at)
        self.assertIsNotNone(model.updated_at)
    def test_datetime_objs(self):
        """ """
        model = TestModel(name="Test")
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)
    def test_to_dict(self):
        model = TestModel(name="Test")
        m_dict = model.to_dict()
        self.assertIsInstance(m_dict, dict)
        self.assertIn("id", m_dict)
        self.assertIn("created_at", m_dict)
    def test_get(self):
        model = TestModel(name="test")
        db.session.add(model)
        db.session.commit()
        obj_id = model.id
        get_obj = model.get(obj_id)
        self.assertEqual(model, get_obj)
    def test_get_none(self):
        m = TestModel()
        db.session.add(m)
        db.session.commit()
        get_obj = m.get("123")
        self.assertNotEqual(m, get_obj)
        self.assertIsNone(get_obj)
