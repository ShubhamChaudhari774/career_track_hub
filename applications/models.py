from django.db import models
from django.contrib.auth.models import User


class Application(models.Model):
    JOB_TYPE_CHOICES = [
        ('internship', 'Internship'),
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('contract', 'Contract'),
    ]

    LOCATION_TYPE_CHOICES = [
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('on_site', 'On-Site'),
    ]

    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('technical_round', 'Technical Round'),
        ('offer', 'Offer Received'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    company_name = models.CharField(max_length=200)
    position_title = models.CharField(max_length=200)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES, default='on_site')
    location = models.CharField(max_length=200, blank=True)
    date_applied = models.DateField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='applied')
    job_url = models.URLField(blank=True, null=True)
    recruiter_name = models.CharField(max_length=200, blank=True)
    recruiter_email = models.EmailField(blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_applied']

    def __str__(self):
        return f"{self.position_title} at {self.company_name}"

    def get_status_color(self):
        colors = {
            'applied': 'blue',
            'interview_scheduled': 'yellow',
            'technical_round': 'orange',
            'offer': 'green',
            'rejected': 'red',
            'withdrawn': 'gray',
        }
        return colors.get(self.status, 'blue')
