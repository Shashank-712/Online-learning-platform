from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Course, Enrollment, Lesson, Progress,
    Quiz, Question, Answer
)


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_instructor',)}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Lesson)
admin.site.register(Progress)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)



