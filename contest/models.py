from django.utils import timezone

from django.db import models

from tbmodels.models import Users


class Tests(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True, verbose_name="TEST NOMI")
    FOR_WHO_CHOICES = [
        ('workers', 'workers'),
        ('specialists', 'specialists'),
    ]
    for_who = models.CharField(max_length=20, choices=FOR_WHO_CHOICES, verbose_name="KIM UCHUN")
    count_questions = models.IntegerField(verbose_name="SAVOLLAR SONI")
    picture = models.CharField(max_length=500, verbose_name='TEST SAVOLLARI RASMI')
    time_limit = models.DurationField(null=True, verbose_name='VAQT LIMITI')
    red_line = models.IntegerField(verbose_name="O'TISH BALI")
    answers = models.CharField(max_length=221, verbose_name="TO'G'RI JAVOBLAR")
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name='YARATILGAN VAQT')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "test"
        verbose_name = 'Test'
        verbose_name_plural = "Testlar"


class Results(models.Model):
    test = models.ForeignKey(Tests, on_delete=models.CASCADE, verbose_name="TEST NOMI")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="YECHGAN SHAXS")
    counts_true = models.IntegerField(null=True, blank=True, verbose_name="TO'G'RI JAVOBLAR SONI")
    counts_false = models.IntegerField(null=True, blank=True, verbose_name="NOTO'G'RI JAVOBLAR SONI")
    time_duration = models.DurationField(null=True, blank=True, verbose_name="SARFLANGAN VAQT")
    is_successful = models.BooleanField(null=True, blank=True, verbose_name="MUVAFFAQIYATLI/SIZ")
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name="NATIJA SAQLANGAN VAQT")

    class Meta:
        db_table = 'result'
        verbose_name = 'Result'
        verbose_name_plural = "Natijalar"

    def __str__(self):
        return f"{self.user.full_name}ning {self.test.title} testi natijasi"
