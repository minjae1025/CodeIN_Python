from django.contrib import admin
from .models import User  # 커스텀 유저 모델 임포트

# 커스텀 유저 모델을 admin 사이트에 등록
admin.site.register(User)