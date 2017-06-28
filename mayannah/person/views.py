from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Person


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
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context["hola"] = "HOLA"
        return context
