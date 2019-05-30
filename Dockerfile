FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY purplship_api purplship_api/
COPY purplship_core purplship_core/
COPY purplship_config.py /app/
COPY manage.py /app/

CMD bash -c "(echo \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')\" | python manage.py shell) > /dev/null 2>&1; python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
