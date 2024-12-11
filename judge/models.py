from datetime import datetime, timedelta, timezone

from django.db import models

from accounts.models import User


class Contest(models.Model):
    class Status(models.TextChoices):
        NOTSTARTED = "N", "Not Started"
        RUNNING = "R", "Running"
        FINISHED = "F", "Finished"

    name = models.CharField(max_length=100, help_text="The name of the contest")
    start_time = models.DateTimeField(help_text="The start time of the contest")
    duration = models.IntegerField(
        help_text="The duration of the contest (minutes)", default=120
    )

    @property
    def status(self):
        now = datetime.now(timezone.utc)
        end_time = self.start_time + timedelta(minutes=self.duration)
        if now < self.start_time:
            return Contest.Status.NOTSTARTED
        elif self.start_time <= now <= end_time:
            return Contest.Status.RUNNING
        else:
            return Contest.Status.FINISHED

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration)

    def __str__(self):
        return self.name


class Problem(models.Model):
    contest = models.ForeignKey(
        Contest, on_delete=models.CASCADE, help_text="The contest"
    )
    name = models.CharField(max_length=100, help_text="The name of the problem")
    description = models.TextField(
        help_text="The description of the problem [Markdown]"
    )

    time_limit = models.IntegerField(
        help_text="The time limit of the problem (in seconds)", default=2
    )
    memory_limit = models.IntegerField(
        help_text="The memory limit of the problem (in megabytes)", default=64
    )
    penalty_time = models.IntegerField(
        help_text="The penalty time of the problem (in minutes)", default=1
    )
    is_open = models.BooleanField(default=True, help_text="Whether the problem is open")

    def __str__(self):
        return self.name


class TestCase(models.Model):
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name="test_cases"
    )
    case_no = models.PositiveIntegerField(help_text="The case number")
    input = models.TextField(help_text="The input of the problem")
    output = models.TextField(help_text="Expected output of the problem")

    def __str__(self):
        return "Case " + str(self.case_no) + " for " + str(self.problem.name)


class Language(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="The name of the language for users",
        null=True,
        blank=True,
    )
    language = models.CharField(
        help_text="The name of the language in piston API.", max_length=100
    )
    version = models.CharField(
        max_length=100, help_text="The version of the language", default=""
    )
    args = models.CharField(
        max_length=100,
        help_text="The arguments that are passed to the compiler/interpreter",
        null=True,
        blank=True,
    )
    active = models.BooleanField(
        help_text="Whether the language is active", default=True
    )

    def __str__(self):
        return (
            self.name if self.name else self.language + " (" + str(self.version) + ")"
        )


class ProblemSubmission(models.Model):
    class SubmissionStatus(models.TextChoices):
        SUCCEED = "S", "Succeed"
        RUNNING = "R", "Running"
        RUNTIMEERROR = "RE", "Runtime Error"
        MEMOERYLIMIITEXCEEDED = "ME", "Memory Limit Exceeded"
        TIMELIMITEXCEEDED = "TO", "Time Limit Exceeded"
        UNMATCHED = "U", "Unmatched"
        ERROR = "E", "Error"

    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name="submissions"
    )
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        help_text="The status of the submission",
        max_length=2,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.RUNNING,
    )

    user_solution = models.TextField(help_text="The solution for this problem.")

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return str(self.id) + " - " + str(self.problem.name)


class TestCaseSubmission(models.Model):
    base_submission = models.ForeignKey(
        ProblemSubmission,
        on_delete=models.CASCADE,
        related_name="test_case_submissions",
    )
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    success = models.BooleanField(
        default=False, help_text="Whether the test case is successful"
    )
    output = models.TextField(
        help_text="Returned Output from Execution.", null=True, blank=True
    )


class LeaderBoard(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    penalty = models.IntegerField(
        help_text="The penalty time of the problem", default=0
    )
    score = models.IntegerField(help_text="The score of the contest", default=0)
    solved_problems = models.ManyToManyField(Problem, blank=True)

    class Meta:
        ordering = ["-score", "penalty", "-id"]

    def __str__(self):
        return f"{self.contest} - {self.participant}"
