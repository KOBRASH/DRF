from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson, Payment, Subscription
from .paginators import LessonPaginator
from .permissions import CanEditLessonOrCourse, IsOwnerOrModerator
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        course = self.get_object()
        user = request.user
        subscription, created = Subscription.objects.get_or_create(user=user, course=course)
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        course = self.get_object()
        user = request.user
        Subscription.objects.filter(user=user, course=course).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


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
    permission_classes = [IsAuthenticated]