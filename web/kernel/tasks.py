from celery import shared_task
import celery
import json
from django.utils.timezone import now
from django.core.files.base import ContentFile
from text.models import TextFile
from django.core.mail import EmailMessage

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
        raw_word = ret['raw_word']
        new_word = candidates[0]['candidate']
        position = ret['position_in_sentence']
        ret_text += "%s %s (%d) -> %s\n" % (sentence, raw_word, position, new_word)
    return ret_text


def generate_dep_result(ret_list):
    ret_text_list = []
    for ret in ret_list:
        sentence = ret['text']
        mistakes = ret['mistakes']
        choose_flag = False
        label_flag = 0
        possible_mistakes_text = ""
        for mistakes_per_type in mistakes:
            if mistakes_per_type['type'] == 'special symbol check':
                continue
            if mistakes_per_type['type'] != 'triples analysis':
                if mistakes_per_type['type'] == "lowly frequent token":
                    if label_flag < 1:
                        label_flag = 1
                else:
                    label_flag = 2
                possible_mistakes_text += " %s: " % mistakes_per_type['type']
                for mistake_info in mistakes_per_type['mistakes']:
                    possible_mistakes_text += "%s(%d) " % (
                        mistake_info[0][0], mistake_info[0][1])

            choose_flag = True
        if choose_flag:
            if label_flag > 0:
                ret_text_list.append(("%s     POSSIBLE ERROR: %s\n" % (sentence, possible_mistakes_text), label_flag))
            else:
                ret_text_list.append(("%s\n" % sentence, label_flag))
    ret_text_list.sort(key=lambda x: -x[1])
    ret_text = "".join([text for text, label in ret_text_list])
    return ret_text


@shared_task(name="preprocess", base=CallbackTask)
def preprocess(file_path):
    su = subprocess.Popen(['/home/pxxgogo/misscut/app/Miss-Cut-Interface/web/kernel/delatex',
                           file_path],
                          stdout=subprocess.PIPE, stderr=None)
    text = su.stdout.read().decode()
    # text = text.replace("\n", "")
    print("parsed text length: ", len(text))
    return text


@shared_task(name="collect_result_lm", base=CallbackTask)
def collect_result_lm(rets_list, email, text_model_ids):
    email_message = EmailMessage(
        '查错结果（简易查错）',
        '附件是简易模型的查错结果，请验收。',
        'pxy18@mails.tsinghua.edu.cn',
        [email],
    )
    for rets_str, text_model_id in zip(rets_list, text_model_ids):
        rets = json.loads(rets_str)
        ret_text = generate_lm_result(rets)
        text_model = TextFile.objects.get(id=text_model_id)
        text_model.ret.save(
            "%s-%s-%s-%d.json" % (str(now()), text_model.ip, text_model.file_name, text_model.model_type),
            ContentFile(rets_str))
        text_model.return_text.save(
            "%s-%s-%s-%d.txt" % (str(now()), text_model.ip, text_model.file_name, text_model.model_type),
            ContentFile(ret_text))
        text_model.save()
        email_message.attach(text_model.file_name[:-4] + "_ret.txt", ret_text)
    email_message.send()


@shared_task(name="collect_result_dep", base=CallbackTask)
def collect_result_dep(rets_list, email, text_model_ids):
    email_message = EmailMessage(
        '查错结果',
        '附件是您所有文件的查错结果，请验收。在文件中每一行表示一处可疑错误。未包含POSSIBLE ERROR的语句表明其中存在语病或错别字。',
        'pxy18@mails.tsinghua.edu.cn',
        [email],
    )
    for rets_str, text_model_id in zip(rets_list, text_model_ids):
        rets = json.loads(rets_str)
        ret_text = generate_dep_result(rets['rets'])
        text_model = TextFile.objects.get(id=text_model_id)
        text_model.ret.save(
            "%s-%s-%s-%d.json" % (str(now()), text_model.ip, text_model.file_name, text_model.model_type),
            ContentFile(json.dumps(rets)))
        text_model.return_text.save(
            "%s-%s-%s-%d.txt" % (str(now()), text_model.ip, text_model.file_name, text_model.model_type),
            ContentFile(ret_text))
        text_model.save()
        email_message.attach(text_model.file_name[:-4] + "_ret.txt", ret_text)
    email_message.send()
