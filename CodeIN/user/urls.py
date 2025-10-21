from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user'

urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login_form.html'), name='login'),
    path('mypage/', views.mypage_view, name='mypage'),
]