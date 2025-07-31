from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Transaction, TransactionCategory, Budget, BankAccount
from .forms import TransactionForm, BudgetForm, BankAccountForm, TransactionCategoryForm

@login_required
def financial_dashboard(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard:home')
    
    # Calculate financial summary
    current_month = timezone.now().month
    current_year = timezone.now().year
    
    # Filter by society
    if request.user.society:
        base_filter = {'created_by__society': request.user.society}
    else:
        base_filter = {}
    
    total_income = Transaction.objects.filter(
        transaction_type='income',
        **base_filter
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_expenses = Transaction.objects.filter(
        transaction_type='expense',
        **base_filter
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    monthly_income = Transaction.objects.filter(
        transaction_type='income',
        transaction_date__month=current_month,
        transaction_date__year=current_year,
        **base_filter
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    monthly_expenses = Transaction.objects.filter(
        transaction_type='expense',
        transaction_date__month=current_month,
        transaction_date__year=current_year,
        **base_filter
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    recent_transactions = Transaction.objects.filter(**base_filter)[:10]
    active_budgets = Budget.objects.filter(is_active=True, created_by__society=request.user.society) if request.user.society else Budget.objects.filter(is_active=True)
    
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': total_income - total_expenses,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'monthly_net': monthly_income - monthly_expenses,
        'recent_transactions': recent_transactions,
        'active_budgets': active_budgets,
    }
    
    return render(request, 'financial/dashboard.html', context)

@login_required
def transaction_list(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard:home')
    
    # Filter transactions by society
    if request.user.society:
        transactions = Transaction.objects.filter(created_by__society=request.user.society)
    else:
        transactions = Transaction.objects.all()
    
    # Filter by type
    transaction_type = request.GET.get('type')
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    
    # Filter categories by society transactions
    if request.user.society:
        categories = TransactionCategory.objects.filter(
            is_active=True,
            transaction__created_by__society=request.user.society
        ).distinct()
    else:
        categories = TransactionCategory.objects.filter(is_active=True)
    
    return render(request, 'financial/transaction_list.html', {
        'transactions': transactions,
        'categories': categories,
        'transaction_type': transaction_type,
        'category_id': category_id
    })

@login_required
def create_transaction(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.created_by = request.user
            transaction.save()
            messages.success(request, 'Transaction created successfully!')
            return redirect('financial:transaction_list')
    else:
        form = TransactionForm()
    
    return render(request, 'financial/create_transaction.html', {'form': form})

@login_required
def budget_list(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard:home')
    
    budgets = Budget.objects.all().order_by('-created_at')
    return render(request, 'financial/budget_list.html', {'budgets': budgets})

@login_required
def create_budget(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.created_by = request.user
            budget.save()
            messages.success(request, 'Budget created successfully!')
            return redirect('financial:budget_list')
    else:
        form = BudgetForm()
    
    return render(request, 'financial/create_budget.html', {'form': form})

@login_required
def bank_accounts(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard:home')
    
    accounts = BankAccount.objects.all()
    return render(request, 'financial/bank_accounts.html', {'accounts': accounts})

@login_required
def create_bank_account(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bank account added successfully!')
            return redirect('financial:bank_accounts')
    else:
        form = BankAccountForm()
    
    return render(request, 'financial/create_bank_account.html', {'form': form})