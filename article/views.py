from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
import logging

from .forms import InquiryForm, AccountSettingForm, MyPasswordChangeForm, ProfileSettingForm
from accounts.models import CustomUser
# Create your views here.

logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name = 'index.html'

class InquiryView(generic.FormView):
    template_name = 'inquiry.html'
    form_class = InquiryForm
    success_url = reverse_lazy('article:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'You successfully sent message !')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

#マイページ関連
class MyPageView(LoginRequiredMixin, generic.DetailView):
    template_name = 'mypage.html'
    model = CustomUser
    slug_field = 'username' #モデルのフィールド名
    slug_url_kwarg = 'username' #urls.pyでのキーワード名

class ProfileSettingView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'profile_setting.html'
    model = CustomUser
    form_class = ProfileSettingForm
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_success_url(self):
        return reverse_lazy('article:mypage', kwargs={'username': self.object.username})
    
    def form_valid(self, form):
        messages.success(self.request, 'Successfully changed your profile')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to change your profile')
        return super().form_invalid(form)

#アカウント設定関係
class AccountSettingView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'account_setting.html'
    model = CustomUser
    form_class = AccountSettingForm
    slug_field = 'username' #モデルのフィールド名
    slug_url_kwarg = 'username' #urls.pyでのキーワード名

    def get_success_url(self):
        return reverse_lazy('article:mypage', kwargs={'username': self.object.username})
    
    def form_valid(self, form):
        messages.success(self.request, 'Successfully changed your account settings')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to change your account settings')
        return super().form_invalid(form)


class MyPasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('article:password_change_done')
    template_name = 'password_change.html'

    def form_valid(self, form):
        messages.success(self.request, 'You successfully changed password !')
        return super().form_valid(form)

class PasswordChengeDone(LoginRequiredMixin, PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'password_change_done.html'