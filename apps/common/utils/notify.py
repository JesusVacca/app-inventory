from django.contrib import messages


class Notify:
    @staticmethod
    def notify(request, message, level='success'):
        LEVELS = {
            'success': messages.SUCCESS,
            'warning': messages.WARNING,
            'danger': messages.ERROR,
            'info': messages.INFO,
            'debug': messages.DEBUG,
            'error': messages.ERROR,
        }
        messages.add_message(
            request,
            LEVELS.get(level, messages.INFO),
            message
        )

