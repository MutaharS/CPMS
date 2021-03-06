"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from adminplus.sites import AdminSitePlus
admin.site = AdminSitePlus()
admin.sites.site = admin.site
admin.autodiscover()

from django.urls import path,include
from pages import views
from author.views import author_signup_view, author_profile, submit_paper_view
from reviewer.views import reviewer_signup_view, choose_review_view, review_form_view, assigned_papers_view, reviewer_profile
from accounts.views import login_view, logout_view, password_reset
from adminplus.sites import AdminSitePlus


from django.conf import settings


urlpatterns = [
    # Standard Pages
    path('', views.home_view, name='home'),
    path('login/', login_view, name='userlogin'),
    path('logout/', logout_view, name='userlogout'),
    path('admin/', admin.site.urls),

    # Author pages
    path('author_sign_up/', author_signup_view, name='authorsignup'),
    path('author_profile/', author_profile, name='authorprofile'),
    path('submit_paper/', submit_paper_view, name='submitpaper'),

    # Reviewer Pages
    path('reviewer_sign_up/', reviewer_signup_view, name='reviewersignup'),
    path('reviewer_profile/', reviewer_profile, name='reviewerprofile'),
    path('assigned_papers/', assigned_papers_view , name='assignedpapers'),
    path('choose_review_form/', choose_review_view , name='choosereviewform'),
    path('review_form/', review_form_view , name='reviewform'),

    # To be removed in production
    path('topic_reset/', views.reset_topic_view),

    # Accounts
    path('accounts/',include('accounts.urls')),
]
