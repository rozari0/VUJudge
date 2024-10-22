from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    Contest,
    Language,
    Problem,
    ProblemSubmission,
    TestCase,
    TestCaseSubmission,
    LeaderBoard,
)

# Register your models here.

admin.site.register(Contest, ModelAdmin)


class TestCaseTabularInline(TabularInline):
    model = TestCase
    extra = 1


class ProblemAdmin(ModelAdmin):
    inlines = [TestCaseTabularInline]


admin.site.register(Problem, ProblemAdmin)


class TestCaseSubmissionInline(TabularInline):
    model = TestCaseSubmission
    extra = 1


class ProblemSubmissionAdmin(ModelAdmin):
    inlines = [TestCaseSubmissionInline]


admin.site.register(ProblemSubmission, ProblemSubmissionAdmin)

admin.site.register(Language, ModelAdmin)

admin.site.register(LeaderBoard, ModelAdmin)
