from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.description


class CashFlow(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    description = models.CharField(max_length=200)
    installments = models.IntegerField(blank=True, null=True)
    amount_planned = models.FloatField()
    amount_payed = models.FloatField(blank=True, null=True)
    date_due = models.DateTimeField()
    date_payed = models.DateTimeField(blank=True, null=True)
    date_inserted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.description
