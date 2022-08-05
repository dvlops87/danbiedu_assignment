from sre_parse import CATEGORIES
from statistics import mode
from django.db import models
from user_app.models import User

# Create your models here.

class routine(models.Model):
    CATEGORIES = (
        ('MC', 'MIRACLE'),
        ('HW', 'HOMEWORK')
    )
    routine_id = models.IntegerField(primary_key=True)
    account_id = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    title = models.TextField(default='', null=True)
    category = models.CharField(max_length=2, choices=CATEGORIES)
    goal = models.TextField(default='', null=True)
    is_alarm = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.routine_id


class routine_result(models.Model):
    RESULTS = (
        ('N','NOT'),
        ('T','TRY'),
        ('D','DONE'),
    )
    routine_result_id = models.IntegerField(primary_key=True)
    routine_id = models.ForeignKey(routine, related_name="routine_result", on_delete=models.CASCADE)
    result = models.CharField(max_length=1, choices=RESULTS)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.routine_result_id


class routine_day(models.Model):
    DAYS = (
        ('MON','Monday'),
        ('TUE','Tuesday'),
        ('WED','Wednesday'),
        ('THU','Thursday'),
        ('FRI','Friday'),
        ('SAT','Saturday'),
        ('SUN','Sunday'),
    )
    day = models.CharField(max_length=3, choices=DAYS)
    routine_id = models.ForeignKey(routine, related_name="routine_day", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)