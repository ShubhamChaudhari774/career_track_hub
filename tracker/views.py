from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import Application
from .forms import RegisterForm, ApplicationForm, SearchForm


# ─────────────────────────────────────────────
# Public
# ─────────────────────────────────────────────

def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tracker/landing.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Career Track Hub, {user.first_name}!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# ─────────────────────────────────────────────
# Authenticated
# ─────────────────────────────────────────────

@login_required
def dashboard_view(request):
    apps = Application.objects.filter(user=request.user)
    total = apps.count()

    # Status breakdown
    status_counts = dict(apps.values_list('status').annotate(count=Count('status')))

    # Key stats
    active = apps.filter(status__in=['applied', 'phone_screen', 'interview_scheduled',
                                      'technical_interview', 'final_round']).count()
    offers = apps.filter(status='offer').count() + apps.filter(status='accepted').count()
    rejected = apps.filter(status='rejected').count()
    response_rate = round((total - apps.filter(status__in=['applied', 'no_response']).count()) / total * 100) if total > 0 else 0

    # Upcoming interviews
    now = timezone.now()
    upcoming = apps.filter(next_interview_date__gte=now).order_by('next_interview_date')[:5]

    # Recent applications
    recent = apps.order_by('-created_at')[:5]

    # High priority items
    high_priority = apps.filter(priority='high').exclude(status__in=['rejected', 'withdrawn', 'accepted'])[:5]

    context = {
        'total': total,
        'active': active,
        'offers': offers,
        'rejected': rejected,
        'response_rate': response_rate,
        'upcoming': upcoming,
        'recent': recent,
        'high_priority': high_priority,
        'status_counts': status_counts,
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required
def application_list_view(request):
    apps = Application.objects.filter(user=request.user)

    # Filtering
    status_filter = request.GET.get('status', '')
    type_filter = request.GET.get('job_type', '')
    location_filter = request.GET.get('location', '')
    sort = request.GET.get('sort', '-date_applied')

    if status_filter:
        apps = apps.filter(status=status_filter)
    if type_filter:
        apps = apps.filter(job_type=type_filter)
    if location_filter:
        apps = apps.filter(location=location_filter)

    valid_sorts = ['date_applied', '-date_applied', 'company_name', '-company_name',
                   'status', '-status', 'priority', '-priority']
    if sort in valid_sorts:
        apps = apps.order_by(sort)

    context = {
        'applications': apps,
        'status_choices': Application.STATUS_CHOICES,
        'type_choices': Application.JOB_TYPE_CHOICES,
        'location_choices': Application.LOCATION_CHOICES,
        'current_status': status_filter,
        'current_type': type_filter,
        'current_location': location_filter,
        'current_sort': sort,
        'total_count': apps.count(),
    }
    return render(request, 'tracker/application_list.html', context)


@login_required
def application_create_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            messages.success(request, f'Application for {app.company_name} added successfully!')
            return redirect('application_list')
    else:
        form = ApplicationForm(initial={'date_applied': timezone.now().date()})
    return render(request, 'tracker/application_form.html', {'form': form, 'title': 'Add Application', 'action': 'Add'})


@login_required
def application_update_view(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, f'Application for {app.company_name} updated!')
            return redirect('application_detail', pk=pk)
    else:
        form = ApplicationForm(instance=app)
    return render(request, 'tracker/application_form.html', {'form': form, 'title': 'Edit Application', 'action': 'Save Changes', 'app': app})


@login_required
def application_delete_view(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        company = app.company_name
        app.delete()
        messages.success(request, f'Application for {company} deleted.')
        return redirect('application_list')
    return render(request, 'tracker/application_confirm_delete.html', {'app': app})


@login_required
def application_detail_view(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    return render(request, 'tracker/application_detail.html', {'app': app})


@login_required
def search_view(request):
    form = SearchForm(request.GET or None)
    results = Application.objects.filter(user=request.user)
    query = ''

    if form.is_valid():
        q = form.cleaned_data.get('q', '').strip()
        status = form.cleaned_data.get('status')
        job_type = form.cleaned_data.get('job_type')
        location = form.cleaned_data.get('location')
        query = q

        if q:
            results = results.filter(
                Q(company_name__icontains=q) |
                Q(position_title__icontains=q) |
                Q(notes__icontains=q) |
                Q(recruiter_name__icontains=q) |
                Q(job_location_city__icontains=q)
            )
        if status:
            results = results.filter(status=status)
        if job_type:
            results = results.filter(job_type=job_type)
        if location:
            results = results.filter(location=location)

    return render(request, 'tracker/search.html', {
        'form': form,
        'results': results,
        'query': query,
        'count': results.count(),
    })
