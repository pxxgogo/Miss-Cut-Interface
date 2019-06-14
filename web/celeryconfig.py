from kombu import Queue
from kombu import Exchange

result_serializer = 'json'
result_expires = 600

broker_url = "amqp://misscut:misscut@166.111.226.247:5672/mc_vhost"
result_backend = "amqp://misscut:misscut@166.111.226.247:5672/mc_vhost"

task_queues = (
    Queue('MC_lm', exchange=Exchange('priority', type='direct'), routing_key='MC_lm'),
    Queue('MC_dep', exchange=Exchange('priority', type='direct'), routing_key='MC_dep'),
    Queue('MC_util', exchange=Exchange('priority', type='direct'), routing_key='MC_util'),

)

task_routes = ([
                   ('kernel_lm_interface.check_text_lm', {'queue': 'MC_lm'}),
                   ('kernel_lm_interface.check_text_lm_for_swn', {'queue': 'MC_lm'}),
                   ('kernel_dep_interface.check_text_dep_1', {'queue': 'MC_dep'}),
                   ('kernel_dep_interface.check_text_dep_2', {'queue': 'MC_dep'}),
                   ('kernel_dep_interface.check_text_dep_full', {'queue': 'MC_dep'}),
                   ('kernel_utils.preprocess', {'queue': 'MC_util'}),
                   ('kernel_utils.collect_result_lm', {'queue': 'MC_util'}),
                   ('kernel_utils.collect_result_dep', {'queue': 'MC_util'}),
               ],)
