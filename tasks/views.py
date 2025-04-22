from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from tasks.services import TaskService
from tasks.serializers import TaskSerializer
from django.http import JsonResponse
from django.views import View

class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_filter = request.query_params.get("status")
        tasks = TaskService.get_all_tasks(request.user, status_filter)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        task = TaskService.create_task(request.data, request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        task = TaskService.get_task(task_id, request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def delete(self, request, task_id):
        TaskService.delete_task(task_id, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, task_id):
        task = TaskService.update_task(task_id, request.data, request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

class HealthCheckView(View):
    def get(self, request):
        return JsonResponse({'status': 'ok'})
