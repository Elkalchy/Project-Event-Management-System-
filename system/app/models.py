from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # إضافة الربط مع المستخدم
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
