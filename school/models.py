from django.db import models

from school.validators import validate_youtube_link
from users.models import User
from django.core.validators import MinValueValidator


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview_image = models.ImageField(upload_to='course_previews/', blank=True, null=True)
    description = models.TextField()
    user = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(User, through='Subscription')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='lesson_previews/', blank=True, null=True)
    video_link = models.URLField(validators=[validate_youtube_link])

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    course_or_lesson = models.ForeignKey('Course', on_delete=models.CASCADE, blank=True, null=True)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Наличные'), ('transfer', 'Перевод')])

    def __str__(self):
        return f'{self.user.username} - {self.payment_date}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)
