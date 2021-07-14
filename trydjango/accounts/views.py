from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
# Create your views here.
def login_view(request):
    # Get the filled form, or the initial empty form
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request,username=username,password=password)
        # user = authenticate(request,username=username,password=password,is_reviewer=True)
        if user != None:
            login(request,user)
            return redirect("/") # Redirect to homepage
        else:
            context["message"] = "Sorry, could not authenticate user."
    return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    print("logout success")
    return redirect("/login") # redirect to login
