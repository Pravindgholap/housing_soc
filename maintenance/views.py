from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.db import models
from django.utils import timezone
from xhtml2pdf import pisa
from .models import MaintenanceBill, Payment, MaintenanceType
from .forms import MaintenanceBillForm, PaymentForm, MaintenanceTypeForm
from financial.models import Transaction, TransactionCategory
import uuid

@login_required
def bill_list(request):
    if request.user.user_type == 'admin':
        bills = MaintenanceBill.objects.all().order_by('-created_at')
    else:
        bills = MaintenanceBill.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'maintenance/bill_list.html', {'bills': bills})

@login_required
def create_bill(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('maintenance:bill_list')
    
    if request.method == 'POST':
        form = MaintenanceBillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.bill_number = f"MB{uuid.uuid4().hex[:8].upper()}"
            bill.created_by = request.user
            bill.save()
            messages.success(request, 'Maintenance bill created successfully!')
            return redirect('maintenance:bill_list')
    else:
        form = MaintenanceBillForm()
    
    return render(request, 'maintenance/create_bill.html', {'form': form})

@login_required
def bill_detail(request, bill_id):
    bill = get_object_or_404(MaintenanceBill, id=bill_id)
    
    # Check permissions
    if request.user.user_type != 'admin' and bill.user != request.user:
        messages.error(request, 'Access denied!')
        return redirect('maintenance:bill_list')
    
    payments = Payment.objects.filter(bill=bill)
    return render(request, 'maintenance/bill_detail.html', {
        'bill': bill, 
        'payments': payments
    })

@login_required
def make_payment(request, bill_id):
    bill = get_object_or_404(MaintenanceBill, id=bill_id)
    
    if request.user.user_type != 'admin' and bill.user != request.user:
        messages.error(request, 'Access denied!')
        return redirect('maintenance:bill_list')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.bill = bill
            payment.received_by = request.user
            payment.save()
            
            # Create financial transaction record
            try:
                maintenance_category, created = TransactionCategory.objects.get_or_create(
                    name='Maintenance Payment',
                    defaults={'is_income': True, 'description': 'Maintenance payments from residents'}
                )
                
                Transaction.objects.create(
                    title=f'Maintenance Payment - {bill.bill_number}',
                    description=f'Payment received from {bill.user.get_full_name() or bill.user.username} for {bill.maintenance_type.name}',
                    amount=payment.amount,
                    transaction_type='income',
                    category=maintenance_category,
                    transaction_date=payment.payment_date.date(),
                    created_by=request.user
                )
            except Exception as e:
                messages.warning(request, 'Payment recorded but financial transaction creation failed.')
            
            # Update bill status if fully paid
            total_paid = Payment.objects.filter(bill=bill).aggregate(
                total=models.Sum('amount')
            )['total'] or 0
            
            if total_paid >= bill.total_amount:
                bill.status = 'paid'
                bill.paid_at = timezone.now()
                bill.save()
            
            messages.success(request, 'Payment recorded successfully!')
            return redirect('maintenance:bill_detail', bill_id=bill.id)
    else:
        form = PaymentForm(initial={'amount': bill.total_amount})
    
    return render(request, 'maintenance/make_payment.html', {
        'form': form, 
        'bill': bill
    })

@login_required
def generate_receipt(request, bill_id):
    bill = get_object_or_404(MaintenanceBill, id=bill_id)
    
    if request.user.user_type != 'admin' and bill.user != request.user:
        messages.error(request, 'Access denied!')
        return redirect('maintenance:bill_list')
    
    template_path = 'maintenance/receipt_pdf.html'
    context = {'bill': bill, 'payments': Payment.objects.filter(bill=bill)}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{bill.bill_number}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    
    return response

@login_required
def maintenance_types(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard:home')
    
    types = MaintenanceType.objects.all()
    return render(request, 'maintenance/maintenance_types.html', {'types': types})

@login_required
def create_maintenance_type(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = MaintenanceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maintenance type created successfully!')
            return redirect('maintenance:maintenance_types')
    else:
        form = MaintenanceTypeForm()
    
    return render(request, 'maintenance/create_maintenance_type.html', {'form': form})