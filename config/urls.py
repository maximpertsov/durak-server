"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from durak import views

urlpatterns = [
    path("status", views.status_view),
    path(
        "api/game/<str:slug>/events",
        views.EventView.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "api/game/request/<int:pk>",
        views.GameRequestView.as_view({"patch": "partial_update"}),
    ),
    path(
        "api/game/request",
        views.GameRequestView.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "api/game",
        views.GameView.as_view({"post": "create"}),
    ),
    path("api/game/<str:slug>", views.GameView.as_view({"get": "retrieve"})),
    path("api/games/me", views.UserGameView.as_view()),
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin/", admin.site.urls),
]
