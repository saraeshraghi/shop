from django.urls import path
from . import views
app_name = 'account'
urlpatterns = [
    path('register/',  views.register_view.as_view(), name='register'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='user_verify_code')
    ]