from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db.models import Q

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
    

class CategoryForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.filter(user_id=user)

    
    class Meta:
        model = Category


class CashFlowForm(forms.ModelForm):
    installments = forms.IntegerField(required=False)
    
    def __init__(self, user, *args, **kwargs):
        super(CashFlowForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user_id=user)

    
    class Meta:
        model = CashFlow
