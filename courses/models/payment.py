from django.db import models
from courses.models import *
from  django.contrib.auth.models import User

class Payment(models.Model):
    order_id = models.CharField(max_length=50, null=False)
    payment_id = models.CharField(max_length=50, null=False)
    user_course = models.ForeignKey(UserCourse, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)