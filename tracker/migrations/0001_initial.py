from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                ('job_type', models.CharField(choices=[('internship', 'Internship'), ('full_time', 'Full-Time'), ('part_time', 'Part-Time'), ('contract', 'Contract'), ('co_op', 'Co-op')], default='full_time', max_length=20)),
                ('location', models.CharField(choices=[('remote', 'Remote'), ('hybrid', 'Hybrid'), ('on_site', 'On-Site')], default='on_site', max_length=20)),
                ('job_location_city', models.CharField(blank=True, help_text='City/State e.g. New York, NY', max_length=100)),
                ('date_applied', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('applied', 'Applied'), ('phone_screen', 'Phone Screen'), ('interview_scheduled', 'Interview Scheduled'), ('technical_interview', 'Technical Interview'), ('final_round', 'Final Round'), ('offer', 'Offer Received'), ('accepted', 'Offer Accepted'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn'), ('no_response', 'No Response')], default='applied', max_length=30)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=10)),
                ('job_posting_url', models.URLField(blank=True, help_text='Link to the job posting')),
                ('salary_range', models.CharField(blank=True, help_text='e.g. $80,000 - $100,000', max_length=100)),
                ('application_deadline', models.DateField(blank=True, null=True)),
                ('recruiter_name', models.CharField(blank=True, max_length=100)),
                ('recruiter_email', models.EmailField(blank=True, max_length=254)),
                ('recruiter_phone', models.CharField(blank=True, max_length=20)),
                ('next_interview_date', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, help_text='Interview reminders, recruiter notes, follow-up actions')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_applied', '-created_at'],
            },
        ),
    ]
