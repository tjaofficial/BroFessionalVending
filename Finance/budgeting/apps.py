from django.apps import AppConfig


class BudgetingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'budgeting'

    def ready(self):
        import budgeting.signals
        import budgeting.cron