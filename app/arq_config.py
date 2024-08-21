from arq.connections import RedisSettings

class WorkerSettings:
    redis_settings = RedisSettings()
    functions = ['app.arq_worker.send_confirmation_email', 'app.arq_worker.send_reset_password_email']
    max_jobs = 10