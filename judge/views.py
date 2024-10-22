from datetime import timedelta, datetime, tzinfo, timezone


from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .forms import ProblemSubmissionForm
from .models import Contest, Problem, ProblemSubmission, TestCaseSubmission, LeaderBoard
from .utils import create_submission_testcase
from django.core.paginator import Paginator


def homepage(request):
    return render(request, "judge/homepage.html")


class ContestListView(ListView):
    model = Contest
    template_name = "judge/contests/all.html"
    context_object_name = "contests"


def contest_detail(request, pk):
    contest = get_object_or_404(Contest, id=pk)
    problems = Problem.objects.filter(contest=contest)
    time_left = None
    if contest.status == "R":
        leaderboard = LeaderBoard.objects.get_or_create(
            contest=contest, participant=request.user
        )[0]
        time_left = (
            contest.end_time
            - datetime.now(timezone.utc)
            - timedelta(minutes=leaderboard.penalty)
        )
    elif contest.status == "N":
        time_left = contest.start_time - datetime.now(timezone.utc)
    if time_left:
        time_left = (
            f"{time_left.days * 24 + time_left.seconds // 3600} hours "
            f"{(time_left.seconds // 60) % 60} minutes "
            f"{time_left.seconds % 60} seconds"
        )
    return render(
        request,
        "judge/contests/detail.html",
        {"contest": contest, "problems": problems, "time_left": time_left},
    )


def problem_detail(request, contest_id, pk):
    problem = get_object_or_404(Problem, id=pk)
    contest = get_object_or_404(Contest, id=contest_id)
    return render(
        request,
        "judge/problems/detail.html",
        {"problem": problem, "contest": contest, "form": ProblemSubmissionForm()},
    )


def problem_submit(request, contest_id, pk):
    if request.method == "POST":
        form = ProblemSubmissionForm(request.POST)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.submitted_by = request.user
            submission.problem = get_object_or_404(Problem, id=pk)
            submission.save()
            print(submission)
            create_submission_testcase(request, submission)
            return render(
                request, "judge/submission/foruser.html", {"submissions": [submission]}
            )
        return HttpResponse("Not Noice")
    if request.method == "GET":
        submission = ProblemSubmission.objects.filter(
            problem=pk, submitted_by=request.user
        )
        return render(
            request, "judge/submission/foruser.html", {"submissions": submission}
        )


def contest_leaderboard(request, pk):
    leaderboard = LeaderBoard.objects.filter(contest=pk)
    problems = Problem.objects.filter(contest=pk)

    paginator = Paginator(leaderboard, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "judge/leaderboard.html",
        {"leaderboard": page_obj, "problems": problems},
    )
