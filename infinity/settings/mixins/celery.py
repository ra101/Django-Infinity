from celery.schedules import crontab


class CelerySettingsMixin:

    CELERY_TIMEZONE = "UTC"

    # CELERY_BEAT_SCHEDULE = {
    #     "update_admin_secret": {
    #         "task": "libs.infinite_admin.tasks.update_admin_secret",
    #         "schedule": crontab(hour=4),
    #     }
    # }

    CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

    CELERY_ACCEPT_CONTENT = ["application/json"]
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_SERIALIZER = 'json'

    # CELERY_TIMEZONE = 'Asia/Kolkata'

    CELERY_TASK_TRACK_STARTED = True

    CELERY_RESULT_BACKEND = 'django-db'

    CELERY_TASK_ROUTES = {
        '*.tasks*': {"queue": "default_queue"},
    }
