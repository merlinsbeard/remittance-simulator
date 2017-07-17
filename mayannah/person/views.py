from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Person
from virtual_money.models import Transaction, TransactionHistory, Branch
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

        deposits = TransactionHistory.objects.filter(account=user,
                                                     type="DEPOSIT")
        withdrawals = TransactionHistory.objects.filter(account=user,
                                                        type="WITHDRAW")

        sum_deposits = sum([n.amount for n in deposits])
        sum_withdraws = sum([n.amount for n in withdrawals])

        context['deposits'] = deposits
        context['withdrawals'] = withdrawals
        context['moneys'] = sum_deposits - sum_withdraws

        return context


class ProfileTransactionList(LoginRequiredMixin, ListView):
    model = Transaction

    def get_queryset(self):
        """Only show users transactions."""
        return Transaction.objects.filter(
                Q(account=self.request.user) | Q(remitter=self.request.user))
