from django.shortcuts import render
from .models import Author
# View for when an author wants to create an account (from navbar)
def author_signup_view(request):
    context = {} # When we use navbar to get here, there is no context
    return render(request,"signup.html", context)

# View for when an author wants to login (from navbar)
def author_login_view(request):
    context = {}
    return render(request,'author_login.html',context)

# Upon creating an author account, should lead to author login page
def author_finish_signup(request):
    if request.method == "POST":
        form_info = request.POST
        Author.objects.create(name=form_info.get('name'), password=form_info.get('password'))
        print(form_info)
    context = {
        'message': 'Author account creation successful.'
    }
    return render(request,'author_login.html',context)

# Upon author login, should validate the login
def author_login_attempt(request):
    print(request.POST)
    context = {}
    return render(request,'author_login.html',context)
    