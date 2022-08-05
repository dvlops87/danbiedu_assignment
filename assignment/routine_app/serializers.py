from rest_framework import serializers
from user_app.models import User
from .models import routine, routine_day, routine_result

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = routine
        fields = '__all__'


class CreateRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = routine
        fields = ['routine_id']