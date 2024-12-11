from django.conf import settings
from httpx import post
from icecream import ic

from .models import LeaderBoard, TestCaseSubmission


def create_submission_testcase(request, submission):
    error = 0
    leaderboard = LeaderBoard.objects.get_or_create(
        contest=submission.problem.contest, participant=request.user
    )[0]
    for case in submission.problem.test_cases.all():
        ic(case, case.id, case.input, case.output)
        data = {
            "language": submission.language.language,
            "version": submission.language.version,
            "files": [{"content": submission.user_solution}],
            "stdin": case.input,
            "args": (
                submission.language.args.split(" ") if submission.language.args else []
            ),
            "compile_timeout": submission.problem.time_limit * 1000,
            "run_memory_limit": submission.problem.memory_limit * 1000000,
        }
        r = post(f"{settings.PISTON_API_BASE}/api/v2/execute", json=data)

        r_json = r.json()
        ic(r_json)

        test_case_submission = TestCaseSubmission(
            base_submission=submission, test_case=case
        )
        if r_json.get("run").get("code") == 0:
            if case.output.replace("\r", "") == r_json.get("run").get("output").strip():
                test_case_submission.success = True
                submission.status = submission.SubmissionStatus.SUCCEED
                if (
                    submission.problem not in leaderboard.solved_problems.all()
                    and leaderboard.contest.status == "R"
                ):
                    leaderboard.solved_problems.add(submission.problem)
                    leaderboard.score += 1
                    leaderboard.save()
            else:
                submission.status = submission.SubmissionStatus.UNMATCHED
                error = 1
        elif r_json.get("run").get("status") == "TO":
            submission.status = submission.SubmissionStatus.TIMELIMITEXCEEDED
            test_case_submission.output = (
                "Time limit exceeded for your code. Please optimize your code."
            )
            error = 1
        elif r_json.get("run").get("status") == "RE":
            submission.status = submission.SubmissionStatus.RUNTIMEERROR
            test_case_submission.output = (
                r_json.get("run").get("stderr")
                if r_json.get("run").get("stderr")
                else r_json.get("run").get("output")
            )
            error = 1
        elif r_json.get("run").get("code") == 137:
            submission.status = submission.SubmissionStatus.MEMOERYLIMIITEXCEEDED
            test_case_submission.output = r_json.get("run").get("message")
            error = 1
        else:
            submission.status = submission.SubmissionStatus.ERROR
            test_case_submission.out = r_json.get("run").get("message") or r_json.get(
                "run"
            ).get("stderr")
            error = 1

        test_case_submission.output = r_json.get("run").get("output").strip()
        submission.save()
        test_case_submission.save()
        if error:
            if leaderboard.contest.status == "R":
                leaderboard.penalty = (
                    leaderboard.penalty + submission.problem.penalty_time
                )
                leaderboard.save()
            break
