from rest_framework import serializers
from .models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview_image', 'video_link', 'course']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview_image', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'course', 'lesson', 'amount', 'payment_method']
