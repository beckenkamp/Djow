from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import Category, CashFlow, CategoryForm, CashFlowForm
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from datetime import *

@login_required(login_url='/login/')
def index(request):
    cash_flow = CashFlow.objects.all()
    user = request.user
    return render_to_response('cashflow.html', {
        'cash_flow' : cash_flow,
        'user' : user,
    })
    
@login_required(login_url='/login/')
def category(request):
    category = Category.objects.all()
    user = request.user
    return render_to_response('category.html', {
        'category' : category,
        'user' : user,
    })

@login_required(login_url='/login/')    
def cashflow_edit(request):    
    user = request.user
    
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
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
                    increment = timedelta(days=30*num)
                    
                    cf = CashFlow()
                    cf.user = user
                    cf.category = category
                    cf.parent = c
                    cf.description = description + installments_string
                    cf.installments = installments
                    cf.amount_planned = amount_planned
                    cf.date_due = date_due + increment
                    cf.save()
                    
            return HttpResponseRedirect('/')
    else:
        form = CashFlowForm()
    
    c = {'form': form}
    c.update({'user' : user,})
    c.update(csrf(request))
    return render_to_response('cashflow_edit.html', c)
    
@login_required(login_url='/login/')    
def category_edit(request):
    user = request.user
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save();
            return HttpResponseRedirect('/category')
    else:
        form = CategoryForm()
    
    c = {'form': form}
    c.update({'user' : user,})
    c.update(csrf(request))
    return render_to_response('category_edit.html', c)