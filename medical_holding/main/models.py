from django.core.validators import (RegexValidator, FileExtensionValidator,
                                    MinValueValidator, MaxValueValidator, MinLengthValidator)
from main.validators import validate_file_size, validate_service_appointment_time
from medical_holding.settings import AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db.models import Q
from django.db import models


def validate_file_size_2mb(value):
    validate_file_size(value, 2)

def validate_file_size_4mb(value):
    validate_file_size(value, 4)


class Gender(models.TextChoices):
    MALE = 'M', 'Мужской'
    FEMALE = 'W', 'Женский'
    NONE = 'N', 'Не указан'


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    avatar = models.ImageField(blank=True, upload_to='avatars/%Y/%m/%d/', validators=[
        validate_file_size_2mb,
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
    ], default='default/avatar.jpg',
                               verbose_name='Аватар')
    background = models.ImageField(blank=True, upload_to='backgrounds/%Y/%m/%d/', validators=[
        validate_file_size_4mb,
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
    ], default='default/background.jpg',
                                   verbose_name='Фон профиля')
    about = models.TextField(max_length=1024, blank=True, default='', verbose_name='О себе')

    first_name = models.CharField(max_length=256,  blank=True, default='', verbose_name='Имя')
    last_name = models.CharField(max_length=256, blank=True, default='', verbose_name='Фамилия')
    gender = models.CharField(max_length=2, blank=True, choices=Gender.choices, default=Gender.NONE,
                              verbose_name='Пол')
    birthday = models.DateField(blank=True, null=True, verbose_name='День рождения')
    phone = models.CharField(blank=True, default='', validators=[
        RegexValidator(r'^\d{6,16}$', 'Номер телефона число от 6 до 16 цифр.')
    ], max_length=16, verbose_name='Номер телефона')

    email = models.EmailField(verbose_name='Почта')

    last_seen = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=False)
    banned = models.BooleanField(default=False, verbose_name='Заблокирован')

    objects = UserManager()


class Organization(models.Model):
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    owner = models.OneToOneField(AUTH_USER_MODEL,
                                 related_name='owner_organization_fk',
                                 on_delete=models.PROTECT, verbose_name='Владелец организации')
    name = models.CharField(max_length=512, unique=True, validators=[
        MinLengthValidator(3),
    ], verbose_name='Название')
    logo = models.ImageField(upload_to='avatars/%Y/%m/%d/', validators=[
        validate_file_size_2mb,
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
    ], default='default/avatar_organization.jpg',
                               verbose_name='Логотип')
    about = models.CharField(max_length=1024, default='', blank=True, verbose_name='Об организации')
    site = models.URLField(max_length=1024, default='', blank=True, verbose_name='Сайт')
    inn = models.CharField(max_length=12, unique=True,
                           validators=[
                               RegexValidator(r'^\d{10,12}$', 'ИНН должен содержать от 10 до 12 цифр.')
                           ], verbose_name='ИНН')

    objects = models.Manager()


class BranchOrganization(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(house__gt=0),
                name='house_not_zero_CK',
            ),
        ]
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    organization = models.ForeignKey(Organization,
                                     related_name='organization_branch_fk',
                                     on_delete=models.PROTECT, verbose_name='Филиал организации')
    street = models.CharField(max_length=512, validators=[
        MinLengthValidator(8),
    ], verbose_name='Улица')
    house = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1)
    ], verbose_name='Дом')
    phone = models.CharField(blank=True, default='', validators=[
        RegexValidator(r'^\d{6,16}$', 'Номер телефона число от 6 до 16 цифр.')
    ], max_length=16, verbose_name='Номер телефона')
    deleted = models.BooleanField(default=False, verbose_name='Удален')

    class NonDeletedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(deleted=False)

    objects = models.Manager()
    non_deleted = NonDeletedManager()

    def __str__(self):
        return f'Ул. {self.street} дом {self.house}'


class EmployeeOrganization(models.Model):
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default='default/employee.jpg', validators=[
        validate_file_size_2mb,
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
    ], verbose_name='Аватар')
    number_in_med_registry = models.CharField(max_length=128, unique=True, validators=[
        MinLengthValidator(1)
    ], verbose_name='Номер в медецинском реестре')
    organization = models.ForeignKey(Organization, related_name='organization_employee_fk',
                                     on_delete=models.PROTECT, verbose_name='Сотрудник организации')
    experience_month = models.PositiveSmallIntegerField(default=0, verbose_name='Опыт в месяцах')
    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=256, verbose_name='Отчество')
    qualification = models.CharField(max_length=512, verbose_name='Квалификация')
    gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.NONE, verbose_name='Пол')
    deleted = models.BooleanField(default=False, verbose_name='Удален')

    class NonDeletedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(deleted=False)

    objects = models.Manager()
    non_deleted = NonDeletedManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.middle_name} | {self.number_in_med_registry}'


class ServiceOrganization(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=0),
                name='price_CK',
            ),
        ]
        ordering = ['-date_created']
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    branch = models.ForeignKey(BranchOrganization,
                               related_name='branch_organization_fk',
                               on_delete=models.PROTECT, verbose_name='Где будет проходить')
    name_service = models.CharField(max_length=512, validators=[
        MinLengthValidator(8)
    ], verbose_name='Название услуги')
    date_created = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    appointment_start_time = models.TimeField(verbose_name='Время начала приемов')
    appointment_end_time = models.TimeField(verbose_name='Время конца приемов')
    appointment_interval = models.PositiveSmallIntegerField(validators=[
            MinValueValidator(5, message='Минимальный интервал 5 минут')
        ],verbose_name='Интервал записей')
    amount_days_for_registration = models.PositiveSmallIntegerField(validators=[
            MinValueValidator(1, message='Минимум дней на оформление вперед это 1 день'),
            MaxValueValidator(14, message='Максимум на перед можно оформить только на 2 недели вперед')
        ], verbose_name='На сколько вперед дней можно оформить')
    employee = models.ManyToManyField(EmployeeOrganization, related_name='employee_organization_fk',
                                      verbose_name='Сотрудники, которые могут выполнять услугу')
    additional_information = models.CharField(max_length=1024, blank=True, verbose_name='Дополнительная информация')
    deleted = models.BooleanField(default=False, verbose_name='Удален')

    def clean(self):
        super().clean()
        validate_service_appointment_time(self.appointment_start_time, self.appointment_end_time, self.appointment_interval)

    class NonDeletedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(Q(deleted=False) &
                                                 Q(branch__organization__owner__banned=False))

    objects = models.Manager()
    non_deleted = NonDeletedManager()


class CommentAboutService(models.Model):
    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_change = models.BooleanField(default=False, verbose_name='Изменен')
    wrote = models.ForeignKey(AUTH_USER_MODEL, related_name='wrote_comment_fk',
                              on_delete=models.PROTECT, verbose_name='Кто написал')
    text = models.CharField(max_length=1024, validators=[
        MinLengthValidator(1)
    ], verbose_name='Текст комментария')
    service = models.ForeignKey(ServiceOrganization, related_name='service_comment_fk',
                                on_delete=models.PROTECT, verbose_name='Комментарий к услуге')
    deleted = models.BooleanField(default=False, verbose_name='Удален')

    class NonDeletedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(Q(deleted=False) & Q(wrote__banned=False))

    objects = models.Manager()
    non_deleted = NonDeletedManager()


class RatingService(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(models.Q(grade__gte=0.0) &
                       models.Q(grade__lte=5.0)),
                name='grade_CK',
            ),
        ]
        unique_together = (('rating_service', 'user_grade'),)
        verbose_name = 'Оценки'
        verbose_name_plural = 'Оценка'

    rating_service = models.ForeignKey(ServiceOrganization, on_delete=models.CASCADE,
                                       related_name='rating_service_fk', verbose_name='Оцениваемый товар')
    user_grade = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='user_grade_fk', verbose_name='Оценка пользователя')
    grade = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Оценка')


class AppointmentDoctor(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(price_appointment__gte=0),
                name='price_appointment_CK',
            ),
            models.CheckConstraint(
                check=models.Q(house_branch__gt=0),
                name='house_branch_not_zero_CK',
            ),
        ]
        ordering = ['-date_time_appointment']
        unique_together = (('date_time_appointment', 'service_now', 'who_provides',),)
        verbose_name = 'Прием'
        verbose_name_plural = 'Приемы'

    who_purchased = models.ForeignKey(AUTH_USER_MODEL, related_name='who_purchased_fk',
                                      on_delete=models.PROTECT, verbose_name='Приобрел услугу')
    service_now = models.ForeignKey(ServiceOrganization, related_name='service_now_fk',
                                    on_delete=models.PROTECT, verbose_name='Ссылка на услугу сейчас')
    who_provides = models.ForeignKey(EmployeeOrganization, related_name='who_provides_fk',
                                    on_delete=models.PROTECT, verbose_name='Кто оказал услугу')
    name_service = models.CharField(max_length=512, verbose_name='Название услуги')
    date_time_appointment = models.DateTimeField(verbose_name='Время и дата приема')
    price_appointment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за прием')
    first_name_specialist = models.CharField(max_length=256, verbose_name='Имя доктора')
    last_name_specialist = models.CharField(max_length=256, verbose_name='Фамилия доктора')
    middle_name_specialist = models.CharField(max_length=256, verbose_name='Отчество доктора')
    qualification_specialist = models.CharField(max_length=512, verbose_name='Квалификация доктора')
    street_branch = models.CharField(max_length=512, verbose_name='Улица')
    house_branch = models.PositiveSmallIntegerField(verbose_name='Дом')
