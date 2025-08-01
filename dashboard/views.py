from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from maintenance.models import MaintenanceBill
from complaints.models import Complaint
from meetings.models import Meeting
from notices.models import Notice
from financial.models import Transaction

@login_required
def home(request):
    # Check if user needs to complete profile or wait for verification
    if not request.user.society:
        messages.warning(request, 'Please complete your profile by selecting a society.')
        return redirect('accounts:profile')
    
    if not request.user.is_verified and request.user.user_type != 'admin':
        messages.info(request, 'Your account is pending admin approval. Some features may be limited.')
    
    context = {}
    
    # Common stats for all users
    # Filter by society
    if request.user.society:
        context['total_notices'] = Notice.objects.filter(
            is_active=True, 
            created_by__society=request.user.society
        ).count()
        context['upcoming_meetings'] = Meeting.objects.filter(
            status='scheduled',
            created_by__society=request.user.society
        ).count()
    else:
        context['total_notices'] = 0
        context['upcoming_meetings'] = 0
    
    if request.user.user_type == 'admin':
        # Admin dashboard stats
        if request.user.society:
            context['total_users'] = request.user.__class__.objects.filter(
                society=request.user.society
            ).count()
            context['pending_complaints'] = Complaint.objects.filter(
                status='open',
                created_by__society=request.user.society
            ).count()
            context['total_maintenance_due'] = MaintenanceBill.objects.filter(
                status='pending',
                user__society=request.user.society
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            context['recent_transactions'] = Transaction.objects.filter(
                created_by__society=request.user.society
            )[:5]
            context['recent_complaints'] = Complaint.objects.filter(
                created_by__society=request.user.society
            )[:5]
        else:
            # Super admin sees all
            context['total_users'] = request.user.__class__.objects.count()
            context['pending_complaints'] = Complaint.objects.filter(status='open').count()
            context['total_maintenance_due'] = MaintenanceBill.objects.filter(
                status='pending'
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            context['recent_transactions'] = Transaction.objects.all()[:5]
            context['recent_complaints'] = Complaint.objects.all()[:5]
    else:
        # Owner/Tenant dashboard stats
        context['my_complaints'] = Complaint.objects.filter(
            created_by=request.user
        ).count()
        context['my_pending_bills'] = MaintenanceBill.objects.filter(
            user=request.user, status='pending'
        ).count()
        context['my_recent_bills'] = MaintenanceBill.objects.filter(
            user=request.user
        )[:3]
    
    return render(request, 'dashboard/home.html', context)