from rest_framework import serializers
from .models import QuizResult, SimulationResult, Profile


class QuizResultSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = QuizResult
        fields = ['id', 'user', 'username', 'score_percent', 'passed', 'taken_at']
        read_only_fields = ['id', 'user', 'username', 'passed', 'taken_at']


class SimulationResultSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = SimulationResult
        fields = ['id', 'user', 'username', 'simulator_type', 'time_taken_seconds', 'score', 'passed', 'completed_at']
        read_only_fields = ['id', 'user', 'username', 'completed_at']

