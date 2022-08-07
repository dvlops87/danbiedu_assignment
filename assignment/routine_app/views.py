from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RoutineSerializer
from .models import routine, routine_day, routine_result
from user_app.models import User
from django.http import HttpResponse
from django.db.models import Q
from datetime import datetime
import json
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
        routine.objects.create(account_id=account_id,title=title,category=category,goal=goal,is_alarm=bool(is_alarm))
        created_routine = routine.objects.last()
        routine_result.objects.create(routine_id=created_routine,result='NOT',is_deleted=False)
        try:
            if len(days) > 1:
                 for day in days:
                     routine_day.objects.create(day=day, routine_id=created_routine)
            else:
                routine_day.objects.create(day=days[0], routine_id=created_routine)
        except:
            return HttpResponse("Check your input form",  status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'data': created_routine.routine_id,
            'message':{
                'msg':'You have successfully created the routine.',
                'status': 'ROUTINE_CREATE_OK'
            }
        })
        
        

class CheckListRoutine(APIView):
    def get(self,request):
        if request.user.is_authenticated == False:
            return Response('등록되지 않은 사용자입니다.',status=status.HTTP_400_BAD_REQUEST)
        account_id = request.query_params.get('account_id')
        today = datetime.strptime(request.query_params.get('today'), '%Y-%m-%d')
        datetime_date = today.weekday()
        dateDict = {0: 'MON', 1:'TUE', 2:'WED', 3:'THU', 4:'FRI', 5:'SAT', 6:'SUN'}
        today_routine = routine_day.objects.select_related(
            'routine_id'
        ).filter(Q(day=dateDict[datetime_date]))
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
        

class CheckRoutine(APIView):
    def get(self,request):
        if request.user.is_authenticated == False:
            return Response('등록되지 않은 사용자입니다.',status=status.HTTP_400_BAD_REQUEST)
        account_id = request.query_params.get('account_id')
        routine_id = request.query_params.get('routine_id')
        today_routine = routine_result.objects.select_related(
            'routine_id'
        ).filter(routine_id=routine_id)
        if len(today_routine) == 0:
            return Response({
                'data': 'None',
                'message':{
                    'msg':"You don't have created the routine.",
                    'status': 'NO_ROUTINE_EXIST'
                }
            })

        if today_routine[0].routine_id.account_id.id == int(account_id):
            routine_day_list = routine_day.objects.filter(routine_id = routine_id)
            print(len(routine_day_list))
            days = []
            if len(routine_day_list) > 1:
                for routine_one in routine_day_list:
                    days.append(routine_one.day)
            else:
                days.append(routine_day_list[0].day)
            data = {
                    'goal' : today_routine[0].routine_id.goal,
                    'id' : today_routine[0].routine_id.routine_id,
                    'result' : today_routine[0].result,
                    'title' : today_routine[0].routine_id.title,
                    'days' : days
            }
        return Response({
            'data': data,
            'message':{
                'msg':'You have successfully created the routine.',
                'status': 'ROUTINE_CREATE_OK'
            }
        })


class updateRoutine(APIView):
    def put(self, request):    
        if request.user.is_authenticated == False:
            return Response('등록되지 않은 사용자입니다.',status=status.HTTP_400_BAD_REQUEST)
        try:
            request_data = json.loads(request.body)
            now_routine = routine.objects.filter(routine_id=request_data["routine_id"])
        except:
            return Response('Routine matching query does not exist.',status=status.HTTP_400_BAD_REQUEST)
        if 'days' in request.data.keys():
            days_data = request.data.pop('days')
            origin_r_day = routine_day.objects.filter(routine_id=request_data["routine_id"])
            origin_r_day.delete()
            if len(days_data) > 1:
                for day in days_data:
                    print('create_1')
                    routine_day.objects.create(day=day, routine_id=now_routine[0], created_at=now_routine[0].created_at, modified_at=datetime.now())
            else:
                print('create_2')
                routine_day.objects.create(day=days_data[0], routine_id=now_routine[0], created_at=now_routine[0].created_at, modified_at=datetime.now())
        
        try:
            now_routine.update(title=request_data["title"],category=request_data["category"],goal=request_data["goal"],is_alarm=request_data["is_alarm"])
            return Response({
                'data': now_routine[0].routine_id,
                'message':{
                    'msg':'The routine has been modified.',
                    'status': 'ROUTINE_UPDATE_OK'
                }
            })
        except:
            return Response("Check your input form", status=status.HTTP_400_BAD_REQUEST)


class deleteRoutine(APIView):
    def delete(self,request):
        if request.user.is_authenticated == False:
            return Response('등록되지 않은 사용자입니다.',status=status.HTTP_400_BAD_REQUEST)
        try:
            request_data = json.loads(request.body)
            now_routine = routine.objects.get(routine_id=request_data["routine_id"],account_id=request_data["account_id"])
        except:
            return Response('Routine matching query does not exist.',status=status.HTTP_400_BAD_REQUEST)
        try:
            now_routine.delete()
            return Response({
                'data': request_data["routine_id"],
                'message':{
                    'msg':'The routine has been deleted.',
                    'status': 'ROUTINE_DELETE_OK'
                }
            })
        except:
            return Response("Fail to delete routine", status=status.HTTP_400_BAD_REQUEST)