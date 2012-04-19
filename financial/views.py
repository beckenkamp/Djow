from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import Category, CashFlow, CategoryForm, CashFlowForm, DjowDateHandler
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from datetime import *

@login_required(login_url='/login/')
def index(request):
    user = request.user
    cf = CashFlow()
        
    if 'year' in request.GET:
        year = request.GET['year']
    else:
        year = datetime.now().year
    
    if 'month' in request.GET:
        month = request.GET['month']
    else:
        month = datetime.now().month
    
    cash_flow = CashFlow.objects.filter(user_id=user.id, date_due__month=month, date_due__year=year)
    amount_planned_sum = CashFlow.get_amount_planned_sum_by_month(cf, month, year)
    amount_payed_sum = CashFlow.get_amount_payed_sum_by_month(cf, month, year)
    
    month = int(month)
    year = int(year)
    month_now = datetime(year, month, 1)
    
    date_handler = DjowDateHandler.month_year_iterator(month_now)
    
    return render_to_response('cashflow.html', {
        'cash_flow' : cash_flow,
        'user' : user,
        'amount_planned_sum' : amount_planned_sum,
        'amount_payed_sum' : amount_payed_sum,
        'month_now' : date_handler['month_now'],
        'month_last' : date_handler['month_last'],
        'month_next' : date_handler['month_next'],
    })
    
@login_required(login_url='/login/')
def category(request):
    user = request.user
    category = Category.objects.filter(user_id=user.id)
    return render_to_response('category.html', {
        'category' : category,
        'user' : user,
    })

@login_required(login_url='/login/')    
def cashflow_edit(request):    
    user = request.user
    
    if request.method == 'POST':
        form = CashFlowForm(user, request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            installments = form.cleaned_data['installments']
            amount_planned = form.cleaned_data['amount_planned']
            amount_payed = form.cleaned_data['amount_payed']
            date_due = form.cleaned_data['date_due']
            date_payed = form.cleaned_data['date_payed']
 
            if installments > 0:
                installments_string = ' (1/' + str(installments) + ')'
 
            c = CashFlow()
            c.user = user
            c.category = category            
            c.description = description + installments_string            
            c.amount_planned = amount_planned
            c.amount_payed = amount_payed
            c.date_due = date_due
            c.date_payed = date_payed
            c.save()
            
            if installments > 0 :
                for num in range(1, installments):
                    installments_string = ' (' + str(num+1) + '/' + str(installments) + ')'
                    
                    if num == 1:
                        new_date_due = date_due
                        
                    new_date_due = DjowDateHandler.month_increment(new_date_due)
                    
                    cf = CashFlow()
                    cf.user = user
                    cf.category = category
                    cf.parent = c
                    cf.description = description + installments_string
                    cf.installments = installments
                    cf.amount_planned = amount_planned
                    cf.date_due = new_date_due
                    cf.save()
                    
            return HttpResponseRedirect('/')
    else:
        form = CashFlowForm(user)
    
    c = {'form': form}
    c.update({'user' : user,})
    c.update(csrf(request))
    return render_to_response('cashflow_edit.html', c)
    
@login_required(login_url='/login/')    
def category_edit(request):
    user = request.user
    
    if request.method == 'POST':
        form = CategoryForm(user, request.POST)
        if form.is_valid():
            form.save();
            return HttpResponseRedirect('/category')
    else:
        form = CategoryForm(user)
    
    c = {'form': form}
    c.update({'user' : user,})
    c.update(csrf(request))
    return render_to_response('category_edit.html', c)