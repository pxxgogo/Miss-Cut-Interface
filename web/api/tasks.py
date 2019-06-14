# -*- coding: utf-8 -*-
from celery import shared_task
import celery
import json

app = celery.Celery('MC_dep')
app.config_from_object('celeryconfig')

check_lm_op = None
check_dep_op = None


class CallbackTask(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        print("----%s is done" % task_id)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


@shared_task(name="check_text_dep_1", base=CallbackTask)
def check_text_dep_1(text, thresholds, force_checking_flag, checking_mode):
    global check_dep_op
    if check_dep_op is None:
        from main import MissCut
        check_dep_op = MissCut()
    result = check_dep_op.check_text_1(text, thresholds, force_checking_flag, checking_mode)
    return json.dumps(result)


@shared_task(name="check_text_dep_2", base=CallbackTask)
def check_text_dep_2(update_info, saving_code):
    global check_dep_op
    if check_dep_op is None:
        from main import MissCut
        check_dep_op = MissCut()
    result = check_dep_op.check_text_2(update_info, saving_code)
    return json.dumps(result)


@shared_task(name="check_text_dep_full", base=CallbackTask)
def check_text_dep_full(text, thresholds, checking_mode):
    global check_dep_op
    if check_dep_op is None:
        from main import MissCut
        check_dep_op = MissCut()
    result = check_dep_op.check_text_full(text, thresholds, checking_mode)
    return json.dumps(result)


@shared_task(name="check_text_lm", base=CallbackTask)
def check_text_lm(text):
    global check_lm_op
    if check_lm_op is None:
        from CheckOp import CheckOp
        check_lm_op = CheckOp()
    check_lm_op.reset()  # MUST call it before every check operation
    result = check_lm_op.feed_text(text)
    return json.dumps(result)


@shared_task(name="check_text_lm_for_swn", base=CallbackTask, autoretry_for=(Exception,), retry_kwargs={'max_retries': 5, 'countdown': 20})
def check_text_lm_for_swn(text):
    global check_lm_op
    if check_lm_op is None:
        from CheckOp import CheckOp
        check_lm_op = CheckOp()
    check_lm_op.reset()  # MUST call it before every check operation
    result = check_lm_op.feed_text_for_swn(text)
    return json.dumps(result)

