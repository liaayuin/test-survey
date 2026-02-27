from django.db import models


class Respondent(models.Model):
    timestamp = models.DateTimeField(unique=True, db_index=True)

    age = models.IntegerField(null=True, blank=True, db_index=True)
    gender = models.CharField(max_length=50, db_index=True)
    sub_city = models.CharField(max_length=100, db_index=True)
    education = models.CharField(max_length=255, db_index=True)
    employment = models.CharField(max_length=100, db_index=True)
    telegram_account = models.BooleanField(default=False)
    heard_about_yne = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["gender"]),
            models.Index(fields=["education"]),
            models.Index(fields=["employment"]),
            models.Index(fields=["age"]),
            models.Index(fields=["sub_city"]),
        ]

    def __str__(self):
        return f"Respondent {self.id}"


class QuestionCategory(models.Model):
    """
    Normalized question categories
    Example:
        Awareness Channel
        Participation Barrier
        Training Interest
        Platform Used
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MultiSelectOption(models.Model):
    """
    Predefined selectable values per category
    Example:
        Category: Barrier
        Options: Internet Cost, Time Conflict, Device Access
    """
    category = models.ForeignKey(
        QuestionCategory,
        related_name="options",
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ("category", "value")
        indexes = [
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.category.name} - {self.value}"


class MultiSelectAnswer(models.Model):
    respondent = models.ForeignKey(
        Respondent,
        related_name="multi_answers",
        on_delete=models.CASCADE
    )
    option = models.ForeignKey(
        MultiSelectOption,
        related_name="answers",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("respondent", "option")
        indexes = [
            models.Index(fields=["respondent"]),
            models.Index(fields=["option"]),
        ]

    def __str__(self):
        return f"{self.respondent.id} - {self.option.value}"