from kombu import Queue
from kombu import Exchange

result_serializer = 'json'


broker_url = "amqp://misscut:misscut@166.111.226.247:5672"
result_backend = "amqp://misscut:misscut@166.111.226.247:5672"

task_queues = (
    Queue('MC_lm',  exchange=Exchange('priority', type='direct'), routing_key='MC_lm'),
    Queue('MC_dep',  exchange=Exchange('priority', type='direct'), routing_key='MC_dep'),
)

task_routes = ([
    ('tasks.check_with_lm', {'queue': 'MC_lm'}),
    ('tasks.check_text_dep_1', {'queue': 'MC_dep'}),
    ('tasks.check_text_dep_2', {'queue': 'MC_dep'}),
    ('tasks.check_text_dep_full', {'queue': 'MC_dep'}),
],)
