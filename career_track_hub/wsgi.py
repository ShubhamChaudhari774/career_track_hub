import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_track_hub.settings')
application = get_wsgi_application()
