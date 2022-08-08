from unicodedata import category
from unittest import result
from urllib import request
from django.test import Client
from rest_framework.test import APITestCase
from rest_framework.views import status
from .models import *
import requests
from django.contrib.auth import authenticate, login

class RoutineTestCase(APITestCase):
    test_user_id = 0
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(email = 'tjdgus1977@gmail.com')
        test_user.set_password('gus29701**')
        test_user.save()
        RoutineTestCase.test_user_id = test_user.id
        test_routine = routine(
            title = "Test routine",     
            category = "HOMEWORK",
            goal= "Test it",
            account_id = test_user
        )
        test_routine.save()

    def setUp(self):
        self.url_1 = 'http://127.0.0.1:8000/routines/create/'
        self.url_2 = 'http://127.0.0.1:8000/routines/get/list/'
        self.url_3 = 'http://127.0.0.1:8000/routines/get/'
        self.url_4 = 'http://127.0.0.1:8000/routines/update/'
        self.url_5 = 'http://127.0.0.1:8000/routines/delete/'
    
    def test_create_routine_success(self):
        data = {
            'email': 'tjdgus1977@gmail.com',
            'password': 'gus29701**'
        }
        self.client.login(email='tjdgus1977@gmail.com', password='gus29701**')
        response_token = self.client.post("http://127.0.0.1:8000/users/api-jwt-auth/",format='json',data=data)
        token = response_token.json()["access"]
        headers={"HTTP_AUTHORIZATION": "Bearer " + token}

        data_create = {
            "title" : "problem solving",     
            "category" : "HOMEWORK",
            "goal": "Increase your problem-solving skills",    
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }
        response = self.client.post(self.url_1, data=data_create,format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_routine_error(self):
        data = {
            'email': 'tjdgus1977@gmail.com',
            'password': 'gus29701**'
        }
        self.client.login(email='tjdgus1977@gmail.com', password='gus29701**')
        response_token = self.client.post("http://127.0.0.1:8000/users/api-jwt-auth/",format='json',data=data)
        token = response_token.json()["access"]
        headers={"HTTP_AUTHORIZATION": "Bearer " + token}
        data_create_fail = {
            "title" : "problem solving",     
            "category" : "anything",
            "goal": "Increase your problem-solving skills",    
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }
        response = self.client.post(self.url_1, data=data_create_fail,format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_routine_list_success(self):
        data = {
            'email': 'tjdgus1977@gmail.com',
            'password': 'gus29701**'
        }
        self.client.login(email='tjdgus1977@gmail.com', password='gus29701**')
        response_token = self.client.post("http://127.0.0.1:8000/users/api-jwt-auth/",format='json',data=data)
        token = response_token.json()["access"]
        headers={"HTTP_AUTHORIZATION": "Bearer " + token}
        data_get_list = {
            "account_id" : 1,
            "today" : "2022-02-14" 
        }
        response = self.client.get(self.url_2, data=data_get_list,format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_routine_list_error(self):
        data = {
            'email': 'tjdgus1977@gmail.com',
            'password': 'gus29701**'
        }
        self.client.login(email='tjdgus1977@gmail.com', password='gus29701**')
        response_token = self.client.post("http://127.0.0.1:8000/users/api-jwt-auth/",format='json',data=data)
        token = response_token.json()["access"]
        headers={"HTTP_AUTHORIZATION": "Bearer " + token}
        data_get_list_fail = {
            "account_id" : 1,
            "today" : "2022-032-14as" 
        }
        response = self.client.get(self.url_2, data=data_get_list_fail, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_routine_success(self):
        data = {
            'email': 'tjdgus1977@gmail.com',
            'password': 'gus29701**'
        }
        self.client.login(email='tjdgus1977@gmail.com', password='gus29701**')
        response_token = self.client.post("http://127.0.0.1:8000/users/api-jwt-auth/",format='json',data=data)
        token = response_token.json()["access"]
        headers={"HTTP_AUTHORIZATION": "Bearer " + token}
        data_get = {
            "account_id" : 1,
            "routine_id" : 1
        }
        response = self.client.get(self.url_3, data=data_get,format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_routine_error(self):
        data = {
            'email': 'tjdgus1977@gmail.com',
            'password': 'gus29701**'
        }
        self.client.login(email='tjdgus1977@gmail.com', password='gus29701**')
        response_token = self.client.post("http://127.0.0.1:8000/users/api-jwt-auth/",format='json',data=data)
        token = response_token.json()["access"]
        headers={"HTTP_AUTHORIZATION": "Bearer " + token}
        data_get_fail = {
            "account_id" : 1,
            "routine_id" : "a"
        }
        response = self.client.get(self.url_3, data=data_get_fail, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_routine_success(self):
        data = {
            'email': 'tjdgus1977@gmail.com',
            'password': 'gus29701**'
        }
        self.client.login(email='tjdgus1977@gmail.com', password='gus29701**')
        response_token = self.client.post("http://127.0.0.1:8000/users/api-jwt-auth/",format='json',data=data)
        token = response_token.json()["access"]
        headers={"HTTP_AUTHORIZATION": "Bearer " + token}
        data_update = {
            "routine_id" : 1,    
            "title" : "Swimming",     
            "category" : "MIRACLE",     
            "goal" : "success the 100m",
            "is_alarm" : False,     
            "days" : ['MON', 'FRI']
        }
        response = self.client.put(self.url_4, data=data_update, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_routine_error(self):
        data = {
            'email': 'tjdgus1977@gmail.com',
            'password': 'gus29701**'
        }
        self.client.login(email='tjdgus1977@gmail.com', password='gus29701**')
        response_token = self.client.post("http://127.0.0.1:8000/users/api-jwt-auth/",format='json',data=data)
        token = response_token.json()["access"]
        headers={"HTTP_AUTHORIZATION": "Bearer " + token}
        data_update_fail = {
            "routine_id" : 1,    
            "title" : "Swimming",     
            "category" : "FUNNY",     
            "goal" : "success the 100m",
            "is_alarm" : 3,
            "days" : ['MON', 'FRI']
        }
        response = self.client.put(self.url_4, data=data_update_fail, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_delete_routine_success(self):
        data = {
            'email': 'tjdgus1977@gmail.com',
            'password': 'gus29701**'
        }
        self.client.login(email='tjdgus1977@gmail.com', password='gus29701**')
        response_token = self.client.post("http://127.0.0.1:8000/users/api-jwt-auth/",format='json',data=data)
        token = response_token.json()["access"]
        headers={"HTTP_AUTHORIZATION": "Bearer " + token}
        data_delete = {
            "account_id" : 1,
            "routine_id" : 1
        }
        response = self.client.delete(self.url_5, data=data_delete, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_routine_error(self):
        data = {
            'email': 'tjdgus1977@gmail.com',
            'password': 'gus29701**'
        }
        self.client.login(email='tjdgus1977@gmail.com', password='gus29701**')
        response_token = self.client.post("http://127.0.0.1:8000/users/api-jwt-auth/",format='json',data=data)
        token = response_token.json()["access"]
        headers={"HTTP_AUTHORIZATION": "Bearer " + token}
        data_delete_fail = {
            "account_id" : 1,
            "routine_id" : "a1"
        }
        response = self.client.delete(self.url_5, data=data_delete_fail, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
