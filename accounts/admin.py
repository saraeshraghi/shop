from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Otpcode
from django.contrib.auth.models import Group
from .forms import UserCreationForm, UserChangForm


class UserAdmin(BaseUserAdmin):
    form = UserChangForm
    add_form = UserCreationForm

    list_display = ('phone_number', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin', 'is_active')

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'phone_number', 'password')}),
        ('permissions', {'fields': ('is_admin', 'is_active', 'last_login')})
    )
    add_fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'phone_number', 'password1', 'password2')}),

    )

    search_field = ('phone_number', 'last_name')
    ordering = ('last_name',)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Otpcode)