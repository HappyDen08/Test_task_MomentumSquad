from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

class CustomLoginView(LoginView):
    template_name = "login.html"
    next_page = "/chat/"

class CustomLogoutView(LogoutView):
    next_page = "/login/"


@login_required
def chat_view(request):
    return render(request, "chat.html")


