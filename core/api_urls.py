from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'progress', ProgressViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', obtain_auth_token, name='login'),
]
