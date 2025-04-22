from tasks.models import Task
from tasks.exceptions import TaskNotFoundException, InvalidTaskDataException
from threading import Timer
import random
import logging

logger = logging.getLogger(__name__)

class TaskService:

    @staticmethod
    def create_task(data, user):
        name = data.get("name")
        if not name:
            raise InvalidTaskDataException("Task name is required.")
        task = Task.objects.create(name=name, user=user, status='running')
        logger.info(f"Created task: {task.name} by user: {user.username}")
        Timer(5.0, TaskService._complete_task, args=[task.id]).start()
        return task

    @staticmethod
    def _complete_task(task_id):
        try:
            task = Task.objects.get(id=task_id)
            task.status = random.choice(['completed', 'failed'])
            task.save()
            logger.info(f"Task {task.id} auto-completed as {task.status}")
        except Task.DoesNotExist:
            logger.warning(f"Tried to complete non-existent task {task_id}")

    @staticmethod
    def get_all_tasks(user, status_filter=None):
        if status_filter:
            return Task.objects.filter(user=user, status=status_filter)
        return Task.objects.filter(user=user)

    @staticmethod
    def get_task(task_id, user):
        try:
            return Task.objects.get(id=task_id, user=user)
        except Task.DoesNotExist:
            raise TaskNotFoundException()

    @staticmethod
    def delete_task(task_id, user):
        task = TaskService.get_task(task_id, user)
        task.delete()
        logger.info(f"Deleted task {task_id} for user {user.username}")

    @staticmethod
    def update_task(task_id, data, user):
        task = TaskService.get_task(task_id, user)
        status = data.get("status")
        if status not in ['running', 'completed', 'failed']:
            raise InvalidTaskDataException("Invalid status.")
        task.status = status
        task.save()
        logger.info(f"Updated task {task_id} to status {status}")
        return task
