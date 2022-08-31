from django.urls import path

from . import views



app_name = 'article'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('inquiry/', views.InquiryView.as_view(), name='inquiry'),
    path('mypage/<username>/', views.MyPageView.as_view(), name='mypage'),
    path('account_setting/<username>/', views.AccountSettingView.as_view(), name='account_setting'),
    path('profile_setting/<username>/', views.ProfileSettingView.as_view(), name='profile_setting'),
    path('password_change/', views.MyPasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChengeDone.as_view(), name='password_change_done'),
]