from django.contrib import admin
from .models import ForgetPasswordToken, User, VerifyToken

admin.site.register(ForgetPasswordToken)
admin.site.register(User)
admin.site.register(VerifyToken)
# Register your models here.
