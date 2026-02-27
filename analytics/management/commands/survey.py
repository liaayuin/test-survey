import os
import pandas as pd
from django.core.management.base import BaseCommand
from analytics.models import Respondent, MultiSelectAnswer, MultiSelectOption, QuestionCategory
from django.conf import settings
from django.utils import timezone

class Command(BaseCommand):
    help = "Import survey data from Excel"

    def handle(self, *args, **kwargs):
        def clean_bool(val):
            if pd.isna(val) or val is None:
                return False
            val_str = str(val).strip().lower()
            return val_str in ['yes', 'true', '1', 'y', 'checked']

        file_path = os.path.join(settings.BASE_DIR, "data", "DNA TECH DATA .xlsx")
        df = pd.read_excel(file_path, header=1)
        df.rename(columns=lambda x: str(x).strip(), inplace=True)

        for _, row in df.iterrows():
            ts_val = row.get("Timestamp")
            if not ts_val or pd.isna(ts_val):
                continue

            ts_val = timezone.make_aware(pd.to_datetime(ts_val))

            # Fixed Boolean mapping here
            res = Respondent.objects.create(
                timestamp=ts_val,
                age=int(row.get("Age")) if pd.notna(row.get("Age")) else None,
                gender=row.get("Gender", ""),
                sub_city=row.get("Sub City", ""),
                education=row.get("Education Level", ""),
                employment=row.get("Employment Status", ""),
                telegram_account=clean_bool(row.get("Do you have a Telegram account?")),
                heard_about_yne=clean_bool(row.get("Have you ever heard about The Youth Network Ethiopia (YNE)?"))
            )

            # 2. Fixed Multi-select mapping to match your models
            mapping = {
                "Awareness Channel": "If yes, how did you first learn about YNE? (Check all that apply)",
                "Participation Barrier": "What would be the most significant barriers for you to participate in free training sessions? (Select all that apply)",
                "Training Interest": "Would you be interested in training sessions on the following topics? (Select all that apply)",
                "Platform Used": "Which social media platforms have you used for online training purposes? (Select all that apply)"
            }

            for cat_name, col in mapping.items():
                val_str = str(row.get(col, "")).strip()
                if val_str and val_str.lower() != 'nan':
                    # Get or create the category
                    category, _ = QuestionCategory.objects.get_or_create(name=cat_name)
                    
                    # Split options (some use commas, some use semicolons)
                    options = [v.strip() for v in val_str.replace(";", ",").split(",")]
                    
                    for opt_val in options:
                        if opt_val:
                            # Get or create the specific option
                            option_obj, _ = MultiSelectOption.objects.get_or_create(
                                category=category, 
                                value=opt_val
                            )
                            # Link it to the respondent
                            MultiSelectAnswer.objects.get_or_create(
                                respondent=res,
                                option=option_obj
                            )

        self.stdout.write(self.style.SUCCESS("Import Complete! Check your dashboard now."))