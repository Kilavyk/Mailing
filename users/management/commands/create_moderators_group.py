from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создаёт группу модераторов'

    def handle(self, *args, **options):

        # Создаем группу
        group, created = Group.objects.get_or_create(name='Менеджеры')

        if created:
            self.stdout.write(self.style.SUCCESS('Успешно созданная группа модераторов'))
        else:
            self.stdout.write('Группа модераторов уже существует')

        # Разрешения
        permissions = [
            'can_block_users',
            'can_block_mailings',
            'view_moderation_panel',
        ]

        # Добавляем
        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Разрешение {perm} не существует'))

        self.stdout.write(self.style.SUCCESS('Успешно установлены разрешения для группы «Модераторы»'))
