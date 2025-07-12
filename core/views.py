from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages

from .models import Course, Lesson, Enrollment, Progress, Quiz, Question, Answer
from .serializers import (
    CourseSerializer, LessonSerializer, EnrollmentSerializer, ProgressSerializer,
    QuizSerializer, QuestionSerializer, AnswerSerializer, UserSerializer, RegisterSerializer
)

User = get_user_model()

# ---------------------------
# User Registration API
# ---------------------------

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------
# API ViewSets
# ---------------------------

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_instructor:
            raise PermissionDenied("Only instructors can create courses.")
        serializer.save(instructor=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


# ---------------------------
# Django Template Views
# ---------------------------

def home(request):
    return render(request, 'core/home.html')


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'core/course_list.html', {'courses': courses})


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    lessons = course.lessons.all()
    return render(request, 'core/course_detail.html', {'course': course, 'lessons': lessons})


def lesson_detail(request, course_pk, lesson_pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk, course_id=course_pk)
    return render(request, 'core/lesson_detail.html', {'lesson': lesson})


def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_instructor = request.POST.get('is_instructor') == 'on'  # checkbox

        data = {
            "username": username,
            "email": email,
            "password": password,
            "is_instructor": is_instructor
        }

        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login_page')
        else:
            messages.error(request, serializer.errors)

    return render(request, 'core/register.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log user in (creates session)
            return redirect('course_list')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'core/login.html')





