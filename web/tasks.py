# -*- coding: utf-8 -*-
import celery
import json
import sys

sys.path.append("/home/misscut/app/Miss-Cut-V5/")
sys.path.append("/home/misscut/app/Miss-Cut-V7/")
from mc_algorithm_v5.CheckOp import CheckOp
from system.main import MissCut

app = celery.Celery('tasks')
app.config_from_object('celeryconfig')

check_lm_op = None
check_dep_op = None


class CallbackTask(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        print("----%s is done" % task_id)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


@app.task(base=CallbackTask)
def check_with_lm(text):
    global check_lm_op
    if check_lm_op is None:
        check_lm_op = CheckOp()
    check_lm_op.reset()  # MUST call it before every check operation
    result = check_lm_op.feed_text(text)
    return json.dumps(result)


@app.task(base=CallbackTask)
def check_text_dep_1(text, thresholds, force_checking_flag, checking_mode):
    global check_dep_op
    if check_dep_op is None:
        check_dep_op = MissCut()
    result = check_dep_op.check_text_1(text, thresholds, force_checking_flag, checking_mode)
    return json.dumps(result)


@app.task(base=CallbackTask)
def check_text_dep_2(update_info, saving_code):
    global check_dep_op
    if check_dep_op is None:
        check_dep_op = MissCut()
    result = check_dep_op.check_text_2(update_info, saving_code)
    return json.dumps(result)


@app.task(base=CallbackTask)
def check_text_dep_full(text, thresholds, checking_mode):
    global check_dep_op
    if check_dep_op is None:
        check_dep_op = MissCut()
    result = check_dep_op.check_text_full(text, thresholds, checking_mode)
    return json.dumps(result)
