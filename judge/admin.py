from django.contrib import admin
from django.db import models
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import (Contest, Language, LeaderBoard, Problem,
                     ProblemSubmission, TestCase, TestCaseSubmission)

# Register your models here.

admin.site.register(Contest, ModelAdmin)


class TestCaseTabularInline(TabularInline):
    model = TestCase
    extra = 1


class ProblemAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    inlines = [TestCaseTabularInline]


admin.site.register(Problem, ProblemAdmin)


class TestCaseSubmissionInline(TabularInline):
    model = TestCaseSubmission
    extra = 1


class ProblemSubmissionAdmin(ModelAdmin, ImportExportModelAdmin):
    inlines = [TestCaseSubmissionInline]
    import_form_class = ImportForm
    export_form_class = ExportForm


admin.site.register(ProblemSubmission, ProblemSubmissionAdmin)

admin.site.register(Language, ModelAdmin)

admin.site.register(LeaderBoard, ModelAdmin)
