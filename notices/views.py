from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Notice, NoticeCategory, NoticeReadStatus
from .forms import NoticeForm, NoticeCategoryForm

@login_required
def notice_list(request):
    notices = Notice.objects.filter(is_active=True)
    
    # Filter by category if provided
    category_filter = request.GET.get('category')
    if category_filter:
        notices = notices.filter(category_id=category_filter)
    
    # Mark notices as read when viewed
    for notice in notices:
        NoticeReadStatus.objects.get_or_create(notice=notice, user=request.user)
    
    categories = NoticeCategory.objects.filter(is_active=True)
    
    return render(request, 'notices/notice_list.html', {
        'notices': notices,
        'categories': categories,
        'category_filter': category_filter
    })

@login_required
def create_notice(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Only admins can create notices!')
        return redirect('notices:notice_list')
    
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = request.user
            notice.save()
            messages.success(request, 'Notice created successfully!')
            return redirect('notices:notice_detail', notice_id=notice.id)
    else:
        form = NoticeForm()
    
    return render(request, 'notices/create_notice.html', {'form': form})

@login_required
def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    
    # Mark as read
    NoticeReadStatus.objects.get_or_create(notice=notice, user=request.user)
    
    # Get read statistics for admin
    read_count = 0
    total_users = 0
    if request.user.user_type == 'admin':
        read_count = NoticeReadStatus.objects.filter(notice=notice).count()
        total_users = notice.created_by.__class__.objects.filter(is_active=True).count()
    
    return render(request, 'notices/notice_detail.html', {
        'notice': notice,
        'read_count': read_count,
        'total_users': total_users
    })

@login_required
def edit_notice(request, notice_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('notices:notice_list')
    
    notice = get_object_or_404(Notice, id=notice_id)
    
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice updated successfully!')
            return redirect('notices:notice_detail', notice_id=notice.id)
    else:
        form = NoticeForm(instance=notice)
    
    return render(request, 'notices/edit_notice.html', {'form': form, 'notice': notice})

@login_required
def delete_notice(request, notice_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('notices:notice_list')
    
    notice = get_object_or_404(Notice, id=notice_id)
    
    if request.method == 'POST':
        notice.delete()
        messages.success(request, 'Notice deleted successfully!')
        return redirect('notices:notice_list')
    
    return render(request, 'notices/delete_notice.html', {'notice': notice})

@login_required
def notice_categories(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('notices:notice_list')
    
    categories = NoticeCategory.objects.all()
    return render(request, 'notices/notice_categories.html', {'categories': categories})

@login_required
def create_notice_category(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('notices:notice_list')
    
    if request.method == 'POST':
        form = NoticeCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice category created successfully!')
            return redirect('notices:notice_categories')
    else:
        form = NoticeCategoryForm()
    
    return render(request, 'notices/create_notice_category.html', {'form': form})