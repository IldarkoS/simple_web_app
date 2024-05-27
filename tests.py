import unittest
import json
from main import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_view_form(self):
        response = self.app.get('/')
        assert response.status_code == 200
        assert b"<!DOCTYPE html>" in response.data

    # def test_get_all_tasks_empty(self):
    #     response = self.app.get('/tasks')
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert 'tasks' in data
    #     assert data['tasks'] == []

    def test_create_task(self):
        response = self.app.post('/tasks', data=json.dumps({
            "title": "Test Task",
            "description": "This is a test task"
        }), content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == "Test Task"
        assert data['description'] == "This is a test task"

    def test_create_task_missing_title(self):
        new_task = {
            'description': 'This task has no title'
        }
        response = self.app.post('/tasks', json=new_task)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'ERROR' in data

    def test_create_task_missing_description(self):
        new_task = {
            'title': 'Title only task'
        }
        response = self.app.post('/tasks', json=new_task)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'ERROR' in data

    def test_get_tasks(self):
        self.app.post('/tasks', data=json.dumps({
            "title": "Test Task 1",
            "description": "This is a test task 1"
        }), content_type='application/json')

        response = self.app.get('/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['tasks'][-1]['title'] == "Test Task 1"
        assert data['tasks'][-1]['description'] == "This is a test task 1"

    def test_get_task(self):
        post_response = self.app.post('/tasks', data=json.dumps({
            "title": "Test Task 2",
            "description": "This is a test task 2"
        }), content_type='application/json')

        task_id = json.loads(post_response.data)['id']
        response = self.app.get(f'/tasks/{task_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == "Test Task 2"
        assert data['description'] == "This is a test task 2"

    def test_update_task(self):
        post_response = self.app.post('/tasks', data=json.dumps({
            "title": "Test Task 3",
            "description": "This is a test task 3"
        }), content_type='application/json')

        task_id = json.loads(post_response.data)['id']
        response = self.app.put(f'/tasks/{task_id}', data=json.dumps({
            "title": "Updated Task 3",
            "description": "This is an updated test task 3"
        }), content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == "Updated Task 3"
        assert data['description'] == "This is an updated test task 3"

    def test_get_nonexistent_task(self):
        response = self.app.get('/tasks/99999')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'ERROR' in data

    def test_delete_task(self):
        post_response = self.app.post('/tasks', data=json.dumps({
            "title": "Test Task 4",
            "description": "This is a test task 4"
        }), content_type='application/json')

        task_id = json.loads(post_response.data)['id']
        response = self.app.delete(f'/tasks/{task_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['task_id'] == "succesfully deleted"

        get_response = self.app.get(f'/tasks/{task_id}')
        assert get_response.status_code == 200
        get_data = json.loads(get_response.data)
        assert 'ERROR' in get_data

    def test_invalid_methods_on_task_endpoints(self):
        new_task = {'title': 'Invalid Methods Task', 'description': 'Testing invalid methods'}
        post_response = self.app.post('/tasks', json=new_task)
        post_data = json.loads(post_response.data)
        task_id = post_data['id']

        response = self.app.post(f'/tasks/{task_id}')
        assert response.status_code == 405

        response = self.app.put('/tasks')
        assert response.status_code == 405
        response = self.app.delete('/tasks')
        assert response.status_code == 405


if __name__ == '__main__':
    unittest.main()
