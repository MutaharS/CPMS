from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from author.models import Author
from reviewer.models import Reviewer

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
# from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, timezone, tzinfo

from django.utils import timezone
from django.core.mail import EmailMessage

from functools import wraps
#---------------------------------------------------------------

# from __future__ import unicode_literals
# from collections import OrderedDict
# from django.contrib.auth import authenticate, get_user_model
# from django.contrib.auth.hashers import (
#     UNUSABLE_PASSWORD_PREFIX, identify_hasher,
# )
# from django.contrib.auth.models import User
# from django.core.mail import EmailMultiAlternatives
# from django.forms.utils import flatatt
# from django.template import loader
# from django.utils.html import format_html, format_html_join
# from django.utils.safestring import mark_safe
# from django.utils.text import capfirst
# from django.utils.translation import ugettext, ugettext_lazy as _
#---------------------------------------------------------------

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
            print("login success")
            login(request,user)
            print(request.user)
            return redirect("/") # Redirect to homepage
        else:
            context["message"] = "Sorry, could not authenticate user."
    return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    print("logout success")
    return redirect("/login") # redirect to login


# @csrf_protect
@csrf_exempt
def password_reset(request):
    if request.method == 'POST':
        # email = request.POST['email']
        email = request.POST.get('email')
        # if Author.objects.filter(Email__exact).exists():
        if Author.objects.filter(Email__exact=email):
            user = Author.objects.get(Email__exact=email)
            user.password = user.Password
            user.last_login = timezone.now()

            # Password Reset logic
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user'  : user,
                'domain': current_site,
                'uid'   : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset email has been sent to email address on file!')
            return redirect('userlogin')
        elif Reviewer.objects.filter(Email__exact=email):
            user = Reviewer.objects.get(Email__exact=email)
            user.password = user.Password
            user.last_login = timezone.now()

            # Password Reset logic
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user'  : user,
                'domain': current_site,
                'uid'   : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset email has been sent to email address on file!')
            return redirect('userlogin')
        else:
            messages.error(request, 'Author/Reviewer does not exist')
            return redirect('password_reset')
    return render(request, 'accounts/password_reset.html')


def resetpassword_validate(request):
    return HttpResponse('ok')
