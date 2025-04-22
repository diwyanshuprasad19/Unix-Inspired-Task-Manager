from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from tasks.models import Task


class TaskManagerAPITests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.client = APIClient()

    def authenticate(self, username, password):
        response = self.client.post('/api-token-auth/', {
            'username': username,
            'password': password
        }, format='json')
        token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def test_create_task(self):
        self.authenticate('user1', 'pass123')
        response = self.client.post('/api/tasks/', {'name': 'Sample Task'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Sample Task')
        self.assertEqual(response.data['status'], 'running')

    def test_create_task_invalid_name(self):
        self.authenticate('user1', 'pass123')
        response = self.client.post('/api/tasks/', {'name': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_tasks(self):
        self.authenticate('user1', 'pass123')
        Task.objects.create(name='T1', user=self.user1)
        Task.objects.create(name='T2', user=self.user1)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_task(self):
        self.authenticate('user1', 'pass123')
        task = Task.objects.create(name='Retrieve Me', user=self.user1)
        response = self.client.get(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Retrieve Me')

    def test_retrieve_task_invalid_user(self):
        task = Task.objects.create(name='Private Task', user=self.user1)
        self.authenticate('user2', 'pass123')
        response = self.client.get(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task(self):
        self.authenticate('user1', 'pass123')
        task = Task.objects.create(name='To Delete', user=self.user1)
        response = self.client.delete(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_patch_task_status(self):
        self.authenticate('user1', 'pass123')
        task = Task.objects.create(name='Status Update', user=self.user1)
        response = self.client.patch(f'/api/tasks/{task.id}/', {'status': 'completed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')

    def test_patch_task_invalid_status(self):
        self.authenticate('user1', 'pass123')
        task = Task.objects.create(name='Invalid Status', user=self.user1)
        response = self.client.patch(f'/api/tasks/{task.id}/', {'status': 'invalid'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_access_denied(self):
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_tasks_by_status(self):
        self.authenticate('user1', 'pass123')
        Task.objects.create(name='C1', user=self.user1, status='completed')
        Task.objects.create(name='R1', user=self.user1, status='running')
        response = self.client.get('/api/tasks/?status=completed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'completed')
