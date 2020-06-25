from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Управление ботом телеграмма'

    def handle(self, *args, **kwargs):

        self.stdout.write("Starting bot")
        
        from ...bot import bot        
        bot.polling()

        print(bot)
