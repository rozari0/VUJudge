from django.shortcuts import render

from judge.models import Contest, ProblemSubmission


# Create your views here.
def profile(request):
    # Fetch the user's recent submissions (limit to 5)
    submissions = ProblemSubmission.objects.filter(submitted_by=request.user).order_by(
        "-id"
    )[:5]

    return render(
        request,
        "accounts/profile.html",
        {
            "submissions": submissions,
        },
    )
