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

from django.urls import path
from pages import views
from products.views import product_detail_view, product_create_view
from author.views import author_signup_view, author_finish_signup, author_login_view
from author.views import author_login_attempt
from reviewer.views import reviewer_signup_view, review_form_view
from accounts.views import login_view, logout_view
from adminplus.sites import AdminSitePlus

urlpatterns = [
    # Standard Pages
    path('', views.home_view, name='home'),
    path('login/', login_view, name='userlogin'),
    path('logout/', logout_view, name='userlogout'),
    path('admin/', admin.site.urls),

    # Author pages
    path('author_sign_up/', author_signup_view, name='authorsignup'),
    path('author_login/', author_finish_signup, name='authorcompletesignup'),
    path('author_login/', author_login_view, name='authorlogin'),
    path('author_login/', author_login_attempt, name='authorloginattempt'),

    # Reviewer Pages
    path('reviewer_sign_up/', reviewer_signup_view, name='reviewersignup'),
    path('review_form/', review_form_view , name='reviewform'),

    # To be removed in production
    path('topic_reset/', views.reset_topic_view),
    path('view_product/', product_detail_view, name='viewproduct'),
    path('create/', product_create_view),
]
