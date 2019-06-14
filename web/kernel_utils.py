import celery
import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
from django.utils.timezone import now
from django.core.files.base import ContentFile
from text.models import TextFile

app = celery.Celery('MC_util')
app.config_from_object('celeryconfig')
import subprocess

class CallbackTask(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        print("----%s is done" % task_id)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


def generate_lm_result(ret_list):
    ret_text = ""
    for ret in ret_list:
        sentence = ret['sentence']
        candidates = ret['candidates']
        raw_word = candidates[0]['raw_word']
        new_word = candidates[0]['candidate']
        position = ret['position_in_sentence']
        ret_text += "%s %s (%d) -> %s\n" % (sentence, raw_word, position, new_word)
    return ret_text


def generate_dep_result(ret_list):
    ret_text = ""
    for ret in ret_list:
        sentence = ret['text']
        mistakes = ret['mistakes']
        possible_mistakes_text = ""
        for mistakes_per_type in mistakes:
            for mistake_info in mistakes_per_type:
                possible_mistakes_text += "%s(%d) " % (mistake_info[0][0], mistake_info[0][1])
        ret_text += "%s     POSSIBLE WORDS: %s\n" % (sentence, possible_mistakes_text)
    return ret_text


@app.task(base=CallbackTask)
def preprocess(file_path):
    su = subprocess.Popen(['/home/pxxgogo/misscut/app/Miss-Cut-Interface/web/kernel/delatex',
                           file_path],
                          stdout=subprocess.PIPE, stderr=None)
    text = su.stdout.read().decode()
    text = text.replace("\n", "")
    print("parsed text length: ", len(text))
    return text


@app.task(base=CallbackTask)
def collect_result_lm(rets_list, profile_id, text_model_ids):
    for rets, text_model_id in zip(rets_list, text_model_ids):
        ret_text = generate_lm_result(rets)
        text_model = TextFile.objects.get(id=text_model_id)
        text_model.ret.save(
            "%s-%s-%s-%d.json" % (str(now()), text_model.ip, text_model.file_name, text_model.model_type),
            ContentFile(json.dumps(rets)))
        text_model.return_text.save(
            "%s-%s-%s-%d.txt" % (str(now()), text_model.ip, text_model.file_name, text_model.model_type),
            ContentFile(ret_text))
        text_model.save()


@app.task(base=CallbackTask)
def collect_result_dep(rets_list, profile_id, text_model_ids):
    for rets, text_model_id in zip(rets_list, text_model_ids):
        ret_text = generate_dep_result(rets['rets'])
        text_model = TextFile.objects.get(id=text_model_id)
        text_model.ret.save(
            "%s-%s-%s-%d.json" % (str(now()), text_model.ip, text_model.file_name, text_model.model_type),
            ContentFile(json.dumps(rets)))
        text_model.return_text.save(
            "%s-%s-%s-%d.txt" % (str(now()), text_model.ip, text_model.file_name, text_model.model_type),
            ContentFile(ret_text))
        text_model.save()
