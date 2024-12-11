from django.urls import path

from .views import (
    ContestListView,
    contest_detail,
    contest_leaderboard,
    homepage,
    problem_detail,
    problem_submit,
    submit_problem_extra_view,
)

urlpatterns = [
    path("", homepage, name="homepage"),
    path("homepage/", homepage, name="homepage"),
    path("contests/", ContestListView.as_view(), name="contests"),
    path("contests/<int:pk>/", contest_detail, name="contest_detail"),
    path(
        "contests/<int:contest_id>/problem/<int:pk>/",
        problem_detail,
        name="problem_detail",
    ),
    path(
        "contests/<int:contest_id>/problem/<int:pk>/submission/",
        problem_submit,
        name="problem_submit",
    ),
    path(
        "contests/<int:pk>/leaderboard/",
        contest_leaderboard,
        name="contest_leaderboard",
    ),
    path(
        "contests/<int:contest_id>/problem/<int:pk>/submit/",
        submit_problem_extra_view,
        name="problem_submit_get",
    ),
]
