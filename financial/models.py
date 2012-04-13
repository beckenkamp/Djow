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
    due_date = models.DateTimeField()
    payed_date = models.DateTimeField(blank=True, null=True)
    insert_date = models.DateTimeField()

    def __unicode__(self):
        return self.description
