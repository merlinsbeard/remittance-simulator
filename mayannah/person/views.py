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
                Q(receiver=user) | Q(sender=user))

        # Filter and sort all transactions by
        # Deposits, Send, and Withdrawals
        # of currently logged user
        deposits = Transaction.deposits.receive(self.request.user)
        send = Transaction.deposits.send(self.request.user)
        withdrawals = Transaction.withdraws.receive(self.request.user)

        # Get the Paid Sum of
        # Deposits, Sent Money, and Withdrawals
        deposits_paid_sum = sum(
                [t.amount for t in deposits.filter(status="PAID")])
        send_paid_sum = sum(
                [t.amount for t in send.filter(status="PAID")])
        withdrawals_paid_sum = sum(
                [t.amount for t in withdrawals.filter(status="PAID")])

        money = deposits_paid_sum - (send_paid_sum + withdrawals_paid_sum)

        context["money"] = money
        context["deposits"] = deposits.order_by('-date_created')
        context["withdrawals"] = withdrawals.order_by('-date_created')
        context["transactions"] = transactions.order_by('-date_created')
        context["send"] = send.order_by('-date_created')

        return context


class ProfileTransactionList(LoginRequiredMixin, ListView):
    model = Transaction

    def get_queryset(self):
        """Only show users transactions."""
        return Transaction.objects.filter(sender=self.request.user)
