import os
import threading
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'survey_analytics.settings')
application = get_wsgi_application()

def auto_setup():
    # We import inside the function so models are ready
    from django.contrib.auth import get_user_model
    from django.core.management import call_command
    
    User = get_user_model()
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

    if username and password:
        try:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
                print(f"--- Superuser {username} created ---")
            
            # Also auto-import your data since you can't use the shell!
            print("--- Starting Data Import ---")
            call_command('import_survey')
            print("--- Data Import Complete ---")
            
        except Exception as e:
            print(f"Auto-setup error: {e}")

# Start the setup in the background so the website doesn't hang
threading.Thread(target=auto_setup).start()