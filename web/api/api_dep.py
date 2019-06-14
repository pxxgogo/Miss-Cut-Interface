from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from api.tasks import check_text_dep_1, check_text_dep_2, check_text_dep_full
import json
import time
from text.models import TextFile
from django.utils.timezone import now
from django.core.files.base import ContentFile


# Create your views here.
log_handle = open("log_CNKI.txt", 'w+')


def demo(request):
    return render(request, "demo.html", {})


@csrf_exempt
def check_text_1_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.POST["data"])
            text = data["text"]
            print("Receive:", text)
            log_handle.write("Receive: %s\n" % text)
            force_checking_flag = data.get("force_checking_flag", 0)
            checking_mode = data.get("checking_mode", 0)
            thresholds = data.get('thresholds', {})
            if text == "":
                return JsonResponse({"return_code": 0, "result": []}, safe=False)
            r = check_text_dep_1.delay(text, thresholds, force_checking_flag, checking_mode)
            while (not r.ready()):
                time.sleep(0.001)
                continue
            text_file = TextFile()
            text_file.ip = request.META.get("REMOTE_ADDR", "unknown")
            text_file.file.save(str(now()) + text_file.ip + ".txt", ContentFile(json.dumps({'text': text})))
            text_file.ret.save(str(now()) + text_file.ip + ".json", ContentFile(r.result))
            text_file.model_type = 2
            text_file.tmp_code = r.result["saving_code"]
            text_file.save()
            log_handle.write("Result: %s\n" % r.result)
            log_handle.flush()
            ret = json.loads(r.result)
            print("Result:", ret)
            return JsonResponse({"return_code": 0, "result": ret}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"return_code": 2}, safe=False)
    return JsonResponse({"return_code": 1}, safe=False)


@csrf_exempt
def check_text_2_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.POST["data"])
            update_info = data["update_info"]
            saving_code = data["saving_code"]
            if saving_code == "":
                return JsonResponse({"return_code": 2, "result": []}, safe=False)
            r = check_text_dep_2.delay(update_info, saving_code)
            while (not r.ready()):
                time.sleep(0.001)
                continue
            ret = json.loads(r.result)
            text_file = TextFile.objects.get(tmp_code=saving_code)
            text_file.ret.save(str(now()) + text_file.ip + ".json", ContentFile(r.result))
            text_file.model_type = 1
            text_file.save()
            print("Result:", ret)
            return JsonResponse({"return_code": 0, "result": ret}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"return_code": 2}, safe=False)
    return JsonResponse({"return_code": 1}, safe=False)


@csrf_exempt
def check_text_full_info(request):
    if request.method == "POST":
        try:
            data = json.loads(request.POST["data"])
            text = data["text"]
            print("Receive:", text)
            log_handle.write("Receive: %s\n" % text)
            force_checking_flag = 1
            checking_mode = data.get("checking_mode", 0)
            thresholds = data.get('thresholds', {})
            if text == "":
                return JsonResponse({"return_code": 0, "result": []}, safe=False)
            r = check_text_dep_full.delay(text, thresholds, checking_mode)
            while (not r.ready()):
                time.sleep(0.001)
                continue
            # log_handle.write("Result: %s\n" % r.result)
            # log_handle.flush()
            ret = json.loads(r.result)

            text_file = TextFile()
            text_file.ip = request.META.get("REMOTE_ADDR", "unknown")
            text_file.file.save(str(now()) + text_file.ip + ".txt", ContentFile(json.dumps({'text': text})))
            text_file.ret.save(str(now()) + text_file.ip + ".json", ContentFile(r.result))
            text_file.model_type = 1
            text_file.save()

            print("Result:", ret)
            return JsonResponse({"return_code": 0, "result": ret}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"return_code": 2}, safe=False)
    return JsonResponse({"return_code": 1}, safe=False)
