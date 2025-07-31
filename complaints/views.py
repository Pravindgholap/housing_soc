from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import models
from .models import Complaint, ComplaintUpdate, ComplaintCategory
from .forms import ComplaintForm, ComplaintUpdateForm, ComplaintStatusForm

@login_required
def complaint_list(request):
    if request.user.user_type == 'admin':
        # Filter by society for society admins
        if request.user.society:
            complaints = Complaint.objects.filter(created_by__society=request.user.society)
        else:
            complaints = Complaint.objects.all()
    else:
        # Show complaints from same society for owners/tenants
        complaints = Complaint.objects.filter(
            models.Q(created_by=request.user) | 
            models.Q(created_by__society=request.user.society)
        )
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    
    return render(request, 'complaints/complaint_list.html', {
        'complaints': complaints,
        'status_filter': status_filter
    })

@login_required
def create_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.created_by = request.user
            complaint.save()
            messages.success(request, 'Complaint submitted successfully!')
            return redirect('complaints:complaint_detail', complaint_id=complaint.id)
    else:
        form = ComplaintForm()
    
    return render(request, 'complaints/create_complaint.html', {'form': form})

@login_required
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    # Check permissions
    if request.user.user_type != 'admin' and complaint.created_by != request.user:
        messages.error(request, 'Access denied!')
        return redirect('complaints:complaint_list')
    
    updates = ComplaintUpdate.objects.filter(complaint=complaint)
    
    # Handle status update (admin only)
    status_form = None
    if request.user.user_type == 'admin':
        if request.method == 'POST' and 'update_status' in request.POST:
            status_form = ComplaintStatusForm(request.POST, instance=complaint)
            if status_form.is_valid():
                updated_complaint = status_form.save()
                if updated_complaint.status == 'resolved':
                    updated_complaint.resolved_at = timezone.now()
                    updated_complaint.save()
                messages.success(request, 'Complaint status updated!')
                return redirect('complaints:complaint_detail', complaint_id=complaint.id)
        else:
            status_form = ComplaintStatusForm(instance=complaint)
    
    # Handle update submission
    if request.method == 'POST' and 'add_update' in request.POST:
        update_form = ComplaintUpdateForm(request.POST, request.FILES)
        if update_form.is_valid():
            update = update_form.save(commit=False)
            update.complaint = complaint
            update.created_by = request.user
            update.save()
            messages.success(request, 'Update added successfully!')
            return redirect('complaints:complaint_detail', complaint_id=complaint.id)
    else:
        update_form = ComplaintUpdateForm()
    
    return render(request, 'complaints/complaint_detail.html', {
        'complaint': complaint,
        'updates': updates,
        'update_form': update_form,
        'status_form': status_form
    })