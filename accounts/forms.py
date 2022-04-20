from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'first_name', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('رمزها به درستی وارد نشده است')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you can ckang password with <a href=\"../password/\">this form</a>.')

    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'email', 'password', 'last_login')


class UserRegisterForm(forms.Form):
    phone_number = forms.CharField(label='شماره موبایل', max_length=11)
    first_name = forms.CharField(label='نام', max_length=80)
    last_name = forms.CharField(label='نام خانوادگی', max_length=80)
    password = forms.CharField(label='رمزعبور', widget=forms.PasswordInput)


class VerifyForm(forms.Form):
    code = forms.IntegerField()
