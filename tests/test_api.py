import unittest
from fastapi.testclient import TestClient
from api.index import app
from api.database import Base, engine, SessionLocal
from api.models import Task

class TaskApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    def setUp(self):
        # Limpa tabela antes de cada teste
        db = SessionLocal()
        db.query(Task).delete()
        db.commit()
        db.close()

    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "app": "neobrutalist-task-list"})

    def test_create_task_success(self):
        response = self.client.post("/api/tasks", json={"title": "Comprar pão na padaria"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["title"], "Comprar pão na padaria")
        self.assertFalse(data["is_completed"])
        self.assertIn("id", data)

    def test_create_task_validation_empty_string(self):
        response = self.client.post("/api/tasks", json={"title": "   "})
        self.assertEqual(response.status_code, 422)

    def test_list_tasks(self):
        self.client.post("/api/tasks", json={"title": "Tarefa 1"})
        self.client.post("/api/tasks", json={"title": "Tarefa 2"})
        response = self.client.get("/api/tasks")
        self.assertEqual(response.status_code, 200)
        tasks = response.json()
        self.assertEqual(len(tasks), 2)

    def test_toggle_task_completion(self):
        created = self.client.post("/api/tasks", json={"title": "Estudar Vue 3"}).json()
        task_id = created["id"]

        patch_res = self.client.patch(f"/api/tasks/{task_id}", json={"is_completed": True})
        self.assertEqual(patch_res.status_code, 200)
        self.assertTrue(patch_res.json()["is_completed"])

    def test_delete_task(self):
        created = self.client.post("/api/tasks", json={"title": "Item descartável"}).json()
        task_id = created["id"]

        del_res = self.client.delete(f"/api/tasks/{task_id}")
        self.assertEqual(del_res.status_code, 204)

        # Verifica se realmente sumiu
        list_res = self.client.get("/api/tasks")
        self.assertEqual(len(list_res.json()), 0)

if __name__ == "__main__":
    unittest.main()
