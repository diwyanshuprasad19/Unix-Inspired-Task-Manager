from rest_framework import serializers
from tasks.models import Task
from tasks.constants import TASK_STATUS

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_status(self, value):
        if value not in TASK_STATUS:
            raise serializers.ValidationError("Invalid status value.")
        return value
