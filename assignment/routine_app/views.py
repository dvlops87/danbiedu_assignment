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
from rest_framework.decorators import   authentication_classes, permission_classes

# Create your views here.

@authentication_classes([])
@permission_classes([]) 
class createRoutine(APIView):
    def post(self,request):
        serializer = RoutineSerializer(data=request.data)       
        
        if request.user.is_authenticated:
            return Response('등록되지 않은 사용자입니다.',status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_anonymous:
            account_id = User.objects.all().first()
        else:
            account_id = request.user
        title = serializer.initial_data['title']
        category = serializer.initial_data['category']
        if 'MIRACLE' not in category and 'HOMEWORK' not in category :
            return Response('Check your input form about category.',status=status.HTTP_400_BAD_REQUEST)
        goal = serializer.initial_data['goal']
        is_alarm = serializer.initial_data['is_alarm']
        days = serializer.initial_data['days']
        routine.objects.create(account_id=account_id,title=title,category=category,goal=goal,is_alarm=bool(is_alarm))
        created_routine = routine.objects.last()
        try:
            if len(days) > 1:
                 for day in days:
                    routine_result.objects.create(routine_id=created_routine,result='NOT',is_deleted=False)
                    routine_day.objects.create(day=day, routine_id=created_routine)
            else:
                routine_day.objects.create(day=days[0], routine_id=created_routine)
                routine_result.objects.create(routine_id=created_routine,result='NOT',is_deleted=False)
        except:
            return HttpResponse("Check your input form",  status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'data': created_routine.routine_id,
            'message':{
                'msg':'You have successfully created the routine.',
                'status': 'ROUTINE_CREATE_OK'
            }
        })
        
        

@authentication_classes([])
@permission_classes([]) 
class CheckListRoutine(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            return Response('등록되지 않은 사용자입니다.',status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_anonymous:
            account_id = request.query_params.get('account_id')
        else:
            account_id = request.query_params.get('account_id')
        try:
            today = datetime.strptime(request.query_params.get('today'), '%Y-%m-%d')
        except:
            return Response('Check your input form about day.',status=status.HTTP_400_BAD_REQUEST)   
        datetime_date = today.weekday()
        dateDict = {0: 'MON', 1:'TUE', 2:'WED', 3:'THU', 4:'FRI', 5:'SAT', 6:'SUN'}
        today_routine = routine_day.objects.select_related(
            'routine_id'
        ).filter(Q(day=dateDict[datetime_date]))
        if len(today_routine) > 1:
            data = []
            for routines in range(len(today_routine)): 
                if today_routine[routines].routine_id.account_id.id == int(account_id):
                    list_routine_day = routine_day.objects.filter(routine_id = today_routine[routines].routine_id)
                    result_routine = routine_result.objects.filter(routine_id = today_routine[routines].routine_id)
                    for list_routine, result_routine in zip(list_routine_day,result_routine):
                        if list_routine.day == dateDict[datetime_date]:
                            data.append({
                                'goal' : today_routine[routines].routine_id.goal,
                                'id' : today_routine[routines].routine_id.routine_id,
                                'result' : result_routine.result,
                                'title' : today_routine[routines].routine_id.title,
                            })
        elif len(today_routine) == 0:
            return Response({
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
                'status': 'ROUTINE_READ_OK'
            }
        })
        

@authentication_classes([])
@permission_classes([]) 
class CheckRoutine(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            return Response('등록되지 않은 사용자입니다.',status=status.HTTP_400_BAD_REQUEST)
        account_id = request.query_params.get('account_id')
        routine_id = request.query_params.get('routine_id')
        if str(account_id).isnumeric()==False or str(routine_id).isnumeric()==False :
            return Response('Check your input form',status=status.HTTP_400_BAD_REQUEST)   
        today_routine = routine_result.objects.select_related(
            'routine_id'
        ).filter(routine_id=routine_id)
        if len(today_routine) == 0:
            return Response({
                'message':{
                    'msg':"You don't have created the routine.",
                    'status': 'NO_ROUTINE_EXIST'
                }
            })
        if today_routine[0].routine_id.account_id.id == int(account_id):
            routine_day_list = routine_day.objects.filter(routine_id = routine_id)
            days = []
            if len(routine_day_list) > 1:
                for routine_one in routine_day_list:
                    days.append(routine_one.day)
            else:
                days.append(routine_day_list[0].day)
            return_result = 'NOT'
            for results in today_routine:
                if results.result == 'TRY':
                    return_result = 'TRY'
                elif results.result == 'DONE':
                    return_result = 'DONE'
            data = {
                    'goal' : today_routine[0].routine_id.goal,
                    'id' : today_routine[0].routine_id.routine_id,
                    'result' : return_result,
                    'title' : today_routine[0].routine_id.title,
                    'days' : days
            }
        return Response({
            'data': data,
            'message':{
                'msg':'You have successfully created the routine.',
                'status': 'ROUTINE_READ_OK'
            }
        })


@authentication_classes([])
@permission_classes([])
class updateRoutine(APIView):
    def put(self, request):    
        if request.user.is_authenticated:
            return Response('등록되지 않은 사용자입니다.',status=status.HTTP_400_BAD_REQUEST)
        serializer = RoutineSerializer(data=request.data)  
        try:
            if request.user.is_anonymous:
                now_routine = routine.objects.filter(routine_id=routine.objects.all().first().routine_id)
            else:
                now_routine = routine.objects.filter(routine_id=serializer.initial_data["routine_id"])
        except:
            return Response('Routine matching query does not exist.',status=status.HTTP_400_BAD_REQUEST)
        if 'MIRACLE' not in serializer.initial_data["category"] and 'HOMEWORK' not in serializer.initial_data["category"] :
            return Response('Check your input form about category.',status=status.HTTP_400_BAD_REQUEST)   
        if serializer.initial_data['days']:
            days_data = serializer.initial_data["days"]
            origin_r_day = routine_day.objects.filter(routine_id=serializer.initial_data["routine_id"])
            origin_r_day.delete()
            if len(days_data) > 1:
                for day in days_data:
                    routine_day.objects.create(day=day, routine_id=now_routine[0], created_at=now_routine[0].created_at, modified_at=datetime.now())
            else:
                routine_day.objects.create(day=days_data[0], routine_id=now_routine[0], created_at=now_routine[0].created_at, modified_at=datetime.now())
        
        try:
            now_routine.update(title=serializer.initial_data["title"],category=serializer.initial_data["category"],goal=serializer.initial_data["goal"],is_alarm=serializer.initial_data["is_alarm"])
            return Response({
                'data': now_routine[0].routine_id,
                'message':{
                    'msg':'The routine has been modified.',
                    'status': 'ROUTINE_UPDATE_OK'
                }
            })
        except:
            return Response("Check your input form", status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([])
@permission_classes([]) 
class deleteRoutine(APIView):
    def delete(self,request):
        if request.user.is_authenticated:
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



@authentication_classes([])
@permission_classes([]) 
class SolvedRoutine(APIView):
    def put(self,request):
        if request.user.is_authenticated:
            return Response('등록되지 않은 사용자입니다.',status=status.HTTP_400_BAD_REQUEST)
        serializer = RoutineSerializer(data=request.data)  
        if len(serializer.initial_data['days'])!=1 or serializer.initial_data['days'][0] not in ['MON','TUE','WED','THU','FRI','SAT','SUN']:
            return Response("Check your input form about days", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if request.user.is_anonymous:
                now_routine = routine_day.objects.filter(Q(routine_id=routine.objects.all().first().routine_id))
                now_routine_result = routine_result.objects.filter(routine_id=routine.objects.all().first().routine_id)
            else:
                now_routine = routine_day.objects.filter(routine_id=serializer.initial_data["routine_id"])
                now_routine_result = routine_result.objects.filter(routine_id=serializer.initial_data["routine_id"])
        except:
            return Response('Routine matching query does not exist.',status=status.HTTP_400_BAD_REQUEST)
        try:
            for r_day, r_result in zip(now_routine, now_routine_result):
                if r_day.day == serializer.initial_data['days'][0]:
                    r_result.result = serializer.initial_data["result"]
                    r_result.save()
            return Response({
                'message':{
                    'msg':'The routine has been modified.',
                    'status': 'ROUTINE_UPDATE_OK'
                }
            })
        except:
            return Response("Check your input form", status=status.HTTP_400_BAD_REQUEST)