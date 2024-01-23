import unittest
from app.app import app, db
from app.models.task import Task

class TaskManagementTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_task(self):
        response = self.app.post('/tasks', json={'description': 'Test task'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)

    def test_get_all_tasks(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)

    def test_get_task(self):
        response = self.app.post('/tasks', json={'description': 'Test task'})
        task_id = response.get_json()['id']

        response = self.app.get(f'/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        response = self.app.post('/tasks', json={'description': 'Test task'})
        task_id = response.get_json()['id']

        response = self.app.put(f'/tasks/{task_id}', json={'description': 'Updated task', 'completed': True})
        self.assertEqual(response.status_code, 200)

    def test_delete_task(self):
        response = self.app.post('/tasks', json={'description': 'Test task'})
        task_id = response.get_json()['id']

        response = self.app.delete(f'/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_all_tasks(self):
        self.app.post('/tasks', json={'description': 'Test task 1'})
        self.app.post('/tasks', json={'description': 'Test task 2'})

        response = self.app.delete('/tasks')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()