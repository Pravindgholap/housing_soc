from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Meeting, MeetingAttendance, MeetingDocument
from .forms import MeetingForm, MeetingMinutesForm, MeetingDocumentForm

@login_required
def meeting_list(request):
    meetings = Meeting.objects.all()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        meetings = meetings.filter(status=status_filter)
    
    return render(request, 'meetings/meeting_list.html', {
        'meetings': meetings,
        'status_filter': status_filter
    })

@login_required
def create_meeting(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Only admins can create meetings!')
        return redirect('meetings:meeting_list')
    
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.created_by = request.user
            meeting.save()
            form.save_m2m()  # Save many-to-many relationships
            
            # Create attendance records for selected attendees
            for attendee in form.cleaned_data['attendees']:
                MeetingAttendance.objects.create(meeting=meeting, user=attendee)
            
            messages.success(request, 'Meeting created successfully!')
            return redirect('meetings:meeting_detail', meeting_id=meeting.id)
    else:
        form = MeetingForm()
    
    return render(request, 'meetings/create_meeting.html', {'form': form})

@login_required
def meeting_detail(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    attendance = MeetingAttendance.objects.filter(meeting=meeting)
    documents = MeetingDocument.objects.filter(meeting=meeting)
    
    # Get user's attendance record if exists
    user_attendance = None
    try:
        user_attendance = MeetingAttendance.objects.get(meeting=meeting, user=request.user)
    except MeetingAttendance.DoesNotExist:
        pass
    
    # Handle RSVP
    if request.method == 'POST' and 'rsvp' in request.POST:
        response = request.POST.get('response')
        if user_attendance:
            user_attendance.response = response
            user_attendance.save()
        else:
            MeetingAttendance.objects.create(
                meeting=meeting,
                user=request.user,
                response=response
            )
        messages.success(request, f'RSVP updated to {response}!')
        return redirect('meetings:meeting_detail', meeting_id=meeting.id)
    
    # Handle minutes update (admin only)
    minutes_form = None
    if request.user.user_type == 'admin':
        if request.method == 'POST' and 'update_minutes' in request.POST:
            minutes_form = MeetingMinutesForm(request.POST, instance=meeting)
            if minutes_form.is_valid():
                minutes_form.save()
                messages.success(request, 'Meeting minutes updated!')
                return redirect('meetings:meeting_detail', meeting_id=meeting.id)
        else:
            minutes_form = MeetingMinutesForm(instance=meeting)
    
    # Handle document upload
    if request.method == 'POST' and 'upload_document' in request.POST:
        doc_form = MeetingDocumentForm(request.POST, request.FILES)
        if doc_form.is_valid():
            document = doc_form.save(commit=False)
            document.meeting = meeting
            document.uploaded_by = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully!')
            return redirect('meetings:meeting_detail', meeting_id=meeting.id)
    else:
        doc_form = MeetingDocumentForm()
    
    return render(request, 'meetings/meeting_detail.html', {
        'meeting': meeting,
        'attendance': attendance,
        'documents': documents,
        'user_attendance': user_attendance,
        'minutes_form': minutes_form,
        'doc_form': doc_form
    })

@login_required
def update_meeting_status(request, meeting_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('meetings:meeting_list')
    
    meeting = get_object_or_404(Meeting, id=meeting_id)
    new_status = request.POST.get('status')
    
    if new_status in dict(Meeting.STATUS_CHOICES):
        meeting.status = new_status
        meeting.save()
        messages.success(request, f'Meeting status updated to {new_status}!')
    
    return redirect('meetings:meeting_detail', meeting_id=meeting.id)