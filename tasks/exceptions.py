from rest_framework.exceptions import APIException

class TaskNotFoundException(APIException):
    status_code = 404
    default_detail = 'Task not found.'

class InvalidTaskDataException(APIException):
    status_code = 400
    default_detail = 'Invalid task data.'
