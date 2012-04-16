from django.shortcuts import render_to_response
from models import Category, CashFlow

def index(request):
    cash_flow = CashFlow.objects.all()
    return render_to_response('cash_flow.html',
        {'cash_flow' : cash_flow})
