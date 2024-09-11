from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    full_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="F.I.SH")
    phone = models.CharField(max_length=13, verbose_name="TELEFON RAQAM")
    username = models.CharField(max_length=30, null=True, blank=True, verbose_name="USERNAME")
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True, default=1, verbose_name="TELEGRAM ID")

    class Meta:
        db_table = 'users'
        verbose_name = "User"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return self.full_name


class Category(models.Model):
    FOR_WHO_CHOICES = [
        ('employee', 'employee'),
        ('employer', 'employer'),
    ]
    name = models.CharField(max_length=200, verbose_name="KATEGORIYA NOMI")
    for_who = models.CharField(max_length=20, choices=FOR_WHO_CHOICES, verbose_name="KIM UCHUN")

    class Meta:
        db_table = 'category'
        verbose_name = "Category"
        verbose_name_plural = "Post Kategoriyalari"

    def __str__(self):
        return self.name


class Posts(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name="POST/MUROJAAT EGASI")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="CATEGORIYA NOMI")
    text = models.TextField(null=True, blank=True, verbose_name="TEXT")
    image = models.CharField(max_length=500, null=True, blank=True, verbose_name="RASM")
    video = models.CharField(max_length=500, null=True, blank=True, verbose_name="VIDEO")
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="YARATILGAN VAQT")

    class Meta:
        db_table = 'post'
        verbose_name = "Post"
        verbose_name_plural = "Postlar"

    def __str__(self):
        return f"{self.category.name} uchun qo'yilgan post"
