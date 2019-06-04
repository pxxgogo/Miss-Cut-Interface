"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from api import api_lm
from api import api_dep

urlpatterns = [
    path('check_with_lm', api_lm.check_lm_api),
    path('check_with_dep_1', api_dep.check_text_1_api),
    path('check_with_dep_2', api_dep.check_text_2_api),
    path('check_with_dep_full', api_dep.check_text_full_info)
]
