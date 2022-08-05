from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .serializers import RoutineSerializer,CreateRoutineSerializer
from .models import routine, routine_day, routine_result
from django.http import HttpResponse

# Create your views here.

class createRoutine(APIView):
    def post(self, request):
        serializer = RoutineSerializer(data=request.data)       
        
        if request.user.is_authenticated == False:
            return Response('등록되지 않은 사용자입니다.',status=status.HTTP_400_BAD_REQUEST)
        
        title = serializer.initial_data['title']
        category = serializer.initial_data['category']
        goal = serializer.initial_data['goal']
        is_alarm = serializer.initial_data['is_alarm']
        days = serializer.initial_data['days']
        account_id = request.user
        # print(title,category,goal,bool(is_alarm),days,sep='/')
        routine.objects.create(account_id=account_id,title=title,category=category,goal=goal,is_alarm=bool(is_alarm))
        created_routine = routine.objects.last()
        try:
            if len(days) > 1:
                 for day in days:
                     routine_day.objects.create(day=day, routine_id=created_routine)
            else:
                routine_day.objects.create(day=days, routine_id=created_routine)
        except:
            return HttpResponse("Check your input form", status=status.HTTP_404_NOT_FOUND)
        return Response({
            'data': created_routine.routine_id,
            'message':{
                'msg':'You have successfully created the routine.',
                'status': 'ROUTINE_CREATE_OK'
            }
        })
        
        
