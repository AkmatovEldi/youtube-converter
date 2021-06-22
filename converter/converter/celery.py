from celery import Celery

app = Celery('converter',
             broker='redis://127.0.0.1:6379/0',
             backend='redis://127.0.0.1:6379/0',
             include=['youconv.tasks'])


# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

# celery -A converter worker -l INFO