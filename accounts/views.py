from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm

class SignUp(CreateView):
    form_class = CustomUserCreationForm  # Use your custom form
    success_url = reverse_lazy('login')  # Redirect to login page after successful sign-up
    template_name = 'registration/signup.html'  # Your template for the signup page
