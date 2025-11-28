import unittest
from app import app, store


class TestWebApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        store.warehouses.clear()
        store.next_id = 1

    def test_index_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Warehouse Management", response.data)

    def test_index_shows_no_warehouses_message(self):
        response = self.client.get("/")
        self.assertIn(b"No warehouses yet", response.data)

    def test_create_warehouse(self):
        response = self.client.post("/create", data={
            "name": "Test Warehouse",
            "tilavuus": "100",
            "alku_saldo": "50"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Warehouse", response.data)
        self.assertEqual(len(store.warehouses), 1)

    def test_create_warehouse_with_invalid_values(self):
        response = self.client.post("/create", data={
            "name": "Test",
            "tilavuus": "invalid",
            "alku_saldo": "0"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(store.warehouses), 0)

    def test_delete_warehouse(self):
        store.add("To Delete", 100, 0)
        self.assertEqual(len(store.warehouses), 1)

        response = self.client.post("/delete/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(store.warehouses), 0)

    def test_delete_nonexistent_warehouse(self):
        response = self.client.post("/delete/999", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_edit_warehouse_rename(self):
        store.add("Original", 100, 0)

        response = self.client.post("/edit/1", data={
            "name": "Renamed"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(store.warehouses[1]["name"], "Renamed")

    def test_edit_warehouse_add_items(self):
        store.add("Test", 100, 0)

        response = self.client.post("/edit/1", data={
            "action": "add",
            "amount": "25"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(store.warehouses[1]["varasto"].saldo, 25)

    def test_edit_warehouse_take_items(self):
        store.add("Test", 100, 50)

        response = self.client.post("/edit/1", data={
            "action": "take",
            "amount": "20"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(store.warehouses[1]["varasto"].saldo, 30)

    def test_edit_nonexistent_warehouse(self):
        response = self.client.post("/edit/999", data={
            "name": "Test"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_edit_with_invalid_amount(self):
        store.add("Test", 100, 50)

        response = self.client.post("/edit/1", data={
            "action": "add",
            "amount": "invalid"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(store.warehouses[1]["varasto"].saldo, 50)

    def test_create_with_empty_name_uses_default(self):
        response = self.client.post("/create", data={
            "name": "",
            "tilavuus": "100",
            "alku_saldo": "0"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(store.warehouses[1]["name"], "New Warehouse")

    def test_create_with_whitespace_name_uses_default(self):
        response = self.client.post("/create", data={
            "name": "   ",
            "tilavuus": "100",
            "alku_saldo": "0"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(store.warehouses[1]["name"], "New Warehouse")

    def test_edit_with_whitespace_name_keeps_original(self):
        store.add("Original", 100, 0)

        response = self.client.post("/edit/1", data={
            "name": "   "
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(store.warehouses[1]["name"], "Original")
