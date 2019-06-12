from kombu import Queue
from kombu import Exchange

result_serializer = 'json'


broker_url = "amqp://misscut:misscut@166.111.226.247:5672/mc_vhost"
result_backend = "amqp://misscut:misscut@166.111.226.247:5672/mc_vhost"

task_queues = (
    Queue('MC_lm',  exchange=Exchange('priority', type='direct'), routing_key='MC_lm'),
    Queue('MC_dep',  exchange=Exchange('priority', type='direct'), routing_key='MC_dep'),
)

task_routes = ([
    ('kernel_lm_interface.check_text_lm', {'queue': 'MC_lm'}),
    ('kernel_lm_interface.check_text_lm_for_swn', {'queue': 'MC_lm'}),
    ('kernel_dep_interface.check_text_dep_1', {'queue': 'MC_dep'}),
    ('kernel_dep_interface.check_text_dep_2', {'queue': 'MC_dep'}),
    ('kernel_dep_interface.check_text_dep_full', {'queue': 'MC_dep'}),
],)
