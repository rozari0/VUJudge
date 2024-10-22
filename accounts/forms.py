from allauth.account.forms import SignupForm
from django import forms


class RegistrationForm(SignupForm):
    first_name = forms.CharField(help_text="Enter your first name.")
    last_name = forms.CharField(help_text="Enter your last name.", required=False)
