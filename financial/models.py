from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db.models import Q
from datetime import *

class Category(models.Model):
    user = models.ForeignKey(User)
    parent = models.ForeignKey('self', blank=True, null=True)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.description


class CashFlow(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    parent = models.ForeignKey('self', blank=True, null=True)
    description = models.CharField(max_length=200)
    amount_planned = models.FloatField()
    amount_payed = models.FloatField(blank=True, null=True)
    date_due = models.DateField()
    date_payed = models.DateField(blank=True, null=True)
    date_inserted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.description
    
    def get_amount_planned_sum_by_month(self, month=datetime.now().month, year=datetime.now().year):
        return CashFlow.objects.filter(date_due__month = month, date_due__year = year).aggregate(models.Sum('amount_planned'))
    
    def get_amount_payed_sum_by_month(self, month=datetime.now().month, year=datetime.now().year):
        return CashFlow.objects.filter(date_payed__month = month, date_due__year = year).aggregate(models.Sum('amount_payed'))
    

class CategoryForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    
    def __init__(self, user, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.filter(user_id=user)

    
    class Meta:
        model = Category


class CashFlowForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    installments = forms.IntegerField(required=False)
    
    def __init__(self, user, *args, **kwargs):
        super(CashFlowForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user_id=user)
        self.fields['installments'].widget.attrs['data-inputmask'] = "99"
    
    class Meta:
        model = CashFlow


class DjowDateHandler():
    @staticmethod
    def month_year_iterator(month_now=datetime.now()):
        month = month_now.month
        year = month_now.year
        
        if month == 12:
            month_plus = 1
            month_minus = 11
            year_plus = year+1
            year_minus = year
        elif month == 1:
            month_plus = 2
            month_minus = 12
            year_plus = year
            year_minus = year-1
        else:
            month_plus = month+1
            month_minus = month-1
            year_plus = year
            year_minus = year
        
        return {'month_now' : month_now,
                'month_next' : datetime(year_plus, month_plus, 1),
                'month_last' : datetime(year_minus, month_minus, 1),
               }
    
    @staticmethod
    def month_increment(date):
        month_days = {1: 31,
                      2: 28,
                      3: 31,
                      4: 30,
                      5: 31,
                      6: 30,
                      7: 31,
                      8: 31,
                      9: 30,
                      10: 31,
                      11: 30,
                      12: 31,
                      }
    
        if date.month == 12:
            month = 1
        else:
            month = date.month+1
        
        return date + timedelta(days=month_days[month])
                 
        
