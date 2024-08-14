from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=13)
    username = models.CharField(max_length=30, null=True, blank=True)
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True, default=1)

    class Meta:
        db_table = 'users'


class Category(models.Model):
    FOR_WHO_CHOICES = [
        ('employee', 'employee'),
        ('employer', 'employer'),
    ]
    name = models.CharField(max_length=200)
    for_who = models.CharField(max_length=20, choices=FOR_WHO_CHOICES)

    class Meta:
        db_table = 'category'


class Posts(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    image = models.TextField(null=True)
    video = models.TextField(null=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'post'
