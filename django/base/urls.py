"""
URL configuration for base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path

from crawler.views import (
    AddSubscriptionView,
    GetEmailsForSubscriptionView,
    GetValuableObjectView,
    RegisterUserView,
    RemoveSubscriptionView,
    StartCeleryView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("start-celery/", StartCeleryView.as_view(), name="start_celery"),
    path(
        "get-valuable-object/",
        GetValuableObjectView.as_view(),
        name="get_valuable_object",
    ),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("add-subscription/", AddSubscriptionView.as_view(), name="add_subscription"),
    path(
        "remove-subscription/",
        RemoveSubscriptionView.as_view(),
        name="remove_subscription",
    ),
    path(
        "get-emails-for-subscription/",
        GetEmailsForSubscriptionView.as_view(),
        name="get_emails_for_subscription",
    ),
]
