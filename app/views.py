from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from .models import Plant
from django.contrib import messages
from django.views.generic import FormView
from .forms import RegisterForm
from django.contrib.auth.models import User


class LoginPageView(LoginView):
    template_name = 'app/login.html'
    redirect_authenticated_user = True

class RegisterView(FormView):
    template_name = 'app/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = User.objects.create_user(username=username, email=email, password=password)

        messages.success(self.request, 'Registration successful! Please log in.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error in the form. Please try again.')
        return super().form_invalid(form)

class LogoutPageView(LogoutView):
    next_page = reverse_lazy('login')

class HomePageView(TemplateView):
    template_name = 'app/home.html'

class PlantListView(ListView):
    model = Plant
    template_name = 'app/plant_list.html'
    context_object_name = 'plants'

class PlantCreateView(CreateView):
    model = Plant
    template_name = 'app/create_plant.html'
    fields = ['name', 'type', 'care_instructions', 'image']
    success_url = reverse_lazy('plant_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assign the logged-in user
        return super().form_valid(form)

class PlantDetailView(DetailView):
    model = Plant
    template_name = 'app/plant_detail.html'
    context_object_name = 'plant'

class PlantUpdateView(UpdateView):
    model = Plant
    fields = ['name', 'type', 'care_instructions', 'image']
    context_object_name = 'plant'
    template_name = 'app/update_plant.html'

class PlantDeleteView(DeleteView):
    model = Plant
    template_name = 'app/delete_plant.html'
    success_url = reverse_lazy('plant_list')



