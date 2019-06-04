# -*- coding: utf-8 -*-
import celery
import json


app = celery.Celery('lm_task')
app.config_from_object('celeryconfig')

check_lm_op = None
check_dep_op = None


class CallbackTask(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        print("----%s is done" % task_id)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


@app.task(base=CallbackTask)
def check_text_lm(text):
    global check_lm_op
    if check_lm_op is None:
        from CheckOp import CheckOp
        check_lm_op = CheckOp()
    check_lm_op.reset()  # MUST call it before every check operation
    result = check_lm_op.feed_text(text)
    return json.dumps(result)
