from django.urls import path

from . import views



app_name = 'article'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('inquiry/', views.InquiryView.as_view(), name='inquiry'),
    path('mypage/<username>/', views.MyPageView.as_view(), name='mypage'),
    path('user/<username>', views.UserPageView.as_view(), name='userpage'),
    path('article_detail/<int:pk>', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article_create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('article_update/<int:pk>', views.ArticleUpdateView.as_view() , name='article_update'),
    path('article_delete/<int:pk>', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('like_for_article/', views.like_for_article, name='like_for_article'),
    path('<int:pk>/comment', views.CommentCreateView.as_view(), name='comment_create'),
    path('<int:pk>/comment/update', views.CommentUpdateView.as_view(), name='comment_update'),
    path('<int:pk>/comment/delete', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('reply/create/<int:pk>', views.ReplyCreateView.as_view(), name='reply_create'),
    path('<int:pk>/reply/update', views.ReplyUpdateView.as_view(), name='reply_update'),
    path('<int:pk>/reply/delete', views.ReplyDeleteView.as_view(), name='reply_delete'),
    path('account_setting/<username>/', views.AccountSettingView.as_view(), name='account_setting'),
    path('profile_setting/<username>/', views.ProfileSettingView.as_view(), name='profile_setting'),
    path('password_change/', views.MyPasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChengeDone.as_view(), name='password_change_done'),
]