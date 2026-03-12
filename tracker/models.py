from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Application(models.Model):
    JOB_TYPE_CHOICES = [
        ('internship', 'Internship'),
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('contract', 'Contract'),
        ('co_op', 'Co-op'),
    ]

    LOCATION_CHOICES = [
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('on_site', 'On-Site'),
    ]

    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('phone_screen', 'Phone Screen'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('technical_interview', 'Technical Interview'),
        ('final_round', 'Final Round'),
        ('offer', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
        ('no_response', 'No Response'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    # Ownership
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    # Core fields
    company_name = models.CharField(max_length=200)
    position_title = models.CharField(max_length=200)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='on_site')
    job_location_city = models.CharField(max_length=100, blank=True, help_text="City/State e.g. New York, NY")

    # Application tracking
    date_applied = models.DateField(default=timezone.now)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='applied')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')

    # Job details
    job_posting_url = models.URLField(blank=True, help_text="Link to the job posting")
    salary_range = models.CharField(max_length=100, blank=True, help_text="e.g. $80,000 - $100,000")
    application_deadline = models.DateField(null=True, blank=True)

    # Contact
    recruiter_name = models.CharField(max_length=100, blank=True)
    recruiter_email = models.EmailField(blank=True)
    recruiter_phone = models.CharField(max_length=20, blank=True)

    # Interview tracking
    next_interview_date = models.DateTimeField(null=True, blank=True)

    # Notes
    notes = models.TextField(blank=True, help_text="Interview reminders, recruiter notes, follow-up actions")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_applied', '-created_at']

    def __str__(self):
        return f"{self.company_name} – {self.position_title}"

    def get_status_color(self):
        color_map = {
            'applied': 'blue',
            'phone_screen': 'cyan',
            'interview_scheduled': 'yellow',
            'technical_interview': 'orange',
            'final_round': 'purple',
            'offer': 'green',
            'accepted': 'emerald',
            'rejected': 'red',
            'withdrawn': 'gray',
            'no_response': 'slate',
        }
        return color_map.get(self.status, 'gray')

    def get_priority_color(self):
        return {'low': 'green', 'medium': 'yellow', 'high': 'red'}.get(self.priority, 'gray')
