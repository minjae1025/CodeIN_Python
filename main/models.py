from django.db import models
from user.models import User


# Create your models here.
class Problem(models.Model):
    title = models.CharField(
        max_length=100, help_text="문제 제목"
    )
    description = models.TextField(
        help_text="문제 설명"
    )
    created = models.DateTimeField(
        help_text="문제 생성 일자",
        auto_now_add=True
    )
    ip = models.GenericIPAddressField(
        help_text="문제 작성자 IP주소"
    )
    example = models.JSONField(
        default=list,
        help_text="문제 예제(테스트 케이스) 목록"
    )
    conditions = models.JSONField(
        default=list,
        help_text="문제 조건 목록"
    )
    answer_count = models.IntegerField(
        default=0,
        help_text="맞춘 사람"
    )
    difficulty = models.IntegerField(
        help_text="문제 난이도"
    )
    create_user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title

