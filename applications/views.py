from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Application
from .forms import RegisterForm, ApplicationForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard_view(request):
    applications = Application.objects.filter(user=request.user)

    # Search
    query = request.GET.get('q', '')
    if query:
        applications = applications.filter(
            Q(company_name__icontains=query) |
            Q(position_title__icontains=query) |
            Q(status__icontains=query) |
            Q(location__icontains=query) |
            Q(notes__icontains=query)
        )

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)

    # Filter by job type
    job_type_filter = request.GET.get('job_type', '')
    if job_type_filter:
        applications = applications.filter(job_type=job_type_filter)

    # Stats
    all_apps = Application.objects.filter(user=request.user)
    stats = {
        'total': all_apps.count(),
        'applied': all_apps.filter(status='applied').count(),
        'interviews': all_apps.filter(status__in=['interview_scheduled', 'technical_round']).count(),
        'offers': all_apps.filter(status='offer').count(),
        'rejected': all_apps.filter(status='rejected').count(),
    }

    context = {
        'applications': applications,
        'stats': stats,
        'query': query,
        'status_filter': status_filter,
        'job_type_filter': job_type_filter,
        'status_choices': Application.STATUS_CHOICES,
        'job_type_choices': Application.JOB_TYPE_CHOICES,
    }
    return render(request, 'applications/dashboard.html', context)


@login_required
def add_application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, f'Application for {application.position_title} at {application.company_name} added!')
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'applications/application_form.html', {'form': form, 'title': 'Add Application'})


@login_required
def edit_application_view(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application updated successfully!')
            return redirect('dashboard')
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'applications/application_form.html', {
        'form': form,
        'title': 'Edit Application',
        'application': application
    })


@login_required
def delete_application_view(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        company = application.company_name
        application.delete()
        messages.success(request, f'Application for {company} deleted.')
        return redirect('dashboard')
    return render(request, 'applications/confirm_delete.html', {'application': application})


@login_required
def application_detail_view(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    return render(request, 'applications/application_detail.html', {'application': application})
