from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.template.context_processors import csrf


def index(request):
    if not request.user.username:
        return HttpResponseRedirect("/login")
    return render(request, "index.html",
                  {'pageName': "首页",
                   'homeClass': 'selected'})


def login(request):
    if request.user.is_active:
        return HttpResponseRedirect("/")
    error = ""
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect("/")
        else:
            error = "登陆失败"
    pageTree = [{'url': "/login", 'name': "登陆页"}]
    return render(request, "login.html",
                  {'error': error,
                   'pageName': "请登陆", 'pageTree': pageTree})


def register(request):
    error = ""
    # if request.method == 'POST':
    #     user = User()
    #     user.username = request.POST["username"]
    #     user.email = request.POST["email"]
    #     user.phone = request.POST["phone"]
    #
    #     if request.POST["gender"] == "M":
    #         user.gender = "男"
    #     else:
    #         user.gender = "女"
    #     user.password = make_password(request.POST["password"], None, 'pbkdf2_sha256')
    #     user.studentID = request.POST["studentID"]
    #     user.personID = "#"
    #     if form.is_valid():
    #         form.save(user)
    #         return HttpResponseRedirect("/login")
    #     else:
    #         # assert False
    #         error = "信息错误！"
    c = {}
    c.update(csrf(request))
    c['error'] = error
    pageTree = [{'url': "/register", 'name': "注册页"}]
    c['pageTree'] = pageTree
    c['pageName'] = "请注册"
    return render(request, "register.html", c)
