from django.core.management import BaseCommand

from mailing.services import send_mailing_manual


class Command(BaseCommand):
    help = "Запускает рассылку по ID"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID рассылки")

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        success, message = send_mailing_manual(mailing_id)

        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stderr.write(self.style.ERROR(message))
