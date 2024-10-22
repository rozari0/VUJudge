from django import forms

from .models import ProblemSubmission


class ProblemSubmissionForm(forms.ModelForm):
    class Meta:
        model = ProblemSubmission
        exclude = ["submitted_by", "problem", "status"]
