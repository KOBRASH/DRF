from rest_framework.test import APITestCase


class CourseTestCase(APITestCase):


    def setUp(self) -> None:
        pass


    def test_create_course(self):
        """ Тестирование создания курсов """
        self.client