from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from .models import Course, Lesson, Payment
from .permissions import CanEditLessonOrCourse, IsOwnerOrModerator
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CanEditLessonOrCourse, IsOwnerOrModerator]

    def perform_create(self, serializer):
        # При создании курса, устанавливаем пользователя владельцем
        serializer.save(user=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]

    def perform_create(self, serializer):
        # При создании урока, устанавливаем пользователя владельцем
        serializer.save(user=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [CanEditLessonOrCourse, IsOwnerOrModerator]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [CanEditLessonOrCourse, IsOwnerOrModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentFilter(filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            'payment_date': ['exact', 'gt', 'lt'],
            'course_or_lesson': ['exact'],
            'payment_method': ['exact'],
        }


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
