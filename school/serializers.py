from rest_framework import serializers
from .models import Course, Lesson, Payment, Subscription


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview_image', 'video_link', 'course', 'user']

        def create(self, validated_data):
            # Извлечем пользователя из контекста запроса
            user = self.context['request'].user

            # Добавим пользователя к validated_data перед созданием урока
            validated_data['user'] = user

            return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview_image', 'description', 'lessons_count', 'lessons', 'is_subscribed']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()


class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'course', 'lesson', 'amount', 'payment_method']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

