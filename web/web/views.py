from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from user_profile.models import Profile
from text.models import TextFile
from django.core.mail import EmailMessage


import sys


from kernel.tasks import preprocess, collect_result_lm, collect_result_dep
from api.tasks import check_text_lm, check_text_dep_full
from celery import group


def tmp_index(request):
    return render(request, "tmp.html")


@csrf_exempt
def submit_files(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        profile = Profile()
        profile.email = email
        profile.files_num = len(request.FILES.getlist('files'))
        profile.finished_num = 0
        profile.save()
        ops_lm = []
        ops_dep = []
        text_models_lm = []
        text_models_dep = []
        # op_group = group([check_text_lm.s().set(queue="MC_lm"), check_text_dep_full.s().set(queue="MC_dep")])

        for file in request.FILES.getlist('files'):
            if not file.name.endswith(".tex") and not file.name.endswith(".txt"):
                continue
            text_file_lm = TextFile()
            text_file_lm.file_name = file.name
            text_file_lm.file = file
            text_file_lm.profile = profile
            text_file_lm.ip = request.META.get("REMOTE_ADDR", "unknown")
            text_file_lm.model_type = 0
            text_file_lm.save()
            text_models_lm.append(text_file_lm.id)

            text_file_dep = TextFile()
            text_file_dep.file_name = file.name
            text_file_dep.file = text_file_lm.file
            text_file_dep.profile = profile
            text_file_dep.ip = request.META.get("REMOTE_ADDR", "unknown")
            text_file_dep.model_type = 1
            text_file_dep.save()
            text_models_dep.append(text_file_dep.id)

            op1 = preprocess.s(text_file_lm.file.path).set(queue="MC_util")
            op2 = check_text_lm.s().set(queue="MC_lm")
            op3 = check_text_dep_full.s({}, 0).set(queue="MC_dep")
            op_lm = (op1 | op2)
            op_dep = (op1 | op3)
            ops_lm.append(op_lm)
            ops_dep.append(op_dep)
        ops_lm_op = (group(ops_lm) | collect_result_lm.s(email, text_models_lm).set(queue="MC_util"))
        ops_dep_op = (group(ops_dep) | collect_result_dep.s(email, text_models_dep).set(queue="MC_util"))
        ops_lm_op.delay()
        ops_dep_op.delay()

        # print(profile.rawfile_set.all())

    return HttpResponseRedirect("/")


def test_email(request):
    email_message = EmailMessage(
        '查错结果（精细查错）',
        '附件是精细模型的查错结果，请验收。',
        'pxy18@mails.tsinghua.edu.cn',
        ['421915293@163.com'],
    )
    email_message.send()
    return HttpResponseRedirect("/")
