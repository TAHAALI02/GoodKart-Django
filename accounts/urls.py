from django.urls import path
from . import views as v



urlpatterns = [
    path('register/',v.register,name='register'),
    path('login/',v.login,name='login'),
    path('logout/',v.logout,name='logout'),
    path('activate/<uidb64>/<token>/', v.activate, name='activate'),
    path('', v.dashboard, name='dashboard'),
    path('forgotPassword/', v.forgotPassword, name='forgotPassword'),
    path('reset/<uidb64>/<token>/', v.reset, name='password_reset_confirm'),
    path('reset_password',v.reset_password, name='reset_password'),
]