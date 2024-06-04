from unittest import TestCase
from flask import json

from app import app, db
from models import Cupcake


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    @classmethod
    def setUpClass(cls):
        """Set up the test class."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = True
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Tear down the test class."""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Set up each test."""
        # Clear existing cupcakes from the database
        Cupcake.query.delete()
        
        # Add a new cupcake to the database
        self.cupcake = Cupcake(**{
            "flavor": "TestFlavor",
            "size": "TestSize",
            "rating": 5,
            "image": "http://test.com/cupcake.jpg"
        })
        db.session.add(self.cupcake)
        db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.data)
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.data)
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            new_cupcake_data = {
                "flavor": "TestFlavor2",
                "size": "TestSize2",
                "rating": 10,
                "image": "http://test.com/cupcake2.jpg"
            }
            resp = client.post("/api/cupcakes", json=new_cupcake_data)
            self.assertEqual(resp.status_code, 201)
            data = json.loads(resp.data)
            self.assertEqual(data['cupcake']['flavor'], "TestFlavor2")
            self.assertEqual(data['cupcake']['size'], "TestSize2")
            self.assertEqual(data['cupcake']['rating'], 10)
            self.assertEqual(data['cupcake']['image'], "http://test.com/cupcake2.jpg")

    def test_update_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            update_data = {
                "flavor": "UpdatedFlavor",
                "size": "UpdatedSize",
                "rating": 1,
                "image": "http://test.com/updated.jpg"
            }
            resp = client.patch(url, json=update_data)
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.data)
            self.assertEqual(data['cupcake']['flavor'], "UpdatedFlavor")
            self.assertEqual(data['cupcake']['size'], "UpdatedSize")
            self.assertEqual(data['cupcake']['rating'], 1)
            self.assertEqual(data['cupcake']['image'], "http://test.com/updated.jpg")

    def test_delete_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.data)
            self.assertEqual(data, {"message": "Deleted"})
            self.assertIsNone(Cupcake.query.get(self.cupcake.id))

    def test_delete_cupcake_not_found(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/99999"
            resp = client.delete(url)
            self.assertEqual(resp.status_code, 404)
