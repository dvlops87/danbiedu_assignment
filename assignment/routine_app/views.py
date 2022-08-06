from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .serializers import RoutineSerializer,CreateRoutineSerializer
from .models import routine, routine_day, routine_result
from django.http import HttpResponse
from django.db.models import Q
from datetime import datetime

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
        routine_result.objects.create(routine_id=created_routine,result='N',is_deleted=False)
        try:
            if len(days) > 1:
                 for day in days:
                     routine_day.objects.create(day=day, routine_id=created_routine)
            else:
                routine_day.objects.create(day=days[0], routine_id=created_routine)
        except:
            return HttpResponse("Check your input form", status=status.HTTP_404_NOT_FOUND)
        return Response({
            'data': created_routine.routine_id,
            'message':{
                'msg':'You have successfully created the routine.',
                'status': 'ROUTINE_CREATE_OK'
            }
        })
        
        

class CheckListRoutine(APIView):
    def get(self,request):
        account_id = request.query_params.get('account_id')
        today = datetime.strptime(request.query_params.get('today'), '%Y-%m-%d')
        datetime_date = today.weekday()
        dateDict = {0: 'MON', 1:'TUE', 2:'WED', 3:'THU', 4:'FRI', 5:'SAT', 6:'SUN'}
        today_routine = routine_day.objects.select_related(
            'routine_id'
        ).filter(Q(day=dateDict[datetime_date]))
        # print(today_routine[0].routine_id)
        if len(today_routine) > 1:
            data = []
            for routines in today_routine:
                if routines.routine_id.account_id.id == int(account_id):
                    result_routine = routine_result.objects.get(routine_id = routines.routine_id.routine_id)
                    data.append({
                        'goal' : routines.routine_id.goal,
                        'id' : routines.routine_id.routine_id,
                        'result' : result_routine.result,
                        'title' : routines.routine_id.title,
                    })
        elif len(today_routine) == 0:
            return Response({
                'data': 'None',
                'message':{
                    'msg':"You don't have created the routine.",
                    'status': 'NO_ROUTINE_EXIST'
                }
            })
        
        else:
            if today_routine[0].routine_id.account_id.id == int(account_id):
                result_routine = routine_result.objects.get(routine_id = today_routine[0].routine_id.routine_id)
                data = {
                        'goal' : today_routine[0].routine_id.goal,
                        'id' : today_routine[0].routine_id.routine_id,
                        'result' : result_routine.result,
                        'title' : today_routine[0].routine_id.title,
                    }
        return Response({
            'data': data,
            'message':{
                'msg':'You have successfully created the routine.',
                'status': 'ROUTINE_CREATE_OK'
            }
        })
        
