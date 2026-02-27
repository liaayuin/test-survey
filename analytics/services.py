from django.db.models import Case, Count, Value, When
from .models import Respondent, MultiSelectAnswer


def demographic_summary():
    total_count = Respondent.objects.count()

    heard_count = Respondent.objects.filter(heard_about_yne=True).count()
    awareness_rate = round((heard_count / total_count * 100), 1) if total_count > 0 else 0
    engaged_count = Respondent.objects.filter(multi_answers__isnull=False).distinct().count()
    engagement_rate = round((engaged_count / total_count * 100), 1) if total_count > 0 else 0
    return {
        "total": Respondent.objects.count(),
        "awareness_rate": awareness_rate,
        "engagement_rate": engagement_rate,
        "gender": list(
            Respondent.objects.values("gender")
            .annotate(count=Count("id"))
            .order_by("-count")
        ),
        "education": list(
            Respondent.objects.values("education")
            .annotate(count=Count("id"))
            .order_by("-count")
        ),
    }


def awareness_stats():
    return {
        "heard_about_yne": list(
            Respondent.objects.values("heard_about_yne")
            .annotate(count=Count("id"))
        ),
        "channels": list(
            MultiSelectAnswer.objects.filter(
                option__category__name="Awareness Channel"
            )
            .values("option__value")
            .annotate(count=Count("id"))
            .order_by("-count")
        ),
    }


def participation_insights():
    return {
        "barriers": list(
            MultiSelectAnswer.objects.filter(
                option__category__name="Participation Barrier"
            )
            .values("option__value")
            .annotate(count=Count("id"))
            .order_by("-count")
        ),
        "platforms": list(
            MultiSelectAnswer.objects.filter(
                option__category__name="Platform Used"
            )
            .values("option__value")
            .annotate(count=Count("id"))
            .order_by("-count")
        ),
    }


def training_preferences():
    return {
        "interests": list(
            MultiSelectAnswer.objects.filter(
                option__category__name="Training Interest"
            )
            .values("option__value")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
    }
def age_distribution_stats():
    return list(
        Respondent.objects.annotate(
            age_range=Case(
                When(age__lt=18, then=Value('Under 18')),
                When(age__gte=18, age__lte=24, then=Value('18-24')),
                When(age__gte=25, age__lte=34, then=Value('25-34')),
                When(age__gt=34, then=Value('35+')),
                default=Value('Unknown'),
            )
        )
        .values("age_range")
        .annotate(count=Count("id"))
        .order_by("age_range")
    )

def subcity_stats():
    return list(
        Respondent.objects.values("sub_city")
        .annotate(count=Count("id"))
        .order_by("-count")
    )