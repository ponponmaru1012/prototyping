from django import forms
from django.core.mail import EmailMessage


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

        from_email = 'devteam@prototypinglabo.com'

        to_list = [
            'prototypinglabo@gmail.com'
        ]

        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
        message.send()

