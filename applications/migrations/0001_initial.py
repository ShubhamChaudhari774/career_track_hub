from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('position_title', models.CharField(max_length=200)),
                ('job_type', models.CharField(choices=[('internship', 'Internship'), ('full_time', 'Full-Time'), ('part_time', 'Part-Time'), ('contract', 'Contract')], default='full_time', max_length=20)),
                ('location_type', models.CharField(choices=[('remote', 'Remote'), ('hybrid', 'Hybrid'), ('on_site', 'On-Site')], default='on_site', max_length=20)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('date_applied', models.DateField()),
                ('status', models.CharField(choices=[('applied', 'Applied'), ('interview_scheduled', 'Interview Scheduled'), ('technical_round', 'Technical Round'), ('offer', 'Offer Received'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn')], default='applied', max_length=30)),
                ('job_url', models.URLField(blank=True, null=True)),
                ('recruiter_name', models.CharField(blank=True, max_length=200)),
                ('recruiter_email', models.EmailField(blank=True, max_length=254)),
                ('salary_range', models.CharField(blank=True, max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_applied'],
            },
        ),
    ]
