# -*- coding: utf-8 -*-
import celery
import json


app = celery.Celery('dep_tasks')
app.config_from_object('celeryconfig')

check_lm_op = None
check_dep_op = None


class CallbackTask(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        print("----%s is done" % task_id)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


@app.task(base=CallbackTask)
def check_text_dep_1(text, thresholds, force_checking_flag, checking_mode):
    global check_dep_op
    if check_dep_op is None:
        from main import MissCut
        check_dep_op = MissCut()
    result = check_dep_op.check_text_1(text, thresholds, force_checking_flag, checking_mode)
    return json.dumps(result)


@app.task(base=CallbackTask)
def check_text_dep_2(update_info, saving_code):
    global check_dep_op
    if check_dep_op is None:
        from main import MissCut
        check_dep_op = MissCut()
    result = check_dep_op.check_text_2(update_info, saving_code)
    return json.dumps(result)


@app.task(base=CallbackTask)
def check_text_dep_full(text, thresholds, checking_mode):
    global check_dep_op
    if check_dep_op is None:
        from main import MissCut
        check_dep_op = MissCut()
    result = check_dep_op.check_text_full(text, thresholds, checking_mode)
    return json.dumps(result)
