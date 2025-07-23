from django.utils import timezone

def get_mailing_status_color(status):
    """Возвращает цвет для отображения статуса рассылки"""
    return {
        'created': 'primary',
        'started': 'success',
        'completed': 'secondary',
    }.get(status, 'warning')
