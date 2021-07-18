from django.urls import path
from . import views


urlpatterns = [
    path('password_reset/', views.password_reset, name='password_reset'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
]
