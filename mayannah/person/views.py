from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Person
from virtual_money.models import Transaction
from django.db.models import Q


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Person

    def get_object(self):
        user = self.request.user
        try:
            person = Person.objects.get(user=user)
        except Person.DoesNotExist:
            person = Person(user=user)
            person.save()
        return person

    def get_context_data(self, **kwargs):
        """Show total amount of money"""
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        user = self.request.user


        transactions = Transaction.objects.filter(
                Q(account=user) | Q(remitter=user))

        accounts = transactions.filter(account=user)
        # cash to online
        deposits = accounts.filter(type="DEPOSIT")
        # online to cash
        withdrawals = transactions.filter(type="WITHDRAW")
        # online to online
        transfers = accounts.filter(type="TRANSFER")

        context['deposits'] = deposits
        context['withdrawals'] = withdrawals
        context['transfers'] = transfers
        context['received'] = accounts

        return context


class ProfileTransactionList(LoginRequiredMixin, ListView):
    model = Transaction

    def get_queryset(self):
        """Only show users transactions."""
        return Transaction.objects.filter(
                Q(account=self.request.user) | Q(remitter=self.request.user))
