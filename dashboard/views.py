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
    context = {}
    
    # Common stats for all users
    context['total_notices'] = Notice.objects.filter(is_active=True).count()
    context['upcoming_meetings'] = Meeting.objects.filter(status='scheduled').count()
    
    if request.user.user_type == 'admin':
        # Admin dashboard stats
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