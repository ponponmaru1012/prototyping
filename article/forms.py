from django import forms
from django.core.mail import EmailMessage
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

from accounts.models import CustomUser
from .models import Article, Comment, SubComment


class InquiryForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=30)
    email = forms.EmailField(label='Email Address')
    message = forms.CharField(label='Message', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['name'].widget.attrs['placeholder'] = 'Your Name'

        self.fields['email'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'

        self.fields['message'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['message'].widget.attrs['rows'] = '7'
        self.fields['message'].widget.attrs['placeholder'] = 'Message'

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ'
        message = '送信者名: {0}\nメールアドレス: {1}\nメッセージ: {2}'.format(name, email, message)

        from_email = 'info@prototyping-labo.com'

        to_list = [
            'info@prototyping-labo.com'
        ]

        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
        message.send()

class AccountSettingForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-lg'

class ProfileSettingForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('fb_link', 'ig_link', 'tw_link', 'icon', 'bg_image', 'profession', 'introduction',)

    def clean_fb_link(self):
        fb_link = self.cleaned_data['fb_link']
        if (fb_link is not None) and ('facebook' not in str(fb_link)):
            raise ValidationError('Please enter your Facebook link')
        return fb_link

    def clean_ig_link(self):
        ig_link = self.cleaned_data['ig_link']
        if (ig_link is not None) and ('instagram' not in str(ig_link)):
            raise ValidationError('Please enter your Instagram link')
        return ig_link

    def clean_tw_link(self):
        tw_link = self.cleaned_data['tw_link']
        if (tw_link is not None) and ('twitter' not in str(tw_link)):
            raise ValidationError('Please enter your Twitter link')
        return tw_link 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-lg'



class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-lg'

class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article 
        fields = ("thumbnail","title", "content",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-lg'

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = SubComment
        fields = ("content",)