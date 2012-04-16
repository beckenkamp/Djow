from django.shortcuts import render_to_response
from models import Category, CashFlow
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def index(request):
    cash_flow = CashFlow.objects.all()
    user = request.user
    return render_to_response('cash_flow.html',
        {'cash_flow' : cash_flow,
         'user' : user })