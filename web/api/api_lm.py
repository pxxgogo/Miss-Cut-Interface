import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from kernel_lm_interface import check_text_lm, check_text_lm_for_swn
from text.models import TextFile
from django.core.files.base import ContentFile
from django.utils.timezone import now
from api.result_generation import generate_lm_result


def submit_text_test(request):
    with open("./footprints/new_sample.json", 'r') as input_file:
        ret = json.loads(input_file.read())
    return JsonResponse(ret, safe=False)


def submit_text(request):
    if request.method != "POST":
        return JsonResponse({"return_code": 1}, safe=False)
    text = request.POST["text"]
    if text == "":
        return JsonResponse([], safe=False)
    r = check_text_lm.delay(text)
    # print(r.ready())
    while (not r.ready()):
        continue
    ret = r.result
    text_file = TextFile()
    text_file.ip = request.META.get("REMOTE_ADDR", "unknown")
    text_file.file.save(str(now()) + text_file.ip + ".txt", ContentFile(json.dumps({'text': text})))
    text_file.ret.save(str(now()) + text_file.ip + ".json", ContentFile(ret))
    text_file.model_type = 0
    text_file.save()

    # print(request.META.get("REMOTE_ADDR", "unknown"))
    # print(text_file)
    return JsonResponse({"return_code": 0, "result": json.loads(r.result)}, safe=False)



@csrf_exempt
def check_lm_api(request):
    if request.method == "POST":
        text = request.POST["text"]
        print(text)
        if text == "":
            return JsonResponse([], safe=False)
        r = check_text_lm.delay(text)
        print(r.ready())
        while (not r.ready()):
            continue
        text_file = TextFile()
        text_file.ip = request.META.get("REMOTE_ADDR", "unknown")
        text_file.request_type = 1
        text_file.model_type = 0
        text_file.file.save(str(now()) + text_file.ip + ".txt", ContentFile(json.dumps({'text': text})))
        text_file.ret.save(str(now()) + text_file.ip + ".json", ContentFile(r.result))
        text_file.save()
        # print(request.META.get("REMOTE_ADDR", "unknown"))
        # print(text_file)
        return JsonResponse({"return_code": 0, "result": json.loads(r.result)}, safe=False)
    return JsonResponse({"return_code": 1}, safe=False)

@csrf_exempt
def check_for_swn(request):
    if request.method == "POST":
        text = request.POST["text"]
        print(text)
        if text == "":
            return JsonResponse([], safe=False)
        r = check_text_lm_for_swn.delay(text)
        print(r.ready())
        while (not r.ready()):
            continue
        # print(request.META.get("REMOTE_ADDR", "unknown"))
        # print(text_file)
        return JsonResponse({"return_code": 0, "result": json.loads(r.result)}, safe=False)
    return JsonResponse({"return_code": 1}, safe=False)


