from main.forms import (ChangeUserProfileForm, MyUserCreationForm, OrganizationForm, BranchOrganizationForm,
                        EmployeeOrganizationForm, ServiceOrganizationForm, EmployeeDateForm, AppointmentTimeForm,
                        RatingServiceForm, CommentAboutServiceForm)
from main.models import (User, Organization, BranchOrganization, EmployeeOrganization, ServiceOrganization,
                         AppointmentDoctor, RatingService, CommentAboutService)
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.views import LoginView, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session
from django.utils.translation import gettext_lazy
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q, Avg
from django.utils import timezone
from django.views import View
from datetime import datetime


class Home(View):
    template_name = 'main/home.html'

    @staticmethod
    def get_context_data():
        context: dict = {
            'title': 'Домашняя страница',
        }

        return context

    def get(self, request):
        return render(request, self.template_name, context=Home.get_context_data())


class ProfileUserView(DetailView):
    model = User
    template_name = 'main/profile_user.html'
    context_object_name = 'user_profile'
    slug_url_kwarg = 'username'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        paginator = None

        if self.request.user == profile_user:
            appointments = AppointmentDoctor.objects.filter(who_purchased=self.request.user)
            page = self.request.GET.get('page')
            paginator = Paginator(appointments, 5).get_page(page if page else 1)

        context = {
            'title': f'Профиль @{self.kwargs.get('username')}',
            'page_obj': paginator,
        }

        return {**base_context, **context}

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()

        if isinstance(profile, HttpResponseRedirect):
            return profile

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            object_user = User.objects.get(username=self.kwargs.get('username'))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Пользователь не найден')
            return redirect('home', permanent=False)

        return object_user


class SignupView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'main/signup.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context: dict = {
            'title': 'Регистрация',
        }

        return {**base_context, **context}

    def form_valid(self, form):
        new_user = form.save()
        new_user.set_password(form.cleaned_data['password1'])
        new_user.save()
        login(request=self.request, user=new_user)
        messages.success(self.request, 'Успешная регистрация')

        return redirect('home', permanent=False)


class MyLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context: dict = {
            'title': 'Вход',
        }

        return {**base_context, **context}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Вы уже авторизованы')
            return redirect('home', permanent=False)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()

        if user.banned:
            form.add_error(None, gettext_lazy('Ваш аккаунт заблокирован'))
            return self.form_invalid(form)

        login(request=self.request, user=user)
        messages.success(self.request, 'Успешный  вход')
        return super().form_valid(form)


class ChangeProfileUserView(UpdateView):
    model = User
    form_class = ChangeUserProfileForm
    template_name = 'main/change_profile_user.html'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context = {
            'title': 'Изменить свой профиль',
        }

        return {**base_context, **context}


    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.warning(self.request, 'Чтобы изменить профиль необходимо авторизоваться')
            return redirect('log_in', permanent=False)

        user_profile = self.get_object()

        if isinstance(user_profile, HttpResponseRedirect):
            return user_profile

        if user_profile != self.request.user:
            messages.error(self.request, 'У вас нет доступа к этому профилю')
            return redirect('home', permanent=False)

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            user_profile = User.objects.get(username=self.kwargs.get('username'))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Пользователь не найден')
            return redirect('home', permanent=False)

        return user_profile

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Успешный  изменение профиля')

        return redirect('profile_user', self.kwargs.get('username'), permanent=False)


class OrganizationRouter(View):
    def get(self, request):
        if self.request.user.is_anonymous:
            messages.warning(self.request, 'Авторизуйтесь, чтобы получить доступ к функциям организации')
            return redirect('log_in', permanent=False)

        try:
            organization_user = Organization.objects.values('id').get(owner=request.user)
        except ObjectDoesNotExist:
            messages.info(request, 'У вас нет организации создайте ее')
            return redirect('new_organization', permanent=False)

        return redirect('profile_organization', organization_user.get('id'), permanent=False)


class RegisterOrganizationView(CreateView):
    form_class = OrganizationForm
    template_name = 'main/register_organization.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context = {
            'title': 'Регистрация организации',
        }

        return {**base_context, **context}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.warning(self.request, 'Авторизуйтесь, чтобы создать организацию')
            return redirect('log_in', permanent=False)

        try:
            Organization.objects.get(owner=self.request.user)
        except ObjectDoesNotExist:
            return super().dispatch(request, *args, **kwargs)

        messages.error(self.request, 'У вас уже есть организация')
        return redirect('home', permanent=False)


    def form_valid(self, form):
        new_organization = form.save(commit=False)
        new_organization.owner = self.request.user

        try:
            new_organization.save()
        except IntegrityError:
            messages.error(self.request, 'У вас может быть только одна организация')
            return redirect('home', permanent=False)

        messages.success(self.request, 'Успешная регистрация организации')
        return redirect('profile_organization', new_organization.id, permanent=False)


class OrganizationProfileView(DetailView):
    model = Organization
    template_name = 'main/organization_profile.html'
    context_object_name = 'organization_profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context: dict = {
            'title': 'Профиль организации',
        }

        return {**base_context, **context}

    def dispatch(self, request, *args, **kwargs):
        organization = self.get_object()

        if isinstance(organization, HttpResponseRedirect):
            return organization

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            object_organization = (Organization.objects.select_related('owner')
                                   .values('pk', 'name', 'logo', 'about', 'site', 'inn', 'owner__banned', 'owner__username',)
                                   .get(pk=self.kwargs.get('pk')))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Организация не найдена')
            return redirect('home', permanent=False)

        return object_organization


class ChangeProfileOrganizationView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'main/change_organization_profile.html'

    def get_context_data(self, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context = {
            'title': 'Изменить профиль организации',
        }

        return {**base_context, **context}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.warning(self.request, 'Авторизуйтесь для изменения профиля')
            return redirect('log_in', permanent=False)

        organization = self.get_object()

        if isinstance(organization, HttpResponseRedirect):
            return organization

        if organization.owner != self.request.user:
            messages.error(self.request, 'У вас нет прав на то, чтобы изменить профиль чужой организации')
            return redirect('home', permanent=False)

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            organization = Organization.objects.get(pk=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Организация не найдена')
            return redirect('home', permanent=False)

        return organization

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Успешное изменение данных организации')
        return redirect('profile_organization', self.kwargs.get('pk'), permanent=False)


class OrganizationBranchListView(ListView):
    paginate_by = 5
    model = BranchOrganization
    template_name = 'main/organization_branch_list.html'
    context_object_name = 'organization_branch_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context = {
            'title': 'Филиалы организации',
            'pk_organization': self.kwargs.get('pk'),
        }

        return {**base_context, **context}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.warning(self.request, 'Авторизуйтесь, чтобы посмотреть филиалы своей организации')
            return redirect('log_in', permanent=False)

        try:
            organization = (Organization.objects.select_related('owner_organization_fk')
                            .values('owner__username').get(pk=self.kwargs.get('pk')))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Организация не найдена')
            return redirect('home', permanent=False)

        if organization.get('owner__username') != self.request.user.username:
            messages.error(self.request, 'У вас нет доступа к данным об филиалов чужой организации')
            return redirect('home', permanent=False)

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = (BranchOrganization.non_deleted
                    .select_related('organization_branch_fk')
                    .values('pk', 'street', 'house', 'phone')
                    .filter(organization__owner=self.request.user))
        return queryset


class CreateBranchOrganizationView(CreateView):
    form_class = BranchOrganizationForm
    template_name = 'main/form_branch_organization.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context: dict = {
            'title': 'Новый филиал',
            'title_form': 'Создание нового филиала',
        }

        return {**base_context, **context}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.warning(self.request, 'Авторизуйтесь, чтобы создать филиал в своей организации')
            return redirect('log_in', permanent=False)

        try:
            organization = Organization.objects.get(pk=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Такой организации не существует')
            return redirect('home', permanent=False)

        if organization.owner != self.request.user:
            messages.error(self.request, 'У вас нет доступа к созданию филиалов в чужой организации')
            return redirect('home', permanent=False)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            organization = Organization.objects.get(pk=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Не найдена организация')
            return redirect('home', permanent=False)

        new_baruch_organization = form.save(commit=False)
        new_baruch_organization.organization = organization

        new_baruch_organization.save()

        messages.success(self.request, 'Успешно добавлен новый филиал')
        return redirect('organization_branch_list', organization.id, permanent=False)


class UpdateBranchOrganizationView(UpdateView):
    model = BranchOrganization
    form_class = BranchOrganizationForm
    template_name = 'main/form_branch_organization.html'

    def get_context_data(self, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context = {
            'title': 'Изменить филиал организации',
            'title_form': 'Изменить филиал',
        }

        return {**base_context, **context}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.warning(self.request, 'Авторизуйтесь, чтобы изменить данные об филиале в своей организации')
            return redirect('log_in', permanent=False)

        branch_organization = self.get_object()

        if isinstance(branch_organization, HttpResponseRedirect):
            return branch_organization

        if branch_organization.organization.owner != self.request.user:
            messages.error(self.request, 'У вас нет доступа к изменению данных об филиалах чужой организации')
            return redirect('home', permanent=False)

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            branch_organization = BranchOrganization.objects.get(Q(pk=self.kwargs.get('pk_branch')) &
                                                                 Q(organization=self.kwargs.get('pk')))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Филиал организации не найдена')
            return redirect('home', permanent=False)

        if branch_organization.deleted:
            messages.error(self.request, 'Филиал был удален')
            return redirect('home', permanent=False)

        return branch_organization

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Успешное изменение данных об филиале')
        return redirect('organization_branch_list', self.kwargs.get('pk'), permanent=False)


def delete_organization_branch(request, pk, pk_branch):
    if request.user.is_anonymous:
        messages.warning(request, 'Авторизуйтесь, чтобы удалить филиал своей организации')
        return redirect('log_in', permanent=False)

    try:
        branch_organization = BranchOrganization.objects.get(Q(pk=pk_branch) & Q(organization=pk))
    except ObjectDoesNotExist:
        messages.error(request, 'Филиал организации не найдена')
        return redirect('home', permanent=False)

    if branch_organization.organization.owner != request.user:
        messages.error(request, 'У вас нет доступа к удалению филиалах чужой организации')
        return redirect('home', permanent=False)

    if branch_organization.deleted:
        messages.error(request, 'Филиал уже удален')
        return redirect('home', permanent=True)

    branch_organization.deleted = True
    branch_organization.save()

    messages.success(request, 'Филиал был удален')
    return redirect('organization_branch_list', pk, permanent=True)


class OrganizationEmployeeListView(ListView):
    paginate_by = 5
    model = EmployeeOrganization
    template_name = 'main/organization_employee_list.html'
    context_object_name = 'organization_employee_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context = {
            'title': 'Сотрудники организации',
            'pk_organization': self.kwargs.get('pk'),
        }

        return {**base_context, **context}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.warning(self.request, 'Авторизуйтесь, чтобы получить данные об сотрудниках своей организации')
            return redirect('log_in', permanent=False)

        try:
            organization = (Organization.objects.select_related('owner_organization_fk')
                            .values('owner__username').get(pk=self.kwargs.get('pk')))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Организация не найдена')
            return redirect('home', permanent=False)

        if organization.get('owner__username') != self.request.user.username:
            messages.error(self.request, 'У вас нет доступа данным об сотрудниках чужой организации')
            return redirect('home', permanent=False)

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = (EmployeeOrganization.non_deleted.select_related('organization_employee_fk')
                    .values('pk', 'photo', 'number_in_med_registry',
                            'experience_month', 'first_name', 'last_name',
                            'middle_name', 'qualification', 'gender')
                    .filter(organization__owner=self.request.user))
        return queryset


class CreateEmployeeOrganizationView(CreateView):
    form_class = EmployeeOrganizationForm
    template_name = 'main/form_employee_organization.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context: dict = {
            'title': 'Создание сотрудника',
            'title_form': 'Создание нового сотрудника',
        }

        return {**base_context, **context}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.warning(self.request, 'Авторизуйтесь, чтобы создать нового сотрудника')
            return redirect('log_in', permanent=False)

        try:
            organization = Organization.objects.get(pk=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Организация не найдена')
            return redirect('home', permanent=False)

        if organization.owner != self.request.user:
            messages.error(self.request, 'У вас нет доступа к созданию сотрудников в чужой организации')
            return redirect('home', permanent=False)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            organization = Organization.objects.get(pk=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Организация не найдена')
            return redirect('home', permanent=False)

        new_employee_organization = form.save(commit=False)
        new_employee_organization.organization = organization

        new_employee_organization.save()

        messages.success(self.request, 'Успешно добавлен новый сотрудник')
        return redirect('organization_employee_list', organization.id, permanent=False)


class UpdateEmployeeOrganizationView(UpdateView):
    model = EmployeeOrganization
    form_class = EmployeeOrganizationForm
    template_name = 'main/form_employee_organization.html'

    def get_context_data(self, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context = {
            'title': 'Изменить филиал организации',
            'title_form': 'Изменить филиал',
        }

        return {**base_context, **context}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.warning(self.request, 'Авторизуйтесь, чтобы обновить данные об сотрудниках своей организации')
            return redirect('log_in', permanent=False)

        try:
            organization = Organization.objects.get(pk=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Сотрудник организации не найдена')
            return redirect('home', permanent=False)

        if organization.owner != self.request.user:
            messages.error(self.request, 'У вас нет доступа к обновлению данных сотрудников чужой организации')
            return redirect('home', permanent=False)

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            employee_organization = EmployeeOrganization.objects.get(Q(pk=self.kwargs.get('pk_employee')) &
                                                                     Q(organization=self.kwargs.get('pk')))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Сотрудник организации не найден')
            return redirect('home', permanent=False)

        if employee_organization.deleted:
            messages.error(self.request, 'Сотрудник не существует')
            return redirect('home', permanent=False)

        return employee_organization

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Успешное изменение данных об сотруднике')
        return redirect('organization_employee_list', self.kwargs.get('pk'), permanent=False)


def delete_organization_employee(request, pk, pk_employee):
    if request.user.is_anonymous:
        messages.warning(request, 'Авторизуйтесь, чтобы удалить сотрудника организации')
        return redirect('log_in', permanent=False)

    try:
        employee_organization = (EmployeeOrganization.objects
                               .get(Q(pk=pk_employee) & Q(organization=pk)))
    except ObjectDoesNotExist:
        messages.error(request, 'Сотрудник организации не найден')
        return redirect('home', permanent=False)

    if employee_organization.organization.owner != request.user:
        messages.error(request, 'У вас нет доступа к удалению сотрудников чужой организации')
        return redirect('home', permanent=False)

    if employee_organization.deleted:
        messages.error(request, 'Сотрудник был удален ранее')
        return redirect('home', permanent=True)

    employee_organization.deleted = True
    employee_organization.save()
    
    messages.success(request, 'Сотрудник был удален')
    return redirect('organization_employee_list', pk, permanent=True)


class ServicesListView(ListView):
    paginate_by = 5
    model = ServiceOrganization
    template_name = 'main/service_list.html'
    context_object_name = 'service_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context = {
            'title': 'Услуги',
        }

        return {**base_context, **context}

    def get_queryset(self):
        queryset = ServiceOrganization.non_deleted.filter()

        service_name = self.request.GET.get('service_name')
        organization_name = self.request.GET.get('organization_name')
        doctor_name = self.request.GET.get('doctor_name')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        qualification = self.request.GET.get('qualification')
        appointment_start_time = self.request.GET.get('appointment_start_time')
        appointment_end_time = self.request.GET.get('appointment_end_time')

        if service_name:
            queryset = queryset.filter(name_service__icontains=service_name)

        if organization_name:
            queryset = queryset.filter(branch__organization__name__icontains=organization_name)

        if doctor_name:
            queryset = (queryset.filter(employee__first_name__icontains=doctor_name) |
                       queryset.filter(employee__last_name__icontains=doctor_name) |
                       queryset.filter(employee__middle_name__icontains=doctor_name))

        if price_min:
            queryset = queryset.filter(price__gte=price_min)

        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        if qualification:
            queryset = queryset.filter(employee__qualification__icontains=qualification)

        if appointment_start_time:
            queryset = queryset.filter(appointment_start_time__gte=appointment_start_time)

        if appointment_end_time:
            queryset = queryset.filter(appointment_end_time__lte=appointment_end_time)

        return queryset


class CreateServicesView(CreateView):
    form_class = ServiceOrganizationForm
    template_name = 'main/form_service_organization.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context: dict = {
            'title': 'Новая услуга',
            'title_form': 'Создание новой услуги',
        }

        return {**base_context, **context}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.warning(self.request, 'Авторизуйтесь, чтобы создать новую услугу')
            return redirect('log_in', permanent=False)

        try:
            Organization.objects.get(owner=self.request.user)
        except ObjectDoesNotExist:
            messages.error(self.request, 'У вас нет организации, вы не можете создавать услуги')
            return redirect('home', permanent=False)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()

        messages.success(self.request, 'Успешно добавлена новая услуга')
        return redirect('services_list', permanent=False)


class ServicesView(View):
    model = ServiceOrganization
    template_name = 'main/services_view.html'
    context_object_name = 'services_view'
    pk_url_kwarg = 'pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        user_rating = self._get_user_rating()
        service = self.get_object()

        if isinstance(service, HttpResponseRedirect):
            return service

        comments = CommentAboutService.non_deleted.filter(service=service)
        page = self.request.GET.get('page')
        context: dict = {
            'title': 'Услуга',
            self.context_object_name: service,
            'employee_date_form': EmployeeDateForm(service=service),
            'rating_service_form': RatingServiceForm(initial={'grade': user_rating.grade if user_rating else None}),
            'comment_about_service_form': CommentAboutServiceForm(),
            'common_rating': self._get_common_rating(),
            'user_rating': user_rating,
            'page_obj': Paginator(comments, 5).get_page(page if page else 1),
        }

        return context

    def _get_user_rating(self):
        if self.request.user.is_anonymous:
            return None

        try:
            rating_service = RatingService.objects.get(rating_service=self.get_object(), user_grade=self.request.user)
        except ObjectDoesNotExist:
            return None

        return rating_service

    def _get_common_rating(self):
        return RatingService.objects.filter(rating_service=self.get_object()).aggregate(Avg('grade'))['grade__avg']


    def dispatch(self, request, *args, **kwargs):
        try:
            service = ServiceOrganization.objects.get(pk=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Услуга не найдена')
            return redirect('home', permanent=False)

        if service.deleted:
            messages.error(self.request, 'Услуга была удалена')
            return redirect('home', permanent=False)

        if service.branch.organization.owner.banned:
            messages.error(self.request, 'Услуги заблокированного пользователя автоматически отключаются')
            return redirect('home', permanent=False)

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            object_service = (ServiceOrganization.non_deleted.get(pk=self.kwargs.get('pk')))
        except IntegrityError:
            messages.error(self.request, 'Услуга не найдена')
            return redirect('home', permanent=False)

        return object_service

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        context_data = self.get_context_data()
        service = self.get_object()

        if isinstance(service, HttpResponseRedirect):
            return service

        employee_date_form = EmployeeDateForm(request.POST, service=service)
        appointment_time_form = None

        if request.POST.get('formId') == 'employee_date_form' and employee_date_form.is_valid():
            employee = employee_date_form.cleaned_data['employee']
            appointment_date = employee_date_form.cleaned_data['appointment_date']

            appointment_time_form = AppointmentTimeForm(employee=employee, appointment_date=appointment_date,
                                                        service=service)

            context_data.update({
                'employee_date_form': employee_date_form,
                'appointment_time_form': appointment_time_form,
            })
            return render(request, self.template_name, context_data)

        if self.request.user.is_anonymous:
            messages.error(self.request, 'Авторизуйтесь, чтобы продолжить')
            return redirect('home', permanent=False)

        if request.POST.get('formId') == 'appointment_time_form':
            service = self.get_object()
            employee = request.POST.get('employee')
            appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')

            date_time_str = f"{appointment_date} {appointment_time}"
            date_time_appointment = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

            who_purchased = self.request.user
            branch = service.branch
            who_provides = EmployeeOrganization.objects.get(id=employee)

            if who_provides.deleted:
                messages.error(self.request, 'Этот сотрудник больше не работает')
                return redirect('services_view', self.kwargs.get('pk'), permanent=False)

            if branch.deleted:
                messages.error(self.request, 'Филиала, где оказывались приемы больше не существует')
                return redirect('services_view', self.kwargs.get('pk'), permanent=False)

            try:
                AppointmentDoctor.objects.create(
                    who_purchased=who_purchased,
                    service_now=service,
                    who_provides=who_provides,
                    name_service=service.name_service,
                    date_time_appointment=date_time_appointment,
                    price_appointment=service.price,
                    first_name_specialist=who_provides.first_name,
                    last_name_specialist=who_provides.last_name,
                    middle_name_specialist=who_provides.middle_name,
                    qualification_specialist=who_provides.qualification,
                    street_branch=branch.street,
                    house_branch=branch.house,
                )
            except IntegrityError:
                messages.error(self.request, 'Произошла ошибка при записи на прием, возможно это время уже занято')
                return redirect('services_view', self.kwargs.get('pk'), permanent=False)

            messages.success(self.request, 'Вы записались на прием')
            return redirect('services_view', self.kwargs.get('pk'), permanent=False)

        if request.POST.get('formId') == 'rating_service_form':
            rating_service_form = RatingServiceForm(request.POST)

            if rating_service_form.is_valid():
                try:
                    rating_user = RatingService.objects.get(rating_service=service, user_grade=self.request.user)
                except ObjectDoesNotExist:
                    RatingService.objects.create(rating_service=service,
                                                 user_grade=self.request.user,
                                                 grade=rating_service_form.cleaned_data['grade'])
                    messages.success(self.request, 'Вы успешно поставили оценку')
                    return redirect('services_view', self.kwargs.get('pk'), permanent=False)

                rating_user.grade = rating_service_form.cleaned_data['grade']
                rating_user.save()
                messages.success(self.request, 'Вы успешно изменили оценку')
                return redirect('services_view', self.kwargs.get('pk'), permanent=False)

            messages.error(self.request, 'Оценка не валидная')
            return redirect('services_view', self.kwargs.get('pk'), permanent=False)

        if request.POST.get('formId') == 'comment_create_form':
            comment_create_form = CommentAboutServiceForm(request.POST)

            if comment_create_form.is_valid():
                CommentAboutService.objects.create(
                    wrote=self.request.user,
                    text=comment_create_form.cleaned_data['text'],
                    service=service,
                )

                messages.success(self.request, 'Вы успешно создали комментарий')
                return redirect('services_view', self.kwargs.get('pk'), permanent=False)

            messages.error(self.request, 'Комментарий не валидный')
            return redirect('services_view', self.kwargs.get('pk'), permanent=False)

        context_data.update({
            'employee_date_form': employee_date_form,
        })
        return render(request, self.template_name, context_data)


def delete_comment_service(request, pk):
    if request.user.is_anonymous:
        messages.warning(request, 'Авторизуйтесь, чтобы удалить комментарий')
        return redirect('log_in', permanent=False)

    try:
        comment_service = CommentAboutService.objects.get(pk=pk)
    except ObjectDoesNotExist:
        messages.error(request, 'Комментарий не найден')
        return redirect('home', permanent=False)

    if comment_service.wrote != request.user and not request.user.is_staff:
        messages.success(request, 'Удалить комментарий может либо тот кто его создал, либо администратор')
        return redirect('home', permanent=False)

    comment_service.deleted = True
    comment_service.save()

    messages.success(request, 'Комментарий успешно удален')
    return redirect('services_view', comment_service.service.id, permanent=False)


class ChangeCommentServicesView(UpdateView):
    model = CommentAboutService
    form_class = CommentAboutServiceForm
    template_name = 'main/change_comment_service.html'

    def get_context_data(self, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context = {
            'title': 'Изменить комментарий',
            'title_form': 'Изменить комментарий',
        }

        return {**base_context, **context}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.warning(self.request, 'Авторизуйтесь, чтобы изменить комментарий')
            return redirect('log_in', permanent=False)

        comment = self.get_object()

        if isinstance(comment, HttpResponseRedirect):
            return comment

        if comment.wrote != self.request.user:
            messages.error(self.request, 'Вы не можете изменить чужой комментарий')
            return redirect('home', permanent=False)

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            organization = CommentAboutService.non_deleted.get(pk=self.kwargs.get('pk'))
        except IntegrityError:
            messages.error(self.request, 'Комментарий не найден не найдена')
            return redirect('home', permanent=False)

        return organization

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.is_change = True
        comment.save()

        messages.success(self.request, 'Успешное изменен комментарий')
        return redirect('services_view', comment.service.id, permanent=False)


class UpdateServicesView(UpdateView):
    model = ServiceOrganization
    form_class = ServiceOrganizationForm
    template_name = 'main/form_service_organization.html'

    def get_context_data(self, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context = {
            'title': 'Изменить услугу организации',
            'title_form': 'Изменить услугу',
        }

        return {**base_context, **context}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.warning(self.request, 'Авторизуйтесь, чтобы изменить данные об услуге')
            return redirect('log_in', permanent=False)

        service_organization = self.get_object()

        if isinstance(service_organization, HttpResponseRedirect):
            return service_organization

        if service_organization.branch.organization.owner != self.request.user:
            messages.error(self.request, 'У вас нет доступа к изменению данных об услугах чужой организации')
            return redirect('home', permanent=False)

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            service_organization = ServiceOrganization.objects.get(Q(pk=self.kwargs.get('pk')) &
                                                                   Q(branch__organization__owner=self.request.user))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Услуга организации не найдена')
            return redirect('home', permanent=False)

        if service_organization.deleted:
            messages.error(self.request, 'Услуга была удалена')
            return redirect('home', permanent=False)

        return service_organization

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Успешное изменен комментарий')
        return redirect('services_view', self.kwargs.get('pk'), permanent=False)


def delete_organization_service(request, pk):
    if request.user.is_anonymous:
        messages.warning(request, 'Авторизуйтесь, чтобы удалить услугу организации')
        return redirect('log_in', permanent=False)

    try:
        service_organization = ServiceOrganization.objects.get(Q(pk=pk) & Q(branch__organization__owner=request.user))
    except ObjectDoesNotExist:
        messages.error(request, 'Услуга организации не найдена')
        return redirect('home', permanent=False)

    if service_organization.branch.organization.owner != request.user:
        messages.error(request, 'У вас нет доступа к удаление услуги чужой организации')
        return redirect('home', permanent=False)

    if service_organization.deleted:
        messages.error(request, 'Услуга уже была удалена ранее')
        return redirect('home', permanent=True)

    service_organization.deleted = True
    service_organization.save()
    
    messages.success(request, 'Услуга была удалена')
    return redirect('services_list', permanent=True)


def delete_grade_service(request, pk, pk_grade):
    if request.user.is_anonymous:
        messages.warning(request, 'Авторизуйтесь, чтобы удалить оценку')
        return redirect('log_in', permanent=False)

    try:
        RatingService.objects.get(Q(pk=pk_grade) & Q(user_grade=request.user)).delete()
    except ObjectDoesNotExist:
        messages.error(request, 'Ваша оценка не найдена')
        return redirect('services_view', pk, permanent=False)

    messages.success(request, 'Оценка удалена')
    return redirect('services_view', pk, permanent=False)


class OrganizationAppointmentListView(ListView):
    paginate_by = 5
    model = AppointmentDoctor
    template_name = 'main/appointment_organization_list.html'
    context_object_name = 'appointment_organization_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        context = {
            'title': 'Приемы моей организации',
        }

        return {**base_context, **context}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.warning(self.request, 'Авторизуйтесь, чтобы просмотреть список приемов в своей организации')
            return redirect('log_in', permanent=False)

        try:
            organization = (Organization.objects.select_related('owner_organization_fk')
                            .values('owner__username').get(owner=self.request.user))
        except ObjectDoesNotExist:
            messages.error(self.request, 'Организация не найдена')
            return redirect('home', permanent=False)

        if organization.get('owner__username') != self.request.user.username:
            messages.error(self.request, 'У вас нет доступа к данным об приемах чужой организации')
            return redirect('home', permanent=False)

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = AppointmentDoctor.objects.filter(service_now__branch__organization__owner=self.request.user)
        return queryset


def ban_user(request, username):
    if request.user.is_anonymous:
        messages.warning(request, 'Авторизуйтесь, чтобы заблокировать пользователя')
        return redirect('log_in', permanent=False)

    try:
        action_user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        messages.error(request, 'Невозможно заблокировать не существующего пользователя')
        return redirect('home', permanent=False)

    if action_user.banned:
        messages.error(request, 'Пользователь уже заблокирован')
        return redirect('home', permanent=False)

    if action_user.is_staff:
        messages.error(request, 'Нельзя заблокировать администрацию')
        return redirect('home', permanent=False)

    if not request.user.is_staff:
        messages.error(request, 'Только администратор может заблокировать пользователя')
        return redirect('home', permanent=False)

    action_user.banned = True
    action_user.is_online = False
    action_user.save()

    sessions = Session.objects.filter(expire_date__gte=timezone.now())

    for session in sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(action_user.id):
            session.delete()


    return redirect('profile_user', username=username, permanent=False)


def unban_user(request, username):
    if request.user.is_anonymous:
        messages.warning(request, 'Авторизуйтесь, чтобы разблокировать пользователя')
        return redirect('log_in', permanent=False)

    try:
        action_user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        messages.error(request, 'Невозможно разблокировать не существующего пользователя')
        return redirect('home', permanent=False)

    if not action_user.banned:
        messages.error(request, 'Пользователь не заблокирован')
        return redirect('home', permanent=False)

    if action_user.is_staff:
        messages.error(request, 'Администрация не может быть заблокирован')
        return redirect('home', permanent=False)

    if not request.user.is_staff:
        messages.error(request, 'Только администратор может разблокировать пользователя')
        return redirect('home', permanent=False)

    action_user.banned = False
    action_user.save()

    return redirect('profile_user', username=username, permanent=False)


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('home', permanent=False)


def http404_page(_, exception):
    return HttpResponse(f'<h1>Страница не найдена {exception}</h1>')
