from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


def validate_file_size(value, max_size_mb: int):
    max_size = max_size_mb * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f'Размер файла не должен превышать {max_size_mb} МБ')


def validate_service_appointment_time(appointment_start_time, appointment_end_time, appointment_interval):
    if appointment_start_time >= appointment_end_time:
        raise ValidationError('Время начала не может быть больше или равно времени конца приема')

    today = datetime.today().date()
    start_datetime = datetime.combine(today, appointment_start_time)
    end_datetime = datetime.combine(today, appointment_end_time)

    total_duration = end_datetime - start_datetime

    appointment_interval_timedelta = timedelta(minutes=appointment_interval)

    number_of_slots = total_duration // appointment_interval_timedelta

    if number_of_slots < 3:
        raise ValidationError('Должно быть хотя бы 3 записи на прием в указанном интервале приема')
