from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.utils import timezone




class Plate(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name='板块')
    dutyUser = models.CharField(max_length=20, verbose_name='责任人')

    class Meta:
        verbose_name = "板块"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Type(models.Model):
    plate = models.ForeignKey(to=Plate, on_delete=models.CASCADE, verbose_name='板块')
    name = models.CharField(max_length=10, unique=True, verbose_name='种类')
    doUser = models.CharField(max_length=20, verbose_name='执行人',null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "种类"
        verbose_name_plural = verbose_name


class Task(models.Model):
    wx_notice_from = models.CharField(max_length=4000, verbose_name="原通知", null=True, blank=True)
    type = models.ForeignKey(to=Type, on_delete=models.CASCADE, verbose_name='种类')
    name = models.CharField(max_length=10, verbose_name='任务')
    to_who = models.CharField(max_length=10, verbose_name='交接人', null=True, blank=True)

    wx_notice_to = models.CharField(max_length=4000, verbose_name="发出通知", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="截止时间")
    status = models.BooleanField(verbose_name="状态", default=False)
    finish_time = models.DateTimeField(verbose_name="完成时间", null=True)

    def left_time(self):
        now = timezone.now()
        remaining_time = self.end_time - now
        days, remainder = divmod(remaining_time.total_seconds(), 86400)  # 86400 seconds in a day
        hours, _ = divmod(remainder, 3600)  # 3600 seconds in an hour
        if days < 0 or hours < 0:
            return '已过截止时间'
        return f"{int(days)}天{int(hours)}时"

    def save(self, *args, **kwargs):
        # 如果 status 从 False 变为 True，更新 finish_time
        if self.pk and self.status and not self.__class__.objects.filter(pk=self.pk).values_list('status', flat=True)[
            0]:
            self.finish_time = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.type) + str(self.type)

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "任务"
        verbose_name_plural = verbose_name
