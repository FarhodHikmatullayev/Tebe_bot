from django.utils import timezone

from django.db import models

from tbmodels.models import Users


class Tests(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True)
    FOR_WHO_CHOICES = [
        ('workers', 'workers'),
        ('specialists', 'specialists'),
    ]
    for_who = models.CharField(max_length=20, choices=FOR_WHO_CHOICES)
    count_questions = models.IntegerField()
    picture = models.CharField(max_length=500)
    time_limit = models.DurationField()
    red_line = models.IntegerField()
    answers = models.CharField(max_length=221)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "test"
        verbose_name = 'Test'
        verbose_name_plural = "Testlar"


class Results(models.Model):
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    counts_true = models.IntegerField(null=True, blank=True)
    counts_false = models.IntegerField(null=True, blank=True)
    time_duration = models.DurationField(null=True, blank=True)
    is_successful = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        db_table = 'result'
        verbose_name = 'Result'
        verbose_name_plural = "Natijalar"

    def __str__(self):
        return f"{self.user.full_name}ning {self.test.title} testi natijasi"
