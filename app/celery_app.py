#
# #
# from celery import Celery
#
#
# app = Celery('fast_api', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
#
#
# app.conf.update(
#     result_expires=3600,
#     task_serializer='json',
#     result_serializer='json',
#     accept_content=['json'],
#     timezone='UTC',
#     enable_utc=True
# )
#
# app.autodiscover_tasks()
#
# app.conf.update(
#     task_routes={
#         'app.tasks.send_confirmation_email': {'queue': 'email_queue'},
#         'app.tasks.send_reset_password_email': {'queue': 'email_queue'},
#     },
# )
#
# app.conf.update(
#     broker_url='redis://localhost:6379/0',
#     result_backend='redis://localhost:6379/0',
# )
#
# # Импорт задач для их регистрации
# from app.celery.tasks import send_confirmation_email
#
#
# # if __name__ == '__main__':
# #     app.start()