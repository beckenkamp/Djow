from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import Category, CashFlow, CategoryForm, CashFlowForm
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory

@login_required(login_url='/login/')
def index(request):
    cash_flow = CashFlow.objects.all()
    user = request.user
    return render_to_response('cashflow.html', {
        'cash_flow' : cash_flow,
        'user' : user,
    })

@login_required(login_url='/login/')    
def cashflow_edit(request):
    user = request.user
    
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save();
            return HttpResponseRedirect('/')
    else:
        form = CashFlowForm()
    
    c = {'form': form}
    c.update({'user' : user,})
    c.update(csrf(request))
    return render_to_response('cashflow_edit.html', c)