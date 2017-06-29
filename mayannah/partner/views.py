from django.shortcuts import render
from django.views import generic
from .models import Person, Remittance
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, generic.ListView):
    model = Remittance

class RemittanceDetailView(LoginRequiredMixin, generic.DetailView):
    model = Remittance
