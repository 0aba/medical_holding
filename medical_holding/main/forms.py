from main.models import (User, Organization, BranchOrganization, EmployeeOrganization, ServiceOrganization,
                         AppointmentDoctor, RatingService, CommentAboutService)
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, MinLengthValidator
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from datetime import timedelta
from django import forms


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    username = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='Допускаются только латиница, цифры и нижнее подчеркивание'
            ),
        ],
        min_length=3,
        max_length=150,
        required=True,
        label='Логин'
    )


class ChangeUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', 'background', 'about', 'first_name',
                  'last_name', 'gender', 'birthday', 'phone',)


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name', 'logo', 'about', 'site', 'inn',)


class BranchOrganizationForm(forms.ModelForm):
    class Meta:
        model = BranchOrganization
        fields = ('street', 'house', 'phone',)


class EmployeeOrganizationForm(forms.ModelForm):
    class Meta:
        model = EmployeeOrganization
        fields = ('photo', 'number_in_med_registry', 'experience_month',
                  'first_name', 'last_name', 'middle_name', 'qualification', 'gender',)


class ServiceOrganizationForm(forms.ModelForm):
    class Meta:
        model = ServiceOrganization
        fields = ('name_service', 'price', 'branch',
                  'appointment_start_time', 'appointment_end_time',
                  'appointment_interval', 'amount_days_for_registration',
                  'employee', 'additional_information',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'owner_organization_fk'):
            self.fields['employee'].queryset = EmployeeOrganization.objects.filter(
                organization=user.owner_organization_fk
            )

    price = forms.DecimalField(widget=forms.NumberInput(attrs={'min': '0', 'step': '0.01'}))
    appointment_start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    appointment_end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    appointment_interval = forms.IntegerField(
        validators=[
            MinValueValidator(5, message='Минимальный интервал 5 минут')
        ],
        widget=forms.NumberInput(attrs={'min': '5'})
    )

    amount_days_for_registration = forms.IntegerField(
        validators=[
            MinValueValidator(1, message='Минимум дней на оформление вперед это 1 день'),
            MaxValueValidator(14, message='Максимум на перед можно оформить только на 2 недели вперед')
        ],
        widget=forms.NumberInput(attrs={'min': '1', 'max': '14'})
    )

    employee = forms.ModelMultipleChoiceField(
        queryset=EmployeeOrganization.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


class EmployeeDateForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=EmployeeOrganization.objects.none(), label='Сотрудник')
    appointment_date = forms.DateField(label='Дата записи', widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        service = kwargs.pop('service')
        super().__init__(*args, **kwargs)

        self.fields['employee'].queryset = service.employee.all()

        now_date = timezone.now().date()
        max_date = now_date + timedelta(days=service.amount_days_for_registration)
        self.fields['appointment_date'].widget.attrs.update({'min': now_date, 'max': max_date})


class AppointmentTimeForm(forms.Form):
    appointment_time = forms.ChoiceField(label='Время записи')

    def __init__(self, *args, **kwargs):
        employee = kwargs.pop('employee')
        appointment_date = kwargs.pop('appointment_date')
        service = kwargs.pop('service')
        super().__init__(*args, **kwargs)

        start_time = service.appointment_start_time
        end_time = service.appointment_end_time
        interval = service.appointment_interval
        current_time = timezone.now().time()

        if appointment_date == timezone.now().date() and current_time > start_time:
            start_time = current_time

        times = []

        current_datetime = timezone.datetime.combine(appointment_date, start_time)

        while current_datetime.time() <= end_time:
            if not AppointmentDoctor.objects.filter(
                    who_provides=employee,
                    date_time_appointment=current_datetime
            ).exists():
                times.append((current_datetime.time(), current_datetime.strftime("%H:%M")))
            current_datetime += timedelta(minutes=interval)

        self.fields['appointment_time'].choices = times


class RatingServiceForm(forms.ModelForm):
    class Meta:
        model = RatingService
        fields = ('grade',)

    grade = forms.DecimalField(widget=forms.NumberInput(attrs={'min': '0', 'max': '5', 'step': '0.1'}), label='Оценка')


class CommentAboutServiceForm(forms.ModelForm):
    class Meta:
        model = CommentAboutService
        fields = ('text',)

    text = forms.CharField(validators=[
        MinLengthValidator(1)
    ], max_length=1024, label='Текст комментария')
