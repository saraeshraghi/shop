from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, VerifyForm
import random
from utils import send_sms
from .models import Otpcode, User
from django.contrib import messages


class register_view(View):
    form_class =UserRegisterForm

    def get(self, request):
        return render(request, 'accounts/register.html', {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_sms(phone=form.cleaned_data['phone_number'], code=random_code)
            Otpcode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_register_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'کد با موفقیت برای شما ارسال شد', 'success')
            return redirect('account:user_verify_code')
        return redirect('home:home')


class UserRegisterVerifyCodeView(View):
    form_class = VerifyForm

    def get(self, request):
        return render(request, 'accounts/verify.html', {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_session = request.session['user_register_info']
            code_instance = Otpcode.objects.get(phone_number=user_session['phone_number'])
            if cd['code'] == code_instance:
                User.objects.create_user(user_session['phone_number'], user_session['first_name'],
                                         user_session['last_name'], user_session['password'])
                code_instance.delete()
                messages.success(request, 'شما با موفقیت ثبت نام کردید', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'کد وارد شده صحیح نیست', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')
